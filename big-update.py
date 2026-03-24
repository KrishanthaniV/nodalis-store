#!/usr/bin/env python3
"""
NODALIS — Big Update: Checkout flow, Payment settings, Hero fix, Mobile fixes
Run from: ~/Downloads/nodalis-v5/nodalis-store
"""
import json, glob, os

print("=" * 55)
print("NODALIS BIG UPDATE")
print("=" * 55)

# ========================================
# 1. UPDATE Order model — add bank_transfer payment method
# ========================================
print("\n1/6 — Updating Order model...")

with open("server/models/Order.js") as f:
    order_model = f.read()

order_model = order_model.replace(
    "enum: ['stripe', 'paypal', 'pending']",
    "enum: ['stripe', 'paypal', 'bank_transfer', 'pending']"
)
with open("server/models/Order.js", "w") as f:
    f.write(order_model)
print("   done")

# ========================================
# 2. ADD payment settings to SiteContent model
# ========================================
print("\n2/6 — Updating SiteContent model for payment settings...")

with open("server/models/SiteContent.js") as f:
    sc = f.read()

if "'payment'" not in sc:
    sc = sc.replace("'instagram', 'general'", "'instagram', 'payment', 'general'")
    # Add payment fields to the data schema
    sc = sc.replace(
        "siteName: { type: String, default: 'Nodalis' }",
        """// PAYMENT
    bankName: { type: String, default: '' },
    accountName: { type: String, default: '' },
    accountNumber: { type: String, default: '' },
    branchName: { type: String, default: '' },
    bankNotes: { type: String, default: '' },

    siteName: { type: String, default: 'Nodalis' }"""
    )
    with open("server/models/SiteContent.js", "w") as f:
        f.write(sc)
    print("   done")

# ========================================
# 3. ADD Payment Settings section to admin/homepage.html
# ========================================
print("\n3/6 — Adding Payment Settings to admin...")

with open("admin/homepage.html") as f:
    hp = f.read()

if "bankName" not in hp:
    payment_section = """
    <!-- PAYMENT SETTINGS -->
    <div class="admin-table-card" style="padding:1.5rem;margin-bottom:1.5rem;">
      <h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark);">Payment / Bank Details</h3>
      <p style="font-size:.82rem;color:var(--grey);margin-bottom:1rem;">These details will be shown to customers at checkout. Update anytime.</p>
      <div class="form-row">
        <div class="form-group">
          <label>Bank Name</label>
          <input type="text" id="bankName" placeholder="e.g. Commercial Bank of Ceylon">
        </div>
        <div class="form-group">
          <label>Account Holder Name</label>
          <input type="text" id="accountName" placeholder="e.g. K. Vadivel">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Account Number</label>
          <input type="text" id="accountNumber" placeholder="e.g. 8012345678">
        </div>
        <div class="form-group">
          <label>Branch</label>
          <input type="text" id="branchName" placeholder="e.g. Negombo Branch">
        </div>
      </div>
      <div class="form-group">
        <label>Additional Notes (shown to customer)</label>
        <textarea id="bankNotes" rows="2" placeholder="e.g. Please include your order ID as the payment reference. Send payment screenshot to our WhatsApp."></textarea>
      </div>
    </div>
"""
    # Insert before the Instagram section
    hp = hp.replace("<!-- INSTAGRAM IMAGES -->", payment_section + "\n    <!-- INSTAGRAM IMAGES -->")

    # Add payment to load and save functions
    # Load payment data
    old_load_end = "} catch (err) {\n    console.log('No saved content yet');"
    new_load_payment = """
    if (data.payment) {
      document.getElementById('bankName').value = data.payment.bankName || '';
      document.getElementById('accountName').value = data.payment.accountName || '';
      document.getElementById('accountNumber').value = data.payment.accountNumber || '';
      document.getElementById('branchName').value = data.payment.branchName || '';
      document.getElementById('bankNotes').value = data.payment.bankNotes || '';
    }
  } catch (err) {
    console.log('No saved content yet');"""
    hp = hp.replace(old_load_end, new_load_payment)

    # Save payment data - add to saveAllSections
    old_save_insta = "saveSection('instagram'"
    new_save_payment = """saveSection('payment', {
        bankName: document.getElementById('bankName').value,
        accountName: document.getElementById('accountName').value,
        accountNumber: document.getElementById('accountNumber').value,
        branchName: document.getElementById('branchName').value,
        bankNotes: document.getElementById('bankNotes').value
      }),
      saveSection('instagram'"""
    hp = hp.replace(old_save_insta, new_save_payment)

    with open("admin/homepage.html", "w") as f:
        f.write(hp)
    print("   done")

# ========================================
# 4. FIX checkout page — real API call + bank details
# ========================================
print("\n4/6 — Rebuilding checkout page...")

with open("client/checkout.html") as f:
    checkout = f.read()

