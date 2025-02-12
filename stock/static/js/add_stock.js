document.getElementById('id_category').addEventListener('change', function () {
    var categoryId = this.value;
    
    // Verifica que se haya seleccionado una categoría
    if (categoryId) {
        fetch(`/stock/load-subcategories/?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
            // Limpiar las opciones actuales del campo subcategoría
            var subcategoryField = document.getElementById('id_subcategory');
            subcategoryField.innerHTML = '';

            // Añadir una opción por defecto (vacía)
            var option = document.createElement('option');
            option.value = '';
            option.text = 'Seleccione una subcategoría';
            subcategoryField.appendChild(option);

            // Añadir las nuevas opciones de subcategorías
            data.subcategories.forEach(function (subcategory) {
                var option = document.createElement('option');
                option.value = subcategory.id;
                option.text = subcategory.name;
                subcategoryField.appendChild(option);
            });
        });
    }

    document.getElementById('scan-button').addEventListener('click', function () {
        const formData = {
            category: document.getElementById('id_category').value,
            subcategory: document.getElementById('id_subcategory').value,
            name: document.getElementById('id_name').value,
            quantity: document.getElementById('id_quantity').value,
            cost: document.getElementById('id_cost').value,
            price: document.getElementById('id_price').value,
            uom: document.getElementById('id_uom').value,
        };
        localStorage.setItem('addStockFormData', JSON.stringify(formData));
        window.location.href = '/stock/scan/';
    });
});