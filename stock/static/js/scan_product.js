document.addEventListener('DOMContentLoaded', function() {
    const formData = JSON.parse(localStorage.getItem('addStockFormData'));
    // console.log('Datos del formulario: ', formData);

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

                Quagga.onDetected(function(result) {
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
                                    formData.barcode = code;
                                    // Una vez confirmado el código de barras, ocultar todo el sistema de escaneo y replazarlo por una confirmación de guardado del producto con toda la informacion obtendida del localstorage más el codigo de barras
                                    document.getElementById('scan-container').style.display = 'none';
                                    document.getElementById('confirmation-card').style.display = 'block';
                                    document.getElementById('confirmation-card').innerHTML = `
                                        <div class="card">
                                            <div class="card-header">
                                                Confirmación de guardado
                                            </div>
                                            <div class="card-body">
                                                <h5 class="card-title">¿Deseas guardar el siguiente producto?</h5>
                                                <p class="card-text">
                                                    <strong>Categoría:</strong> ${formData.category}<br>
                                                    <strong>Subcategoría:</strong> ${formData.subcategory}<br>
                                                    <strong>Nombre:</strong> ${formData.name}<br>
                                                    <strong>Cantidad:</strong> ${formData.quantity}<br>
                                                    <strong>Costo:</strong> ${formData.cost}<br>
                                                    <strong>Precio:</strong> ${formData.price}<br>
                                                    <strong>Unidad de medida:</strong> ${formData.uom}<br>
                                                    <strong>Código de barras:</strong> ${formData.barcode}
                                                </p>
                                                <button id="save-button" class="btn btn-primary">Guardar</button>
                                                <button id="cancel-button" class="btn btn-danger">Cancelar</button>
                                            </div>
                                        </div>
                                    `;
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
                            console.error("No se pudieron calcular errores válidos.");
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