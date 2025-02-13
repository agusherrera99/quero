document.addEventListener('DOMContentLoaded', function() {
    const cartItems = document.getElementById('cartItems');
    const isReturningFromScan = sessionStorage.getItem('returningFromScan') === 'true';
    
    if (!isReturningFromScan) {
        localStorage.removeItem('cart');
    }
    sessionStorage.removeItem('returningFromScan'); // Reset the flag

    const cart = JSON.parse(localStorage.getItem('cart') || '[]');

    // Cargar productos del carrito desde localStorage
    cart.forEach(product => {
        const newRow = document.createElement('tr');
        newRow.dataset.productId = product.product_id;
        newRow.innerHTML = `
            <td>${product.product_name}</td>
            <td class="quantity-cell">
                <input type="number" class="quantity-input" value="${product.quantity}" min="1" 
                    data-product-id="${product.product_id}" data-price="${product.price}" data-uom="${product.uom}">
            </td>
            <td class="price-cell">$${product.price}</td>
            <td class="actions-cell">
                <button class="btn-remove" title="Eliminar producto" data-product-id="${product.product_id}" aria-label="Eliminar ${product.product_name}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        cartItems.appendChild(newRow);
        setupRowEventListeners(newRow);
    });

    // Buscador de productos
    const searchProduct = document.getElementById('searchProduct');
    searchProduct.addEventListener('input', function() {
        const searchValue = this.value.toLowerCase();
        const productCards = document.querySelectorAll('.product-card');
        productCards.forEach(card => {
            const productName = card.querySelector('.product-name').textContent.toLowerCase();
            if (productName.includes(searchValue)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Selección de categoría
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            categoryButtons.forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected');
            
            const categoryId = this.dataset.categoryId;
            const productCards = document.querySelectorAll('.product-card');
            productCards.forEach(card => {
                if (categoryId == 0 || card.dataset.categoryId == categoryId) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Selección de productos
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('click', function() {
            AddToCart(this);
        });
    });

    // Limpiar el carrito de ventas actual
    const clearCartBtn = document.getElementById('clearCartBtn');
    clearCartBtn.addEventListener('click', function() {
        cartItems.innerHTML = `
            <tr id="emptyCart">
                <td colspan="4" style="text-align: center; padding: 1rem;">
                    No hay productos en la venta actual
                </td>
            </tr>
        `;
        localStorage.removeItem('cart');
        updateTotalAmount();
    });

    // Función para actualizar el total de la fila
    function updateRowTotal(row, quantity, price, uom) {
        let totalPrice;

        if (uom === 'unidad') {
            totalPrice = quantity * price;
        } else if (uom === 'kilogramo' || uom === 'litro') {
            totalPrice = quantity * price;
        } else if (uom === 'gramo' || uom === 'mililitro') {
            // Convertimos gramos o mililitros a la unidad base (kilogramo o litro)
            totalPrice = (quantity / 1000) * price; // Conversión a kilos o litros
        } else {
            totalPrice = 0;
        }

        row.querySelector('.price-cell').textContent = `$${totalPrice.toFixed(2)}`;
        updateTotalAmount(); // Actualizamos el total general del carrito
    }

    // Actualiza el total de todos los productos en el carrito
    function updateTotalAmount() {
        const rows = cartItems.querySelectorAll('tr[data-product-id]');
        let total = 0;

        rows.forEach(row => {
            const quantityInput = row.querySelector('.quantity-input');
            const price = parseFloat(quantityInput.dataset.price);
            const quantity = parseFloat(quantityInput.value);
            const uom = quantityInput.dataset.uom;

            let rowTotal = quantity * price; // Calculamos el total de la fila

            if (uom === 'gramo' || uom === 'mililitro') {
                rowTotal = (quantity / 1000) * price; // Ajuste para gramos/mililitros
            }

            total += rowTotal;
        });

        const totalAmountSpan = document.getElementById('totalAmount');
        totalAmountSpan.textContent = total.toFixed(2);
    }

    // Añadir un producto al carrito
    function AddToCart(productCard) {
        const productId = productCard.dataset.productId;
        const productName = productCard.querySelector('.product-name').textContent;
        const productPrice = parseFloat(productCard.querySelector('.product-price').textContent.replace('$', ''));
        const productUom = productCard.dataset.uom;

        // Chequear si el producto ya está en el carrito
        const existingItem = cartItems.querySelector(`tr[data-product-id="${productId}"]`);

        if (existingItem) {
            // Actualizar la cantidad del producto existente
            const quantityInput = existingItem.querySelector('.quantity-input');
            const newQuantity = parseInt(quantityInput.value) + 1;
            quantityInput.value = newQuantity;

            updateRowTotal(existingItem, newQuantity, productPrice, productUom);  // Se pasa el precio correctamente
        } else {
            // Elimina el mensaje de carrito vacío si está presente
            const emptyCart = document.getElementById('emptyCart');
            if (emptyCart) {
                emptyCart.remove();
            }

            // Añadir una nueva fila al carrito
            const newRow = document.createElement('tr');
            newRow.dataset.productId = productId;
            newRow.innerHTML = `
                <td>${productName}</td>
                <td class="quantity-cell">
                    <input type="number" class="quantity-input" value="1" min="1" 
                        data-product-id="${productId}" data-price="${productPrice}" data-uom="${productUom}">
                </td>
                <td class="price-cell">$${productPrice}</td> <!-- Se muestra el precio de manera correcta -->
                <td class="actions-cell">
                    <button class="btn-remove" title="Eliminar producto" data-product-id="${productId}" aria-label="Eliminar ${productName}">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            cartItems.appendChild(newRow);

            // Añadir manejadores de eventos para la nueva fila
            setupRowEventListeners(newRow);
        }
        
        // Feedback visual (efecto de destello rápido)
        productCard.classList.add('added-to-cart');
        setTimeout(() => productCard.classList.remove('added-to-cart'), 300);

        updateTotalAmount();
        saveCartToLocalStorage();
    }

    // Agrega manejadores de eventos a las filas del carrito
    function setupRowEventListeners(row) {
        // Actualiza la cantidad cuando se cambia el input de cantidad
        const quantityInputs = document.querySelectorAll('.quantity-input');
        quantityInputs.forEach(input => {
            input.addEventListener('input', function() {
                const quantity = parseFloat(this.value);
                const price = parseFloat(this.dataset.price);
                const uom = this.dataset.uom;

                updateRowTotal(this.closest('tr'), quantity, price, uom);
                saveCartToLocalStorage();
            });
        });
        
        // Evento que se dispara cuando se elimina un producto del carrito
        const removeButton = row.querySelector('.btn-remove');
        removeButton.addEventListener('click', function() {
            row.remove();
            updateTotalAmount();
            saveCartToLocalStorage();
            
            // Show empty cart message if no items left
            if (!cartItems.querySelector('tr[data-product-id]')) {
                cartItems.innerHTML = `
                    <tr id="emptyCart">
                        <td colspan="4" style="text-align: center; padding: 1rem;">
                            No hay productos en la venta actual
                        </td>
                    </tr>
                `;
            }
        });
    }

    // Guardar el carrito en localStorage
    function saveCartToLocalStorage() {
        const rows = cartItems.querySelectorAll('tr[data-product-id]');
        const cart = [];

        rows.forEach(row => {
            const productId = row.dataset.productId;
            const productName = row.querySelector('td').textContent;
            const quantity = row.querySelector('.quantity-input').value;
            const productPrice = parseFloat(row.querySelector('.price-cell').textContent.replace('$', ''));
            const productUom = row.querySelector('.quantity-input').dataset.uom;
            cart.push({ product_id: productId, product_name: productName, quantity: quantity, price: productPrice, uom: productUom });
        });

        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Esto se ejecuta cuando la página se carga por primera vez
    const existingRows = cartItems.querySelectorAll('tr[data-product-id]');
    existingRows.forEach(setupRowEventListeners); // Esto agrega los manejadores de eventos a los productos ya en el carrito

    // Confirmar venta
    const confirmSaleForm = document.getElementById('confirmSaleForm');
    confirmSaleForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const rows = cartItems.querySelectorAll('tr[data-product-id]');

        if (rows.length === 0) {
            alert('No hay productos en el carrito. Por favor, agrega productos antes de confirmar la venta.');
            return;
        }

        const cart = [];
        rows.forEach(row => {
            const productId = row.dataset.productId;
            const productName = row.querySelector('td').textContent;
            const quantity = row.querySelector('.quantity-input').value;
            const productPrice = parseFloat(row.querySelector('.price-cell').textContent.replace('$', ''));
            const productUom = row.querySelector('.quantity-input').dataset.uom;
            cart.push({ product_id: productId, product_name: productName, quantity: quantity, price: productPrice, uom: productUom });
        });

        const cartInput = document.getElementById('cartInput');
        const totalAmountInput = document.getElementById('totalAmountInput');
        cartInput.value = JSON.stringify(cart);
        totalAmountInput.value = document.getElementById('totalAmount').textContent;

        this.submit();
    });
});