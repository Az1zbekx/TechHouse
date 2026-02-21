// Product detail page functionality

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = parseInt(urlParams.get('id'));

    if (!productId) {
        window.location.href = 'products.html';
        return;
    }

    const product = productsData.find(p => p.id === productId);

    if (!product) {
        window.location.href = 'products.html';
        return;
    }

    // Update page content
    document.title = `${product.name} - Tech House`;
    document.getElementById('product-image').src = product.imageUrl;
    document.getElementById('product-image').alt = product.name;
    document.getElementById('product-category').textContent = product.category;
    document.getElementById('product-name').textContent = product.name;
    document.getElementById('product-price').textContent = `$${product.price.toFixed(2)}`;
    document.getElementById('product-description').textContent = product.description;

    // Render specifications
    const specsContainer = document.getElementById('product-specs');
    specsContainer.innerHTML = Object.entries(product.specifications).map(([key, value]) => `
        <li>
            <span class="spec-label">${key}</span>
            <span class="spec-value">${value}</span>
        </li>
    `).join('');

    // Quantity controls
    const quantityInput = document.getElementById('quantity');
    const decreaseBtn = document.getElementById('qty-decrease');
    const increaseBtn = document.getElementById('qty-increase');

    decreaseBtn.addEventListener('click', () => {
        const current = parseInt(quantityInput.value);
        if (current > 1) {
            quantityInput.value = current - 1;
        }
    });

    increaseBtn.addEventListener('click', () => {
        const current = parseInt(quantityInput.value);
        if (current < 10) {
            quantityInput.value = current + 1;
        }
    });

    // Add to cart
    const addToCartBtn = document.getElementById('add-to-cart');
    addToCartBtn.addEventListener('click', () => {
        const quantity = parseInt(quantityInput.value);
        Cart.addItem(product.id, quantity);
    });

    // Mobile menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const nav = document.querySelector('.nav');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        });
    }
});
