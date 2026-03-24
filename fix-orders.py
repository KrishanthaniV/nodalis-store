#!/usr/bin/env python3
"""Fix checkout + order details + payment receipt"""
import re

print("NODALIS: Checkout fix + Order details")
print("="*50)

# 1. FIX checkout JS — use correct field IDs + add phone/email
print("\n1/4 — Fixing checkout...")
with open("client/checkout.html") as f:
    co = f.read()

# Fix field IDs in placeOrder function
co = co.replace("document.getElementById('shippingStreet')", "document.getElementById('shipStreet')")
co = co.replace("document.getElementById('shippingCity')", "document.getElementById('shipCity')")
co = co.replace("document.getElementById('shippingState')", "document.getElementById('shipState')")
co = co.replace("document.getElementById('shippingZip')", "document.getElementById('shipZip')")

# Add phone and email fields to the checkout form
old_street = """<div class="form-group"><label>Street Address</label><input type="text" id="shipStreet" required></div>"""
new_street = """<div class="form-row"><div class="form-group"><label>Phone Number</label><input type="tel" id="shipPhone" placeholder="07X XXX XXXX" required></div><div class="form-group"><label>Email</label><input type="email" id="shipEmail" required></div></div>
<div class="form-group"><label>Street Address</label><input type="text" id="shipStreet" required></div>"""

co = co.replace(old_street, new_street)

# Update the shippingAddress object to include phone, email, name
old_addr = """var shippingAddress = {
    street: street ? street.value : '',
    city: city ? city.value : '',
    state: state ? state.value : '',
    zip: zip ? zip.value : '',
    country: 'Sri Lanka'
  };"""

new_addr = """var phone = document.getElementById('shipPhone');
  var email = document.getElementById('shipEmail');
  var firstName = document.getElementById('shipFirst');
  var lastName = document.getElementById('shipLast');
  var country = document.getElementById('shipCountry');

  var shippingAddress = {
    firstName: firstName ? firstName.value : '',
    lastName: lastName ? lastName.value : '',
    phone: phone ? phone.value : '',
    email: email ? email.value : '',
    street: street ? street.value : '',
    city: city ? city.value : '',
    state: state ? state.value : '',
    zip: zip ? zip.value : '',
    country: country ? country.options[country.selectedIndex].text : 'Sri Lanka'
  };"""

co = co.replace(old_addr, new_addr)

# Update the order confirmation to show "Upload receipt" option
old_confirm_end = """<p style="margin-top:2rem;font-size:.82rem;color:var(--grey);">Send your payment confirmation screenshot to our <a href="https://wa.me/94767003630" style="color:var(--gold);">WhatsApp</a></p>"""
new_confirm_end = """<div style="margin-top:2rem;background:var(--white);padding:1.5rem;text-align:left;">
<p style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.8rem;">Upload Payment Receipt</p>
<input type="file" id="receiptFile" accept="image/*,.pdf" style="padding:.5rem;border:1px solid var(--cream-dark);width:100%;font-size:.85rem;">
<button onclick="uploadReceipt()" class="btn-luxury btn-gold" style="margin-top:.8rem;width:100%;justify-content:center;" id="receiptBtn">Upload Receipt</button>
<p style="font-size:.75rem;color:var(--grey);margin-top:.5rem;">Or send via <a href="https://wa.me/94767003630" style="color:var(--gold);">WhatsApp</a></p>
</div>"""
co = co.replace(old_confirm_end, new_confirm_end)

# Add uploadReceipt function
receipt_fn = """
async function uploadReceipt() {
  var file = document.getElementById('receiptFile');
  if (!file || !file.files[0]) { showToast('Please select a receipt', 'error'); return; }
  var token = localStorage.getItem('nodalis_token');
  var formData = new FormData();
  formData.append('image', file.files[0]);
  var btn = document.getElementById('receiptBtn');
  btn.textContent = 'Uploading...'; btn.disabled = true;
  try {
    var res = await fetch('/api/upload', { method: 'POST', headers: { 'Authorization': 'Bearer ' + token }, body: formData });
    if (res.ok) {
      var data = await res.json();
      // Save receipt URL to the order
      var orderId = document.querySelector('[style*="monospace"]');
      if (orderId) {
        await fetch('/api/orders/' + orderId.textContent.trim() + '/receipt', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
          body: JSON.stringify({ receiptUrl: data.url })
        });
      }
      showToast('Receipt uploaded! We will verify your payment.', 'success');
      btn.textContent = 'Receipt Uploaded ✓'; btn.style.background = '#7BA06B';
    } else { showToast('Upload failed', 'error'); btn.textContent = 'Upload Receipt'; btn.disabled = false; }
  } catch (err) { showToast('Error: ' + err.message, 'error'); btn.textContent = 'Upload Receipt'; btn.disabled = false; }
}
</script>"""

