#!/usr/bin/env python3
"""
NODALIS UPDATE — Hero fix + Email notifications + Order tracking
Run from: ~/Downloads/nodalis-v5/nodalis-store
"""
import os, glob

print("🔧 Nodalis Update: Hero fix + Emails + Order Tracking")
print("=" * 55)

# ========================================
# 1. FIX HERO — dynamic script should not override opacity
# ========================================
print("\n1/5 — Fixing hero image display...")

with open("client/index.html") as f:
    idx = f.read()

# Fix the dynamic hero media loading to keep proper styling
old_hero_img = """if (media && h.heroMediaType === 'image' && h.heroMediaUrl) {
        media.innerHTML = '<img src="' + h.heroMediaUrl + '" alt="Nodalis Hero" style="width:100%;height:100%;object-fit:cover;opacity:.5;">';"""

new_hero_img = """if (media && h.heroMediaType === 'image' && h.heroMediaUrl) {
        media.innerHTML = '<img src="' + h.heroMediaUrl + '" alt="Nodalis Hero" style="width:100%;height:100%;object-fit:cover;opacity:.4;">';"""

if old_hero_img in idx:
    idx = idx.replace(old_hero_img, new_hero_img)
    print("   ✅ Fixed hero image opacity")

old_hero_vid = """} else if (media && h.heroMediaType === 'video' && h.heroMediaUrl) {
        media.innerHTML = '<video autoplay muted loop playsinline style="width:100%;height:100%;object-fit:cover;opacity:.5;"><source src="' + h.heroMediaUrl + '"></video>';"""

new_hero_vid = """} else if (media && h.heroMediaType === 'video' && h.heroMediaUrl) {
        media.innerHTML = '<video autoplay muted loop playsinline style="width:100%;height:100%;object-fit:cover;opacity:.4;"><source src="' + h.heroMediaUrl + '"></video>';"""

if old_hero_vid in idx:
    idx = idx.replace(old_hero_vid, new_hero_vid)
    print("   ✅ Fixed hero video opacity")

with open("client/index.html", "w") as f:
    f.write(idx)


# ========================================
# 2. CREATE email utility — server/utils/email.js
# ========================================
print("\n2/5 — Creating email utility...")

os.makedirs("server/utils", exist_ok=True)

