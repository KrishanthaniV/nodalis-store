#!/usr/bin/env python3
"""
Switch email from Gmail SMTP to Resend HTTP API
Run from: ~/Downloads/nodalis-v5/nodalis-store
"""

print("🔧 Switching email to Resend...")

new_email = '''/* ============================================================
   NODALIS — Email Utility (Resend HTTP API)
   ============================================================
   Setup: Add to Railway environment variables:
     RESEND_API_KEY=re_xxxxxxxxxxxxx
   
   Get your API key at: https://resend.com/api-keys
   ============================================================ */

const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const FROM_EMAIL = 'Nodalis <onboarding@resend.dev>';
// Once you verify your domain at resend.com, change FROM_EMAIL to:
// const FROM_EMAIL = 'Nodalis <hello@nodalis.lk>';

async function sendEmail(to, subject, html) {
  if (!RESEND_API_KEY) {
    console.log('⚠️  Email skipped — no RESEND_API_KEY set');
    return false;
  }
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + RESEND_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: FROM_EMAIL,
        to: [to],
        subject: subject,
        html: html
      })
    });
    const data = await res.json();
    if (res.ok) {
      console.log('📧 Email sent to:', to, '| ID:', data.id);
      return true;
    } else {
      console.log('📧 Email error:', data);
      return false;
    }
  } catch (err) {
    console.error('📧 Email send failed:', err.message);
    return false;
  }
}

// Verify on startup
if (RESEND_API_KEY) {
  console.log('📧 Email service ready (Resend)');
} else {
  console.log('⚠️  Email not configured: Add RESEND_API_KEY to environment variables');
}

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
      <p style="margin-top:.5rem;">© 2026 Nodalis. All rights reserved.</p>
    </div>
  </div>`;
}

// Send welcome email
async function sendWelcomeEmail(user) {
  const content = `
    <h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;margin-bottom:1rem;">Welcome to Nodalis, ${user.firstName}!</h2>
    <p style="line-height:1.8;color:#5A554F;">Thank you for creating your account. You're now part of our community of people who appreciate the beauty of handmade fashion.</p>
    <p style="line-height:1.8;color:#5A554F;margin-top:1rem;">Every piece in our collection is crafted by hand with love — crocheted tops, hand-painted tees, bags, and artisan accessories. Each one is unique, just like you.</p>
    <div style="text-align:center;margin:2rem 0;">
      <a href="https://nodalis-store-production.up.railway.app/client/shop.html" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Explore the Collection</a>
    </div>
    <p style="line-height:1.8;color:#5A554F;">If you have any questions, reach out to us at <a href="mailto:nodalislk@gmail.com" style="color:#B8977E;">nodalislk@gmail.com</a> or on <a href="https://wa.me/94767003630" style="color:#B8977E;">WhatsApp</a>.</p>
    <p style="margin-top:1.5rem;color:#2A2826;">With love,<br><strong>The Nodalis Team</strong></p>
  `;
  return sendEmail(user.email, 'Welcome to Nodalis — Handmade with Love 🧶', emailTemplate(content));
}

// Send order confirmation
async function sendOrderConfirmationEmail(user, order) {
  const itemsList = (order.items || []).map(item =>
    '<tr><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;">' + (item.name || 'Product') + '</td><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;text-align:center;">' + (item.quantity || 1) + '</td><td style="padding:.5rem;border-bottom:1px solid #E5DDD4;text-align:right;">$' + (item.price || 0).toFixed(2) + '</td></tr>'
  ).join('');

  const content = `
    <h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;margin-bottom:1rem;">Order Confirmed! 🎉</h2>
    <p style="line-height:1.8;color:#5A554F;">Hi ${user.firstName}, your order has been received and is being prepared with care.</p>
    <div style="background:#F2EDE8;padding:1rem;margin:1.5rem 0;">
      <p style="font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#B8977E;margin-bottom:.5rem;">Order ID</p>
      <p style="font-family:monospace;font-size:.9rem;">${order._id}</p>
    </div>
    <table style="width:100%;border-collapse:collapse;margin:1rem 0;">
      <tr style="background:#F2EDE8;"><th style="padding:.5rem;text-align:left;font-size:.7rem;text-transform:uppercase;">Item</th><th style="padding:.5rem;text-align:center;font-size:.7rem;text-transform:uppercase;">Qty</th><th style="padding:.5rem;text-align:right;font-size:.7rem;text-transform:uppercase;">Price</th></tr>
      ${itemsList}
      <tr><td colspan="2" style="padding:.8rem .5rem;font-weight:600;text-align:right;">Total</td><td style="padding:.8rem .5rem;text-align:right;font-weight:600;">$${(order.total || 0).toFixed(2)}</td></tr>
    </table>
    <div style="text-align:center;margin:2rem 0;">
      <a href="https://nodalis-store-production.up.railway.app/client/track-order.html?id=${order._id}" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Track Your Order</a>
    </div>
  `;
  return sendEmail(user.email, 'Your Nodalis Order is Confirmed! #' + String(order._id).slice(-6).toUpperCase(), emailTemplate(content));
}

// Send order status update
async function sendOrderStatusEmail(user, order) {
  const statusMessages = {
    'pending': { emoji: '⏳', title: 'Order Received', desc: 'We have received your order and are preparing it with care.' },
    'confirmed': { emoji: '✅', title: 'Order Confirmed', desc: 'Your order has been confirmed and is being prepared.' },
    'ready': { emoji: '📦', title: 'Order Ready', desc: 'Your order is packed and ready to ship!' },
    'shipped': { emoji: '🚚', title: 'Order Shipped', desc: 'Your order is on its way to you!' },
    'in-transit': { emoji: '🛣️', title: 'In Transit', desc: 'Your order is moving through the delivery network.' },
    'delivered': { emoji: '🎉', title: 'Order Delivered', desc: 'Your order has been delivered. Enjoy your handmade pieces!' },
    'cancelled': { emoji: '❌', title: 'Order Cancelled', desc: 'Your order has been cancelled. If you have questions, please contact us.' }
  };
  const status = statusMessages[order.status] || statusMessages['pending'];

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
  return sendEmail(user.email, status.emoji + ' Your Nodalis Order — ' + status.title, emailTemplate(content));
}

module.exports = {
  sendWelcomeEmail,
  sendOrderConfirmationEmail,
  sendOrderStatusEmail
};
'''

