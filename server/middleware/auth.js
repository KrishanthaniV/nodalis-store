/* ============================================================
   NODALIS — Authentication Middleware
   Verifies JWT tokens and attaches user to request
   ============================================================ */

const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { JWT_SECRET } = require('../config/config');

/**
 * Protect routes — requires valid JWT token
 */
const protect = async (req, res, next) => {
  let token;

  // Check for Bearer token in Authorization header
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({ message: 'Not authorized — no token provided' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, JWT_SECRET);

    // Attach user to request (exclude password)
    req.user = await User.findById(decoded.id).select('-password');

    if (!req.user) {
      return res.status(401).json({ message: 'Not authorized — user not found' });
    }

    next();
  } catch (err) {
    return res.status(401).json({ message: 'Not authorized — invalid token' });
  }
};

/**
 * Admin-only middleware — must be used after protect
 */
const adminOnly = (req, res, next) => {
  if (req.user && req.user.role === 'admin') {
    next();
  } else {
    return res.status(403).json({ message: 'Access denied — admin only' });
  }
};

module.exports = { protect, adminOnly };