email_util = '''/* ============================================================
   NODALIS — Email Utility (Gmail via Nodemailer)
   ============================================================
   Setup: Add these to your Railway environment variables:
     EMAIL_USER=nodalislk@gmail.com
     EMAIL_PASS=your-gmail-app-password
   
   To get a Gmail App Password:
   1. Go to myaccount.google.com → Security
   2. Enable 2-Step Verification
   3. Go to App Passwords → Generate one for "Mail"
   4. Use that 16-character password as EMAIL_PASS
   ============================================================ */

const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER || 'nodalislk@gmail.com',
    pass: process.env.EMAIL_PASS || ''
  }
});

// Verify connection on startup
transporter.verify().then(() => {
  console.log('📧 Email service ready');
}).catch((err) => {
  console.log('⚠️  Email not configured:', err.message);
  console.log('   Add EMAIL_USER and EMAIL_PASS to environment variables');
});

// Base email template
function emailTemplate(content) {
  return `
  <div style="max-width:600px;margin:0 auto;font-family:'Helvetica Neue',Arial,sans-serif;color:#2A2826;background:#FAFAFA;">
    <div style="background:#0A0A0A;padding:2rem;text-align:center;">
      <h1 style="font-family:Georgia,serif;color:#FAFAFA;font-weight:400;font-size:1.8rem;margin:0;">Nodalis</h1>
      <p style="color:#B8977E;font-size:.7rem;letter-spacing:.3em;text-transform:uppercase;margin:.5rem 0 0;">Timeless Pieces</p>
    </div>
    <div style="padding:2rem;">
      ${content}
    </div>
    <div style="background:#F2EDE8;padding:1.5rem;text-align:center;font-size:.75rem;color:#8A8580;">
      <p>Nodalis — Handmade Fashion from Sri Lanka</p>
      <p style="margin-top:.5rem;">
        <a href="https://instagram.com/nodalis.lk" style="color:#B8977E;text-decoration:none;">Instagram</a> · 
        <a href="https://tiktok.com/@nodalis.lk" style="color:#B8977E;text-decoration:none;">TikTok</a>
      </p>
      <p style="margin-top:.5rem;">© ${new Date().getFullYear()} Nodalis. All rights reserved.</p>
    </div>
  </div>`;
}

// Send welcome email
async function sendWelcomeEmail(user) {
  try {
    const content = `
      <h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;margin-bottom:1rem;">Welcome to Nodalis, ${user.firstName}!</h2>
      <p style="line-height:1.8;color:#5A554F;">Thank you for creating your account. You're now part of our community of people who appreciate the beauty of handmade fashion.</p>
      <p style="line-height:1.8;color:#5A554F;margin-top:1rem;">Every piece in our collection is crafted by hand with love — crocheted tops, hand-painted tees, bags, and artisan accessories. Each one is unique, just like you.</p>
      <div style="text-align:center;margin:2rem 0;">
        <a href="https://nodalis-store-production.up.railway.app/client/shop.html" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Explore the Collection</a>
      </div>
      <p style="line-height:1.8;color:#5A554F;">If you have any questions, reach out to us anytime at <a href="mailto:nodalislk@gmail.com" style="color:#B8977E;">nodalislk@gmail.com</a> or message us on <a href="https://wa.me/94767003630" style="color:#B8977E;">WhatsApp</a>.</p>
      <p style="margin-top:1.5rem;color:#2A2826;">With love,<br><strong>The Nodalis Team</strong></p>
    `;

    await transporter.sendMail({
      from: '"Nodalis" <' + (process.env.EMAIL_USER || 'nodalislk@gmail.com') + '>',
      to: user.email,
      subject: 'Welcome to Nodalis — Handmade with Love 🧶',
      html: emailTemplate(content)
    });
    console.log('📧 Welcome email sent to:', user.email);
    return true;
  } catch (err) {
    console.error('Email send error:', err.message);
    return false;
  }
}

// Send order confirmation email
async function sendOrderConfirmationEmail(user, order) {
  try {
    const itemsList = (order.items || []).map(item => 
      `<tr><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;">${item.name || 'Product'}</td><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;text-align:center;">${item.quantity || 1}</td><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;text-align:right;">$${(item.price || 0).toFixed(2)}</td></tr>`
    ).join('');

    const content = `
      <h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;margin-bottom:1rem;">Order Confirmed! 🎉</h2>
      <p style="line-height:1.8;color:#5A554F;">Hi ${user.firstName}, your order has been received and is being prepared with care.</p>
      <div style="background:#F2EDE8;padding:1rem;margin:1.5rem 0;">
        <p style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#B8977E;margin-bottom:.5rem;">Order ID</p>
        <p style="font-family:monospace;font-size:.9rem;">${order._id}</p>
      </div>
      <table style="width:100%;border-collapse:collapse;margin:1rem 0;">
        <tr style="background:#F2EDE8;"><th style="padding:.5rem;text-align:left;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;">Item</th><th style="padding:.5rem;text-align:center;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;">Qty</th><th style="padding:.5rem;text-align:right;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;">Price</th></tr>
        ${itemsList}
        <tr><td colspan="2" style="padding:.8rem .5rem;font-weight:600;text-align:right;">Total</td><td style="padding:.8rem .5rem;text-align:right;font-weight:600;">$${(order.total || 0).toFixed(2)}</td></tr>
      </table>
      <div style="text-align:center;margin:2rem 0;">
        <a href="https://nodalis-store-production.up.railway.app/client/track-order.html?id=${order._id}" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Track Your Order</a>
      </div>
      <p style="line-height:1.8;color:#5A554F;">We'll email you when your order ships. Thank you for supporting handmade! 🧶</p>
    `;

    await transporter.sendMail({
      from: '"Nodalis" <' + (process.env.EMAIL_USER || 'nodalislk@gmail.com') + '>',
      to: user.email,
      subject: 'Your Nodalis Order is Confirmed! #' + String(order._id).slice(-6).toUpperCase(),
      html: emailTemplate(content)
    });
    console.log('📧 Order confirmation sent to:', user.email);
    return true;
  } catch (err) {
    console.error('Order email error:', err.message);
    return false;
  }
}

// Send order status update email
async function sendOrderStatusEmail(user, order) {
  const statusMessages = {
    'pending': { emoji: '⏳', title: 'Order Received', desc: 'We\\'ve received your order and are preparing it with care.' },
    'confirmed': { emoji: '✅', title: 'Order Confirmed', desc: 'Your order has been confirmed and is being prepared.' },
    'ready': { emoji: '📦', title: 'Order Ready', desc: 'Your order is packed and ready to ship!' },
    'shipped': { emoji: '🚚', title: 'Order Shipped', desc: 'Your order is on its way to you!' },
    'in-transit': { emoji: '🛣️', title: 'In Transit', desc: 'Your order is moving through the delivery network.' },
    'delivered': { emoji: '🎉', title: 'Order Delivered', desc: 'Your order has been delivered. Enjoy your handmade pieces!' },
    'cancelled': { emoji: '❌', title: 'Order Cancelled', desc: 'Your order has been cancelled. If you have questions, please contact us.' }
  };

  const status = statusMessages[order.status] || statusMessages['pending'];

  try {
    const content = `
      <h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;margin-bottom:1rem;">${status.emoji} ${status.title}</h2>
      <p style="line-height:1.8;color:#5A554F;">Hi ${user.firstName}, here's an update on your order:</p>
      <div style="background:#F2EDE8;padding:1rem;margin:1.5rem 0;">
        <p style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#B8977E;margin-bottom:.5rem;">Order ID</p>
        <p style="font-family:monospace;font-size:.9rem;">${order._id}</p>
        <p style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#B8977E;margin-bottom:.5rem;margin-top:1rem;">Status</p>
        <p style="font-size:1.1rem;font-weight:600;">${status.title}</p>
      </div>
      <p style="line-height:1.8;color:#5A554F;">${status.desc}</p>
      <div style="text-align:center;margin:2rem 0;">
        <a href="https://nodalis-store-production.up.railway.app/client/track-order.html?id=${order._id}" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Track Your Order</a>
      </div>
    `;

    await transporter.sendMail({
      from: '"Nodalis" <' + (process.env.EMAIL_USER || 'nodalislk@gmail.com') + '>',
      to: user.email,
      subject: `${status.emoji} Your Nodalis Order — ${status.title}`,
      html: emailTemplate(content)
    });
    console.log('📧 Status update email sent to:', user.email);
    return true;
  } catch (err) {
    console.error('Status email error:', err.message);
    return false;
  }
}

module.exports = {
  sendWelcomeEmail,
  sendOrderConfirmationEmail,
  sendOrderStatusEmail
};
'''

