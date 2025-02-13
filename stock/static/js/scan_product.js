document.addEventListener('DOMContentLoaded', function() {
    const formData = JSON.parse(localStorage.getItem('addStockFormData'));

    function isSupportedBrowser() {
        const ua = navigator.userAgent;
        return /Chrome|Firefox|Safari|Opera|Edg/.test(ua);
    }

    async function requestCameraPermissions() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            stream.getTracks().forEach(track => track.stop()); 
            return true;
        } catch (err) {
            console.error('Error al solicitar permisos de cámara: ', err);
            return false;
        }
    }

    async function getCategoryName(categoryId) {
        const response = await fetch(`get_category_name?category_id=${categoryId}`);
        const data = await response.json();
        return data.category_name;
    }

    async function getSubcategoryName(subcategoryId) {
        const response = await fetch(`get_subcategory_name?subcategory_id=${subcategoryId}`);
        const data = await response.json();
        return data.subcategory_name;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if the cookie name matches
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (isSupportedBrowser() && navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
        requestCameraPermissions().then(granted => {
            if (granted) {
                Quagga.init({
                    inputStream: {
                        name: "Live",
                        type: "LiveStream",
                        target: document.querySelector('#interactive'),
                        constraints: {
                            facingMode: "environment"
                        },
                    },
                    decoder: {
                        readers: ["code_128_reader", "ean_reader", "ean_8_reader"]
                    },
                    locate: true,
                    locator: {
                        patchSize: "medium",
                        halfSample: true
                    },
                    numOfWorkers: navigator.hardwareConcurrency,
                    frequency: 10,
                    debug: {
                        drawBoundingBox: true,
                        showFrequency: true,
                        drawScanline: true,
                        showPattern: true
                    }
                }, function(err) {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    Quagga.start();
                });

                Quagga.onDetected(async function(result) {
                    if (result.codeResult && result.codeResult.code && result.codeResult.decodedCodes) {
                        // Filtrar los códigos que tienen valores válidos de error
                        const validErrors = result.codeResult.decodedCodes
                            .filter(code => code.error !== undefined && code.error !== null)
                            .map(code => code.error);
                
                        if (validErrors.length > 0) {
                            const averageError = validErrors.reduce((acc, err) => acc + err, 0) / validErrors.length;
                            const confidence = 1 - averageError; // Entre más bajo el error, mayor la confianza
                
                            if (confidence > 0.9) { // Confianza mayor al 90%
                                const code = result.codeResult.code;
                                const confirmed = confirm(`Código de barras detectado: ${code}. ¿Deseas confirmarlo?`);
                
                                if (confirmed) {
                                    try {
                                        formData.barcode = code;
                                    }   
                                    catch (err) {
                                        alert('Ocurrió un error al asignar el código de barras al formulario. Por favor, inténtalo de nuevo.');
                                        window.location.href = '/stock/add/';
                                    }

                                    const categoryName = await getCategoryName(formData.category);
                                    const subcategoryName = await getSubcategoryName(formData.subcategory);
                                    const csrfToken = getCookie('csrftoken');
                                    
                                    document.getElementById('scan-container').style.display = 'none';
                                    document.getElementById('confirmation-card').style.display = 'block';
                                    
                                    document.getElementById('category').value = categoryName;
                                    document.getElementById('subcategory').value = subcategoryName;
                                    document.getElementById('name').value = formData.name;
                                    document.getElementById('quantity').value = formData.quantity;
                                    document.getElementById('cost').value = formData.cost;
                                    document.getElementById('price').value = formData.price;
                                    document.getElementById('uom').value = formData.uom;
                                    document.getElementById('barcode').value = formData.barcode;

                                    document.getElementById('cancel-button').addEventListener('click', function() {
                                        localStorage.removeItem('addStockFormData');
                                        window.location.href = '/stock/add/';
                                    });
                                    
                                    localStorage.removeItem('addStockFormData');
                                } else {
                                    setTimeout(() => Quagga.start(), 2000); // Esperar 2 segundos antes de reiniciar el escaneo
                                }
                            }
                        } else {
                            alert('No se pudo calcular la confianza del código de barras. Por favor, inténtalo de nuevo.');
                            setTimeout(() => Quagga.start(), 2000); // Esperar 2 segundos antes de reiniciar el escaneo
                        }
                    }
                });
            } else {
                alert('No se pudo acceder a la cámara. Por favor, asegúrate de haber otorgado los permisos necesarios.');  
                window.location.href = '/stock/add/';
            }
        });
    } else {
        alert('Tu navegador no soporta acceso a la cámara o no es compatible.');
        window.location.href = '/stock/add/';
    }
});