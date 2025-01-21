document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const clearButton = document.querySelector('.search-clear');
    
    // Función para mostrar u ocultar el botón de limpiar
    function toggleClearButton() {
        if (searchInput.value.trim() !== '') {
            clearButton.style.display = 'block'; // Muestra el botón
        } else {
            clearButton.style.display = 'none'; // Oculta el botón
        }
    }

    // Llama a la función al cargar la página para verificar si debe mostrarse
    toggleClearButton();

    // Detectar cambios en el input
    searchInput.addEventListener('input', function() {
        toggleClearButton(); // Muestra u oculta el botón según el contenido
    });

    // Limpiar el campo de búsqueda y enviar el formulario
    clearButton.addEventListener('click', function() {
        searchInput.value = ''; // Limpia el input
        toggleClearButton(); // Oculta el botón
        searchInput.focus(); // Opcional: vuelve a enfocar el campo de búsqueda
        searchInput.closest('form').submit(); // Envía el formulario
    });

    // Auto envía el formulario después de 1000ms de inactividad
    let timeout = null;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            this.closest('form').submit();
        }, 1000);
    });
});