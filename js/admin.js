/* ============================================================
   NODALIS — Admin Panel JavaScript (Fixed)
   ============================================================ */

let adminProducts = [];

document.addEventListener('DOMContentLoaded', () => {
  loadAdminProducts();
  loadAdminOrders();
});

async function loadAdminProducts() {
  const tbody = document.getElementById('productsTableBody');
  if (!tbody) return;
  try {
    const res = await fetch('/api/products');
    if (res.ok) { adminProducts = await res.json(); }
    else { adminProducts = []; }
  } catch { adminProducts = []; }
  renderAdminProducts(adminProducts);
}

function renderAdminProducts(products) {
  const tbody = document.getElementById('productsTableBody');
  if (!tbody) return;
  const countLabel = document.getElementById('productCountLabel');
  if (countLabel) countLabel.textContent = 'All Products (' + products.length + ')';
  if (products.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:var(--space-3xl);color:var(--charcoal-light);">No products found. Click "+ Add Product" to get started.</td></tr>';
    return;
  }
  tbody.innerHTML = products.map(function(p) {
    var hasImage = p.images && p.images.length > 0 && p.images[0].url;
    var hue = hashStr(p.name) % 360;
    var statusClass = 'status-active';
    var statusText = 'In Stock';
    if (p.stock <= 0) { statusClass = 'status-out'; statusText = 'Out of Stock'; }
    else if (p.stock <= 5) { statusClass = 'status-pending'; statusText = 'Low Stock'; }
    var thumbStyle = hasImage ? '' : 'background:hsl(' + hue + ',20%,82%);';
    var thumbImg = hasImage ? '<img src="' + p.images[0].url + '" alt="' + p.name + '">' : '';
    return '<tr>' +
      '<td><div class="admin-product-cell"><div class="admin-product-thumb" style="' + thumbStyle + '">' + thumbImg + '</div><div><strong>' + p.name + '</strong><br><span class="text-small" style="color:var(--charcoal-light);">' + formatCategory(p.category) + '</span></div></div></td>' +
      '<td>' + formatCategory(p.category) + '</td>' +
      '<td>$' + p.price.toFixed(2) + '</td>' +
      '<td>' + p.stock + '</td>' +
      '<td><span class="status-badge ' + statusClass + '">' + statusText + '</span></td>' +
      '<td><div style="display:flex;gap:var(--space-sm);"><button class="btn btn-sm btn-secondary" onclick="editProduct(\'' + p._id + '\')">Edit</button><button class="btn btn-sm btn-secondary" style="color:var(--error);border-color:var(--error);" onclick="confirmDelete(\'' + p._id + '\')">Delete</button></div></td>' +
      '</tr>';
  }).join('');
}

function filterAdminProducts() {
  var query = (document.getElementById('adminSearch')?.value || '').toLowerCase();
  var filtered = adminProducts.filter(function(p) {
    return p.name.toLowerCase().includes(query) || p.category.toLowerCase().includes(query);
  });
  renderAdminProducts(filtered);
}

function openProductModal(productId) {
  var modal = document.getElementById('productModal');
  var title = document.getElementById('modalTitle');
  var form = document.getElementById('productForm');
  form.reset();
  document.getElementById('editProductId').value = '';
  document.getElementById('imagePreview').innerHTML = '';
  if (productId) {
    title.textContent = 'Edit Product';
    var p = adminProducts.find(function(pr) { return pr._id === productId; });
    if (p) {
      document.getElementById('editProductId').value = p._id;
      document.getElementById('prodName').value = p.name;
      document.getElementById('prodPrice').value = p.price;
      document.getElementById('prodStock').value = p.stock;
      document.getElementById('prodCategory').value = p.category;
      document.getElementById('prodSizes').value = (p.sizes || []).join(', ');
      document.getElementById('prodDesc').value = p.description;
      document.getElementById('prodFeatured').checked = p.featured || false;
      document.getElementById('prodHandmade').checked = (p.badges || []).includes('handmade');
      document.getElementById('prodLimited').checked = (p.badges || []).includes('limited');
      if (p.images && p.images.length > 0) {
        var previewHtml = '<div style="display:flex;gap:8px;flex-wrap:wrap;">';
        p.images.forEach(function(img, idx) {
          if (img.url) previewHtml += '<img src="' + img.url + '" style="width:80px;height:80px;object-fit:cover;">';
        });
        previewHtml += '</div><p style="font-size:.7rem;color:var(--grey);margin-top:6px;">' + p.images.length + ' image(s) — upload new to replace</p>';
        document.getElementById('imagePreview').innerHTML = previewHtml;
      }
    }
  } else {
    title.textContent = 'Add New Product';
  }
  modal.classList.add('open');
}

function closeProductModal() {
  var modal = document.getElementById('productModal');
  if (modal) modal.classList.remove('open');
}

function editProduct(id) { openProductModal(id); }

