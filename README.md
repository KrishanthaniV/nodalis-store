# 🧶 Nodalis — Handmade Fashion E-Commerce Store

A complete, production-ready e-commerce website for a boutique handmade fashion brand. Built with Node.js, Express, MongoDB, and vanilla HTML/CSS/JS.

---

## 📁 Project Structure

```
nodalis-store/
├── client/                  # Frontend pages
│   ├── index.html          # Homepage
│   ├── shop.html           # Shop (all products)
│   ├── product.html        # Single product page
│   ├── about.html          # Brand story
│   ├── contact.html        # Contact form
│   ├── cart.html           # Shopping cart
│   ├── checkout.html       # Checkout page
│   ├── login.html          # User login
│   └── register.html       # User registration
├── admin/                   # Admin panel pages
│   ├── dashboard.html      # Admin overview
│   ├── products.html       # Product management (CRUD)
│   ├── orders.html         # Order management
│   └── media.html          # Media library & logo upload
├── css/
│   └── style.css           # Complete stylesheet
├── js/
│   ├── script.js           # Main frontend JS + sample products
│   ├── cart.js             # Cart system (localStorage)
│   └── admin.js            # Admin panel JS
├── server/
│   ├── server.js           # Express server entry point
│   ├── config/
│   │   └── config.js       # Configuration & env vars
│   ├── middleware/
│   │   └── auth.js         # JWT authentication middleware
│   ├── models/
│   │   ├── User.js         # User/customer model
│   │   ├── Product.js      # Product model
│   │   └── Order.js        # Order model
│   └── routes/
│       ├── auth.js         # Auth routes (register/login)
│       ├── products.js     # Product CRUD routes
│       ├── orders.js       # Order routes
│       └── upload.js       # Image upload routes
├── assets/                  # Static assets
│   ├── images/
│   └── logo/
├── uploads/                 # Uploaded images (created at runtime)
├── package.json
├── .env.example             # Environment variables template
└── README.md
```

---

## 🚀 How to Install & Run Locally

### Prerequisites

