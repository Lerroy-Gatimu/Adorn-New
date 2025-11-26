// ── AUTH DETECTION (must be at the very top) ──
function isLoggedIn() {
    return document.body.dataset.userAuthenticated === "True";
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
}

// ── Your original localStorage functions (100% unchanged) ──
function getWishlist() {
    return JSON.parse(localStorage.getItem('wishlist')) || [];
}

function saveWishlist(wishlist) {
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistCount();
}

// ── MODIFIED: toggleWishlist now works for both guest & logged-in users ──
async function toggleWishlist(id, name, price, image) {
    if (isLoggedIn()) {
        // ── Logged-in user: use database ──
        try {
            const response = await fetch('/api/add-to-wishlist/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ product_id: id })
            });

            const data = await response.json();

            if (data.success) {
                updateWishlistCount();
                showNotification(
                    data.action === 'added' 
                        ? 'Added to wishlist!' 
                        : 'Removed from wishlist'
                );
                updateWishlistButtons();

                // If on wishlist page, reload to show server data
                if (window.location.pathname.includes('/wishlist/')) {
                    setTimeout(() => location.reload(), 800);
                }
            }
        } catch (err) {
            console.error(err);
            alert("Session expired. Please log in again.");
            window.location.href = `/login/?next=${window.location.pathname}`;
        }
    } else {
        // ── Guest user: your original perfect localStorage logic ──
        const wishlist = getWishlist();
        const existingIndex = wishlist.findIndex(item => item.id === id);
        
        if (existingIndex > -1) {
            wishlist.splice(existingIndex, 1);
            showNotification('Removed from wishlist');
        } else {
            wishlist.push({
                id: id,
                name: name,
                price: parseFloat(price),
                image: image || ''
            });
            showNotification('Added to wishlist!');
        }
        
        saveWishlist(wishlist);
        
        if (document.getElementById('wishlist-items-list')) {
            displayWishlistItems();
        }
        
        updateWishlistButtons();
    }
}

function removeFromWishlist(id) {
    if (isLoggedIn()) {
        // For logged-in users: trigger toggle to remove
        toggleWishlist(id);
    } else {
        let wishlist = getWishlist();
        wishlist = wishlist.filter(item => item.id !== id);
        saveWishlist(wishlist);
        displayWishlistItems();
    }
}

// ── MODIFIED: updateWishlistCount shows correct count for both cases ──
async function updateWishlistCount() {
    if (isLoggedIn()) {
        try {
            const res = await fetch('/api/wishlist-count/');
            const data = await res.json();
            document.getElementById('wishlist-count').textContent = data.wishlist_count || 0;
        } catch (e) {
            console.error("Failed to fetch wishlist count", e);
        }
    } else {
        const wishlist = getWishlist();
        const countElement = document.getElementById('wishlist-count');
        if (countElement) {
            countElement.textContent = wishlist.length;
        }
    }
}

function displayWishlistItems() {
    const wishlist = getWishlist();
    const wishlistEmpty = document.getElementById('wishlist-empty');
    const wishlistContent = document.getElementById('wishlist-content');
    const itemsList = document.getElementById('wishlist-items-list');
    
    if (!itemsList) return;
    
    if (wishlist.length === 0) {
        if (wishlistEmpty) wishlistEmpty.style.display = 'block';
        if (wishlistContent) wishlistContent.style.display = 'none';
        return;
    }
    
    if (wishlistEmpty) wishlistEmpty.style.display = 'none';
    if (wishlistContent) wishlistContent.style.display = 'block';
    
    let html = '';
    
    wishlist.forEach(item => {
        html += `
            <article class="product-card">
                <div class="product-image">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}">` : `<div class="placeholder-image">${item.name.charAt(0)}</div>`}
                    <button class="wishlist-btn active" onclick="removeFromWishlist(${item.id})" title="Remove from Wishlist">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                        </svg>
                    </button>
                </div>
                <div class="product-info">
                    <h3 class="product-name">${item.name}</h3>
                    <div class="product-price">
                        <span class="current-price">KES. ${item.price.toFixed(2)}</span>
                    </div>
                    <div class="product-actions">
                        <button onclick="addToCart(${item.id}, '${item.name.replace(/'/g, "\\'")}', ${item.price}, '${item.image || ''}')" class="btn btn-primary">Add to Cart</button>
                        <button onclick="removeFromWishlist(${item.id})" class="btn btn-secondary">Remove</button>
                    </div>
                </div>
            </article>
        `;
    });
    
    itemsList.innerHTML = html;
}

function updateWishlistButtons() {
    const wishlist = getWishlist();
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(button => {
        const productId = parseInt(button.getAttribute('data-product-id'));
        if (wishlist.some(item => item.id === productId)) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background-color: #2ecc71;
        color: white;
        padding: 1rem 2rem;
        border-radius: 4px;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// ── DOM Loaded ──
document.addEventListener('DOMContentLoaded', function() {
    updateWishlistCount();
    updateWishlistButtons();
    
    if (document.getElementById('wishlist-items-list')) {
        displayWishlistItems();
    }
});