// ---- PRODUCT FORM SUBMIT ----
document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('productForm');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Get token FIRST before anything else
    var token = localStorage.getItem('nodalis_token');
    if (!token) {
      showToast('Please log in as admin first', 'error');
      window.location.href = '/client/login.html';
      return;
    }

    var badges = [];
    if (document.getElementById('prodHandmade').checked) badges.push('handmade');
    if (document.getElementById('prodLimited').checked) badges.push('limited');

    var sizesRaw = document.getElementById('prodSizes').value;
    var sizes = sizesRaw ? sizesRaw.split(',').map(function(s) { return s.trim(); }).filter(Boolean) : [];

    var productData = {
      name: document.getElementById('prodName').value,
      price: parseFloat(document.getElementById('prodPrice').value),
      stock: parseInt(document.getElementById('prodStock').value),
      category: document.getElementById('prodCategory').value,
      sizes: sizes,
      description: document.getElementById('prodDesc').value,
      featured: document.getElementById('prodFeatured').checked,
      badges: badges,
      images: []
    };

    // Step 1: Upload image if selected
    var imageInput = document.getElementById('prodImageInput');
    if (imageInput && imageInput.files && imageInput.files.length > 0) {
      var filesToUpload = Array.from(imageInput.files).slice(0, 4);
      for (var i = 0; i < filesToUpload.length; i++) {
        var formData = new FormData();
        formData.append('image', filesToUpload[i]);
        try {
          var uploadRes = await fetch('/api/upload', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token },
            body: formData
          });
          if (uploadRes.ok) {
            var uploadData = await uploadRes.json();
            productData.images.push({ url: uploadData.url, alt: productData.name });
            console.log('Image uploaded:', uploadData.url);
          } else {
            console.log('Upload failed:', uploadRes.status);
          }
        } catch (err) {
          console.log('Image upload error:', err);
        }
      }
    }

    // If editing and no new image uploaded, keep existing
    var editId = document.getElementById('editProductId').value;
    if (editId && productData.images.length === 0) {
      var existing = adminProducts.find(function(p) { return p._id === editId; });
      if (existing && existing.images) {
        productData.images = existing.images;
      }
    }

    // Step 2: Save product
    try {
      var res;
      if (editId) {
        res = await fetch('/api/products/' + editId, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
          body: JSON.stringify(productData)
        });
      } else {
        res = await fetch('/api/products', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
          body: JSON.stringify(productData)
        });
      }

      if (res.ok) {
        showToast(editId ? 'Product updated!' : 'Product added!', 'success');
        closeProductModal();
        loadAdminProducts();
      } else {
        var errData = await res.json();
        showToast(errData.message || 'Error saving product', 'error');
        console.log('Save error:', errData);
      }
    } catch (err) {
      showToast('Server error', 'error');
      console.error('Save product error:', err);
    }
  });
});

// ---- Delete ----
var deleteTargetId = null;

function confirmDelete(id) {
  deleteTargetId = id;
  var modal = document.getElementById('deleteModal');
  if (modal) modal.classList.add('open');
  document.getElementById('confirmDeleteBtn').onclick = function() { deleteProduct(id); };
}

function closeDeleteModal() {
  var modal = document.getElementById('deleteModal');
  if (modal) modal.classList.remove('open');
  deleteTargetId = null;
}

async function deleteProduct(id) {
  var token = localStorage.getItem('nodalis_token');
  try {
    var res = await fetch('/api/products/' + id, {
      method: 'DELETE',
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (res.ok) {
      showToast('Product deleted!', 'success');
      closeDeleteModal();
      loadAdminProducts();
      return;
    }
  } catch {}
  showToast('Error deleting product', 'error');
  closeDeleteModal();
}

function handleImagePreview(input) {
  var preview = document.getElementById('imagePreview');
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      preview.innerHTML = '<img src="' + e.target.result + '" style="width:100px;height:100px;object-fit:cover;border-radius:var(--radius-sm);">';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

// ---- Orders ----
async function loadAdminOrders() {
  var tbody = document.getElementById('ordersTableBody');
  if (!tbody) return;
  try {
    var token = localStorage.getItem('nodalis_token');
    var res = await fetch('/api/orders', { headers: { 'Authorization': 'Bearer ' + token } });
    if (res.ok) { renderAdminOrders(await res.json()); }
  } catch {}
}

function renderAdminOrders(orders) {
  var tbody = document.getElementById('ordersTableBody');
  if (!tbody || orders.length === 0) return;
  tbody.innerHTML = orders.map(function(o) {
    var statusMap = { pending: 'status-pending', shipped: 'status-active', delivered: 'status-active', cancelled: 'status-out' };
    return '<tr><td><strong>#' + (o._id?.slice(-8) || 'N/A') + '</strong></td><td>' + (o.customer?.firstName || 'N/A') + ' ' + (o.customer?.lastName || '') + '</td><td>' + (o.items?.length || 0) + ' items</td><td>$' + (o.total || 0).toFixed(2) + '</td><td><span class="status-badge ' + (statusMap[o.status] || 'status-pending') + '">' + (o.status || 'pending') + '</span></td><td>' + (o.createdAt ? new Date(o.createdAt).toLocaleDateString() : 'N/A') + '</td><td><select onchange="updateOrderStatus(\'' + o._id + '\', this.value)" style="padding:0.3rem 0.5rem;border-radius:var(--radius-sm);border:1px solid var(--beige-dark);font-size:0.8rem;"><option value="pending"' + (o.status === 'pending' ? ' selected' : '') + '>Pending</option><option value="shipped"' + (o.status === 'shipped' ? ' selected' : '') + '>Shipped</option><option value="delivered"' + (o.status === 'delivered' ? ' selected' : '') + '>Delivered</option><option value="cancelled"' + (o.status === 'cancelled' ? ' selected' : '') + '>Cancelled</option></select></td></tr>';
  }).join('');
}

async function updateOrderStatus(orderId, status) {
  var token = localStorage.getItem('nodalis_token');
  try {
    await fetch('/api/orders/' + orderId + '/status', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ status: status })
    });
    showToast('Order marked as ' + status, 'success');
  } catch { showToast('Error updating order', 'error'); }
}

function logout() {
  localStorage.removeItem('nodalis_token');
  localStorage.removeItem('nodalis_user');
  window.location.href = '/client/login.html';
}

function formatCategory(cat) {
  return (cat || '').replace(/-/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
}

function hashStr(str) {
  var h = 0;
  for (var i = 0; i < (str || '').length; i++) h = str.charCodeAt(i) + ((h << 5) - h);
  return Math.abs(h);
}
