#!/usr/bin/env python3
"""
NODALIS UPDATE — Homepage Content Management from Admin
Run from: ~/Downloads/nodalis-v5/nodalis-store
Usage: python3 update-homepage-admin.py

Creates:
  - server/models/SiteContent.js  (MongoDB model for homepage content)
  - server/routes/content.js      (API routes for content CRUD)
  - admin/homepage.html           (Admin page to edit homepage sections)
  - Updates server.js to register new routes
  - Updates admin sidebar nav to include Homepage link
  - Updates client/index.html to load dynamic content
"""
import os, glob, re

print("🔧 Nodalis Update: Homepage Content Management")
print("=" * 55)

# ========================================
# 1. CREATE server/models/SiteContent.js
# ========================================
print("\n1/6 — Creating SiteContent model...")

site_content_model = '''/* ============================================================
   NODALIS — Site Content Model (Homepage & Settings)
   ============================================================ */

const mongoose = require('mongoose');

const siteContentSchema = new mongoose.Schema({
  section: {
    type: String,
    required: true,
    unique: true,
    enum: ['hero', 'categories', 'about-preview', 'newsletter', 'highlight', 'instagram', 'general']
  },
  data: {
    // HERO
    heroEyebrow: { type: String, default: 'Handcrafted \\u00B7 Limited Edition \\u00B7 One of a Kind' },
    heroTitle: { type: String, default: 'The Art of' },
    heroTitleEm: { type: String, default: 'Handmade' },
    heroDescription: { type: String, default: '' },
    heroCtaText: { type: String, default: 'Discover the Collection' },
    heroCtaLink: { type: String, default: '/client/shop.html' },
    heroMediaType: { type: String, enum: ['image', 'video', 'placeholder'], default: 'placeholder' },
    heroMediaUrl: { type: String, default: '' },

    // CATEGORIES (array of 4 categories)
    categories: [{
      name: String,
      slug: String,
      imageUrl: String
    }],

    // ABOUT PREVIEW
    aboutTitle: { type: String, default: '' },
    aboutDescription: { type: String, default: '' },
    aboutImageUrl: { type: String, default: '' },
    aboutCtaText: { type: String, default: 'Discover Our Story' },

    // HIGHLIGHT / QUOTE
    highlightQuote: { type: String, default: '' },
    highlightAuthor: { type: String, default: '' },

    // NEWSLETTER
    newsletterTitle: { type: String, default: '' },
    newsletterDescription: { type: String, default: '' },

    // INSTAGRAM
    instagramHandle: { type: String, default: '@nodalis.lk' },
    instagramImages: [{ url: String }],

    // GENERAL
    siteName: { type: String, default: 'Nodalis' },
    tagline: { type: String, default: 'Timeless Pieces' }
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

siteContentSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

module.exports = mongoose.model('SiteContent', siteContentSchema);
'''

with open("server/models/SiteContent.js", "w") as f:
    f.write(site_content_model)
print("   ✅ server/models/SiteContent.js created")


# ========================================
# 2. CREATE server/routes/content.js
# ========================================
print("\n2/6 — Creating content API routes...")

content_routes = '''/* ============================================================
   NODALIS — Site Content Routes (Homepage Management)
   ============================================================ */

const express = require('express');
const router = express.Router();
const SiteContent = require('../models/SiteContent');
const { protect, adminOnly } = require('../middleware/auth');

// GET all content sections (public)
router.get('/', async (req, res) => {
  try {
    const content = await SiteContent.find({});
    const result = {};
    content.forEach(c => { result[c.section] = c.data; });
    res.json(result);
  } catch (err) {
    res.status(500).json({ message: 'Error loading content' });
  }
});

// GET single section (public)
router.get('/:section', async (req, res) => {
  try {
    const content = await SiteContent.findOne({ section: req.params.section });
    if (!content) return res.json({ data: {} });
    res.json(content);
  } catch (err) {
    res.status(500).json({ message: 'Error loading content' });
  }
});

// PUT update a section (admin only)
router.put('/:section', protect, adminOnly, async (req, res) => {
  try {
    const content = await SiteContent.findOneAndUpdate(
      { section: req.params.section },
      { section: req.params.section, data: req.body },
      { upsert: true, new: true, runValidators: true }
    );
    res.json({ success: true, content });
  } catch (err) {
    console.error('Content update error:', err);
    res.status(500).json({ message: 'Error saving content' });
  }
});

module.exports = router;
'''