with open("server/utils/email.js", "w") as f:
    f.write(email_util)
print("   ✅ server/utils/email.js created")


# ========================================
# 3. UPDATE auth routes — send welcome email on register
# ========================================
print("\n3/5 — Adding welcome email to registration...")

with open("server/routes/auth.js") as f:
    auth = f.read()

if "sendWelcomeEmail" not in auth:
    # Add require at top
    auth = auth.replace(
        "const { protect",
        "const { sendWelcomeEmail } = require('../utils/email');\nconst { protect"
    )
    
    # Add email send after user creation
    auth = auth.replace(
        "// Generate token\n    const token = generateToken(user._id);",
        "// Send welcome email (don't block registration if email fails)\n    sendWelcomeEmail({ firstName: user.firstName, email: user.email }).catch(err => console.log('Welcome email skipped'));\n\n    // Generate token\n    const token = generateToken(user._id);"
    )
    
    with open("server/routes/auth.js", "w") as f:
        f.write(auth)
    print("   ✅ Welcome email added to registration flow")
else:
    print("   ⏭️  Already has welcome email")


# ========================================
# 4. UPDATE order routes — send status email on update
# ========================================
print("\n4/5 — Adding order status emails...")

with open("server/routes/orders.js") as f:
    orders = f.read()

if "sendOrderStatusEmail" not in orders:
    # Add require
    if "require('../utils/email')" not in orders:
        orders = orders.replace(
            "const { protect",
            "const { sendOrderStatusEmail, sendOrderConfirmationEmail } = require('../utils/email');\nconst User = require('../models/User');\nconst { protect"
        )
    
    # Find the status update route and add email
    # Look for where status is updated
    if "status" in orders and "findById" in orders:
        # Add email sending after status update - try to find the pattern
        old_status = "res.json({ message: 'Order status updated'"
        if old_status in orders:
            new_status = """// Send status email to customer
    try {
      const customer = await User.findById(order.user || order.userId);
      if (customer) {
        sendOrderStatusEmail(
          { firstName: customer.firstName, email: customer.email },
          order
        ).catch(err => console.log('Status email skipped'));
      }
    } catch (emailErr) { console.log('Status email lookup error'); }

    res.json({ message: 'Order status updated'"""
            orders = orders.replace(old_status, new_status)
            print("   ✅ Order status emails added")
        else:
            print("   ⚠️  Could not find status update response pattern")
    
    with open("server/routes/orders.js", "w") as f:
        f.write(orders)
