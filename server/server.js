/* ============================================================
   NODALIS — Backend Server (Node.js + Express + MongoDB)
   ============================================================
   
   Run: npm install && node server.js
   Make sure MongoDB is running on localhost:27017
   ============================================================ */

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const multer = require('multer');

// Import routes
const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
const orderRoutes = require('./routes/orders');
const uploadRoutes = require('./routes/upload');
const contentRoutes = require('./routes/content');

// Import config
const { MONGODB_URI, PORT, JWT_SECRET } = require('./config/config');

// Initialize Express app
const app = express();

// ---- Middleware ----
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ---- Serve Static Files ----
// Serve the frontend from the project root
app.use('/css', express.static(path.join(__dirname, '..', 'css')));
app.use('/js', express.static(path.join(__dirname, '..', 'js')));
app.use('/assets', express.static(path.join(__dirname, '..', 'assets')));
app.use('/client', express.static(path.join(__dirname, '..', 'client')));
app.use('/admin', express.static(path.join(__dirname, '..', 'admin')));
app.use('/uploads', express.static(path.join(__dirname, '..', 'uploads')));

// ---- API Routes ----
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/content', contentRoutes);

// ---- Contact Form Endpoint ----
app.post('/api/contact', (req, res) => {
  const { name, email, subject, message } = req.body;
  console.log(`📩 Contact form: ${name} (${email}) — ${subject}`);
  // In production: send email via nodemailer, SendGrid, etc.
  res.json({ success: true, message: 'Message received!' });
});

// ---- Homepage Route ----
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'client', 'index.html'));
});

// ---- Connect to MongoDB & Start Server ----
mongoose.connect(MONGODB_URI)
  .then(async () => {
    console.log('✅ Connected to MongoDB');
    
    // Seed sample products if database is empty
    const Product = require('./models/Product');
    const count = await Product.countDocuments();
    if (count === 0) {
      await seedProducts();
      console.log('🌱 Seeded 8 sample products');
    }

    // Create default admin if none exists
    const User = require('./models/User');
    const adminExists = await User.findOne({ role: 'admin' });
    if (!adminExists) {
      const bcrypt = require('bcryptjs');
      const hashedPassword = await bcrypt.hash('admin123', 10);
      await User.create({
        firstName: 'Nodalis',
        lastName: 'Admin',
        email: 'admin@nodalis.com',
        password: hashedPassword,
        role: 'admin'
      });
      console.log('👤 Default admin created: admin@nodalis.com / admin123');
    }

    app.listen(PORT, () => {
      console.log(`\n🧶 Nodalis Store running at http://localhost:${PORT}`);
      console.log(`   Admin panel: http://localhost:${PORT}/admin/dashboard.html`);
      console.log(`   Admin login: admin@nodalis.com / admin123\n`);
    });
  })
  .catch(err => {
    console.error('❌ MongoDB connection failed:', err.message);
    console.log('\n💡 Starting in demo mode (no database)...\n');
    
    // Start server without DB for frontend-only demo
    app.listen(PORT, () => {
      console.log(`🧶 Nodalis Store (demo) running at http://localhost:${PORT}`);
      console.log('   Note: API routes require MongoDB. Frontend works with sample data.\n');
    });
  });

// ---- Seed Sample Products ----
async function seedProducts() {
  const Product = require('./models/Product');
  
  const products = [
    {
      name: 'Sage Garden Crochet Top',
      price: 68.00,
      category: 'crochet-tops',
      description: 'A delicate crochet crop top in sage green, featuring an intricate floral pattern. Made with 100% organic cotton yarn. Perfect for layering or wearing solo on warm evenings.',
      stock: 8,
      sizes: ['XS', 'S', 'M', 'L'],
      badges: ['handmade'],
      featured: true
    },
    {
      name: 'Sunset Bloom Hand-Painted Tee',
      price: 95.00,
      category: 'hand-painted-tees',
      description: 'One-of-a-kind hand-painted oversized tee on 300 GSM heavyweight cotton. Abstract sunset blooms in warm oranges and soft pinks. Each piece is uniquely painted — no two are alike.',
      stock: 3,
      sizes: ['S', 'M', 'L', 'XL'],
      badges: ['handmade', 'limited'],
      featured: true
    },
    {
      name: 'Luna Crochet Tote Bag',
      price: 54.00,
      category: 'bags',
      description: 'A spacious crochet tote bag in cream and beige tones. Features a magnetic closure and inner lining. Perfect for market days and everyday carry.',
      stock: 12,
      sizes: [],
      badges: ['handmade'],
      featured: true
    },
    {
      name: 'Abstract Waves Painted Tee',
      price: 89.00,
      category: 'hand-painted-tees',
      description: 'Oversized 300 GSM tee with hand-painted abstract ocean waves. Blues, teals, and white crests. Wearable art that turns heads. Unisex fit.',
      stock: 5,
      sizes: ['M', 'L', 'XL'],
      badges: ['handmade', 'limited'],
      featured: true
    },
    {
      name: 'Wildflower Crochet Halter',
      price: 72.00,
      category: 'crochet-tops',
      description: 'A bohemian halter-neck crochet top with wildflower motifs. Handmade with soft bamboo-blend yarn for a lightweight, breathable feel. Ties at the neck and back.',
      stock: 6,
      sizes: ['XS', 'S', 'M'],
      badges: ['handmade'],
      featured: false
    },
    {
      name: 'Handmade Beaded Earrings Set',
      price: 32.00,
      category: 'accessories',
      description: 'A set of three pairs of handmade beaded drop earrings in sage, cream, and warm brown. Lightweight and comfortable for all-day wear. Hypoallergenic hooks.',
      stock: 20,
      sizes: [],
      badges: ['handmade'],
      featured: false
    },
    {
      name: 'Oversized Essentials Tee — Oat',
      price: 48.00,
      category: 'oversized-tees',
      description: 'Premium 220 GSM oversized unisex tee in warm oat. Dropped shoulders, boxy fit, and ribbed neckline. The perfect everyday staple with a Nodalis woven label.',
      stock: 25,
      sizes: ['S', 'M', 'L', 'XL', 'XXL'],
      badges: [],
      featured: true
    },
    {
      name: 'Mini Crochet Crossbody',
      price: 42.00,
      category: 'bags',
      description: 'A charming mini crossbody bag in dusty rose crochet. Features an adjustable strap and zip closure. Just the right size for phone, keys, and essentials.',
      stock: 0,
      sizes: [],
      badges: ['handmade'],
      featured: false
    }
  ];

  await Product.insertMany(products);
}
