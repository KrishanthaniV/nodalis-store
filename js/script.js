/* ============================================================
   NODALIS — Main Frontend JavaScript
   ============================================================ */

// ---- Sample Products (used when backend is unavailable) ----
window.sampleProducts = [
  {
    _id: 'prod_001',
    name: 'Sage Garden Crochet Top',
    price: 68.00,
    category: 'crochet-tops',
    description: 'A delicate crochet crop top in sage green, featuring an intricate floral pattern. Made with 100% organic cotton yarn. Perfect for layering or wearing solo on warm evenings.',
    stock: 8,
    sizes: ['XS', 'S', 'M', 'L'],
    badges: ['handmade'],
    featured: true
  },
  {
    _id: 'prod_002',
    name: 'Sunset Bloom Hand-Painted Tee',
    price: 95.00,
    category: 'hand-painted-tees',
    description: 'One-of-a-kind hand-painted oversized tee on 300 GSM heavyweight cotton. Abstract sunset blooms in warm oranges and soft pinks. Each piece is uniquely painted — no two are alike.',
    stock: 3,
    sizes: ['S', 'M', 'L', 'XL'],
    badges: ['handmade', 'limited'],
    featured: true
  },
  {
    _id: 'prod_003',
    name: 'Luna Crochet Tote Bag',
    price: 54.00,
    category: 'bags',
    description: 'A spacious crochet tote bag in cream and beige tones. Features a magnetic closure and inner lining. Perfect for market days and everyday carry.',
    stock: 12,
    sizes: [],
    badges: ['handmade'],
    featured: true
  },
  {
    _id: 'prod_004',
    name: 'Abstract Waves Painted Tee',
    price: 89.00,
    category: 'hand-painted-tees',
    description: 'Oversized 300 GSM tee with hand-painted abstract ocean waves. Blues, teals, and white crests. Wearable art that turns heads. Unisex fit.',
    stock: 5,
    sizes: ['M', 'L', 'XL'],
    badges: ['handmade', 'limited'],
    featured: true
  },
  {
    _id: 'prod_005',
    name: 'Wildflower Crochet Halter',
    price: 72.00,
    category: 'crochet-tops',
    description: 'A bohemian halter-neck crochet top with wildflower motifs. Handmade with soft bamboo-blend yarn for a lightweight, breathable feel. Ties at the neck and back.',
    stock: 6,
    sizes: ['XS', 'S', 'M'],
    badges: ['handmade'],
    featured: false
  },
  {
    _id: 'prod_006',
    name: 'Handmade Beaded Earrings Set',
    price: 32.00,
    category: 'accessories',
    description: 'A set of three pairs of handmade beaded drop earrings in sage, cream, and warm brown. Lightweight and comfortable for all-day wear. Hypoallergenic hooks.',
    stock: 20,
    sizes: [],
    badges: ['handmade'],
    featured: false
  },
  {
    _id: 'prod_007',
    name: 'Oversized Essentials Tee — Oat',
    price: 48.00,
    category: 'oversized-tees',
    description: 'Premium 220 GSM oversized unisex tee in warm oat. Dropped shoulders, boxy fit, and ribbed neckline. The perfect everyday staple with a Nodalis woven label.',
    stock: 25,
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    badges: [],
    featured: true
  },
  {
    _id: 'prod_008',
    name: 'Mini Crochet Crossbody',
    price: 42.00,
    category: 'bags',
    description: 'A charming mini crossbody bag in dusty rose crochet. Features an adjustable strap and zip closure. Just the right size for phone, keys, and essentials.',
    stock: 0,
    sizes: [],
    badges: ['handmade'],
    featured: false
  }
];

// ---- Navigation ----
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initScrollAnimations();
  initHomepage();
  initShopPage();
  updateCartCount();
});

function initNav() {
  const nav = document.getElementById('mainNav');
  const toggle = document.getElementById('navToggle');
  const mobile = document.getElementById('navMobile');

  // Scroll behavior — add shadow on scroll
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // Mobile toggle
  if (toggle && mobile) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      mobile.classList.toggle('open');
    });
  }
}