with open("server/routes/content.js", "w") as f:
    f.write(content_routes)
print("   ✅ server/routes/content.js created")


# ========================================
# 3. UPDATE server/server.js — register content routes
# ========================================
print("\n3/6 — Registering content routes in server.js...")

with open("server/server.js", "r") as f:
    server_js = f.read()

if "content" not in server_js.lower() or "contentRoutes" not in server_js:
    # Add require
    server_js = server_js.replace(
        "const uploadRoutes = require('./routes/upload');",
        "const uploadRoutes = require('./routes/upload');\nconst contentRoutes = require('./routes/content');"
    )
    # Add route
    server_js = server_js.replace(
        "app.use('/api/upload', uploadRoutes);",
        "app.use('/api/upload', uploadRoutes);\napp.use('/api/content', contentRoutes);"
    )
    with open("server/server.js", "w") as f:
        f.write(server_js)
    print("   ✅ Content routes registered")
else:
    print("   ⏭️  Content routes already registered")


# ========================================
# 4. CREATE admin/homepage.html
# ========================================
print("\n4/6 — Creating admin homepage editor...")

# Read an existing admin page to get the style block
with open("admin/dashboard.html", "r") as f:
    dashboard_html = f.read()

# Extract the <head> section up to </style> for reuse
head_end = dashboard_html.find("</style>") + len("</style>")
head_section = dashboard_html[:head_end]
# Replace the title
head_section = head_section.replace("<title>", "<title>Homepage Editor — ")

