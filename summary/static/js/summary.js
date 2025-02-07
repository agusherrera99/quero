document.addEventListener('DOMContentLoaded', function() {
    // Gráficos principales
    const chartToggleButtons = document.querySelectorAll('.chart-toggle .chart-btn');
    const chartContainers = document.querySelectorAll('.chart-container');

    // Funcion para alternar entre los gráficos principales
    chartToggleButtons.forEach(button => {
        button.addEventListener('click', () => {
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
    const salesPeriodButton = document.querySelectorAll('.sales-period-btn');
    
    // Función para alternar entre los periodos de tiempo para el gráfico de ventas en el tiempo
    salesPeriodButton.forEach(button => {
        button.addEventListener('click', () => {
            const period = button.getAttribute('data-period-sales');
            salesPeriodButton.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            fetchSalesChartData(period);
        });
    });

    async function fetchSalesChartData(period) {
        let response = await fetch(`sales-data?period=${period}`);
        let data = await response.json();
        
        updateSalesChart(data.dates, data.values);
    }

    function updateSalesChart(dates, values) {
        Plotly.react('sales-chart', [{
            x: dates,
            y: values,
            type: 'bar',
        }], {
            title: 'Ventas en el tiempo',
            xaxis: {
                title: 'Fecha'
            },
            yaxis: {
                title: 'Ventas'
            },
            responsive: true
        });
    }

    // Cargar datos para el periodo 7 días al cargar la página
    fetchSalesChartData('7d');

    // Función para cargar datos de categorías
    async function fetchCategoryData() {
        let response = await fetch(`category-sales-data`);
        let data = await response.json();
        updateCategoryChart(data.labels, data.values);
    }

    // Función para cargar datos de subcategorías
    async function fetchSubcategoryData() {
        let response = await fetch(`subcategory-sales-data`);
        let data = await response.json();
        updateSubcategoryChart(data.labels, data.values);
    }

    // Función para actualizar el gráfico de categorías
    function updateCategoryChart(labels, values) {
        Plotly.react('category-chart', [{
            labels: labels,
            values: values,
            type: 'pie',
            hole: 0.3
        }], {
            title: 'Ventas por Categoría',
            responsive: true
        });
    }

    // Función para actualizar el gráfico de subcategorías
    function updateSubcategoryChart(labels, values) {
        Plotly.react('subcategory-chart', [{
            labels: labels,
            values: values,
            type: 'pie',
            hole: 0.3
        }], {
            title: 'Ventas por Subcategoría',
            responsive: true
        });
    }

    // Ventas por categorias/subcategorias
    
    // Cargar datos de categorías y subcategorías al cambiar entre gráficos
    const categorySubcategoriesButtons = document.querySelectorAll('.chart-type-btn');
    const categoryContainer = document.getElementById('category-chart');
    const subcategoryContainer = document.getElementById('subcategory-chart');

    categorySubcategoriesButtons.forEach(button => {
        button.addEventListener('click', () => {
            const chartType = button.getAttribute('data-type-chart');

            categorySubcategoriesButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            if (chartType === 'category') {
                fetchCategoryData();
                categoryContainer.style.display = 'block';
                subcategoryContainer.style.display = 'none';
            } else if (chartType === 'subcategory') {
                fetchSubcategoryData();
                subcategoryContainer.style.display = 'block';
                categoryContainer.style.display = 'none';
            }
        });
    });

    // Cargar datos de categorías por defecto al cargar la página
    fetchCategoryData();

    // Tablas de productos más vendidos e historial de ventas
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

    // Función para alternar entre los periodos de tiempo para el gráfico de ingresos vs gastos
    const incomeSpendsPeriodButton = document.querySelectorAll('.income-spends-period-btn');

    incomeSpendsPeriodButton.forEach(button => {
        button.addEventListener('click', () => {
            const period = button.getAttribute('data-period-income-spends');
            incomeSpendsPeriodButton.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            fetchIncomeSpendsData(period);
        });
    });

    async function fetchIncomeSpendsData(period) {
        let response = await fetch(`income-spends-data?period=${period}`);
        let data = await response.json();
        
        updateIncomeSpendsChart(data.dates, data.incomes, data.spends);
    };

    function updateIncomeSpendsChart(dates, incomes, spends) {
        Plotly.react('income-spends-chart', [{
            x: dates,
            y: incomes,
            type: 'area',
            mode: 'line',
            fill: 'tozeroy', // Relleno bajo la curva
            name: 'Ingresos'
        }, {
            x: dates,
            y: spends,
            type: 'area',
            mode: 'line',
            fill: 'tozeroy',
            name: 'Gastos'
        }], {
            title: 'Ingresos vs Gastos',
            xaxis: {
                title: 'Fecha'
            },
            yaxis: {
                title: 'Cantidad'
            },
            responsive: true
        });
    };

    fetchIncomeSpendsData('7d');

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