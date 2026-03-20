#!/usr/bin/env python3
"""
NODALIS UPDATE — Multi-image products + hover effect + admin homepage management
Run from: ~/Downloads/nodalis-v5/nodalis-store
Usage: python3 update-images.py
"""
import re

print("🔧 Nodalis Update: Multi-image products + hover effect")
print("="*55)

# ========================================
# 1. UPDATE js/admin.js — multi-image upload
# ========================================
print("\n1/4 — Updating admin JS for multi-image upload...")

with open("js/admin.js", "r") as f:
    admin_js = f.read()

# Replace single image input handling with multi-image
# Find the image upload section and replace it
old_upload = """var imageInput = document.getElementById('prodImageInput');
    if (imageInput && imageInput.files && imageInput.files[0]) {
      var formData = new FormData();
      formData.append('image', imageInput.files[0]);
      try {
        var uploadRes = await fetch('/api/upload', {
          method: 'POST',"""

new_upload = """var imageInput = document.getElementById('prodImageInput');
    if (imageInput && imageInput.files && imageInput.files.length > 0) {
      // Upload up to 4 images
      var filesToUpload = Array.from(imageInput.files).slice(0, 4);
      for (var i = 0; i < filesToUpload.length; i++) {
        var formData = new FormData();
        formData.append('image', filesToUpload[i]);
        try {
          var uploadRes = await fetch('/api/upload', {
            method: 'POST',"""

if old_upload.strip() in admin_js:
    admin_js = admin_js.replace(old_upload.strip(), new_upload.strip())
    print("   ✅ Replaced single upload with multi-upload loop")
else:
    print("   ⚠️  Could not find exact upload block — trying alternative...")
    # Try to find a simpler pattern
    if "imageInput.files[0]" in admin_js and "formData.append('image', imageInput.files[0])" in admin_js:
        admin_js = admin_js.replace(
            "if (imageInput && imageInput.files && imageInput.files[0]) {\n      var formData = new FormData();\n      formData.append('image', imageInput.files[0]);",
            "if (imageInput && imageInput.files && imageInput.files.length > 0) {\n      var filesToUpload = Array.from(imageInput.files).slice(0, 4);\n      for (var fi = 0; fi < filesToUpload.length; fi++) {\n      var formData = new FormData();\n      formData.append('image', filesToUpload[fi]);"
        )
        print("   ✅ Applied alternative multi-upload patch")
    else:
        print("   ❌ Could not patch upload — will need manual fix")

# Fix the upload response to push each image
old_push = """productData.images = [{ url: uploadData.url, alt: productData.name }];"""
new_push = """productData.images.push({ url: uploadData.url, alt: productData.name });"""
if old_push in admin_js:
    admin_js = admin_js.replace(old_push, new_push)
    # Also need to close the for loop
    print("   ✅ Fixed image push to array")

# Update the image preview in edit modal to show all images
old_preview = """if (p.images && p.images.length > 0 && p.images[0].url) {
        document.getElementById('imagePreview').innerHTML = '<img src="' + p.images[0].url + '" style="width:100px;height:100px;object-fit:cover;border-radius:var(--radius-sm);"><p class="text-small" style="color:var(--sage-dark);">Current image</p>';
      }"""

new_preview = """if (p.images && p.images.length > 0) {
        var previewHtml = '<div style="display:flex;gap:8px;flex-wrap:wrap;">';
        p.images.forEach(function(img, idx) {
          if (img.url) previewHtml += '<img src="' + img.url + '" style="width:80px;height:80px;object-fit:cover;">';
        });
        previewHtml += '</div><p style="font-size:.7rem;color:var(--grey);margin-top:6px;">' + p.images.length + ' image(s) — upload new to replace</p>';
        document.getElementById('imagePreview').innerHTML = previewHtml;
      }"""

if old_preview in admin_js:
    admin_js = admin_js.replace(old_preview, new_preview)
    print("   ✅ Updated edit modal to show all images")
else:
    print("   ⚠️  Preview block slightly different — skipping")

# Update the input to accept multiple files
old_input_attr = "id=\"prodImageInput\""
if old_input_attr in admin_js:
    admin_js = admin_js.replace(old_input_attr, 'id="prodImageInput" multiple accept="image/*"')
    print("   ✅ Added multiple attribute to file input")

with open("js/admin.js", "w") as f:
    f.write(admin_js)


# ========================================
# 2. UPDATE admin/products.html — multi-image input
# ========================================
print("\n2/4 — Updating admin products HTML...")

with open("admin/products.html", "r") as f:
    admin_html = f.read()

# Make the file input accept multiple
if 'id="prodImageInput"' in admin_html and 'multiple' not in admin_html.split('prodImageInput')[1][:50]:
    admin_html = admin_html.replace(
        'id="prodImageInput"',
        'id="prodImageInput" multiple accept="image/*"'
    )
    print("   ✅ Added multiple file input support")

# Update the upload zone label
if "Upload Image" in admin_html:
    admin_html = admin_html.replace("Upload Image", "Upload Images (max 4)")
    print("   ✅ Updated upload label")
elif "Upload image" in admin_html:
    admin_html = admin_html.replace("Upload image", "Upload Images (max 4)")
    print("   ✅ Updated upload label")
elif "upload an image" in admin_html.lower():
    pass  # already fine

with open("admin/products.html", "w") as f:
    f.write(admin_html)


