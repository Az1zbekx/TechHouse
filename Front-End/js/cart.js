// Cart functionality
const Cart = {
    items: [],

    init() {
        this.loadFromStorage();
        this.updateCartCount();
    },

    loadFromStorage() {
        const stored = localStorage.getItem('techhouse_cart');
        if (stored) {
            this.items = JSON.parse(stored);
        }
    },

    saveToStorage() {
        localStorage.setItem('techhouse_cart', JSON.stringify(this.items));
    },

    addItem(productId, quantity = 1) {
        const existingItem = this.items.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({ productId, quantity });
        }

        this.saveToStorage();
        this.updateCartCount();
        this.showToast('Item added to cart!');
    },

    removeItem(productId) {
        this.items = this.items.filter(item => item.productId !== productId);
        this.saveToStorage();
        this.updateCartCount();
    },

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.productId === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            this.saveToStorage();
        }
    },

    getItems() {
        return this.items.map(item => {
            const product = productsData.find(p => p.id === item.productId);
            return {
                ...item,
                product
            };
        }).filter(item => item.product);
    },

    getTotal() {
        return this.getItems().reduce((total, item) => {
            return total + (item.product.price * item.quantity);
        }, 0);
    },

    getItemCount() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    },

    clear() {
        this.items = [];
        this.saveToStorage();
        this.updateCartCount();
    },

    updateCartCount() {
        const countElements = document.querySelectorAll('#cart-count');
        const count = this.getItemCount();
        countElements.forEach(el => {
            el.textContent = count;
        });
    },

    showToast(message, type = 'success') {
        // Remove existing toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }

        // Create new toast
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        // Show toast
        setTimeout(() => toast.classList.add('show'), 10);

        // Hide and remove toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', () => {
    Cart.init();
});