homepage_admin = head_section + '''
</head>
<body>
<div class="admin-layout">
  <!-- SIDEBAR -->
  <aside class="admin-sidebar">
    <div class="logo-area">
      <a href="/"><img src="/assets/logo/nodalis-logo.png" alt="Nodalis"></a>
      <p class="admin-subtitle">Admin Panel</p>
    </div>
    <nav class="admin-nav">
      <a href="/admin/dashboard.html" class="admin-nav-item">
        <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        Dashboard
      </a>
      <a href="/admin/products.html" class="admin-nav-item">
        <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
        Products
      </a>
      <a href="/admin/orders.html" class="admin-nav-item">
        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        Orders
      </a>
      <a href="/admin/homepage.html" class="admin-nav-item active">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
        Homepage
      </a>
      <a href="/admin/media.html" class="admin-nav-item">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        Media
      </a>
    </nav>
  </aside>

  <!-- MAIN -->
  <main class="admin-main">
    <div class="admin-header">
      <h1>Homepage Editor</h1>
      <button class="btn-luxury btn-gold" onclick="saveAllSections()">Save All Changes</button>
    </div>

    <!-- HERO SECTION -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Hero Section</h3>
      <div class="form-group">
        <label>Eyebrow Text</label>
        <input type="text" id="heroEyebrow" placeholder="Handcrafted · Limited Edition · One of a Kind">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Title (main text)</label>
          <input type="text" id="heroTitle" placeholder="The Art of">
        </div>
        <div class="form-group">
          <label>Title (italic/gold part)</label>
          <input type="text" id="heroTitleEm" placeholder="Handmade">
        </div>
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="heroDesc" rows="2" placeholder="Crocheted pieces, hand-painted tees & artisan accessories..."></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Button Text</label>
          <input type="text" id="heroCtaText" placeholder="Discover the Collection">
        </div>
        <div class="form-group">
          <label>Button Link</label>
          <input type="text" id="heroCtaLink" placeholder="/client/shop.html">
        </div>
      </div>
      <div class="form-group">
        <label>Hero Media Type</label>
        <select id="heroMediaType">
          <option value="placeholder">Dark Gradient (default)</option>
          <option value="image">Image</option>
          <option value="video">Video</option>
        </select>
      </div>
      <div class="form-group" id="heroMediaUrlGroup" style="display:none;">
        <label>Media URL (upload via Media page first, then paste URL)</label>
        <input type="text" id="heroMediaUrl" placeholder="/uploads/hero-image.jpg or /uploads/hero-video.mp4">
      </div>
      <div id="heroMediaPreview" style="margin-top:.5rem;"></div>
    </div>

    <!-- ABOUT PREVIEW -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">About Preview Section</h3>
      <div class="form-group">
        <label>Title</label>
        <input type="text" id="aboutTitle" placeholder="Every Piece Tells a Story">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="aboutDesc" rows="3" placeholder="Our pieces are crafted by hand in small batches..."></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Button Text</label>
          <input type="text" id="aboutCtaText" placeholder="Discover Our Story">
        </div>
        <div class="form-group">
          <label>Image URL</label>
          <input type="text" id="aboutImageUrl" placeholder="/uploads/about-image.jpg">
        </div>
      </div>
    </div>

    <!-- HIGHLIGHT / QUOTE -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Highlight Quote</h3>
      <div class="form-group">
        <label>Quote Text</label>
        <textarea id="highlightQuote" rows="2" placeholder="Fashion should be sustainable, personal, and made with love."></textarea>
      </div>
      <div class="form-group">
        <label>Author</label>
        <input type="text" id="highlightAuthor" placeholder="— Nodalis">
      </div>
    </div>

    <!-- NEWSLETTER -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Newsletter Section</h3>
      <div class="form-group">
        <label>Title</label>
        <input type="text" id="newsletterTitle" placeholder="Join the Nodalis Circle">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="newsletterDesc" rows="2" placeholder="Be the first to know about new drops..."></textarea>
      </div>
    </div>

    <!-- CATEGORY IMAGES -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Category Card Images</h3>
      <p style="font-size:.82rem;color:var(--grey);margin-bottom:1rem;">Upload images via the Media page, then paste the URL here for each category.</p>
      <div class="form-row">
        <div class="form-group">
          <label>Crochet Tops Image</label>
          <input type="text" id="catCrochetImg" placeholder="/uploads/cat-crochet.jpg">
        </div>
        <div class="form-group">
          <label>Bags Image</label>
          <input type="text" id="catBagsImg" placeholder="/uploads/cat-bags.jpg">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Hand-Painted Tees Image</label>
          <input type="text" id="catTeesImg" placeholder="/uploads/cat-tees.jpg">
        </div>
        <div class="form-group">
          <label>Accessories Image</label>
          <input type="text" id="catAccessoriesImg" placeholder="/uploads/cat-accessories.jpg">
        </div>
      </div>
    </div>

    <div style="text-align:center;padding:2rem 0;">
      <button class="btn-luxury btn-dark" onclick="saveAllSections()">Save All Changes</button>
    </div>
  </main>
</div>

<div class="toast" id="toast"></div>

<script>
var token = localStorage.getItem('adminToken') || localStorage.getItem('token');
if (!token) window.location.href = '/client/login.html';

var heroMediaType = document.getElementById('heroMediaType');
var heroMediaUrlGroup = document.getElementById('heroMediaUrlGroup');
heroMediaType.addEventListener('change', function() {
  heroMediaUrlGroup.style.display = this.value === 'placeholder' ? 'none' : 'block';
});

// Load existing content
async function loadContent() {
  try {
    var res = await fetch('/api/content');
    if (!res.ok) return;
    var data = await res.json();

    // Hero
    if (data.hero) {
      document.getElementById('heroEyebrow').value = data.hero.heroEyebrow || '';
      document.getElementById('heroTitle').value = data.hero.heroTitle || '';
      document.getElementById('heroTitleEm').value = data.hero.heroTitleEm || '';
      document.getElementById('heroDesc').value = data.hero.heroDescription || '';
      document.getElementById('heroCtaText').value = data.hero.heroCtaText || '';
      document.getElementById('heroCtaLink').value = data.hero.heroCtaLink || '';
      document.getElementById('heroMediaType').value = data.hero.heroMediaType || 'placeholder';
      document.getElementById('heroMediaUrl').value = data.hero.heroMediaUrl || '';
      if (data.hero.heroMediaType !== 'placeholder') heroMediaUrlGroup.style.display = 'block';
    }

    // About
    if (data['about-preview']) {
      var a = data['about-preview'];
      document.getElementById('aboutTitle').value = a.aboutTitle || '';
      document.getElementById('aboutDesc').value = a.aboutDescription || '';
      document.getElementById('aboutCtaText').value = a.aboutCtaText || '';
      document.getElementById('aboutImageUrl').value = a.aboutImageUrl || '';
    }

    // Highlight
    if (data.highlight) {
      document.getElementById('highlightQuote').value = data.highlight.highlightQuote || '';
      document.getElementById('highlightAuthor').value = data.highlight.highlightAuthor || '';
    }

    // Newsletter
    if (data.newsletter) {
      document.getElementById('newsletterTitle').value = data.newsletter.newsletterTitle || '';
      document.getElementById('newsletterDesc').value = data.newsletter.newsletterDescription || '';
    }

    // Categories
    if (data.categories && data.categories.categories) {
      var cats = data.categories.categories;
      cats.forEach(function(c) {
        if (c.slug === 'crochet-tops') document.getElementById('catCrochetImg').value = c.imageUrl || '';
        if (c.slug === 'bags') document.getElementById('catBagsImg').value = c.imageUrl || '';
        if (c.slug === 'hand-painted-tees') document.getElementById('catTeesImg').value = c.imageUrl || '';
        if (c.slug === 'accessories') document.getElementById('catAccessoriesImg').value = c.imageUrl || '';
      });
    }
  } catch (err) {
    console.log('No saved content yet — using defaults');
  }
}

async function saveSection(section, data) {
  var res = await fetch('/api/content/' + section, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
    body: JSON.stringify(data)
  });
  return res.ok;
}

async function saveAllSections() {
  try {
    var results = await Promise.all([
      saveSection('hero', {
        heroEyebrow: document.getElementById('heroEyebrow').value,
        heroTitle: document.getElementById('heroTitle').value,
        heroTitleEm: document.getElementById('heroTitleEm').value,
        heroDescription: document.getElementById('heroDesc').value,
        heroCtaText: document.getElementById('heroCtaText').value,
        heroCtaLink: document.getElementById('heroCtaLink').value,
        heroMediaType: document.getElementById('heroMediaType').value,
        heroMediaUrl: document.getElementById('heroMediaUrl').value
      }),
      saveSection('about-preview', {
        aboutTitle: document.getElementById('aboutTitle').value,
        aboutDescription: document.getElementById('aboutDesc').value,
        aboutCtaText: document.getElementById('aboutCtaText').value,
        aboutImageUrl: document.getElementById('aboutImageUrl').value
      }),
      saveSection('highlight', {
        highlightQuote: document.getElementById('highlightQuote').value,
        highlightAuthor: document.getElementById('highlightAuthor').value
      }),
      saveSection('newsletter', {
        newsletterTitle: document.getElementById('newsletterTitle').value,
        newsletterDescription: document.getElementById('newsletterDesc').value
      }),
      saveSection('categories', {
        categories: [
          { name: 'Crochet Tops', slug: 'crochet-tops', imageUrl: document.getElementById('catCrochetImg').value },
          { name: 'Bags', slug: 'bags', imageUrl: document.getElementById('catBagsImg').value },
          { name: 'Hand-Painted Tees', slug: 'hand-painted-tees', imageUrl: document.getElementById('catTeesImg').value },
          { name: 'Accessories', slug: 'accessories', imageUrl: document.getElementById('catAccessoriesImg').value }
        ]
      })
    ]);

    if (results.every(r => r)) {
      showToast('All sections saved!', 'success');
    } else {
      showToast('Some sections failed to save', 'error');
    }
  } catch (err) {
    showToast('Error saving: ' + err.message, 'error');
  }
}

function showToast(msg, type) {
  var toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.style.background = type === 'success' ? '#7BA06B' : type === 'error' ? '#C45B5B' : 'var(--charcoal)';
  toast.classList.add('show');
  setTimeout(function() { toast.classList.remove('show'); }, 3000);
}

loadContent();
</script>
</body>
</html>
'''

