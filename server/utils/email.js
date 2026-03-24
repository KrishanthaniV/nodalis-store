/* ============================================================
   NODALIS — Email Utility (Resend HTTP API)
   ============================================================ */

const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const FROM_EMAIL = 'Nodalis <onboarding@resend.dev>';

async function sendEmail(to, subject, html) {
  if (!RESEND_API_KEY) { console.log('No RESEND_API_KEY'); return false; }
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM_EMAIL, to: [to], subject, html })
    });
    const data = await res.json();
    if (res.ok) { console.log('Email sent to:', to); return true; }
    else { console.log('Email error:', data); return false; }
  } catch (err) { console.error('Email failed:', err.message); return false; }
}

if (RESEND_API_KEY) { console.log('Email service ready (Resend)'); }
else { console.log('Email not configured: Add RESEND_API_KEY'); }

function emailTemplate(content) {
  return '<div style="max-width:600px;margin:0 auto;font-family:Helvetica,Arial,sans-serif;color:#2A2826;background:#FAFAFA;"><div style="background:#0A0A0A;padding:2rem;text-align:center;"><h1 style="font-family:Georgia,serif;color:#FAFAFA;font-weight:400;font-size:1.8rem;margin:0;">Nodalis</h1><p style="color:#B8977E;font-size:.7rem;letter-spacing:.3em;text-transform:uppercase;margin:.5rem 0 0;">Timeless Pieces</p></div><div style="padding:2rem;">' + content + '</div><div style="background:#F2EDE8;padding:1.5rem;text-align:center;font-size:.75rem;color:#8A8580;"><p>Nodalis - Handmade Fashion from Sri Lanka</p></div></div>';
}

async function sendWelcomeEmail(user) {
  var content = '<h2 style="font-family:Georgia,serif;font-weight:400;font-size:1.5rem;">Welcome to Nodalis, ' + user.firstName + '!</h2><p style="line-height:1.8;color:#5A554F;">Thank you for joining. Every piece is crafted by hand with love.</p><div style="text-align:center;margin:2rem 0;"><a href="https://nodalis-store-production.up.railway.app/client/shop.html" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Explore Collection</a></div>';
  return sendEmail(user.email, 'Welcome to Nodalis!', emailTemplate(content));
}

async function sendOrderConfirmationEmail(user, order) {
  var content = '<h2 style="font-family:Georgia,serif;font-weight:400;">Order Confirmed!</h2><p>Hi ' + user.firstName + ', your order #' + String(order._id).slice(-6) + ' is being prepared.</p><div style="text-align:center;margin:2rem 0;"><a href="https://nodalis-store-production.up.railway.app/client/track-order.html?id=' + order._id + '" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Track Order</a></div>';
  return sendEmail(user.email, 'Order Confirmed! #' + String(order._id).slice(-6).toUpperCase(), emailTemplate(content));
}

async function sendOrderStatusEmail(user, order) {
  var titles = {pending:'Order Received',confirmed:'Confirmed',ready:'Ready to Ship',shipped:'Shipped','in-transit':'In Transit',delivered:'Delivered',cancelled:'Cancelled'};
  var title = titles[order.status] || 'Update';
  var content = '<h2 style="font-family:Georgia,serif;font-weight:400;">' + title + '</h2><p>Hi ' + user.firstName + ', your order #' + String(order._id).slice(-6) + ' status: <strong>' + title + '</strong></p><div style="text-align:center;margin:2rem 0;"><a href="https://nodalis-store-production.up.railway.app/client/track-order.html?id=' + order._id + '" style="display:inline-block;padding:.8rem 2rem;background:#2A2826;color:#FAFAFA;text-decoration:none;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;">Track Order</a></div>';
  return sendEmail(user.email, 'Nodalis Order - ' + title, emailTemplate(content));
}

module.exports = { sendWelcomeEmail, sendOrderConfirmationEmail, sendOrderStatusEmail };