# Find the script section and replace it
old_script_start = "<script>\ndocument.addEventListener('DOMContentLoaded'"
# Find from <script> after cart.js to </body>
script_idx = checkout.rfind("<script>")
body_idx = checkout.rfind("</body>")

if script_idx > 0 and body_idx > 0:
    new_script = """<script>
document.addEventListener('DOMContentLoaded', async function() {
  var cart = getCart();
  if (cart.length === 0) { window.location.href = '/client/cart.html'; return; }

  // Load payment settings
  var paymentInfo = {};
  try {
    var pRes = await fetch('/api/content/payment');
    if (pRes.ok) {
      var pData = await pRes.json();
      paymentInfo = pData.data || {};
    }
  } catch(e) {}

  // Build summary
  var el = document.getElementById('checkoutSummary');
  var subtotal = cart.reduce(function(s, i) { return s + i.price * i.quantity; }, 0);
  var shipping = subtotal > 5000 ? 0 : 350;
  var total = subtotal + shipping;

  var summaryHtml = '<h3 style="font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1rem;">Order Summary</h3>';
  summaryHtml += cart.map(function(item) {
    return '<div class="cart-summary-row"><span>' + item.name + ' x' + item.quantity + '</span><span>LKR ' + (item.price * item.quantity).toLocaleString() + '</span></div>';
  }).join('');
  summaryHtml += '<div class="cart-summary-row" style="margin-top:1rem;padding-top:.5rem;border-top:1px solid var(--cream-dark);"><span>Subtotal</span><span>LKR ' + subtotal.toLocaleString() + '</span></div>';
  summaryHtml += '<div class="cart-summary-row"><span>Shipping</span><span>' + (shipping === 0 ? 'Free' : 'LKR ' + shipping.toLocaleString()) + '</span></div>';
  summaryHtml += '<div class="cart-summary-row total" style="font-size:1.15rem;font-weight:600;border-top:1px solid var(--cream-dark);padding-top:.8rem;margin-top:.5rem;"><span>Total</span><span>LKR ' + total.toLocaleString() + '</span></div>';

  // Payment info
  if (paymentInfo.bankName) {
    summaryHtml += '<div style="margin-top:1.5rem;padding:1.2rem;background:var(--cream-dark);border-left:3px solid var(--gold);">';
    summaryHtml += '<p style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.8rem;font-weight:500;">Payment Details</p>';
    summaryHtml += '<p style="font-size:.85rem;line-height:1.8;"><strong>' + paymentInfo.bankName + '</strong><br>';
    summaryHtml += 'Account: <strong>' + (paymentInfo.accountNumber || '') + '</strong><br>';
    summaryHtml += 'Name: ' + (paymentInfo.accountName || '') + '<br>';
    if (paymentInfo.branchName) summaryHtml += 'Branch: ' + paymentInfo.branchName + '<br>';
    summaryHtml += '</p>';
    if (paymentInfo.bankNotes) {
      summaryHtml += '<p style="font-size:.8rem;color:var(--grey);margin-top:.5rem;font-style:italic;">' + paymentInfo.bankNotes + '</p>';
    }
    summaryHtml += '</div>';
  }

  el.innerHTML = summaryHtml;

  // Store totals for order
  window._checkoutData = { subtotal: subtotal, shipping: shipping, total: total, cart: cart };
});

async function placeOrder() {
  var token = localStorage.getItem('nodalis_token');
  if (!token) {
    showToast('Please log in first', 'error');
    setTimeout(function() { window.location.href = '/client/login.html'; }, 1500);
    return;
  }

  var data = window._checkoutData;
  if (!data) { showToast('Error loading cart', 'error'); return; }

  // Get shipping address
  var street = document.getElementById('shippingStreet');
  var city = document.getElementById('shippingCity');
  var state = document.getElementById('shippingState');
  var zip = document.getElementById('shippingZip');

  var shippingAddress = {
    street: street ? street.value : '',
    city: city ? city.value : '',
    state: state ? state.value : '',
    zip: zip ? zip.value : '',
    country: 'Sri Lanka'
  };

  // Build order items
  var items = data.cart.map(function(item) {
    return {
      product: item.id || item._id || item.productId,
      name: item.name,
      price: item.price,
      size: item.size || '',
      quantity: item.quantity
    };
  });

  var btn = document.querySelector('[onclick="placeOrder()"]');
  if (btn) { btn.textContent = 'PLACING ORDER...'; btn.disabled = true; }

  try {
    var res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({
        items: items,
        shippingAddress: shippingAddress,
        subtotal: data.subtotal,
        shipping: data.shipping,
        total: data.total,
        paymentMethod: 'bank_transfer'
      })
    });

    if (res.ok) {
      var order = await res.json();
      clearCart();
      // Show success with order ID and tracking
      document.querySelector('.section').innerHTML = '<div style="text-align:center;padding:3rem 1rem;max-width:600px;margin:0 auto;">' +
        '<div style="width:64px;height:64px;background:var(--gold);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.5rem;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg></div>' +
        '<h2 style="font-family:var(--font-display);font-size:1.8rem;font-weight:400;margin-bottom:.5rem;">Order Placed!</h2>' +
        '<p style="color:var(--grey);margin-bottom:1.5rem;">Thank you for your order. Please complete the bank transfer using the details below.</p>' +
        '<div style="background:var(--white);padding:1.5rem;text-align:left;margin-bottom:1.5rem;">' +
        '<p style="font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem;">Your Order ID</p>' +
        '<p style="font-family:monospace;font-size:1rem;margin-bottom:1rem;">' + (order._id || order.order?._id || 'N/A') + '</p>' +
        '<p style="font-size:.82rem;color:var(--grey);">Use this ID as your payment reference when transferring.</p>' +
        '</div>' +
        '<div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">' +
        '<a href="/client/track-order.html?id=' + (order._id || order.order?._id || '') + '" class="btn-luxury btn-dark">Track Your Order</a>' +
        '<a href="/client/shop.html" class="btn-luxury btn-outline">Continue Shopping</a>' +
        '</div>' +
        '<p style="margin-top:2rem;font-size:.82rem;color:var(--grey);">Send your payment confirmation screenshot to our <a href="https://wa.me/94767003630" style="color:var(--gold);">WhatsApp</a></p>' +
        '</div>';
    } else {
      var err = await res.json();
      showToast(err.message || 'Error placing order', 'error');
      if (btn) { btn.textContent = 'PLACE ORDER'; btn.disabled = false; }
    }
  } catch (err) {
    showToast('Server error: ' + err.message, 'error');
    if (btn) { btn.textContent = 'PLACE ORDER'; btn.disabled = false; }
  }
}
</script>"""

    checkout = checkout[:script_idx] + new_script + "\n</body></html>"
    with open("client/checkout.html", "w") as f:
        f.write(checkout)
    print("   done")