with open("server/utils/email.js", "w") as f:
    f.write(new_email)
print("   ✅ Email switched to Resend HTTP API")

# Remove nodemailer from package.json since we no longer need it
import json
with open("package.json") as f:
    pkg = json.load(f)
if "nodemailer" in pkg.get("dependencies", {}):
    del pkg["dependencies"]["nodemailer"]
    with open("package.json", "w") as f:
        json.dump(pkg, f, indent=2)
    print("   ✅ Removed nodemailer from dependencies")

print("\\n" + "="*50)
print("Done! Now:")
print("  1. Run: npm install")
print("  2. Push to GitHub")
print("  3. Add RESEND_API_KEY to Railway Variables")
print("     (get it from https://resend.com/api-keys)")
print("="*50)
'''

with open("server/utils/email.js", "w") as f:
    f.write(new_email)

print("   ✅ Email utility rewritten for Resend")

# Remove nodemailer dependency
import json
with open("package.json") as f:
    pkg = json.load(f)
if "nodemailer" in pkg.get("dependencies", {}):
    del pkg["dependencies"]["nodemailer"]
    with open("package.json", "w") as f:
        json.dump(pkg, f, indent=2)
    print("   ✅ Removed nodemailer from package.json")

print()
print("="*50)
print("Now do these steps:")
print("  1. npm install")
print("  2. git add -A")
print('  3. git commit -m "Switch email to Resend API"')
print("  4. git push")
print()
print("Then in Railway Variables:")
print("  - Remove EMAIL_USER and EMAIL_PASS")
print("  - Add RESEND_API_KEY = (your key from resend.com)")
print("="*50)
