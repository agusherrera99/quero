document.getElementById('id_category').addEventListener('change', function () {
    var categoryId = this.value;
    if (categoryId) {
        fetch(`/stock/load-subcategories/?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
            var subcategoryField = document.getElementById('id_subcategory');
            subcategoryField.innerHTML = '';
            var option = document.createElement('option');
            option.value = '';
            option.text = 'Seleccione una subcategoría';
            subcategoryField.appendChild(option);

            data.subcategories.forEach(function (subcategory) {
                var option = document.createElement('option');
                option.value = subcategory.id;
                option.text = subcategory.name;
                subcategoryField.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching subcategories:', error);
        });
    }
});
