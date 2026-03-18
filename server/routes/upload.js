/* ============================================================
   NODALIS — Upload Routes
   POST /api/upload          — Upload single image
   POST /api/upload/multiple — Upload multiple images
   DELETE /api/upload/:filename — Delete image
   ============================================================ */

const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { protect, adminOnly } = require('../middleware/auth');
const { UPLOAD_DIR, MAX_FILE_SIZE } = require('../config/config');

// Ensure upload directory exists
const uploadPath = path.join(__dirname, '..', '..', UPLOAD_DIR);
if (!fs.existsSync(uploadPath)) {
  fs.mkdirSync(uploadPath, { recursive: true });
}

// Multer storage configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    // Generate unique filename: timestamp-randomhex-originalname
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E6);
    const ext = path.extname(file.originalname);
    const name = file.originalname.replace(ext, '').replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
    cb(null, `${uniqueSuffix}-${name}${ext}`);
  }
});

// File filter — only allow images
const fileFilter = (req, file, cb) => {
  const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
  if (allowed.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Only JPEG, PNG, GIF, and WebP images are allowed'), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: MAX_FILE_SIZE }
});

// ---- Upload Single Image (Admin Only) ----
router.post('/', protect, adminOnly, upload.single('image'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: 'No image file provided' });
    }

    res.json({
      message: 'Image uploaded successfully',
      url: `/uploads/${req.file.filename}`,
      filename: req.file.filename,
      size: req.file.size,
      mimetype: req.file.mimetype
    });
  } catch (err) {
    console.error('Upload error:', err);
    res.status(500).json({ message: 'Error uploading image' });
  }
});

// ---- Upload Multiple Images (Admin Only) ----
router.post('/multiple', protect, adminOnly, upload.array('images', 10), (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ message: 'No image files provided' });
    }

    const uploaded = req.files.map(file => ({
      url: `/uploads/${file.filename}`,
      filename: file.filename,
      size: file.size,
      mimetype: file.mimetype
    }));

    res.json({
      message: `${uploaded.length} image(s) uploaded successfully`,
      files: uploaded
    });
  } catch (err) {
    console.error('Multi-upload error:', err);
    res.status(500).json({ message: 'Error uploading images' });
  }
});

// ---- Delete Image (Admin Only) ----
router.delete('/:filename', protect, adminOnly, (req, res) => {
  try {
    const filePath = path.join(uploadPath, req.params.filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ message: 'File not found' });
    }

    fs.unlinkSync(filePath);
    res.json({ message: 'File deleted successfully' });
  } catch (err) {
    console.error('Delete file error:', err);
    res.status(500).json({ message: 'Error deleting file' });
  }
});

// ---- List All Uploads (Admin Only) ----
router.get('/', protect, adminOnly, (req, res) => {
  try {
    const files = fs.readdirSync(uploadPath)
      .filter(f => !f.startsWith('.'))
      .map(filename => ({
        filename,
        url: `/uploads/${filename}`,
        size: fs.statSync(path.join(uploadPath, filename)).size
      }));

    res.json(files);
  } catch (err) {
    console.error('List uploads error:', err);
    res.status(500).json({ message: 'Error listing uploads' });
  }
});

// ---- Error Handler for Multer ----
router.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ message: 'File too large — max 5MB' });
    }
    return res.status(400).json({ message: err.message });
  }
  if (err) {
    return res.status(400).json({ message: err.message });
  }
  next();
});

module.exports = router;