- **Node.js** v18+ → [Download](https://nodejs.org/)
- **MongoDB** → [Download Community Edition](https://www.mongodb.com/try/download/community) or use [MongoDB Atlas](https://www.mongodb.com/atlas) (free cloud)

### Step 1 — Clone or copy the project

Place the `nodalis-store` folder wherever you like on your computer.

### Step 2 — Install dependencies

Open a terminal in the `nodalis-store` folder and run:

```bash
npm install
```

### Step 3 — Set up environment variables

Copy the example file and edit it:

```bash
cp .env.example .env
```

Edit `.env` with your values (or leave defaults for local development).

### Step 4 — Start MongoDB

**Option A — Local MongoDB:**
```bash
mongod
```

**Option B — MongoDB Atlas (cloud):**
Update `MONGODB_URI` in your `.env` file with your Atlas connection string:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/nodalis
```

### Step 5 — Start the server

```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

### Step 6 — Open the store

Visit: **http://localhost:3000**

The server will:
- ✅ Connect to MongoDB
- ✅ Seed 8 sample products automatically
- ✅ Create a default admin account

> **Note:** If MongoDB is unavailable, the site runs in "demo mode" — the frontend works with sample data baked into the JavaScript, but API routes won't function.

---

## 👤 Default Admin Login

| Field    | Value               |
|----------|---------------------|
| Email    | admin@nodalis.com   |
| Password | admin123            |

**⚠️ Change this password immediately in production!**

- Login at: http://localhost:3000/client/login.html
- Admin panel: http://localhost:3000/admin/dashboard.html

---

## 📦 How to Upload Products from the Admin Panel

1. Log in with admin credentials
2. Go to **Admin → Products** (http://localhost:3000/admin/products.html)
3. Click **"+ Add Product"**
4. Fill in the form:
   - **Name** — Product title
   - **Price** — Price in dollars
   - **Stock** — Quantity available
   - **Category** — Select from dropdown
   - **Sizes** — Comma-separated (e.g., `XS, S, M, L`)
   - **Description** — Product details
   - **Image** — Click upload zone to select an image
   - **Badges** — Check "Handmade" and/or "Limited edition"
   - **Featured** — Check to show on homepage
5. Click **"Save Product"**

### Editing & Deleting

- Click **"Edit"** on any product row to modify it
- Click **"Delete"** to remove (with confirmation)

---

## 🖼️ How to Change the Nodalis Brand Logo

### Option 1 — Via Admin Panel
1. Go to **Admin → Media Library** (http://localhost:3000/admin/media.html)
2. Scroll to **"Brand Logo"** section
3. Click **"Upload Logo"** and select your image
4. Recommended: 400×100px PNG with transparent background

### Option 2 — Via Code
Replace the text logo in the HTML navigation with an image:

```html
<!-- In all HTML files, find this: -->
<a href="/" class="nav-logo">Nodali<span>s</span></a>

<!-- Replace with: -->
<a href="/" class="nav-logo">
  <img src="/assets/logo/nodalis-logo.png" alt="Nodalis" style="height: 36px;">
</a>
```

Place your logo image at: `assets/logo/nodalis-logo.png`

---

## 💳 How to Configure Payments

### Stripe Setup

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from the [Stripe Dashboard → Developers → API Keys](https://dashboard.stripe.com/apikeys)
3. Add to your `.env` file:
   ```
   STRIPE_SECRET_KEY=sk_test_your_actual_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_publishable_key
   ```
4. To add Stripe checkout, include Stripe.js in the checkout page:
   ```html
   <script src="https://js.stripe.com/v3/"></script>
   ```
5. Initialize in JavaScript:
   ```javascript
   const stripe = Stripe('pk_test_your_publishable_key');
   const elements = stripe.elements();
   const card = elements.create('card');
   card.mount('#stripeCardElement');
   ```

### PayPal Setup

1. Create a PayPal Developer account at [developer.paypal.com](https://developer.paypal.com)
2. Create a sandbox app and get your credentials
3. Add to your `.env` file:
   ```
   PAYPAL_CLIENT_ID=your_paypal_client_id
   PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   PAYPAL_MODE=sandbox
   ```
4. Include PayPal SDK in checkout:
   ```html
   <script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID"></script>
   ```
5. Change `PAYPAL_MODE` to `live` when going to production.

---

## 🗄️ MongoDB Database

### Collections

| Collection | Description |
|-----------|-------------|
| `users`    | Customer accounts & admin users |
| `products` | All products with inventory |
| `orders`   | Customer orders with status tracking |

### Connecting to MongoDB Atlas (Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your IP (or allow all: `0.0.0.0/0`)
5. Click "Connect" → "Connect your application"
6. Copy the connection string and add to `.env`:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/nodalis?retryWrites=true&w=majority
   ```

---

## 🧪 8 Sample Test Products

The server automatically seeds these when the database is empty:

| # | Name | Category | Price | Stock |
|---|------|----------|-------|-------|
| 1 | Sage Garden Crochet Top | Crochet Tops | $68.00 | 8 |
| 2 | Sunset Bloom Hand-Painted Tee | Hand-Painted Tees | $95.00 | 3 |
| 3 | Luna Crochet Tote Bag | Bags | $54.00 | 12 |
| 4 | Abstract Waves Painted Tee | Hand-Painted Tees | $89.00 | 5 |
| 5 | Wildflower Crochet Halter | Crochet Tops | $72.00 | 6 |
| 6 | Handmade Beaded Earrings Set | Accessories | $32.00 | 20 |
| 7 | Oversized Essentials Tee — Oat | Oversized Tees | $48.00 | 25 |
| 8 | Mini Crochet Crossbody | Bags | $42.00 | 0 (Sold Out) |

---

## 🔐 API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login (returns JWT) |
| GET | `/api/auth/profile` | Get profile (auth required) |
| PUT | `/api/auth/profile` | Update profile (auth required) |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List all products |
| GET | `/api/products?category=bags` | Filter by category |
| GET | `/api/products?featured=true` | Featured only |
| GET | `/api/products?search=crochet` | Search products |
| GET | `/api/products/:id` | Get single product |
| POST | `/api/products` | Create product (admin) |
| PUT | `/api/products/:id` | Update product (admin) |
| DELETE | `/api/products/:id` | Delete product (admin) |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders` | Create order (auth) |
| GET | `/api/orders` | List all orders (admin) |
| GET | `/api/orders/my` | My orders (auth) |
| PUT | `/api/orders/:id/status` | Update status (admin) |

### Uploads
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload single image (admin) |
| POST | `/api/upload/multiple` | Upload multiple images (admin) |
| GET | `/api/upload` | List uploads (admin) |
| DELETE | `/api/upload/:filename` | Delete upload (admin) |

---

## 🌐 Deployment Tips

- Set `NODE_ENV=production` in your environment
- Use a process manager like **PM2**: `pm2 start server/server.js`
- Set up **Nginx** as a reverse proxy
- Enable **HTTPS** with Let's Encrypt
- Use **MongoDB Atlas** for cloud database
- Set a strong `JWT_SECRET` in production
- Configure your real Stripe & PayPal keys

---

## 📝 License

MIT — Built with care for the Nodalis brand.
