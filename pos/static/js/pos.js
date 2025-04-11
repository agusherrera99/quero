import { CartUtils } from './cart-utils.js';
import { setupEventListeners } from './event-handlers.js';

document.addEventListener('DOMContentLoaded', function() {
    // DOM events
    const elements = {
        cartItems: document.getElementById('cartItems'),
        searchProduct: document.getElementById('search-product'),
        clearSearchBtn: document.getElementById('clearSearchBtn'),
        totalAmountBtn: document.getElementById('totalAmount'),
        confirmSaleForm: document.getElementById('confirmSaleForm'),
        clearCartBtn: document.getElementById('clearCartBtn')
    };

    class CartManager {
        constructor(container) {
            this.container = container;
            this.initializeCart();
        }


        initializeCart() {
            if (!sessionStorage.getItem('returningFromScan')) {
                localStorage.removeItem('cart');
            }
            sessionStorage.removeItem('returningFromScan');
            
            this.loadCartFromStorage();
        }

        loadCartFromStorage() {
            const savedCart = JSON.parse(localStorage.getItem('cart') || '[]');
            savedCart.forEach(item => this.addItemToCart(item));
            
            this.updateTotal();
        }

        addItemToCart(productData) {
            const existingItem = this.findExistingItem(productData.id);

            if (existingItem) {
                this.updateExitingItem(existingItem, productData);
            } else {
                this.createNewCartItem(productData);
            }

            this.updateTotal();
            this.saveCart();
        }

        findExistingItem(productId) {
            return this.container.querySelector(`tr[data-product-id="${productId}"]`);
        }

        updateExitingItem(row, productData) {
            const input = row.querySelector('.quantity-input');
            const newQuantity = parseInt(input.value) + 1;

            if (CartUtils.validateStock(newQuantity, productData.stock, productData.uom)) {
                input.value = newQuantity;

                this.updateRowTotal(row);
            }
        }

        updateRowTotal(row) {
            const input = row.querySelector('.quantity-input');
            const quantity = parseFloat(input.value);
            const price = parseFloat(input.dataset.price);
            const uom = input.dataset.uom;

            const total = CartUtils.calculatePrice(quantity, price, uom);
            row.querySelector('.price-cell').textContent = `$${total.toFixed(2)}`;

            this.updateTotal();
            this.saveCart();
        }

        createNewCartItem(productData) {
            const row = document.createElement('tr');
            row.dataset.productId = productData.id;
            row.dataset.maxStock = productData.stock;
            row.innerHTML = this.generateRowHTML(productData);

            this.container.appendChild(row);
            this.setupRowEventListeners(row);
        }

        generateRowHTML(product) {
            return `
                <td>${product.name}</td>
                <td class="quantity-cell">
                    <input type="number" class="quantity-input" value="1" min="1" max="${product.stock}"
                        data-product-id="${product.id}" data-price="${product.price}" data-uom="${product.uom}">
                </td>
                <td class="price-cell">$${product.price}</td>
                <td class="actions-cell">
                    <button class="btn-remove" title="Eliminar producto" data-product-id="${product.id}" 
                        aria-label="Eliminar ${product.name}">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
        }

        setupRowEventListeners(row) {
            this.setupQuantityListener(row);
            this.setupRemoveListener(row);
        }

        setupQuantityListener(row) {
            const input = row.querySelector('.quantity-input');
            const maxStock = parseInt(row.dataset.maxStock);

            input.addEventListener('change', () => {
                let quantity = parseInt(input.value);

                if (quantity < 1) {
                    quantity = 1;
                    input.value = 1;
                }

                if (CartUtils.validateStock(quantity, maxStock, input.dataset.uom)) {
                    this.updateRowTotal(row)
                } else {
                    input.value = maxStock;
                    this.updateRowTotal(row);
                }
            });
        }

        setupRemoveListener(row) {
            const removeBtn = row.querySelector('.btn-remove');
            removeBtn.addEventListener('click', () => {
                row.remove();
                this.updateTotal();
                this.saveCart();

                if (!this.container.querySelector('tr[data-product-id]')) {
                    CartUtils.showEmptyCartMessage(this.container);
                }
            });
        }

        updateTotal() {
            const rows = this.container.querySelectorAll('tr[data-product-id]');
            const total = Array.from(rows).reduce((sum, row) => {
                const input = row.querySelector('.quantity-input');
                return sum + CartUtils.calculatePrice(
                    parseFloat(input.value),
                    parseFloat(input.dataset.price),
                    input.dataset.uom
                );
            }, 0);
            elements.totalAmountBtn.textContent = total.toFixed(2);
        }

        saveCart() {
            const cartData = Array.from(this.container.querySelectorAll('tr[data-product-id]'))
                .map(row => CartUtils.createCartItem({
                    id: row.dataset.productId,
                    name: row.querySelector('td').textContent,
                    quantity: row.querySelector('.quantity-input').value,
                    price: parseFloat(row.querySelector('.price-cell').textContent),
                    uom: row.querySelector('.quantity-input').dataset.uom,
                    stock: parseInt(row.dataset.maxStock)
                }));
            localStorage.setItem('cart', JSON.stringify(cartData));
        }
    }

    // Initialize
    const cartManager = new CartManager(elements.cartItems);
    setupEventListeners(cartManager);

});