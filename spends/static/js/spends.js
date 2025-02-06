document.addEventListener('DOMContentLoaded', function() {
    const chartToggleButtons = document.querySelectorAll('.chart-toggle .chart-btn');
    const chartContainers = document.querySelectorAll('.chart-container');

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

    chartToggleButtons[0].classList.add('active');
    chartContainers[0].classList.add('active');

    const periodButtons = document.querySelectorAll('.period-btn');

    periodButtons.forEach(button => {
        button.addEventListener('click', () => {
            const period = button.getAttribute('data-period-chart');
            periodButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            fetchChartData(period);
        });
    });

    async function fetchChartData(period) {
        let response = await fetch(`spends-data?period=${period}`);
        let data = await response.json();
        
        updateChart(data.dates, data.values);
    }

    function updateChart(dates, values) {
        Plotly.react('spends-chart', [{
            x: dates,
            y: values,
            type: 'bar',
        }], {
            title: 'Gastos en el tiempo',
            xaxis: {
                title: 'Fecha'
            },
            yaxis: {
                title: 'Gasto'
            },
            responsive: true
        });
    }

    fetchChartData('7d');

    // Gastos por categoría
    async function fetchCategoryData() {
        let response = await fetch('category-spends-data');
        let data = await response.json();

        updateCategoryChart(data.labels, data.values);
    }

    function updateCategoryChart(labels, values) {
        Plotly.react('category-spends-chart', [{
            labels: labels,
            values: values,
            type: 'pie',
            hole: 0.3
        }], {
            title: 'Gastos por categoría',
            responsive: true
        });
    }

    fetchCategoryData();

    const searchInput = document.querySelector('.search-input');
    const clearButton = document.querySelector('.search-clear');
    
    function toggleClearButton() {
        if (searchInput.value.trim() !== '') {
            clearButton.style.display = 'block';
        } else {
            clearButton.style.display = 'none';
        }
    }

    toggleClearButton();

    searchInput.addEventListener('input', function() {
        toggleClearButton();
    });

    clearButton.addEventListener('click', function() {
        searchInput.value = '';
        toggleClearButton();
        searchInput.focus();
        searchInput.closest('form').submit();
    });

    let timeout = null;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            this.closest('form').submit();
        }, 1000);
    });
});