else:
    print("   ⏭️  Already has order status emails")


# ========================================
# 5. CREATE order tracking page — client/track-order.html
# ========================================
print("\n5/5 — Creating order tracking page...")

# Get the style block from an existing client page
with open("client/shop.html") as f:
    shop = f.read()

style_end = shop.find("</style>") + len("</style>")
head_section = shop[:style_end].replace("<title>", "<title>Track Order — ")

track_html = head_section + """
</head>
<body>

<!-- NAV -->
<nav class="nav scrolled" id="mainNav">
  <a href="/" class="nav-logo">
    <img src="/assets/logo/nodalis-logo.png" alt="Nodalis">
  </a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/client/shop.html">Shop</a>
    <a href="/client/about.html">About</a>
    <a href="/client/contact.html">Contact</a>
  </div>
  <div class="nav-icons">
    <a href="/client/login.html" class="nav-icon"><svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></a>
    <a href="/client/cart.html" class="nav-icon"><svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg></a>
  </div>
</nav>

<div class="page-header">
  <p class="section-eyebrow">Order Status</p>
  <h1 class="section-title">Track Your Order</h1>
</div>

<div class="section" style="max-width:700px;margin:0 auto;">
  
  <!-- Search -->
  <div id="searchSection">
    <div class="form-group">
      <label>Enter your Order ID</label>
      <div style="display:flex;gap:.5rem;">
        <input type="text" id="orderIdInput" placeholder="Paste your order ID here" style="flex:1;">
        <button class="btn-luxury btn-dark" onclick="trackOrder()">Track</button>
      </div>
    </div>
  </div>

  <!-- Result -->
  <div id="trackResult" style="display:none;">
    <div style="background:var(--white);padding:2rem;margin-bottom:1.5rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;">
        <div>
          <p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Order ID</p>
          <p id="trackOrderId" style="font-family:monospace;font-size:.9rem;"></p>
        </div>
        <div>
          <p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Date</p>
          <p id="trackDate" style="font-size:.9rem;"></p>
        </div>
        <div>
          <p style="font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem;">Total</p>
          <p id="trackTotal" style="font-size:1.1rem;font-weight:600;"></p>
        </div>
      </div>

      <!-- Status Timeline -->
      <div id="statusTimeline" style="margin:2rem 0;"></div>
    </div>

    <!-- Items -->
    <div style="background:var(--white);padding:2rem;">
      <h3 style="font-family:var(--font-display);font-size:1.1rem;font-weight:400;margin-bottom:1rem;">Items</h3>
      <div id="trackItems"></div>
    </div>

    <div style="text-align:center;margin-top:2rem;">
      <button class="btn-luxury btn-outline" onclick="document.getElementById('trackResult').style.display='none';document.getElementById('searchSection').style.display='block';">Track Another Order</button>
    </div>
  </div>

  <div id="trackError" style="display:none;text-align:center;padding:2rem;">
    <p style="color:#C45B5B;font-size:1rem;">Order not found. Please check your Order ID and try again.</p>
  </div>
</div>

<footer class="footer">
  <div class="footer-bottom">
    <p>&copy; 2026 Nodalis. All rights reserved.</p>
  </div>
</footer>

<script>
var statuses = ['pending', 'confirmed', 'ready', 'shipped', 'in-transit', 'delivered'];
var statusLabels = {
  'pending': 'Order Received',
  'confirmed': 'Confirmed',
  'ready': 'Ready to Ship',
  'shipped': 'Shipped',
  'in-transit': 'In Transit',
  'delivered': 'Delivered',
  'cancelled': 'Cancelled'
};

// Check URL for order ID
var params = new URLSearchParams(window.location.search);
var urlOrderId = params.get('id');
if (urlOrderId) {
  document.getElementById('orderIdInput').value = urlOrderId;
  trackOrder();
}

async function trackOrder() {
  var orderId = document.getElementById('orderIdInput').value.trim();
  if (!orderId) return;

  document.getElementById('trackResult').style.display = 'none';
  document.getElementById('trackError').style.display = 'none';

  try {
    var token = localStorage.getItem('nodalis_token');
    var headers = token ? { 'Authorization': 'Bearer ' + token } : {};
    var res = await fetch('/api/orders/' + orderId, { headers: headers });
    
    if (!res.ok) {
      document.getElementById('trackError').style.display = 'block';
      return;
    }

    var order = await res.json();
    
    document.getElementById('trackOrderId').textContent = order._id;
    document.getElementById('trackDate').textContent = new Date(order.createdAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('trackTotal').textContent = '$' + (order.total || 0).toFixed(2);

    // Build timeline
    var currentIdx = statuses.indexOf(order.status);
    if (order.status === 'cancelled') currentIdx = -2;
    
    var timelineHtml = '<div style="display:flex;justify-content:space-between;position:relative;padding:0 .5rem;">';
    timelineHtml += '<div style="position:absolute;top:12px;left:5%;right:5%;height:2px;background:var(--cream-dark);z-index:0;"></div>';
    timelineHtml += '<div style="position:absolute;top:12px;left:5%;width:' + Math.max(0, (currentIdx / (statuses.length - 1)) * 90) + '%;height:2px;background:var(--gold);z-index:1;transition:width .5s;"></div>';
    
    statuses.forEach(function(s, i) {
      var isActive = i <= currentIdx;
      var isCurrent = i === currentIdx;
      var dotColor = isActive ? 'var(--gold)' : 'var(--cream-dark)';
      var dotSize = isCurrent ? '24px' : '12px';
      var textWeight = isCurrent ? '600' : '400';
      var textColor = isActive ? 'var(--charcoal)' : 'var(--grey-light)';
      
      timelineHtml += '<div style="text-align:center;position:relative;z-index:2;flex:1;">';
      timelineHtml += '<div style="width:' + dotSize + ';height:' + dotSize + ';border-radius:50%;background:' + dotColor + ';margin:' + (isCurrent ? '0' : '6px') + ' auto .5rem;transition:all .3s;' + (isCurrent ? 'box-shadow:0 0 0 4px rgba(184,151,126,.3);' : '') + '"></div>';
      timelineHtml += '<p style="font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:' + textColor + ';font-weight:' + textWeight + ';">' + statusLabels[s] + '</p>';
      timelineHtml += '</div>';
    });
    timelineHtml += '</div>';

    if (order.status === 'cancelled') {
      timelineHtml = '<div style="text-align:center;padding:1rem;background:rgba(196,91,91,.1);"><p style="color:#C45B5B;font-weight:600;">Order Cancelled</p></div>';
    }

    document.getElementById('statusTimeline').innerHTML = timelineHtml;

    // Build items
    var itemsHtml = (order.items || []).map(function(item) {
      return '<div style="display:flex;justify-content:space-between;padding:.8rem 0;border-bottom:1px solid var(--cream-dark);">' +
        '<div><p style="font-family:var(--font-display);font-size:.95rem;">' + (item.name || 'Product') + '</p>' +
        '<p style="font-size:.75rem;color:var(--grey);">Qty: ' + (item.quantity || 1) + '</p></div>' +
        '<p style="font-weight:600;">$' + (item.price || 0).toFixed(2) + '</p></div>';
    }).join('');
    document.getElementById('trackItems').innerHTML = itemsHtml || '<p style="color:var(--grey);">No items data available</p>';

    document.getElementById('searchSection').style.display = 'none';
    document.getElementById('trackResult').style.display = 'block';

  } catch (err) {
    document.getElementById('trackError').style.display = 'block';
  }
}
</script>
</body>
</html>
"""

