/* ============================================================
   NODALIS — Cart System (localStorage-based)
   ============================================================ */

const CART_KEY = 'nodalis_cart';

/**
 * Get current cart from localStorage
 * @returns {Array} Cart items
 */
function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch {
    return [];
  }
}

/**
 * Save cart to localStorage
 * @param {Array} cart
 */
function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCount();
}

/**
 * Add item to cart. If same product+size exists, increment quantity.
 * @param {Object} item - { _id, name, price, size, quantity, category }
 */
function addToCart(item) {
  const cart = getCart();
  const existing = cart.findIndex(c => c._id === item._id && c.size === item.size);

  if (existing >= 0) {
    cart[existing].quantity += item.quantity || 1;
  } else {
    cart.push({
      _id: item._id,
      name: item.name,
      price: item.price,
      size: item.size || null,
      quantity: item.quantity || 1,
      category: item.category,
      image: item.image || null
    });
  }

  saveCart(cart);
}

/**
 * Remove item from cart by index
 * @param {number} index
 */
function removeFromCart(index) {
  const cart = getCart();
  cart.splice(index, 1);
  saveCart(cart);
}

/**
 * Update quantity for an item
 * @param {number} index
 * @param {number} newQty
 */
function updateQuantity(index, newQty) {
  const cart = getCart();
  if (newQty <= 0) {
    cart.splice(index, 1);
  } else {
    cart[index].quantity = newQty;
  }
  saveCart(cart);
}

/**
 * Clear the entire cart
 */
function clearCart() {
  localStorage.removeItem(CART_KEY);
  updateCartCount();
}

/**
 * Get total number of items in cart
 * @returns {number}
 */
function getCartTotal() {
  return getCart().reduce((sum, item) => sum + item.quantity, 0);
}

/**
 * Get cart subtotal price
 * @returns {number}
 */
function getCartSubtotal() {
  return getCart().reduce((sum, item) => sum + item.price * item.quantity, 0);
}

/**
 * Update the cart count badge in the navigation
 */
function updateCartCount() {
  const countEl = document.getElementById('cartCount');
  if (countEl) {
    const total = getCartTotal();
    countEl.textContent = total;
    countEl.style.display = total > 0 ? 'flex' : 'none';
  }
}

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', updateCartCount);
