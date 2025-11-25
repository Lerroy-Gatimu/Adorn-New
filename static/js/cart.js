function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(id, name, price, image, quantity = 1) {
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

function removeFromCart(id) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== id);
    saveCart(cart);
    displayCartItems();
}

function updateCartQuantity(id, quantity) {
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

function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = totalItems;
    }
}

function displayCartItems() {
    const cart = getCart();
    const cartEmpty = document.getElementById('cart-empty');
    const cartContent = document.getElementById('cart-content');
    const itemsList = document.getElementById('cart-items-list');
    
    if (!itemsList) return;
    
    if (cart.length === 0) {
        if (cartEmpty) cartEmpty.style.display = 'block';
        if (cartContent) cartContent.style.display = 'none';
        return;
    }
    
    if (cartEmpty) cartEmpty.style.display = 'none';
    if (cartContent) cartContent.style.display = 'grid';
    
    let html = '';
    let total = 0;
    
    cart.forEach(item => {
        const subtotal = item.price * item.quantity;
        total += subtotal;
        
        html += `
            <div class="cart-item">
                <div class="cart-item-image">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}">` : `<div class="placeholder-image">${item.name.charAt(0)}</div>`}
                </div>
                <div class="cart-item-info">
                    <h3 class="cart-item-name">${item.name}</h3>
                    <p class="cart-item-price">KES. ${item.price.toFixed(2)}</p>
                    <div class="cart-item-actions">
                        <div class="quantity-selector">
                            <button onclick="updateCartQuantity(${item.id}, ${item.quantity - 1})" class="quantity-btn">-</button>
                            <input type="number" value="${item.quantity}" min="1" readonly style="width: 50px; text-align: center; border: 1px solid #e0e0e0;">
                            <button onclick="updateCartQuantity(${item.id}, ${item.quantity + 1})" class="quantity-btn">+</button>
                        </div>
                        <button onclick="removeFromCart(${item.id})" class="btn btn-secondary" style="padding: 0.5rem 1rem;">Remove</button>
                    </div>
                </div>
                <div class="cart-item-subtotal">
                    <strong>KES. ${subtotal.toFixed(2)}</strong>
                </div>
            </div>
        `;
    });
    
    itemsList.innerHTML = html;
    
    const subtotalElement = document.getElementById('cart-subtotal');
    const totalElement = document.getElementById('cart-total');
    
    if (subtotalElement) subtotalElement.textContent = `KES. ${total.toFixed(2)}`;
    if (totalElement) totalElement.textContent = `KES. ${total.toFixed(2)}`;
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

document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    if (document.getElementById('cart-items-list')) {
        displayCartItems();
    }
});
