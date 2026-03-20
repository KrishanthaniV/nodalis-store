#!/usr/bin/env python3
"""
NODALIS — Update Homepage Editor with Direct Image Upload
Run from: ~/Downloads/nodalis-v5/nodalis-store
"""

print("🔧 Updating Homepage Editor with direct uploads...")

# Read the current homepage.html to get the head/style section
with open("admin/homepage.html") as f:
    old = f.read()

# Extract everything up to </style>
style_end = old.find("</style>") + len("</style>")
head_section = old[:style_end]

new_html = head_section + """
</head>
<body>
<div class="admin-layout">
  <aside class="admin-sidebar">
    <div class="logo-area">
      <a href="/"><img src="/assets/logo/nodalis-logo.png" alt="Nodalis"></a>
      <p class="admin-subtitle">Admin Panel</p>
    </div>
    <nav class="admin-nav">
      <a href="/admin/dashboard.html" class="admin-nav-item"><svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>Dashboard</a>
      <a href="/admin/products.html" class="admin-nav-item"><svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>Products</a>
      <a href="/admin/orders.html" class="admin-nav-item"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Orders</a>
      <a href="/admin/homepage.html" class="admin-nav-item active"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>Homepage</a>
      <a href="/admin/media.html" class="admin-nav-item"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>Media</a>
    </nav>
  </aside>

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
        <label>Hero Background (image or video)</label>
        <div style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
          <input type="file" id="heroMediaFile" accept="image/*,video/*" style="flex:1;padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;">
          <span id="heroMediaStatus" style="font-size:.75rem;color:var(--grey);"></span>
        </div>
        <div id="heroMediaPreview" style="margin-top:.8rem;"></div>
      </div>
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
      <div class="form-group">
        <label>Button Text</label>
        <input type="text" id="aboutCtaText" placeholder="Discover Our Story">
      </div>
      <div class="form-group">
        <label>About Image</label>
        <div style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
          <input type="file" id="aboutImageFile" accept="image/*" style="flex:1;padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;">
          <span id="aboutImageStatus" style="font-size:.75rem;color:var(--grey);"></span>
        </div>
        <div id="aboutImagePreview" style="margin-top:.8rem;"></div>
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
      <div class="form-row">
        <div class="form-group">
          <label>Crochet Tops</label>
          <input type="file" id="catCrochetFile" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;">
          <div id="catCrochetPreview" style="margin-top:.5rem;"></div>
        </div>
        <div class="form-group">
          <label>Bags</label>
          <input type="file" id="catBagsFile" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;">
          <div id="catBagsPreview" style="margin-top:.5rem;"></div>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Hand-Painted Tees</label>
          <input type="file" id="catTeesFile" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;">
          <div id="catTeesPreview" style="margin-top:.5rem;"></div>
        </div>
        <div class="form-group">
          <label>Accessories</label>
          <input type="file" id="catAccessoriesFile" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;">
          <div id="catAccessoriesPreview" style="margin-top:.5rem;"></div>
        </div>
      </div>
    </div>

    <!-- INSTAGRAM IMAGES -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Instagram Section Images (6 images)</h3>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
        <div class="form-group"><label>Image 1</label><input type="file" id="insta1File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta1Preview" style="margin-top:.5rem;"></div></div>
        <div class="form-group"><label>Image 2</label><input type="file" id="insta2File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta2Preview" style="margin-top:.5rem;"></div></div>
        <div class="form-group"><label>Image 3</label><input type="file" id="insta3File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta3Preview" style="margin-top:.5rem;"></div></div>
        <div class="form-group"><label>Image 4</label><input type="file" id="insta4File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta4Preview" style="margin-top:.5rem;"></div></div>
        <div class="form-group"><label>Image 5</label><input type="file" id="insta5File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta5Preview" style="margin-top:.5rem;"></div></div>
        <div class="form-group"><label>Image 6</label><input type="file" id="insta6File" accept="image/*" style="padding:.5rem;border:1px solid var(--cream-dark);font-size:.85rem;width:100%;"><div id="insta6Preview" style="margin-top:.5rem;"></div></div>
      </div>
    </div>

    <div style="text-align:center;padding:2rem 0;">
      <button class="btn-luxury btn-dark" onclick="saveAllSections()" id="saveBtn">Save All Changes</button>
      <p style="font-size:.75rem;color:var(--grey);margin-top:.5rem;">Images will be uploaded automatically when you save.</p>
    </div>
  </main>
</div>

<div class="toast" id="toast"></div>

<script>
var token = localStorage.getItem('nodalis_token');
if (!token) window.location.href = '/client/login.html';

// Store uploaded URLs
var uploadedUrls = {
  heroMedia: '', aboutImage: '',
  catCrochet: '', catBags: '', catTees: '', catAccessories: '',
  insta1: '', insta2: '', insta3: '', insta4: '', insta5: '', insta6: ''
};

// Upload a single file and return the URL
async function uploadFile(fileInput) {
  if (!fileInput || !fileInput.files || !fileInput.files[0]) return null;
  var formData = new FormData();
  formData.append('image', fileInput.files[0]);
  try {
    var res = await fetch('/api/upload', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token },
      body: formData
    });
    if (res.ok) {
      var data = await res.json();
      return data.url;
    }
  } catch (err) {
    console.error('Upload error:', err);
  }
  return null;
}

// Show preview for file inputs
function setupPreview(inputId, previewId) {
  var input = document.getElementById(inputId);
  if (!input) return;
  input.addEventListener('change', function() {
    var file = this.files[0];
    if (!file) return;
    var preview = document.getElementById(previewId);
    if (file.type.startsWith('video/')) {
      preview.innerHTML = '<video src="' + URL.createObjectURL(file) + '" style="width:120px;height:80px;object-fit:cover;" muted></video>';
    } else {
      preview.innerHTML = '<img src="' + URL.createObjectURL(file) + '" style="width:120px;height:80px;object-fit:cover;">';
    }
  });
}

// Setup all previews
setupPreview('heroMediaFile', 'heroMediaPreview');
setupPreview('aboutImageFile', 'aboutImagePreview');
setupPreview('catCrochetFile', 'catCrochetPreview');
setupPreview('catBagsFile', 'catBagsPreview');
setupPreview('catTeesFile', 'catTeesPreview');
setupPreview('catAccessoriesFile', 'catAccessoriesPreview');
for (var i = 1; i <= 6; i++) setupPreview('insta' + i + 'File', 'insta' + i + 'Preview');

// Load existing content
async function loadContent() {
  try {
    var res = await fetch('/api/content');
    if (!res.ok) return;
    var data = await res.json();

    if (data.hero) {
      document.getElementById('heroEyebrow').value = data.hero.heroEyebrow || '';
      document.getElementById('heroTitle').value = data.hero.heroTitle || '';
      document.getElementById('heroTitleEm').value = data.hero.heroTitleEm || '';
      document.getElementById('heroDesc').value = data.hero.heroDescription || '';
      document.getElementById('heroCtaText').value = data.hero.heroCtaText || '';
      document.getElementById('heroCtaLink').value = data.hero.heroCtaLink || '';
      if (data.hero.heroMediaUrl) {
        uploadedUrls.heroMedia = data.hero.heroMediaUrl;
        var isVideo = data.hero.heroMediaUrl.match(/\\.(mp4|webm|mov)$/i);
        document.getElementById('heroMediaPreview').innerHTML = isVideo
          ? '<video src="' + data.hero.heroMediaUrl + '" style="width:200px;height:120px;object-fit:cover;" muted controls></video><p style="font-size:.7rem;color:var(--grey);">Current hero media</p>'
          : '<img src="' + data.hero.heroMediaUrl + '" style="width:200px;height:120px;object-fit:cover;"><p style="font-size:.7rem;color:var(--grey);">Current hero image</p>';
        document.getElementById('heroMediaStatus').textContent = 'Current: ' + data.hero.heroMediaUrl;
      }
    }

    if (data['about-preview']) {
      var a = data['about-preview'];
      document.getElementById('aboutTitle').value = a.aboutTitle || '';
      document.getElementById('aboutDesc').value = a.aboutDescription || '';
      document.getElementById('aboutCtaText').value = a.aboutCtaText || '';
      if (a.aboutImageUrl) {
        uploadedUrls.aboutImage = a.aboutImageUrl;
        document.getElementById('aboutImagePreview').innerHTML = '<img src="' + a.aboutImageUrl + '" style="width:120px;height:80px;object-fit:cover;"><p style="font-size:.7rem;color:var(--grey);">Current</p>';
      }
    }

    if (data.highlight) {
      document.getElementById('highlightQuote').value = data.highlight.highlightQuote || '';
      document.getElementById('highlightAuthor').value = data.highlight.highlightAuthor || '';
    }

    if (data.newsletter) {
      document.getElementById('newsletterTitle').value = data.newsletter.newsletterTitle || '';
      document.getElementById('newsletterDesc').value = data.newsletter.newsletterDescription || '';
    }

    if (data.categories && data.categories.categories) {
      data.categories.categories.forEach(function(c) {
        var key = c.slug === 'crochet-tops' ? 'catCrochet' : c.slug === 'bags' ? 'catBags' : c.slug === 'hand-painted-tees' ? 'catTees' : c.slug === 'accessories' ? 'catAccessories' : '';
        if (key && c.imageUrl) {
          uploadedUrls[key] = c.imageUrl;
          var previewId = key + 'Preview';
          var el = document.getElementById(previewId);
          if (el) el.innerHTML = '<img src="' + c.imageUrl + '" style="width:120px;height:80px;object-fit:cover;">';
        }
      });
    }

    if (data.instagram && data.instagram.instagramImages) {
      data.instagram.instagramImages.forEach(function(img, idx) {
        if (img.url) {
          uploadedUrls['insta' + (idx + 1)] = img.url;
          var el = document.getElementById('insta' + (idx + 1) + 'Preview');
          if (el) el.innerHTML = '<img src="' + img.url + '" style="width:120px;height:80px;object-fit:cover;">';
        }
      });
    }
  } catch (err) {
    console.log('No saved content yet');
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
  var btn = document.getElementById('saveBtn');
  btn.textContent = 'Uploading & Saving...';
  btn.disabled = true;

  try {
    // Upload any new files first
    var heroFile = document.getElementById('heroMediaFile');
    if (heroFile.files.length > 0) {
      var url = await uploadFile(heroFile);
      if (url) uploadedUrls.heroMedia = url;
    }

    var aboutFile = document.getElementById('aboutImageFile');
    if (aboutFile.files.length > 0) {
      var url = await uploadFile(aboutFile);
      if (url) uploadedUrls.aboutImage = url;
    }

    // Category images
    var catFiles = [
      { id: 'catCrochetFile', key: 'catCrochet' },
      { id: 'catBagsFile', key: 'catBags' },
      { id: 'catTeesFile', key: 'catTees' },
      { id: 'catAccessoriesFile', key: 'catAccessories' }
    ];
    for (var c of catFiles) {
      var f = document.getElementById(c.id);
      if (f && f.files.length > 0) {
        var url = await uploadFile(f);
        if (url) uploadedUrls[c.key] = url;
      }
    }

    // Instagram images
    for (var i = 1; i <= 6; i++) {
      var f = document.getElementById('insta' + i + 'File');
      if (f && f.files.length > 0) {
        var url = await uploadFile(f);
        if (url) uploadedUrls['insta' + i] = url;
      }
    }

    // Determine hero media type
    var heroMediaType = 'placeholder';
    if (uploadedUrls.heroMedia) {
      heroMediaType = uploadedUrls.heroMedia.match(/\\.(mp4|webm|mov)$/i) ? 'video' : 'image';
    }

    // Save all sections
    var results = await Promise.all([
      saveSection('hero', {
        heroEyebrow: document.getElementById('heroEyebrow').value,
        heroTitle: document.getElementById('heroTitle').value,
        heroTitleEm: document.getElementById('heroTitleEm').value,
        heroDescription: document.getElementById('heroDesc').value,
        heroCtaText: document.getElementById('heroCtaText').value,
        heroCtaLink: document.getElementById('heroCtaLink').value,
        heroMediaType: heroMediaType,
        heroMediaUrl: uploadedUrls.heroMedia
      }),
      saveSection('about-preview', {
        aboutTitle: document.getElementById('aboutTitle').value,
        aboutDescription: document.getElementById('aboutDesc').value,
        aboutCtaText: document.getElementById('aboutCtaText').value,
        aboutImageUrl: uploadedUrls.aboutImage
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
          { name: 'Crochet Tops', slug: 'crochet-tops', imageUrl: uploadedUrls.catCrochet },
          { name: 'Bags', slug: 'bags', imageUrl: uploadedUrls.catBags },
          { name: 'Hand-Painted Tees', slug: 'hand-painted-tees', imageUrl: uploadedUrls.catTees },
          { name: 'Accessories', slug: 'accessories', imageUrl: uploadedUrls.catAccessories }
        ]
      }),
      saveSection('instagram', {
        instagramHandle: '@nodalis.lk',
        instagramImages: [
          { url: uploadedUrls.insta1 }, { url: uploadedUrls.insta2 }, { url: uploadedUrls.insta3 },
          { url: uploadedUrls.insta4 }, { url: uploadedUrls.insta5 }, { url: uploadedUrls.insta6 }
        ]
      })
    ]);

    if (results.every(function(r) { return r; })) {
      showToast('All sections saved!', 'success');
    } else {
      showToast('Some sections failed to save', 'error');
    }
  } catch (err) {
    showToast('Error: ' + err.message, 'error');
  }

  btn.textContent = 'Save All Changes';
  btn.disabled = false;
}

function showToast(msg, type) {
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = type === 'success' ? '#7BA06B' : type === 'error' ? '#C45B5B' : 'var(--charcoal)';
  t.classList.add('show');
  setTimeout(function() { t.classList.remove('show'); }, 3000);
}

loadContent();
</script>
</body>
</html>
"""