# ========================================
# 5. FIX hero — ensure text is visible over image
# ========================================
print("\n5/6 — Fixing hero text visibility...")

# Add stronger hero overlay CSS to all HTML files
hero_fix_css = """
/* HERO TEXT FIX */
.hero-content{text-shadow:0 2px 20px rgba(0,0,0,.4)}
.hero-media-placeholder{background:linear-gradient(135deg,#0a0a0a 0%,#1a1816 30%,#2a2826 60%,#1a1816 100%)}
.hero-overlay{background:linear-gradient(to bottom,rgba(10,10,10,.4) 0%,rgba(10,10,10,.65) 50%,rgba(10,10,10,.8) 100%)!important}
"""

patched = 0
for filepath in glob.glob("client/*.html"):
    with open(filepath) as f:
        content = f.read()
    if "HERO TEXT FIX" in content:
        continue
    if "</style>" in content:
        content = content.replace("</style>", hero_fix_css + "</style>", 1)
        with open(filepath, "w") as f:
            f.write(content)
        patched += 1
print(f"   patched {patched} files")

# ========================================
# 6. MOBILE FIXES — product images, responsive layout
# ========================================
print("\n6/6 — Adding mobile fixes...")

mobile_fix_css = """
/* MOBILE FIXES */
@media(max-width:768px){
  .hero-content h1{font-size:2.2rem}
  .hero-sub{font-size:.85rem}
  .hero-cta{padding:.8rem 1.5rem;font-size:.6rem}
  .nav{padding:0 1rem;height:70px}
  .nav-logo img{height:40px}
  .section{padding:2.5rem 1rem}
  .page-header{padding-top:calc(70px + 2rem);padding-bottom:2rem}
  .product-card-image{aspect-ratio:1}
  .product-card-name{font-size:.9rem}
  .product-card-price{font-size:.8rem}
  .cart-item{flex-direction:column;align-items:flex-start}
  .cart-item-image{width:100%;height:200px}
  .checkout-layout{grid-template-columns:1fr}
}
@media(max-width:480px){
  .hero-content h1{font-size:1.8rem}
  .marquee-item{font-size:.6rem;padding:0 1rem}
}
"""

patched_m = 0
for filepath in glob.glob("client/*.html"):
    with open(filepath) as f:
        content = f.read()
    if "MOBILE FIXES" in content:
        continue
    if "</style>" in content:
        content = content.replace("</style>", mobile_fix_css + "</style>", 1)
        with open(filepath, "w") as f:
            f.write(content)
        patched_m += 1
print(f"   patched {patched_m} files")

print("\n" + "=" * 55)
print("ALL DONE! Push to GitHub:")
print("  git add -A")
print('  git commit -m "Big update: checkout, payments, hero, mobile"')
print("  git push")
print()
print("Then go to Admin → Homepage → fill in your bank details!")
print("=" * 55)
