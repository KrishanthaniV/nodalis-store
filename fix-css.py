#!/usr/bin/env python3
"""
NODALIS CSS FIX — Append missing hero/marquee/category styles to inline <style> blocks.
Run from: ~/Downloads/nodalis-v5/nodalis-store
Usage: python3 fix-css.py
"""
import os, glob

PATCH_CSS = """
/* === HERO === */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;overflow:hidden;background:var(--black);color:var(--white)}
.hero-media{position:absolute;inset:0;z-index:1}
.hero-media img,.hero-media video{width:100%;height:100%;object-fit:cover;opacity:.5}
.hero-media-placeholder{width:100%;height:100%;background:linear-gradient(135deg,#1a1816 0%,#2a2826 40%,#3a3632 100%)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(10,10,10,.3) 0%,rgba(10,10,10,.6) 100%);z-index:2}
.hero-content{position:relative;z-index:3;padding:0 clamp(1.5rem,4vw,4rem);max-width:700px}
.hero-eyebrow{font-size:.65rem;letter-spacing:.35em;text-transform:uppercase;color:var(--gold-light);margin-bottom:1.5rem;font-weight:400}
.hero-content h1{font-family:var(--font-display);font-size:clamp(3rem,7vw,5.5rem);font-weight:400;line-height:1.05;letter-spacing:-.02em;margin-bottom:1.5rem}
.hero-content h1 em{font-style:italic;color:var(--gold-light)}
.hero-sub{font-size:.95rem;line-height:1.8;color:rgba(255,255,255,.65);max-width:45ch;margin-bottom:2.5rem}
.hero-cta{display:inline-flex;align-items:center;gap:.8rem;padding:1.1rem 2.8rem;font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;font-weight:500;background:var(--white);color:var(--black);transition:all .4s cubic-bezier(.4,0,.2,1)}
.hero-cta:hover{background:var(--gold);color:var(--white)}
.hero-cta svg{transition:transform .3s}
.hero-cta:hover svg{transform:translateX(4px)}
.hero-scroll{position:absolute;bottom:2.5rem;left:50%;transform:translateX(-50%);z-index:3;text-align:center;color:rgba(255,255,255,.35)}
.hero-scroll-line{width:1px;height:40px;background:rgba(255,255,255,.2);margin:0 auto .8rem}
.hero-scroll span{font-size:.6rem;letter-spacing:.25em;text-transform:uppercase}
/* === MARQUEE === */
.marquee{overflow:hidden;background:var(--cream-dark);padding:1.1rem 0;white-space:nowrap}
.marquee-inner{display:inline-flex;animation:marquee-scroll 35s linear infinite}
.marquee-item{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--grey);padding:0 1.5rem;font-weight:500;flex-shrink:0}
.marquee-item span{color:var(--gold);margin:0 .3rem}
@keyframes marquee-scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
/* === CATEGORIES === */
.category-card{position:relative;aspect-ratio:3/4;overflow:hidden;cursor:pointer;display:block}
.category-card-bg{position:absolute;inset:0;background:var(--cream-dark);transition:transform .8s cubic-bezier(.4,0,.2,1)}
.category-card-bg.cat-crochet{background:linear-gradient(135deg,#d4bfa8 0%,#e5ddd4 100%)}
.category-card-bg.cat-bags{background:linear-gradient(135deg,#c5c0ba 0%,#e5ddd4 100%)}
.category-card-bg.cat-tees{background:linear-gradient(135deg,#b8977e 0%,#d4bfa8 100%)}
.category-card-bg.cat-accessories{background:linear-gradient(135deg,#8a8580 0%,#c5c0ba 100%)}
.category-card:hover .category-card-bg{transform:scale(1.06)}
.category-card-content{position:absolute;bottom:0;left:0;right:0;padding:1.5rem;z-index:3;color:var(--charcoal)}
.category-card-content .eyebrow{font-size:.55rem;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem}
.category-card-content h3{font-family:var(--font-display);font-size:1.3rem;font-weight:400;margin-bottom:.5rem}
.category-card-cta{font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);display:inline-flex;align-items:center;gap:.5rem;transition:color .3s}
.category-card-cta svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.5}
.category-card-cta:hover{color:var(--charcoal)}
/* === SECTION HEADER === */
.section-header{text-align:center;margin-bottom:clamp(2rem,4vw,4rem)}
.section-header .section-desc{margin:0 auto}
/* === PRODUCT DETAIL === */
.product-detail{max-width:1200px;margin:0 auto;padding-top:calc(80px + 3rem)}
.product-layout{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}
.product-gallery{position:relative}
.product-gallery-main{aspect-ratio:3/4;overflow:hidden;background:var(--cream-dark);margin-bottom:1rem;cursor:zoom-in}
.product-gallery-main img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.product-gallery-main:hover img{transform:scale(1.03)}
.product-gallery-thumbs{display:flex;gap:.5rem}
.product-gallery-thumb{width:80px;height:100px;overflow:hidden;background:var(--cream-dark);cursor:pointer;opacity:.6;transition:opacity .3s;border:2px solid transparent}
.product-gallery-thumb.active{opacity:1;border-color:var(--gold)}
.product-gallery-thumb img{width:100%;height:100%;object-fit:cover}
.product-info{padding:1rem 0}
.product-info .product-category{font-size:.6rem;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem}
.product-info h1{font-family:var(--font-display);font-size:clamp(1.5rem,3vw,2.2rem);font-weight:400;margin-bottom:1rem;line-height:1.2}
.product-info .product-price{font-size:1.3rem;font-weight:600;margin-bottom:1.5rem}
.product-info .product-description{font-size:.9rem;line-height:1.8;color:var(--grey);margin-bottom:2rem}
.product-options{margin-bottom:2rem}
.product-options label{display:block;font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;font-weight:500;margin-bottom:.8rem}
.product-actions{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}
.product-meta{border-top:1px solid var(--cream-dark);padding-top:1.5rem;font-size:.82rem;color:var(--grey);line-height:2}
/* === ABOUT === */
.about-preview{display:grid;grid-template-columns:1fr 1fr;gap:3rem;max-width:1200px;margin:0 auto;align-items:center}
.about-preview-image{aspect-ratio:4/5;overflow:hidden;background:var(--cream-dark)}
.about-preview-image img{width:100%;height:100%;object-fit:cover}
.about-preview-content{padding:1rem 0}
.about-values{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:3rem;max-width:1200px;margin-left:auto;margin-right:auto}
.value-card{text-align:center;padding:2rem 1rem}
.value-card .value-icon{width:48px;height:48px;margin:0 auto 1rem;stroke:var(--gold);fill:none;stroke-width:1.5}
.value-card h3{font-family:var(--font-display);font-size:1.1rem;font-weight:400;margin-bottom:.5rem}
.value-card p{font-size:.85rem;color:var(--grey);line-height:1.7}
/* === NEWSLETTER === */
.newsletter{background:var(--charcoal);color:var(--white);padding:clamp(3rem,5vw,5rem);text-align:center;max-width:900px;margin:0 auto}
.newsletter .section-eyebrow{color:var(--gold-light)}
.newsletter .section-title{color:var(--white)}
.newsletter .section-desc{color:rgba(255,255,255,.6);margin:0 auto 2rem}
.newsletter-form{display:flex;gap:.5rem;max-width:480px;margin:0 auto}
.newsletter-form input{flex:1;padding:1rem;border:1px solid rgba(255,255,255,.15);background:transparent;color:var(--white);font-size:.85rem;outline:none}
.newsletter-form input::placeholder{color:rgba(255,255,255,.35)}
.newsletter-form input:focus{border-color:var(--gold)}
/* === INSTA === */
.insta-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.insta-item{aspect-ratio:1;overflow:hidden;background:var(--cream-dark);cursor:pointer;position:relative}
.insta-item img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.insta-item:hover img{transform:scale(1.08)}
/* === HIGHLIGHT === */
.highlight-section{text-align:center;padding:clamp(3rem,6vw,6rem) clamp(1.5rem,4vw,4rem);background:var(--cream-dark)}
.highlight-section blockquote{font-family:var(--font-display);font-size:clamp(1.3rem,3vw,2rem);font-style:italic;font-weight:400;line-height:1.4;max-width:50ch;margin:0 auto 1rem;color:var(--charcoal)}
.highlight-section cite{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-style:normal}
/* === CONTACT === */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:3rem;max-width:1000px;margin:0 auto}
.contact-info h3{font-family:var(--font-display);font-size:1.3rem;font-weight:400;margin-bottom:1.5rem}
.contact-info-item{display:flex;align-items:flex-start;gap:1rem;margin-bottom:1.5rem}
.contact-info-item svg{width:20px;height:20px;stroke:var(--gold);fill:none;stroke-width:1.5;flex-shrink:0;margin-top:2px}
.contact-info-item .label{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--grey);margin-bottom:.2rem}
.contact-info-item .value{font-size:.9rem;color:var(--charcoal)}
.contact-info-item .value a{color:var(--gold);transition:color .3s}
.contact-info-item .value a:hover{color:var(--charcoal)}
.contact-social{display:flex;gap:1rem;margin-top:2rem}
.contact-social a{width:40px;height:40px;border:1px solid var(--cream-dark);display:flex;align-items:center;justify-content:center;transition:all .3s}
.contact-social a:hover{background:var(--charcoal);border-color:var(--charcoal);color:var(--white)}
.contact-social a svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.5}
/* === CHECKOUT === */
.checkout-layout{display:grid;grid-template-columns:1fr 380px;gap:2rem;max-width:1200px;margin:0 auto;align-items:start}
.checkout-section{background:var(--white);padding:2rem;margin-bottom:1.5rem}
.checkout-section h3{font-family:var(--font-display);font-size:1.2rem;font-weight:400;margin-bottom:1.5rem;padding-bottom:.8rem;border-bottom:1px solid var(--cream-dark)}
/* === SHOP CONTROLS === */
.shop-controls{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:2rem;flex-wrap:wrap;max-width:1400px;margin-left:auto;margin-right:auto}
/* === ZOOM === */
.zoom-overlay{display:none;position:fixed;inset:0;background:rgba(10,10,10,.9);z-index:2500;align-items:center;justify-content:center;cursor:zoom-out}
.zoom-overlay.open{display:flex}
.zoom-overlay img{max-width:90vw;max-height:90vh;object-fit:contain}
/* === TOAST === */
.toast{position:fixed;bottom:2rem;right:2rem;background:var(--charcoal);color:var(--white);padding:1rem 1.5rem;font-size:.85rem;z-index:3000;transform:translateY(100px);opacity:0;transition:all .4s cubic-bezier(.4,0,.2,1)}
.toast.show{transform:translateY(0);opacity:1}
/* === RESPONSIVE extras === */
@media(max-width:1024px){.categories-grid{grid-template-columns:repeat(2,1fr)}.about-preview{grid-template-columns:1fr}.insta-grid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:768px){.categories-grid{grid-template-columns:1fr 1fr;gap:1rem}.product-layout{grid-template-columns:1fr}.contact-grid{grid-template-columns:1fr}.checkout-layout{grid-template-columns:1fr}.newsletter-form{flex-direction:column}.about-values{grid-template-columns:1fr}.insta-grid{grid-template-columns:repeat(3,1fr)}.hero{min-height:80vh}}
@media(max-width:480px){.categories-grid{grid-template-columns:1fr;max-width:400px;margin:0 auto}.insta-grid{grid-template-columns:repeat(2,1fr)}}
"""

patched = 0
skipped = 0

html_files = glob.glob("client/*.html") + glob.glob("admin/*.html")

for filepath in html_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Skip if already patched
    if "hero-media-placeholder" in content and "marquee-inner" in content and "category-card-bg" in content:
        print(f"  ⏭️  Already patched: {filepath}")
        skipped += 1
        continue
    
    # Find </style> and insert patch CSS before it
    if "</style>" in content:
        content = content.replace("</style>", PATCH_CSS + "\n</style>", 1)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  ✅ Patched: {filepath}")
        patched += 1
    else:
        print(f"  ⚠️  No <style> block: {filepath}")

print(f"\n{'='*50}")
print(f"✅ Patched {patched} files, skipped {skipped}")
print(f"\nNow push to GitHub:")
print(f"  git add -A")
print(f'  git commit -m "Fix: add hero, marquee, category CSS"')
print(f"  git push")
print(f"\nRailway auto-deploys in 1-2 min. Refresh your site!")
print(f"{'='*50}")
