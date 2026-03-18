/* ============================================================
   NODALIS — Product Routes
   GET    /api/products          — List all products (with filters)
   GET    /api/products/:id      — Get single product
   POST   /api/products          — Create product (admin)
   PUT    /api/products/:id      — Update product (admin)
   DELETE /api/products/:id      — Delete product (admin)
   ============================================================ */

const express = require('express');
const router = express.Router();
const Product = require('../models/Product');
const { protect, adminOnly } = require('../middleware/auth');

// ---- Get All Products (Public) ----
router.get('/', async (req, res) => {
  try {
    const { category, featured, search, limit, sort } = req.query;
    let query = {};

    // Category filter
    if (category) query.category = category;

    // Featured filter
    if (featured === 'true') query.featured = true;

    // Search filter
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } }
      ];
    }

    // Build query
    let productQuery = Product.find(query);

    // Sort
    if (sort === 'price-asc') productQuery = productQuery.sort({ price: 1 });
    else if (sort === 'price-desc') productQuery = productQuery.sort({ price: -1 });
    else if (sort === 'newest') productQuery = productQuery.sort({ createdAt: -1 });
    else productQuery = productQuery.sort({ featured: -1, createdAt: -1 });

    // Limit
    if (limit) productQuery = productQuery.limit(parseInt(limit));

    const products = await productQuery;
    res.json(products);
  } catch (err) {
    console.error('Get products error:', err);
    res.status(500).json({ message: 'Error fetching products' });
  }
});

// ---- Get Single Product (Public) ----
router.get('/:id', async (req, res) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(product);
  } catch (err) {
    console.error('Get product error:', err);
    res.status(500).json({ message: 'Error fetching product' });
  }
});

// ---- Create Product (Admin Only) ----
router.post('/', protect, adminOnly, async (req, res) => {
  try {
    const { name, description, price, category, sizes, stock, images, badges, featured } = req.body;

    const product = await Product.create({
      name,
      description,
      price,
      category,
      sizes: sizes || [],
      stock: stock || 0,
      images: images || [],
      badges: badges || [],
      featured: featured || false
    });

    res.status(201).json(product);
  } catch (err) {
    console.error('Create product error:', err);
    res.status(500).json({ message: 'Error creating product' });
  }
});

// ---- Update Product (Admin Only) ----
router.put('/:id', protect, adminOnly, async (req, res) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    // Update fields
    const fields = ['name', 'description', 'price', 'category', 'sizes', 'stock', 'images', 'badges', 'featured'];
    fields.forEach(field => {
      if (req.body[field] !== undefined) {
        product[field] = req.body[field];
      }
    });

    product.updatedAt = Date.now();
    await product.save();

    res.json(product);
  } catch (err) {
    console.error('Update product error:', err);
    res.status(500).json({ message: 'Error updating product' });
  }
});

// ---- Delete Product (Admin Only) ----
router.delete('/:id', protect, adminOnly, async (req, res) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    await Product.findByIdAndDelete(req.params.id);
    res.json({ message: 'Product deleted successfully' });
  } catch (err) {
    console.error('Delete product error:', err);
    res.status(500).json({ message: 'Error deleting product' });
  }
});

module.exports = router;
