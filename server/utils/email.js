/* ============================================================
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
    'pending': { emoji: '⏳', title: 'Order Received', desc: 'We\'ve received your order and are preparing it with care.' },
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