// ---- Scroll Animations ----
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// ---- Homepage ----
function initHomepage() {
  const featuredGrid = document.getElementById('featuredProducts');
  if (!featuredGrid) return;

  // Try fetching from API first, fallback to sample
  fetchProducts('/api/products?featured=true&limit=4')
    .then(products => {
      renderProductCards(products, 'featuredProducts');
    })
    .catch(() => {
      const featured = window.sampleProducts.filter(p => p.featured).slice(0, 4);
      renderProductCards(featured, 'featuredProducts');
    });

  // Newsletter
  const nlForm = document.getElementById('newsletterForm');
  if (nlForm) {
    nlForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showToast('Thanks for subscribing! Welcome to the Nodalis community.', 'success');
      nlForm.reset();
    });
  }
}

// ---- Shop Page ----
function initShopPage() {
  const shopGrid = document.getElementById('shopProducts');
  if (!shopGrid) return;

  let allProducts = [];

  // Check for URL category filter
  const params = new URLSearchParams(window.location.search);
  const urlCategory = params.get('category');

  // Load products
  fetchProducts('/api/products')
    .then(products => {
      allProducts = products;
      applyFiltersAndSearch(allProducts, urlCategory);
    })
    .catch(() => {
      allProducts = [...window.sampleProducts];
      applyFiltersAndSearch(allProducts, urlCategory);
    });

  // Filter tabs
  const filterTabs = document.getElementById('filterTabs');
  if (filterTabs) {
    // If URL has category, set active tab
    if (urlCategory) {
      filterTabs.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.category === urlCategory);
      });
    }

    filterTabs.addEventListener('click', (e) => {
      if (!e.target.classList.contains('filter-tab')) return;
      filterTabs.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      e.target.classList.add('active');
      applyFiltersAndSearch(allProducts);
    });
  }

  // Search
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      applyFiltersAndSearch(allProducts);
    });
  }
}

function applyFiltersAndSearch(allProducts, forceCategory) {
  const activeTab = document.querySelector('.filter-tab.active');
  const category = forceCategory || (activeTab ? activeTab.dataset.category : 'all');
  const searchVal = (document.getElementById('searchInput')?.value || '').toLowerCase().trim();

  let filtered = [...allProducts];

  // Category filter
  if (category && category !== 'all') {
    filtered = filtered.filter(p => p.category === category);
  }

  // Search filter
  if (searchVal) {
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(searchVal) ||
      p.description.toLowerCase().includes(searchVal) ||
      p.category.toLowerCase().includes(searchVal)
    );
  }

  renderProductCards(filtered, 'shopProducts');

  // Show/hide no results
  const noResults = document.getElementById('noResults');
  if (noResults) {
    noResults.classList.toggle('hidden', filtered.length > 0);
  }
}

// ---- Fetch Products Helper ----
async function fetchProducts(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch');
  return await res.json();
}

