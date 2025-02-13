document.addEventListener('DOMContentLoaded', function() {
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

    async function startQuagga() {
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
    };

    if (isSupportedBrowser() && navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
        requestCameraPermissions().then(granted => {
            if (granted) {
                startQuagga();

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
                                const response = await fetch(`/pos/scan/search/?barcode=${code}`);
                                
                                if (response.ok) {
                                    const product = await response.json();
                                    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
                                    
                                    // Verificar si el producto ya está en el carrito
                                    const existingProduct = cart.find(item => item.product_id === product.product.product_id);
                                    if (existingProduct) {
                                        // Si el producto ya está en el carrito, actualizar la cantidad
                                        existingProduct.quantity += 1;
                                    } else {
                                        // Si el producto no está en el carrito, añadirlo
                                        cart.push(product.product);
                                    }

                                    localStorage.setItem('cart', JSON.stringify(cart));
                                    sessionStorage.setItem('returningFromScan', 'true');
                                    window.location.href = '/pos/';
                                } else {
                                    const confirmed = confirm('No se encontró un producto con el código de barras proporcionado. ¿Deseas buscar intentarlo de nuevo?');
                                    if (confirmed) {
                                        Quagga.stop();
                                        startQuagga();
                                    } else {
                                        sessionStorage.setItem('returningFromScan', 'true');
                                        window.location.href = '/pos/';
                                    }
                                }
                            }
                        }
                    }
                });
            } else {
                alert('No se pudo acceder a la cámara. Por favor, asegúrate de haber otorgado los permisos necesarios.');  
            }
        });
    } else {
        alert('Tu navegador no soporta acceso a la cámara o no es compatible.');
    }
});