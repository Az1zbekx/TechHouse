// Products page functionality
let currentCategory = 'all';
let currentPriceRange = 'all';
let currentSort = 'name';
let currentSearch = '';

document.addEventListener('DOMContentLoaded', () => {
    // Check for category in URL
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    if (categoryParam) {
        currentCategory = categoryParam;
        // Update active filter button
        document.querySelectorAll('[data-category]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === categoryParam);
        });
    }

    // Check for search in URL
    const searchParam = urlParams.get('search');
    if (searchParam) {
        currentSearch = searchParam.toLowerCase();
        // Update search input
        const searchInput = document.getElementById('product-search');
        if (searchInput) {
            searchInput.value = searchParam;
        }
    }

    // Initial load
    renderProducts();

    // Search listener
    const searchInput = document.getElementById('product-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value.toLowerCase();
            renderProducts();
        });
    }

    // Category filter listeners
    document.querySelectorAll('[data-category]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('[data-category]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            renderProducts();
        });
    });

    // Price filter listeners
    document.querySelectorAll('.price-filter').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.price-filter').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentPriceRange = btn.dataset.price;
            renderProducts();
        });
    });

    // Sort listener
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            currentSort = e.target.value;
            renderProducts();
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

function renderProducts() {
    const productsGrid = document.getElementById('products-grid');
    const productCount = document.getElementById('product-count');
    if (!productsGrid) return;

    let filtered = [...productsData];

    // Apply search filter
    if (currentSearch) {
        filtered = filtered.filter(p =>
            p.name.toLowerCase().includes(currentSearch) ||
            p.description.toLowerCase().includes(currentSearch)
        );
    }

    // Apply category filter
    if (currentCategory !== 'all') {
        filtered = filtered.filter(p => p.category.toLowerCase().includes(currentCategory.toLowerCase()));
    }

    // Apply price filter
    if (currentPriceRange !== 'all') {
        if (currentPriceRange === '0-100') {
            filtered = filtered.filter(p => p.price < 100);
        } else if (currentPriceRange === '100-300') {
            filtered = filtered.filter(p => p.price >= 100 && p.price <= 300);
        } else if (currentPriceRange === '300+') {
            filtered = filtered.filter(p => p.price > 300);
        }
    }

    // Apply sorting
    if (currentSort === 'name') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (currentSort === 'price-low') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (currentSort === 'price-high') {
        filtered.sort((a, b) => b.price - a.price);
    }

    // Update count
    if (productCount) {
        productCount.textContent = filtered.length;
    }

    // Render products
    productsGrid.innerHTML = filtered.map(product => `
        <div class="product-card">
            <a href="product-detail.html?id=${product.id}">
                <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
            </a>
            <div class="product-content">
                <span class="product-category">${product.category}</span>
                <h3><a href="product-detail.html?id=${product.id}">${product.name}</a></h3>
                <p class="price">$${product.price.toFixed(2)}</p>
                <button class="btn btn-primary add-to-cart" data-product-id="${product.id}">
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');

    // Add event listeners to add to cart buttons
    productsGrid.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = parseInt(btn.dataset.productId);
            Cart.addItem(productId);
        });
    });
}
