// Main JavaScript for Tech House

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const nav = document.querySelector('.nav');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        });
    }

    // Load featured products on home page
    const featuredGrid = document.getElementById('featured-products');
    if (featuredGrid) {
        loadFeaturedProducts();
    }
});

function loadFeaturedProducts() {
    const featuredGrid = document.getElementById('featured-products');
    if (!featuredGrid) return;

    // Show first 4 products as featured
    const featured = productsData.slice(0, 6);

    featuredGrid.innerHTML = featured.map(product => createProductCard(product)).join('');

    // Add event listeners to add to cart buttons
    featuredGrid.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = parseInt(btn.dataset.productId);
            Cart.addItem(productId);
        });
    });
}

function createProductCard(product) {
    return `
        <div class="product-card">
            <div class="product-image-wrapper">
                <a href="product-detail.html?id=${product.id}">
                    <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
                </a>
            </div>
            <div class="product-content">
                <span class="product-category">${product.category}</span>
                <h3><a href="product-detail.html?id=${product.id}">${product.name}</a></h3>
                <p class="price">$${product.price.toFixed(2)}</p>
                <button class="btn btn-primary add-to-cart" data-product-id="${product.id}">
                    Add to Cart
                </button>
            </div>
        </div>
    `;
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}