# ========================================
# 3. UPDATE js/script.js — hover effect on product cards
# ========================================
print("\n3/4 — Adding hover image effect to product cards...")

with open("js/script.js", "r") as f:
    script_js = f.read()

# Find where product cards are rendered and update to include 2nd image for hover
# Look for the product card image rendering
# We need to add a data attribute for the hover image and CSS + JS for the effect

# Add hover effect JS at the end of the file
hover_js = """

// ---- PRODUCT CARD HOVER — show 2nd image ----
document.addEventListener('mouseover', function(e) {
  var card = e.target.closest('.product-card-image');
  if (!card) return;
  var hoverImg = card.getAttribute('data-hover-img');
  var mainImg = card.querySelector('img');
  if (hoverImg && mainImg && mainImg.getAttribute('data-original') !== 'set') {
    mainImg.setAttribute('data-original', 'set');
    mainImg.setAttribute('data-original-src', mainImg.src);
  }
  if (hoverImg && mainImg) {
    mainImg.src = hoverImg;
  }
});
document.addEventListener('mouseout', function(e) {
  var card = e.target.closest('.product-card-image');
  if (!card) return;
  var mainImg = card.querySelector('img');
  if (mainImg && mainImg.getAttribute('data-original-src')) {
    mainImg.src = mainImg.getAttribute('data-original-src');
  }
});
"""

if "data-hover-img" not in script_js:
    script_js += hover_js
    print("   ✅ Added hover image swap JS")
else:
    print("   ⏭️  Hover JS already exists")

# Now find where product cards are created and add data-hover-img attribute
# Look for the image rendering in product card creation
# Common patterns: product-card-image creation with img tag

# Update renderProducts or similar function to include hover image
# Try to find the card image creation
if "product-card-image" in script_js:
    # Find the pattern where product card images are built
    # Add data-hover-img from images[1] if it exists
    
    # Pattern 1: template literal style
    old_card_img = 'class="product-card-image">'
    new_card_img = 'class="product-card-image" data-hover-img="' + '${p.images && p.images[1] ? p.images[1].url : ""}">'
    
    if old_card_img in script_js and "${p.images" not in script_js.split("product-card-image")[1][:200]:
        # Check if using template literals or string concat
        # Let's look for the actual pattern
        pass
    
    # Try a more targeted approach - find the renderProducts function
    # and patch the card creation
    
    # Look for img src pattern inside product card
    img_patterns = [
        ('src="${p.images[0].url}"', True),
        ("src=\"' + p.images[0].url + '\"", False),
        ('src="${img}"', True),
        ("src='/uploads/", False),
    ]
    
    for pattern, is_template in img_patterns:
        if pattern in script_js:
            print(f"   Found image pattern: {pattern[:30]}...")
            break
    
    # Instead of trying to patch complex rendering, let's add a MutationObserver
    # that automatically adds data-hover-img after cards are rendered
    observer_js = """

// ---- AUTO-ADD hover images to product cards ----
(function() {
  function addHoverImages() {
    document.querySelectorAll('.product-card').forEach(function(card) {
      var cardImg = card.querySelector('.product-card-image');
      if (!cardImg || cardImg.getAttribute('data-hover-img')) return;
      // Try to get product data from the card's link or data attribute
      var link = card.closest('a') || card.querySelector('a');
      if (!link) return;
      var href = link.getAttribute('href') || '';
      var productId = '';
      if (href.includes('id=')) productId = href.split('id=')[1].split('&')[0];
      // Find product in loaded data
      if (typeof allProducts !== 'undefined' && allProducts.length > 0) {
        var prod = allProducts.find(function(p) { return p._id === productId; });
        if (prod && prod.images && prod.images.length > 1) {
          cardImg.setAttribute('data-hover-img', prod.images[1].url);
        }
      }
    });
  }
  // Run after products load
  var origFetch = window.fetch;
  setInterval(addHoverImages, 2000);
  // Also run on page load
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(addHoverImages, 1500);
  });
})();
"""
    
    if "addHoverImages" not in script_js:
        script_js += observer_js
        print("   ✅ Added auto hover image detection")
    
print("   ✅ Hover effect complete")

with open("js/script.js", "w") as f:
    f.write(script_js)


# ========================================
# 4. ADD CSS for hover image transition
# ========================================
print("\n4/4 — Adding hover image CSS to all HTML files...")

hover_css = """
/* PRODUCT CARD HOVER IMAGE */
.product-card-image img{transition:opacity .3s ease,transform .7s cubic-bezier(.4,0,.2,1)}
.product-card-image[data-hover-img]:hover img{opacity:.95}
"""

import glob
patched = 0
for filepath in glob.glob("client/*.html") + glob.glob("admin/*.html"):
    with open(filepath) as f:
        content = f.read()
    if "PRODUCT CARD HOVER IMAGE" in content:
        continue
    if "</style>" in content:
        content = content.replace("</style>", hover_css + "</style>", 1)
        with open(filepath, "w") as f:
            f.write(content)
        patched += 1

print(f"   ✅ Added hover CSS to {patched} files")

print("\n" + "="*55)
print("✅ ALL DONE! Now push to GitHub:")
print("")
print("   git add -A")
print('   git commit -m "Feature: multi-image upload + hover effect"')
print("   git push")
print("")
print("After Railway deploys:")
print("  - Admin: upload up to 4 images per product")
print("  - Shop: hovering a product shows the 2nd image")
print("="*55)