# Also update the SiteContent model to allow 'instagram' as a section
with open("server/models/SiteContent.js") as f:
    model = f.read()

if "'instagram'" not in model:
    model = model.replace(
        "'general'",
        "'instagram', 'general'"
    )
    with open("server/models/SiteContent.js", "w") as f:
        f.write(model)
    print("   ✅ Added 'instagram' to SiteContent model sections")

# Update the dynamic content loading in index.html to load instagram images
with open("client/index.html") as f:
    idx = f.read()

# Add instagram image loading to the dynamic script
insta_js = """
    // Instagram images
    if (data.instagram && data.instagram.instagramImages) {
      var instaItems = document.querySelectorAll('.insta-item');
      data.instagram.instagramImages.forEach(function(img, idx) {
        if (img.url && instaItems[idx]) {
          instaItems[idx].innerHTML = '<img src="' + img.url + '" alt="Instagram">';
        }
      });
    }
"""

if "instagramImages" not in idx.split("loadHomepageContent")[1] if "loadHomepageContent" in idx else "":
    # Insert before the closing of the try block in loadHomepageContent
    idx = idx.replace(
        "} catch (err) {\n    console.log('Using default homepage content');",
        insta_js + "\n  } catch (err) {\n    console.log('Using default homepage content');"
    )
    print("   ✅ Added instagram image loading to index.html")

with open("client/index.html", "w") as f:
    f.write(idx)

with open("admin/homepage.html", "w") as f:
    f.write(new_html)

print("   ✅ admin/homepage.html rebuilt with direct upload")
print("\n" + "="*50)
print("Done! Now push:")
print("   git add -A")
print('   git commit -m "Homepage editor: direct image upload"')
print("   git push")
print("="*50)
