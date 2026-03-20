/* ============================================================
   NODALIS — Site Content Model (Homepage & Settings)
   ============================================================ */

const mongoose = require('mongoose');

const siteContentSchema = new mongoose.Schema({
  section: {
    type: String,
    required: true,
    unique: true,
    enum: ['hero', 'categories', 'about-preview', 'newsletter', 'highlight', 'instagram', 'general']
  },
  data: {
    // HERO
    heroEyebrow: { type: String, default: 'Handcrafted \u00B7 Limited Edition \u00B7 One of a Kind' },
    heroTitle: { type: String, default: 'The Art of' },
    heroTitleEm: { type: String, default: 'Handmade' },
    heroDescription: { type: String, default: '' },
    heroCtaText: { type: String, default: 'Discover the Collection' },
    heroCtaLink: { type: String, default: '/client/shop.html' },
    heroMediaType: { type: String, enum: ['image', 'video', 'placeholder'], default: 'placeholder' },
    heroMediaUrl: { type: String, default: '' },

    // CATEGORIES (array of 4 categories)
    categories: [{
      name: String,
      slug: String,
      imageUrl: String
    }],

    // ABOUT PREVIEW
    aboutTitle: { type: String, default: '' },
    aboutDescription: { type: String, default: '' },
    aboutImageUrl: { type: String, default: '' },
    aboutCtaText: { type: String, default: 'Discover Our Story' },

    // HIGHLIGHT / QUOTE
    highlightQuote: { type: String, default: '' },
    highlightAuthor: { type: String, default: '' },

    // NEWSLETTER
    newsletterTitle: { type: String, default: '' },
    newsletterDescription: { type: String, default: '' },

    // INSTAGRAM
    instagramHandle: { type: String, default: '@nodalis.lk' },
    instagramImages: [{ url: String }],

    // GENERAL
    siteName: { type: String, default: 'Nodalis' },
    tagline: { type: String, default: 'Timeless Pieces' }
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

siteContentSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

module.exports = mongoose.model('SiteContent', siteContentSchema);