co = co.replace("</script>\n</body>", receipt_fn + "\n</body>")
# Also try without newline
co = co.replace("</script></body>", receipt_fn + "\n</body>")

with open("client/checkout.html", "w") as f:
    f.write(co)
print("   done")

# 2. UPDATE Order model — add receipt + phone in shipping
print("\n2/4 — Updating Order model...")
with open("server/models/Order.js") as f:
    om = f.read()

if "receiptUrl" not in om:
    om = om.replace(
        "shippingAddress: {\n    street: String,\n    city: String,\n    state: String,\n    zip: String,\n    country: String\n  }",
        """shippingAddress: {
    firstName: String,
    lastName: String,
    phone: String,
    email: String,
    street: String,
    city: String,
    state: String,
    zip: String,
    country: String
  },
  receiptUrl: {
    type: String,
    default: ''
  }"""
    )
    with open("server/models/Order.js", "w") as f:
        f.write(om)
    print("   done")

# 3. ADD receipt upload route to orders
print("\n3/4 — Adding receipt route...")
with open("server/routes/orders.js") as f:
    ort = f.read()

if "receipt" not in ort:
    receipt_route = """
// ---- Upload Payment Receipt ----
router.put('/:id/receipt', protect, async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);
    if (!order) return res.status(404).json({ message: 'Order not found' });
    order.receiptUrl = req.body.receiptUrl;
    await order.save();
    res.json({ message: 'Receipt uploaded', receiptUrl: order.receiptUrl });
  } catch (err) {
    res.status(500).json({ message: 'Error saving receipt' });
  }
});

"""
    ort = ort.replace("module.exports", receipt_route + "module.exports")
    with open("server/routes/orders.js", "w") as f:
        f.write(ort)
    print("   done")

# 4. UPDATE admin orders — clickable rows with detail modal
print("\n4/4 — Adding order detail view to admin...")
with open("js/admin.js") as f:
    aj = f.read()

# Replace the order rendering to make rows clickable
old_render = """function renderAdminOrders(orders) {
  var tbody = document.getElementById('ordersTableBody');
  if (!tbody || orders.length === 0) return;"""

new_render = """var allOrders = [];

function renderAdminOrders(orders) {
  allOrders = orders;
  var tbody = document.getElementById('ordersTableBody');
  if (!tbody || orders.length === 0) return;"""

aj = aj.replace(old_render, new_render)

# Update the row to be clickable and show more info
old_row_start = """    var statusMap = { pending: 'status-pending', shipped: 'status-active', delivered: 'status-active', cancelled: 'status-out' };
    var addr = o.shippingAddress || {};"""

new_row_start = """    var statusMap = { pending: 'status-pending', shipped: 'status-active', delivered: 'status-active', cancelled: 'status-out', processing: 'status-pending' };
    var addr = o.shippingAddress || {};"""

aj = aj.replace(old_row_start, new_row_start)

# Add the order ID click handler
old_order_id = """return '<tr><td><strong>#' + (o._id?.slice(-8) || 'N/A') + '</strong><br><span style="font-size:.7rem;color:var(--grey);font-family:monospace;">' + (o._id || '') + '</span></td>"""

new_order_id = """return '<tr style="cursor:pointer;" onclick="viewOrderDetail(\\'' + o._id + '\\')"><td><strong>#' + (o._id?.slice(-8) || 'N/A') + '</strong><br><span style="font-size:.7rem;color:var(--grey);font-family:monospace;">' + (o._id || '') + '</span></td>"""

aj = aj.replace(old_order_id, new_order_id)

