/* ============================================================
   NODALIS — Configuration
   ============================================================
   
   For production, use environment variables instead of defaults.
   Create a .env file in the /server directory with your values.
   ============================================================ */

require('dotenv').config();

module.exports = {
  // Server
  PORT: process.env.PORT || 3000,

  // MongoDB
  MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/nodalis',

  // JWT Authentication
  JWT_SECRET: process.env.JWT_SECRET || 'nodalis_secret_key_change_in_production',
  JWT_EXPIRES_IN: process.env.JWT_EXPIRES_IN || '7d',

  // Stripe Payment (placeholder — add your keys)
  STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY || 'sk_test_YOUR_STRIPE_SECRET_KEY',
  STRIPE_PUBLISHABLE_KEY: process.env.STRIPE_PUBLISHABLE_KEY || 'pk_test_YOUR_STRIPE_PUBLISHABLE_KEY',

  // PayPal Payment (placeholder — add your keys)
  PAYPAL_CLIENT_ID: process.env.PAYPAL_CLIENT_ID || 'YOUR_PAYPAL_CLIENT_ID',
  PAYPAL_CLIENT_SECRET: process.env.PAYPAL_CLIENT_SECRET || 'YOUR_PAYPAL_CLIENT_SECRET',
  PAYPAL_MODE: process.env.PAYPAL_MODE || 'sandbox', // 'sandbox' or 'live'

  // File Uploads
  UPLOAD_DIR: process.env.UPLOAD_DIR || 'uploads',
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5 MB
};
