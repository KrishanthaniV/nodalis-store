/* ============================================================
   NODALIS — Order Routes
   POST   /api/orders              — Create order (checkout)
   GET    /api/orders              — List all orders (admin)
   GET    /api/orders/my           — Get user's orders
   GET    /api/orders/:id          — Get single order
   PUT    /api/orders/:id/status   — Update order status (admin)
   ============================================================ */

const express = require('express');
const router = express.Router();
const Order = require('../models/Order');
const Product = require('../models/Product');
const { sendOrderStatusEmail, sendOrderConfirmationEmail } = require('../utils/email');
const User = require('../models/User');
const { protect, adminOnly } = require('../middleware/auth');

// ---- Create Order (Checkout) ----
router.post('/', protect, async (req, res) => {
  try {
    const { items, shippingAddress, paymentMethod } = req.body;

    if (!items || items.length === 0) {
      return res.status(400).json({ message: 'No items in order' });
    }

    // Calculate totals and validate stock
    let subtotal = 0;
    const orderItems = [];

    for (const item of items) {
      const product = await Product.findById(item.product);
      if (!product) {
        return res.status(404).json({ message: `Product not found: ${item.product}` });
      }
      if (product.stock < item.quantity) {
        return res.status(400).json({ message: `Insufficient stock for ${product.name}` });
      }

      // Decrease stock
      product.stock -= item.quantity;
      await product.save();

      subtotal += product.price * item.quantity;
      orderItems.push({
        product: product._id,
        name: product.name,
        price: product.price,
        size: item.size || null,
        quantity: item.quantity
      });
    }

    const shipping = subtotal > 100 ? 0 : 8.50;
    const total = subtotal + shipping;

    const order = await Order.create({
      customer: req.user._id,
      items: orderItems,
      shippingAddress,
      subtotal,
      shipping,
      total,
      paymentMethod: paymentMethod || 'pending'
    });

    // Populate customer info
    await order.populate('customer', 'firstName lastName email');

    res.status(201).json(order);
  } catch (err) {
    console.error('Create order error:', err);
    res.status(500).json({ message: 'Error creating order' });
  }
});

// ---- Get All Orders — Admin ----
router.get('/', protect, adminOnly, async (req, res) => {
  try {
    const orders = await Order.find().populate('customer', 'firstName lastName email')
      .populate('customer', 'firstName lastName email')
      .sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    console.error('Get orders error:', err);
    res.status(500).json({ message: 'Error fetching orders' });
  }
});

// ---- Get My Orders — Customer ----
router.get('/my', protect, async (req, res) => {
  try {
    const orders = await Order.find({ customer: req.user._id })
      .sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    console.error('Get my orders error:', err);
    res.status(500).json({ message: 'Error fetching your orders' });
  }
});

// ---- Get Single Order ----
router.get('/:id', protect, async (req, res) => {
  try {
    const order = await Order.findById(req.params.id)
      .populate('customer', 'firstName lastName email');

    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Only allow admin or the order's customer to view
    if (req.user.role !== 'admin' && order.customer._id.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Not authorized to view this order' });
    }

    res.json(order);
  } catch (err) {
    console.error('Get order error:', err);
    res.status(500).json({ message: 'Error fetching order' });
  }
});

// ---- Update Order Status — Admin ----
router.put('/:id/status', protect, adminOnly, async (req, res) => {
  try {
    const { status } = req.body;
    const order = await Order.findById(req.params.id);

    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    order.status = status;

    // Set timestamps
    if (status === 'shipped') order.shippedAt = Date.now();
    if (status === 'delivered') order.deliveredAt = Date.now();

    // If cancelled, restore stock
    if (status === 'cancelled') {
      for (const item of order.items) {
        const product = await Product.findById(item.product);
        if (product) {
          product.stock += item.quantity;
          await product.save();
        }
      }
    }

    await order.save();
    res.json(order);
  } catch (err) {
    console.error('Update order status error:', err);
    res.status(500).json({ message: 'Error updating order status' });
  }
});


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

module.exports = router;
