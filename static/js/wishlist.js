function getWishlist() {
    return JSON.parse(localStorage.getItem('wishlist')) || [];
}

function saveWishlist(wishlist) {
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistCount();
}

function toggleWishlist(id, name, price, image) {
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

function removeFromWishlist(id) {
    let wishlist = getWishlist();
    wishlist = wishlist.filter(item => item.id !== id);
    saveWishlist(wishlist);
    displayWishlistItems();
}

function updateWishlistCount() {
    const wishlist = getWishlist();
    const countElement = document.getElementById('wishlist-count');
    if (countElement) {
        countElement.textContent = wishlist.length;
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
                        <span class="current-price">Ksh. ${item.price.toFixed(2)}</span>
                    </div>
                    <div class="product-actions">
                        <button onclick="addToCart(${item.id}, '${item.name}', ${item.price}, '${item.image}')" class="btn btn-primary">Add to Cart</button>
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

document.addEventListener('DOMContentLoaded', function() {
    updateWishlistCount();
    updateWishlistButtons();
    
    if (document.getElementById('wishlist-items-list')) {
        displayWishlistItems();
    }
});
