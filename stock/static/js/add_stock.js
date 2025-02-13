document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.getElementById('id_category');
    const subcategoryField = document.getElementById('id_subcategory');
    const nameField = document.getElementById('id_name');
    const quantityField = document.getElementById('id_quantity');
    const costField = document.getElementById('id_cost');
    const priceField = document.getElementById('id_price');
    const uomField = document.getElementById('id_uom');
    const scanButton = document.getElementById('scan-button');

    function checkFields() {
        if (
            categoryField.value &&
            subcategoryField.value &&
            nameField.value &&
            quantityField.value &&
            costField.value &&
            priceField.value &&
            uomField.value
        ) {
            scanButton.classList.remove('disabled');
        } else {
            scanButton.classList.add('disabled');
        }
    }

    categoryField.addEventListener('change', function () {
        var categoryId = this.value;

        // Verifica que se haya seleccionado una categoría
        if (categoryId) {
            fetch(`/stock/load-subcategories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    // Limpiar las opciones actuales del campo subcategoría
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

                    checkFields(); // Verificar campos después de cargar subcategorías
                });
        } else {
            subcategoryField.innerHTML = '';
            var option = document.createElement('option');
            option.value = '';
            option.text = 'Seleccione una subcategoría';
            subcategoryField.appendChild(option);
        }

        checkFields(); // Verificar campos después de cambiar la categoría
    });

    // Agregar eventos de cambio a todos los campos para verificar si están llenos
    subcategoryField.addEventListener('change', checkFields);
    nameField.addEventListener('input', checkFields);
    quantityField.addEventListener('input', checkFields);
    costField.addEventListener('input', checkFields);
    priceField.addEventListener('input', checkFields);
    uomField.addEventListener('input', checkFields);

    scanButton.addEventListener('click', function () {
        const formData = {
            category: categoryField.value,
            subcategory: subcategoryField.value,
            name: nameField.value,
            quantity: quantityField.value,
            cost: costField.value,
            price: priceField.value,
            uom: uomField.value,
        };
        localStorage.setItem('addStockFormData', JSON.stringify(formData));
        window.location.href = '/stock/scan/';
    });

    // Inicialmente deshabilitar el botón de escaneo
    scanButton.classList.add('disabled');
});