with open("client/track-order.html", "w") as f:
    f.write(track_html)
print("   ✅ client/track-order.html created")


# ========================================
# ADD order lookup route (public by order ID)
# ========================================
with open("server/routes/orders.js") as f:
    orders = f.read()

if "Get single order by ID" not in orders:
    # Add a public route to get order by ID (for tracking)
    new_route = """
// ---- Get Single Order by ID (for tracking) ----
router.get('/:id', async (req, res) => {
  try {
    const Order = require('../models/Order');
    const order = await Order.findById(req.params.id);
    if (!order) return res.status(404).json({ message: 'Order not found' });
    res.json(order);
  } catch (err) {
    res.status(500).json({ message: 'Error fetching order' });
  }
});
// ---- Get Single Order by ID (for tracking) ----
"""
    # Insert before module.exports
    if "module.exports" in orders:
        orders = orders.replace("module.exports", new_route + "\nmodule.exports")
        with open("server/routes/orders.js", "w") as f:
            f.write(orders)
        print("   ✅ Added public order lookup route")


# ========================================
# UPDATE package.json — add nodemailer
# ========================================
import json

with open("package.json") as f:
    pkg = json.load(f)

if "nodemailer" not in pkg.get("dependencies", {}):
    pkg["dependencies"]["nodemailer"] = "^6.9.8"
    with open("package.json", "w") as f:
        json.dump(pkg, f, indent=2)
    print("   ✅ Added nodemailer to package.json")


print("\n" + "=" * 55)
print("✅ ALL DONE! Now:")
print("")
print("1. Push to GitHub:")
print("   git add -A")
print('   git commit -m "Feature: email notifications + order tracking"')
print("   git push")
print("")
print("2. Add these ENVIRONMENT VARIABLES in Railway:")
print("   EMAIL_USER = nodalislk@gmail.com")
print("   EMAIL_PASS = (your Gmail App Password)")
print("")
print("   To get a Gmail App Password:")
print("   → myaccount.google.com → Security → 2-Step Verification → App Passwords")
print("   → Create one for 'Mail' → Use the 16-character code")
print("")
print("3. After deploy, test by registering a new account!")
print("   Order tracking: /client/track-order.html")
print("=" * 55)
