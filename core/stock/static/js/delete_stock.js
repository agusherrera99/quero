document.addEventListener('DOMContentLoaded', function () {
    const confirmInput = document.querySelector('.input-confirm');
    const deleteButton = document.querySelector('.btn-danger');

    // Deshabilitar el botón al cargar la página
    deleteButton.disabled = true;

    // Función que habilita el botón si el texto es "ELIMINAR"
    confirmInput.addEventListener('input', function () {
        if (confirmInput.value === 'ELIMINAR') {
            deleteButton.disabled = false;
        } else {
            deleteButton.disabled = true;
        }
    });
});