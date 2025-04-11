export const CartUtils = {
    createCartItem(productData) {
        return {
            product_id: productData.id,
            product_name: productData.name,
            quantity: productData.quantity || 1,
            price: productData.price,
            uom: productData.uom,
            stock: productData.stock
        };
    },

    calculatePrice(quantity, price, uom) {
        if (uom === 'gramo' || uom === 'mililitro') {
            return (quantity / 1000) * price;
        }
        return quantity * price;
    },

    validateStock(quantity, maxStock, uom) {
        if (quantity > maxStock) {
            alert(`No hay suficiente stock. Stock disponible: ${maxStock} ${uom}`);
            return false;
        }
        return true;
    },

    showEmptyCartMessage(cartContainer) {
        cartContainer.innerHTML = `
            <tr id="emptyCart">
                <td colspan="4" style="text-align: center; padding: 1rem;">
                    No hay productos en la venta actual
                </td>
            </tr>
        `;
    },

    extractProductData(productCard) {
        return {
            id: productCard.dataset.productId,
            name: productCard.querySelector('.product-name').textContent,
            price: parseFloat(productCard.querySelector('.product-price').textContent.replace('$', '')),
            uom: productCard.dataset.uom,
            stock: parseInt(productCard.dataset.stock)
        };
    }
};