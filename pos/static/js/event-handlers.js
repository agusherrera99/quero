import { CartUtils } from './cart-utils.js';

export function setupEventListeners(cartManager) {
    // Search functionality
    const searchProduct = document.getElementById('searchProduct');
    const clearSearchBtn = document.getElementById('clearSearchBtn');

    searchProduct.addEventListener('input', function() {
        const searchValue = this.value.toLowerCase();
        filterProducts(searchValue);
        toggleClearButton();
    });

    clearSearchBtn.addEventListener('click', () => clearSearch());

    // Clear cart functionality
    const clearCartBtn = document.getElementById('clearCartBtn');
    clearCartBtn.addEventListener('click', () => {
        clearCart();
    });

    // Category filtering
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => handleCategoryChange(button));
    });

    // Product selection
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('click', () => cartManager.addItemToCart(CartUtils.extractProductData(card)));
    });

    // Form submission
    const confirmSaleForm = document.getElementById('confirmSaleForm');
    confirmSaleForm.addEventListener('submit', (e) => handleFormSubmission(e));
}

function filterProducts(searchValue) {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        const productName = card.querySelector('.product-name').textContent.toLowerCase();
        if (productName.includes(searchValue)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

function toggleClearButton() {
    const searchInput = document.getElementById('searchProduct');
    const clearBtn = document.getElementById('clearSearchBtn');
    clearBtn.classList.toggle('visible', searchInput.value.length > 0);
}

function clearSearch() {
    const searchInput = document.getElementById('searchProduct');
    searchInput.value = '';
    toggleClearButton();
    filterProducts('');
}

function handleCategoryChange(button) {
    // Limpiar búsqueda
    const searchInput = document.getElementById('searchProduct');
    searchInput.value = '';
    toggleClearButton();
    
    // Actualizar botones
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    button.classList.add('selected');
    
    // Filtrar productos
    const categoryId = button.dataset.categoryId;
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        if (categoryId === '0' || card.dataset.categoryId === categoryId) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

function clearCart() {
    const cartItems = document.getElementById('cartItems');
    const totalAmount = document.getElementById('totalAmount');

    cartItems.innerHTML = `
        <tr id="emptyCart">
            <td colspan="4" style="text-align: center; padding: 1rem;">
                No hay productos en la venta actual
            </td>
        </tr>
    `;
    totalAmount.textContent = '$0.00';
    localStorage.removeItem('cart');
}

function handleFormSubmission(event) {
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
            const productStock = parseInt(row.dataset.maxStock); // Guardar el stock máximo
            cart.push({ product_id: productId, product_name: productName, quantity: quantity, price: productPrice, uom: productUom, stock: productStock });
        });

        const cartInput = document.getElementById('cartInput');
        const totalAmountInput = document.getElementById('totalAmountInput');
        cartInput.value = JSON.stringify(cart);
        totalAmountInput.value = document.getElementById('totalAmount').textContent;

        event.target.submit();
}