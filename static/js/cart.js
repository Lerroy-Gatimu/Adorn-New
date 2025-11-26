// ── AUTH DETECTION ──
function isLoggedIn() {
    return document.body.dataset.userAuthenticated === "True";
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
}

// ── Your original localStorage functions (unchanged) ──
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

// ── MODIFIED: addToCart now supports both guest & logged-in users ──
async function addToCart(id, name, price, image, quantity = 1) {
    if (isLoggedIn()) {
        // ── Logged-in user → save to database ──
        try {
            const response = await fetch('/api/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ product_id: id, quantity: quantity })
            });
            if (response.ok) {
                const data = await response.json();
                document.getElementById('cart-count').textContent = data.cart_count || 0;
                showNotification('Item added to cart!');
                if (window.location.pathname.includes('/cart/')) {
                    location.reload(); // refresh to show server items
                }
            }
        } catch (err) {
            console.error("Failed to add to server cart", err);
            alert("Please log in again.");
        }
    } else {
        // ── Guest user → use your original localStorage logic ──
        const cart = getCart();
        const existingItem = cart.find(item => item.id === id);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({
                id: id,
                name: name,
                price: parseFloat(price),
                image: image || '',
                quantity: quantity
            });
        }
        
        saveCart(cart);
        showNotification('Item added to cart!');
    }
}

// ── Keep all your other functions EXACTLY as they are ──
function removeFromCart(id) {
    if (isLoggedIn()) {
        // For logged-in users, we'll just reload the page (simpler)
        if (confirm("Remove this item?")) {
            location.href = `/cart/remove/${id}/`; // we'll create this URL later if needed
        }
    } else {
        let cart = getCart();
        cart = cart.filter(item => item.id !== id);
        saveCart(cart);
        displayCartItems();
    }
}

function updateCartQuantity(id, quantity) {
    if (isLoggedIn()) {
        location.reload(); // simple for now
        return;
    }
    const cart = getCart();
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity = parseInt(quantity);
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            saveCart(cart);
            displayCartItems();
        }
    }
}

// ── updateCartCount: show server count when logged in ──
async function updateCartCount() {
    if (isLoggedIn()) {
        try {
            const res = await fetch('/api/cart-count/');
            const data = await res.json();
            document.getElementById('cart-count').textContent = data.cart_count || 0;
        } catch (e) {
            console.error(e);
        }
    } else {
        const cart = getCart();
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        const countElement = document.getElementById('cart-count');
        if (countElement) countElement.textContent = totalItems;
    }
}

// Keep ALL your existing functions below unchanged:
function displayCartItems() { /* ... your beautiful code ... */ }
function showNotification(message) { /* ... your animation ... */ }

document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    if (document.getElementById('cart-items-list')) {
        displayCartItems();
    }
});