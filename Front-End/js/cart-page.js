// Cart page functionality

let currentDelivery = 9.99;

document.addEventListener('DOMContentLoaded', () => {
    renderCart();

    // Delivery option listeners
    document.querySelectorAll('input[name="delivery"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'home') {
                currentDelivery = 9.99;
            } else if (e.target.value === 'express') {
                currentDelivery = 19.99;
            } else {
                currentDelivery = 0;
            }
            updateTotals();
        });
    });

    // Checkout button
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            if (Cart.getItemCount() > 0) {
                document.getElementById('checkout-modal').classList.add('active');
            }
        });
    }

    // Modal close
    const modalClose = document.getElementById('modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', () => {
            document.getElementById('checkout-modal').classList.remove('active');
        });
    }

    // Close modal on outside click
    const checkoutModal = document.getElementById('checkout-modal');
    if (checkoutModal) {
        checkoutModal.addEventListener('click', (e) => {
            if (e.target === checkoutModal) {
                checkoutModal.classList.remove('active');
            }
        });
    }

    // Checkout form
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', (e) => {
            e.preventDefault();
            Cart.clear();
            document.getElementById('checkout-modal').classList.remove('active');
            Cart.showToast('Order placed successfully! (Prototype)');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        });
    }

    // Mobile menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const nav = document.querySelector('.nav');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        });
    }
});

function renderCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    const emptyCart = document.getElementById('empty-cart');
    const items = Cart.getItems();

    if (items.length === 0) {
        if (cartItemsContainer) cartItemsContainer.style.display = 'none';
        if (cartSummary) cartSummary.style.display = 'none';
        if (emptyCart) emptyCart.style.display = 'block';
        return;
    }

    if (cartItemsContainer) cartItemsContainer.style.display = 'flex';
    if (cartSummary) cartSummary.style.display = 'block';
    if (emptyCart) emptyCart.style.display = 'none';

    cartItemsContainer.innerHTML = items.map(item => `
        <div class="cart-item" data-product-id="${item.product.id}">
            <img src="${item.product.imageUrl}" alt="${item.product.name}" class="cart-item-image">
            <div class="cart-item-info">
                <h3>${item.product.name}</h3>
                <p class="category">${item.product.category}</p>
                <p class="price">$${item.product.price.toFixed(2)}</p>
                <div class="cart-item-actions">
                    <div class="quantity-selector">
                        <button class="qty-btn qty-decrease" data-product-id="${item.product.id}">-</button>
                        <input type="number" value="${item.quantity}" min="1" max="10" class="item-qty" data-product-id="${item.product.id}">
                        <button class="qty-btn qty-increase" data-product-id="${item.product.id}">+</button>
                    </div>
                    <button class="remove-btn" data-product-id="${item.product.id}">Remove</button>
                </div>
            </div>
        </div>
    `).join('');

    // Add event listeners
    cartItemsContainer.querySelectorAll('.qty-decrease').forEach(btn => {
        btn.addEventListener('click', () => {
            const productId = parseInt(btn.dataset.productId);
            const input = document.querySelector(`.item-qty[data-product-id="${productId}"]`);
            const newQty = Math.max(1, parseInt(input.value) - 1);
            input.value = newQty;
            Cart.updateQuantity(productId, newQty);
            updateTotals();
        });
    });

    cartItemsContainer.querySelectorAll('.qty-increase').forEach(btn => {
        btn.addEventListener('click', () => {
            const productId = parseInt(btn.dataset.productId);
            const input = document.querySelector(`.item-qty[data-product-id="${productId}"]`);
            const newQty = Math.min(10, parseInt(input.value) + 1);
            input.value = newQty;
            Cart.updateQuantity(productId, newQty);
            updateTotals();
        });
    });

    cartItemsContainer.querySelectorAll('.item-qty').forEach(input => {
        input.addEventListener('change', () => {
            const productId = parseInt(input.dataset.productId);
            const newQty = Math.max(1, Math.min(10, parseInt(input.value) || 1));
            input.value = newQty;
            Cart.updateQuantity(productId, newQty);
            updateTotals();
        });
    });

    cartItemsContainer.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const productId = parseInt(btn.dataset.productId);
            Cart.removeItem(productId);
            renderCart();
        });
    });

    updateTotals();
}

function updateTotals() {
    const subtotal = Cart.getTotal();
    const delivery = Cart.getItemCount() > 0 ? currentDelivery : 0;
    const total = subtotal + delivery;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('delivery').textContent = delivery === 0 ? 'Free' : `$${delivery.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}