# Add viewOrderDetail function
detail_fn = """

// ---- ORDER DETAIL VIEW ----
function viewOrderDetail(orderId) {
  var o = allOrders.find(function(ord) { return ord._id === orderId; });
  if (!o) return;
  
  var addr = o.shippingAddress || {};
  var addrLines = [addr.firstName ? addr.firstName + ' ' + (addr.lastName || '') : '', addr.street, [addr.city, addr.state, addr.zip].filter(Boolean).join(', '), addr.country].filter(Boolean);
  
  var itemsHtml = (o.items || []).map(function(i) {
    return '<div style="display:flex;justify-content:space-between;padding:.6rem 0;border-bottom:1px solid var(--cream-dark);font-size:.85rem;"><div><strong>' + (i.name || 'Product') + '</strong>' + (i.size ? ' <span style="color:var(--grey);">(' + i.size + ')</span>' : '') + '<br><span style="color:var(--grey);">Qty: ' + i.quantity + '</span></div><div style="font-weight:600;">LKR ' + (i.price * i.quantity).toLocaleString() + '</div></div>';
  }).join('');
  
  var receiptHtml = o.receiptUrl ? '<div style="margin-top:1rem;"><p style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem;">Payment Receipt</p><a href="' + o.receiptUrl + '" target="_blank"><img src="' + o.receiptUrl + '" style="max-width:300px;max-height:200px;object-fit:contain;border:1px solid var(--cream-dark);"></a></div>' : '<p style="font-size:.82rem;color:var(--grey);margin-top:1rem;font-style:italic;">No payment receipt uploaded yet</p>';

  var html = '<div style="position:fixed;inset:0;background:rgba(10,10,10,.6);z-index:2000;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);" onclick="if(event.target===this)this.remove();">' +
    '<div style="background:var(--white);padding:2rem;width:90%;max-width:700px;max-height:90vh;overflow-y:auto;">' +
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;"><h3 style="font-family:var(--font-display);font-size:1.3rem;font-weight:400;">Order #' + (o._id?.slice(-8) || '') + '</h3><button onclick="this.closest(\'[style*=fixed]\')" style="font-size:1.5rem;cursor:pointer;background:none;border:none;" onclick="this.parentElement.parentElement.parentElement.remove()">×</button></div>' +
    
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem;">' +
    '<div style="background:var(--cream);padding:1rem;"><p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem;">Customer</p><p style="font-size:.9rem;"><strong>' + (addr.firstName || o.customer?.firstName || 'N/A') + ' ' + (addr.lastName || o.customer?.lastName || '') + '</strong></p>' + (addr.phone ? '<p style="font-size:.85rem;margin-top:.3rem;">📞 ' + addr.phone + '</p>' : '') + (addr.email ? '<p style="font-size:.85rem;">✉️ ' + addr.email + '</p>' : '') + '</div>' +
    '<div style="background:var(--cream);padding:1rem;"><p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem;">Shipping Address</p><p style="font-size:.85rem;line-height:1.7;">' + addrLines.join('<br>') + '</p></div>' +
    '</div>' +
    
    '<div style="background:var(--cream);padding:1rem;margin-bottom:1.5rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">' +
    '<div><p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Status</p><p style="font-weight:600;">' + (o.status || 'pending') + '</p></div>' +
    '<div><p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Payment</p><p>' + (o.paymentMethod || 'bank_transfer') + '</p></div>' +
    '<div><p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Date</p><p>' + (o.createdAt ? new Date(o.createdAt).toLocaleDateString() : 'N/A') + '</p></div>' +
    '</div>' +
    
    '<p style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.8rem;">Items</p>' +
    itemsHtml +
    '<div style="display:flex;justify-content:space-between;padding:.8rem 0;font-size:1rem;font-weight:600;margin-top:.5rem;"><span>Total</span><span>LKR ' + (o.total || 0).toLocaleString() + '</span></div>' +
    
    receiptHtml +
    
    '<div style="margin-top:1.5rem;text-align:center;"><button onclick="this.closest(\'[style*=fixed]\').remove();" class="btn-luxury btn-outline" style="padding:.6rem 1.5rem;">Close</button></div>' +
    '</div></div>';
  
  document.body.insertAdjacentHTML('beforeend', html);
}
"""

if "viewOrderDetail" not in aj:
    aj += detail_fn
    with open("js/admin.js", "w") as f:
        f.write(aj)
    print("   done")

# 5. Fix server to use client-sent totals instead of recalculating
print("\n5/5 — Fixing server to accept LKR totals...")
with open("server/routes/orders.js") as f:
    ort = f.read()

old_calc = """    const shipping = subtotal > 100 ? 0 : 8.50;
    const total = subtotal + shipping;

    const order = await Order.create({
      customer: req.user._id,
      items: orderItems,
      shippingAddress,
      subtotal,
      shipping,
      total,
      paymentMethod: paymentMethod || 'pending'
    });"""

new_calc = """    // Use client-sent totals (LKR) if provided, otherwise calculate
    const clientSubtotal = req.body.subtotal || subtotal;
    const clientShipping = req.body.shipping !== undefined ? req.body.shipping : (subtotal > 5000 ? 0 : 350);
    const clientTotal = req.body.total || (clientSubtotal + clientShipping);

    const order = await Order.create({
      customer: req.user._id,
      items: orderItems,
      shippingAddress,
      subtotal: clientSubtotal,
      shipping: clientShipping,
      total: clientTotal,
      paymentMethod: paymentMethod || 'bank_transfer'
    });"""

if old_calc in ort:
    ort = ort.replace(old_calc, new_calc)
    with open("server/routes/orders.js", "w") as f:
        f.write(ort)
    print("   done")
else:
    print("   calc block not found exactly")

print("\n" + "="*50)
print("Push:")
print("  git add -A")
print('  git commit -m "Orders: detail view, receipt upload, address fix"')
print("  git push")
print("="*50)