with open("admin/homepage.html", "w") as f:
    f.write(homepage_admin)
print("   ✅ admin/homepage.html created")


# ========================================
# 5. UPDATE admin sidebar on all admin pages
# ========================================
print("\n5/6 — Adding Homepage link to admin sidebar...")

admin_pages = glob.glob("admin/*.html")
for filepath in admin_pages:
    if filepath == "admin/homepage.html":
        continue
    with open(filepath, "r") as f:
        content = f.read()
    
    if "homepage.html" in content:
        print(f"   ⏭️  {filepath} already has link")
        continue
    
    # Add Homepage nav item after Orders
    homepage_nav = '''<a href="/admin/homepage.html" class="admin-nav-item">
        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
        Homepage
      </a>'''
    
    # Try to insert after the Orders nav item
    if "Orders" in content and "admin-nav-item" in content:
        # Find the Orders nav item and insert after it
        orders_pattern = r'(Orders\s*</a>)'
        match = re.search(orders_pattern, content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n      " + homepage_nav + content[insert_pos:]
            with open(filepath, "w") as f:
                f.write(content)
            print(f"   ✅ {filepath}")
        else:
            print(f"   ⚠️  Could not find insert point: {filepath}")
    else:
        print(f"   ⚠️  No Orders nav: {filepath}")


# ========================================
# 6. ADD dynamic content loading to index.html
# ========================================
print("\n6/6 — Adding dynamic content loading to homepage...")

with open("client/index.html", "r") as f:
    index_html = f.read()

# Add a script that loads content from API and updates the DOM
dynamic_script = '''
<script>
// ---- DYNAMIC HOMEPAGE CONTENT ----
(async function loadHomepageContent() {
  try {
    var res = await fetch('/api/content');
    if (!res.ok) return;
    var data = await res.json();

    // Hero
    if (data.hero) {
      var h = data.hero;
      var eyebrow = document.querySelector('.hero-eyebrow');
      var title = document.querySelector('.hero-content h1');
      var sub = document.querySelector('.hero-sub');
      var cta = document.querySelector('.hero-cta');
      var media = document.querySelector('.hero-media');

      if (eyebrow && h.heroEyebrow) eyebrow.textContent = h.heroEyebrow;
      if (title && h.heroTitle) title.innerHTML = h.heroTitle + '<br><em>' + (h.heroTitleEm || '') + '</em>';
      if (sub && h.heroDescription) sub.textContent = h.heroDescription;
      if (cta && h.heroCtaText) {
        var svgHtml = cta.querySelector('svg') ? cta.querySelector('svg').outerHTML : '';
        cta.innerHTML = h.heroCtaText + ' ' + svgHtml;
        if (h.heroCtaLink) cta.setAttribute('href', h.heroCtaLink);
      }

      // Hero media
      if (media && h.heroMediaType === 'image' && h.heroMediaUrl) {
        media.innerHTML = '<img src="' + h.heroMediaUrl + '" alt="Nodalis Hero" style="width:100%;height:100%;object-fit:cover;opacity:.5;">';
      } else if (media && h.heroMediaType === 'video' && h.heroMediaUrl) {
        media.innerHTML = '<video autoplay muted loop playsinline style="width:100%;height:100%;object-fit:cover;opacity:.5;"><source src="' + h.heroMediaUrl + '"></video>';
      }
    }

    // About preview
    if (data['about-preview']) {
      var a = data['about-preview'];
      var aboutSection = document.querySelector('.about-preview-content');
      if (aboutSection) {
        var aboutTitle = aboutSection.querySelector('.section-title, h2');
        var aboutDesc = aboutSection.querySelector('.section-desc, p:not(.section-eyebrow)');
        var aboutCta = aboutSection.querySelector('a');
        if (aboutTitle && a.aboutTitle) aboutTitle.textContent = a.aboutTitle;
        if (aboutDesc && a.aboutDescription) aboutDesc.textContent = a.aboutDescription;
        if (aboutCta && a.aboutCtaText) aboutCta.textContent = a.aboutCtaText;
      }
      // About image
      if (a.aboutImageUrl) {
        var aboutImg = document.querySelector('.about-preview-image img');
        if (aboutImg) aboutImg.src = a.aboutImageUrl;
        else {
          var aboutImgDiv = document.querySelector('.about-preview-image');
          if (aboutImgDiv) aboutImgDiv.innerHTML = '<img src="' + a.aboutImageUrl + '" alt="About Nodalis">';
        }
      }
    }

    // Highlight quote
    if (data.highlight) {
      var q = data.highlight;
      var blockquote = document.querySelector('.highlight-section blockquote');
      var cite = document.querySelector('.highlight-section cite');
      if (blockquote && q.highlightQuote) blockquote.textContent = q.highlightQuote;
      if (cite && q.highlightAuthor) cite.textContent = q.highlightAuthor;
    }

    // Newsletter
    if (data.newsletter) {
      var n = data.newsletter;
      var nlSection = document.querySelector('.newsletter-section, .newsletter');
      if (nlSection) {
        var nlTitle = nlSection.querySelector('.section-title');
        var nlDesc = nlSection.querySelector('.section-desc');
        if (nlTitle && n.newsletterTitle) nlTitle.textContent = n.newsletterTitle;
        if (nlDesc && n.newsletterDescription) nlDesc.textContent = n.newsletterDescription;
      }
    }

    // Category images
    if (data.categories && data.categories.categories) {
      data.categories.categories.forEach(function(cat) {
        if (!cat.imageUrl) return;
        var slug = cat.slug;
        var cardBg = document.querySelector('.cat-' + slug.replace('-', ''));
        if (!cardBg) cardBg = document.querySelector('[class*="cat-' + slug.split('-')[0] + '"]');
        if (cardBg) {
          cardBg.style.backgroundImage = 'url(' + cat.imageUrl + ')';
          cardBg.style.backgroundSize = 'cover';
          cardBg.style.backgroundPosition = 'center';
        }
      });
    }

  } catch (err) {
    console.log('Using default homepage content');
  }
})();
</script>
'''

if "loadHomepageContent" not in index_html:
    # Insert before </body>
    index_html = index_html.replace("</body>", dynamic_script + "\n</body>")
    with open("client/index.html", "w") as f:
        f.write(index_html)
    print("   ✅ Dynamic content loading added to index.html")
else:
    print("   ⏭️  Already has dynamic loading")


print("\n" + "=" * 55)
print("✅ ALL DONE! Now push to GitHub:")
print("")
print("   git add -A")
print('   git commit -m "Feature: homepage editor in admin panel"')
print("   git push")
print("")
print("After deploy, go to:")
print("  https://nodalis-store-production.up.railway.app/admin/homepage.html")
print("  Login as admin → edit hero text, upload images, etc.")
print("=" * 55)
