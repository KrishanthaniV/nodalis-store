/* ============================================================
   NODALIS — Site Content Routes (Homepage Management)
   ============================================================ */

const express = require('express');
const router = express.Router();
const SiteContent = require('../models/SiteContent');
const { protect, adminOnly } = require('../middleware/auth');

// GET all content sections (public)
router.get('/', async (req, res) => {
  try {
    const content = await SiteContent.find({});
    const result = {};
    content.forEach(c => { result[c.section] = c.data; });
    res.json(result);
  } catch (err) {
    res.status(500).json({ message: 'Error loading content' });
  }
});

// GET single section (public)
router.get('/:section', async (req, res) => {
  try {
    const content = await SiteContent.findOne({ section: req.params.section });
    if (!content) return res.json({ data: {} });
    res.json(content);
  } catch (err) {
    res.status(500).json({ message: 'Error loading content' });
  }
});

// PUT update a section (admin only)
router.put('/:section', protect, adminOnly, async (req, res) => {
  try {
    const content = await SiteContent.findOneAndUpdate(
      { section: req.params.section },
      { section: req.params.section, data: req.body },
      { upsert: true, new: true, runValidators: true }
    );
    res.json({ success: true, content });
  } catch (err) {
    console.error('Content update error:', err);
    res.status(500).json({ message: 'Error saving content' });
  }
});

module.exports = router;
