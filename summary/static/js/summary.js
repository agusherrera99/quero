document.addEventListener('DOMContentLoaded', function() {
    // Gráficos principales
    const chartToggleButtons = document.querySelectorAll('.chart-toggle .chart-btn');
    const chartContainers = document.querySelectorAll('.chart-container');

    // Funcion para alternar entre los gráficos principales
    chartToggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const chartType = button.getAttribute('data-chart');

            chartToggleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const selectedChart = button.textContent.trim().toLowerCase();

            chartContainers.forEach(container => {
                container.classList.remove('active');

                if (container.id === `${selectedChart}-chart`) {
                    container.classList.add('active');
                }
            });
        });
    });

    // Inicializar la interfaz para mostrar el primer gráfico por defecto (Ventas en el tiempo)
    chartToggleButtons[0].classList.add('active'); // Activa el primer botón "Ventas en el tiempo" por defecto
    chartContainers[0].classList.add('active'); // Muestra el gráfico de ventas en el tiempo por defecto

    // Ventas en el tiempo
    // Función para alternar entre los periodos de tiempo
    const periodButtons = document.querySelectorAll('.period-btn');
    const periodContainers = document.querySelectorAll('.chart-period-container');

    periodButtons.forEach(button => {
        button.addEventListener('click', () => {
            const period = button.getAttribute('data-period-chart');
            periodButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            periodContainers.forEach(container => {
                container.classList.remove('active');
                if (container.id === `${period}-chart`) {
                    container.classList.add('active');
                }
            });
        });
    });

    // Ventas por categorias/subcategorias
    // Función para alternar entre las categorías y subcategorías
    const categorySubcategoriesButtons = document.querySelectorAll('.chart-type-btn');
    const categorySubcategoriesContainer = document.querySelectorAll('.chart-type-container');

    categorySubcategoriesButtons.forEach(button => {
        button.addEventListener('click', () => {
            const chartType = button.getAttribute('data-type-chart');
            
            categorySubcategoriesButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            categorySubcategoriesContainer.forEach(container => {
                container.classList.remove('active');
                if (container.id === `${chartType}-chart`) {
                    container.classList.add('active');
                }
            });
        });
    });

    // Tablas de productos más vendidos e historial de ventas
    // Este código es solo un marcador de posición y no actualizará realmente los datos de la tabla
    const tableToggleButtons = document.querySelectorAll('.table-toggle .toggle-btn');
    const tableContainers = document.querySelectorAll('.table-container');

    tableToggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tableType = button.getAttribute('data-table');
            tableToggleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            tableContainers.forEach(container => {
                container.classList.remove('active');
                if (container.id === `${tableType}-table`) {
                    container.classList.add('active');
                }
            });
        });
    });

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