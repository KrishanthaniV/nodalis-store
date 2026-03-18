/* ============================================================
   NODALIS LUXURY — Main Frontend JavaScript
   ============================================================ */

window.sampleProducts = [];

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initScrollReveal();
  initHomepage();
  initShopPage();
  updateCartCount();
});

function initNav() {
  var nav = document.getElementById('mainNav');
  var toggle = document.getElementById('navToggle');
  var mobile = document.getElementById('navMobile');
  if (nav) {
    window.addEventListener('scroll', function() {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }
  if (toggle && mobile) {
    toggle.addEventListener('click', function() {
      toggle.classList.toggle('open');
      mobile.classList.toggle('open');
    });
  }
}

function initScrollReveal() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
  document.querySelectorAll('.reveal, .fade-in').forEach(function(el) { observer.observe(el); });
}

function initHomepage() {
  var grid = document.getElementById('featuredProducts');
  if (!grid) return;
  fetchProducts('/api/products?featured=true&limit=4')
    .then(function(products) { renderProductCards(products, 'featuredProducts'); })
    .catch(function() {});
  var nlForm = document.getElementById('newsletterForm');
  if (nlForm) {
    nlForm.addEventListener('submit', function(e) {
      e.preventDefault();
      showToast('Welcome to the Nodalis inner circle!', 'success');
      nlForm.reset();
    });
  }
}

function initShopPage() {
  var shopGrid = document.getElementById('shopProducts');
  if (!shopGrid) return;
  var allProducts = [];
  var params = new URLSearchParams(window.location.search);
  var urlCategory = params.get('category');

  fetchProducts('/api/products')
    .then(function(products) {
      allProducts = products;
      applyFiltersAndSearch(allProducts, urlCategory);
    })
    .catch(function() {});

  var filterTabs = document.getElementById('filterTabs');
  if (filterTabs) {
    if (urlCategory) {
      filterTabs.querySelectorAll('.filter-tab').forEach(function(tab) {
        tab.classList.toggle('active', tab.dataset.category === urlCategory);
      });
    }
    filterTabs.addEventListener('click', function(e) {
      if (!e.target.classList.contains('filter-tab')) return;
      filterTabs.querySelectorAll('.filter-tab').forEach(function(t) { t.classList.remove('active'); });
      e.target.classList.add('active');
      applyFiltersAndSearch(allProducts);
    });
  }

  var searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function() { applyFiltersAndSearch(allProducts); });
  }
}

function applyFiltersAndSearch(allProducts, forceCategory) {
  var activeTab = document.querySelector('.filter-tab.active');
  var category = forceCategory || (activeTab ? activeTab.dataset.category : 'all');
  var searchVal = (document.getElementById('searchInput')?.value || '').toLowerCase().trim();
  var filtered = allProducts.slice();
  if (category && category !== 'all') filtered = filtered.filter(function(p) { return p.category === category; });
  if (searchVal) filtered = filtered.filter(function(p) {
    return p.name.toLowerCase().includes(searchVal) || p.description.toLowerCase().includes(searchVal);
  });
  renderProductCards(filtered, 'shopProducts');
  var noResults = document.getElementById('noResults');
  if (noResults) noResults.classList.toggle('hidden', filtered.length > 0);
}

async function fetchProducts(url) {
  var res = await fetch(url);
  if (!res.ok) throw new Error('Failed');
  return await res.json();
}

function renderProductCards(products, containerId) {
  var container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = products.map(function(p) {
    var hasImage = p.images && p.images.length > 0 && p.images[0].url;
    var outOfStock = p.stock <= 0;
    var badge = '';
    if (outOfStock) badge = '<div class="product-card-badge">Sold Out</div>';
    else if (p.badges && p.badges.includes('limited')) badge = '<div class="product-card-badge">Limited</div>';
    else if (p.badges && p.badges.includes('handmade')) badge = '<div class="product-card-badge">Handmade</div>';

    var imageContent = hasImage
      ? '<img src="' + p.images[0].url + '" alt="' + p.name + '">'
      : '<div class="product-card-placeholder">' + p.name + '</div>';

    return '<div class="product-card reveal">' +
      '<a href="/client/product.html?id=' + p._id + '">' +
      '<div class="product-card-image">' + imageContent + badge + '</div>' +
      '</a>' +
      '<div class="product-card-info">' +
      '<p class="product-card-category">' + formatCategory(p.category) + '</p>' +
      '<a href="/client/product.html?id=' + p._id + '"><h3 class="product-card-name">' + p.name + '</h3></a>' +
      '<p class="product-card-price">' + (outOfStock ? '<s style="opacity:0.4">$' + p.price.toFixed(2) + '</s>' : '$' + p.price.toFixed(2)) + '</p>' +
      '</div></div>';
  }).join('');

  initScrollReveal();
}

function quickAdd(productId) {
  fetchProducts('/api/products/' + productId).then(function(product) {
    if (!product || product.stock <= 0) { showToast('Out of stock', 'error'); return; }
    addToCart({
      _id: product._id, name: product.name, price: product.price,
      size: product.sizes?.[0] || null, quantity: 1, category: product.category,
      image: (product.images && product.images.length > 0) ? product.images[0].url : null
    });
    showToast(product.name + ' added to cart!', 'success');
  }).catch(function() { showToast('Error adding to cart', 'error'); });
}

function formatCategory(cat) {
  return (cat || '').replace(/-/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
}

function showToast(message, type) {
  var container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = 'position:fixed;top:90px;right:1.5rem;z-index:3000;display:flex;flex-direction:column;gap:0.5rem;';
    document.body.appendChild(container);
  }
  var toast = document.createElement('div');
  toast.style.cssText = 'background:#fafafa;border-radius:4px;padding:1rem 1.5rem;box-shadow:0 4px 24px rgba(0,0,0,0.12);font-size:0.85rem;display:flex;align-items:center;gap:0.8rem;animation:toastIn 0.3s ease;border-left:3px solid ' + (type === 'success' ? '#7BA06B' : '#C45B5B') + ';';
  toast.innerHTML = '<span>' + (type === 'success' ? '✓' : '✕') + '</span> ' + message;
  container.appendChild(toast);
  setTimeout(function() {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s';
    setTimeout(function() { toast.remove(); }, 300);
  }, 3000);
}