// ---- Render Product Cards ----
function renderProductCards(products, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = products.map(p => {
    const hue = hashStr(p.name) % 360;
    const outOfStock = p.stock <= 0;
    const badges = (p.badges || []).map(b => {
      if (b === 'handmade') return '<span class="badge badge-handmade">Handmade</span>';
      if (b === 'limited') return '<span class="badge badge-limited">Limited</span>';
      return '';
    }).join('');

    const hasImage = p.images && p.images.length > 0 && p.images[0].url;

    return `
      <div class="product-card fade-in">
        <a href="/client/product.html?id=${p._id}">
          <div class="product-card-image" style="${hasImage ? '' : 'background: hsl(' + hue + ', 20%, 82%);'}">
            ${hasImage
              ? `<img src="${p.images[0].url}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;">`
              : `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-family:var(--font-accent);font-size:1.1rem;color:hsl(${hue},25%,45%);padding:1rem;text-align:center;">${p.name}</div>`
            }
            <div class="product-card-badges">
              ${badges}
              ${outOfStock ? '<span class="badge badge-out">Sold Out</span>' : ''}
            </div>
            <div class="product-card-actions">
              <button class="btn-icon" onclick="event.preventDefault(); quickAdd('${p._id}')" title="Quick Add">
                <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
              </button>
              <button class="btn-icon" onclick="event.preventDefault(); openQuickView('${p._id}')" title="Quick View">
                <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            </div>
          </div>
        </a>
        <div class="product-card-info">
          <p class="product-card-category">${formatCategory(p.category)}</p>
          <a href="/client/product.html?id=${p._id}">
            <h3 class="product-card-name">${p.name}</h3>
          </a>
          <p class="product-card-price">${outOfStock ? '<s style="opacity:0.5">$' + p.price.toFixed(2) + '</s> Sold Out' : '$' + p.price.toFixed(2)}</p>
        </div>
      </div>
    `;
  }).join('');

  // Re-observe new fade-in elements
  initScrollAnimations();
}

// ---- Quick Add to Cart ----
function quickAdd(productId) {
  const product = findProduct(productId);
  if (!product || product.stock <= 0) {
    showToast('This item is currently out of stock.', 'error');
    return;
  }
  addToCart({
    _id: product._id,
    name: product.name,
    price: product.price,
    size: product.sizes?.[0] || null,
    quantity: 1,
    category: product.category,
    image: (product.images && product.images.length > 0) ? product.images[0].url : null
  });
  showToast(`${product.name} added to cart!`, 'success');
}

// ---- Quick View ----
function openQuickView(productId) {
  const product = findProduct(productId);
  if (!product) return;
  const modal = document.getElementById('quickViewModal');
  const content = document.getElementById('quickViewContent');
  if (!modal || !content) return;

  const hue = hashStr(product.name) % 360;
  const hasImage = product.images && product.images.length > 0 && product.images[0].url;
  content.innerHTML = `
    <div class="quick-view-image" style="${hasImage ? '' : 'background: hsl(' + hue + ', 20%, 82%); display:flex;align-items:center;justify-content:center;font-family:var(--font-accent);color:hsl(' + hue + ',25%,45%);'}">
      ${hasImage ? `<img src="${product.images[0].url}" alt="${product.name}" style="width:100%;height:100%;object-fit:cover;">` : product.name}
    </div>
    <div>
      <p class="product-card-category">${formatCategory(product.category)}</p>
      <h3 style="font-family:var(--font-display);font-size:1.4rem;margin:var(--space-sm) 0;">${product.name}</h3>
      <p class="product-card-price" style="font-size:1.2rem;margin-bottom:var(--space-md);">$${product.price.toFixed(2)}</p>
      <p style="font-size:0.9rem;color:var(--charcoal-light);margin-bottom:var(--space-lg);line-height:1.7;">${product.description}</p>
      ${product.stock <= 0 ? '<p style="color:var(--error);font-weight:600;">Out of Stock</p>' : `
        <a href="/client/product.html?id=${product._id}" class="btn btn-primary" style="width:100%;margin-bottom:var(--space-sm);">View Full Details</a>
        <button class="btn btn-secondary" style="width:100%;" onclick="quickAdd('${product._id}'); closeQuickView();">Add to Cart</button>
      `}
    </div>
  `;
  modal.classList.add('open');
}

function closeQuickView() {
  const modal = document.getElementById('quickViewModal');
  if (modal) modal.classList.remove('open');
}

// ---- Helpers ----
function findProduct(id) {
  return window.sampleProducts.find(p => p._id === id) || null;
}

function formatCategory(cat) {
  return cat.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function hashStr(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = str.charCodeAt(i) + ((h << 5) - h);
  return Math.abs(h);
}

// ---- Toast Notifications ----
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === 'success' ? '✓' : '✕'}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 300ms ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
