# Maui Food Truck Websites — by Frontline Web Designs

A **niche lead-generation property**: a single-page static site that sells websites to
Maui County food-truck **owners**. A free, real **food-truck directory** is the SEO draw and
top of the funnel; the conversion goal is owners requesting a site.

- **Owner / type:** Frontline-owned real niche property (sub-brand of Frontline Web Designs).
- **Stack:** lightweight static HTML/CSS/JS, single `index.html` (Frontline default).
- **Domain (target):** `mauifoodtruckwebsites.com` (not yet registered/wired).
- **Deploy:** none yet — **push ≠ live** until a host + DNS are set up. Build + verify locally first.
- **Accessibility:** WCAG 2.1 AA — skip link, landmarks, `:focus-visible`, labeled controls,
  `aria-live` on the directory filter and quote form, reduced-motion.

## Page structure (`index.html`)
1. Hero — "Websites built for Maui food trucks" + quote / demo CTAs.
2. Why — social media isn't a website (3 problem cards).
3. What You Get — feature grid mirroring the demo build.
4. Live Demo — the Fuego & Flame sample as "the site we'll build you".
5. Pricing — 3 tiers (**placeholder prices**, clearly marked).
6. Directory — filterable grid of **real** Maui trucks (area filter) + "claim your listing".
7. Quote — Web3Forms lead form (demo fallback until a real key is set).
8. Footer — Frontline sub-brand + cross-link.

## ⚠ Placeholders to confirm BEFORE launch (do not publish as-is)
- **Pricing** — all three tiers show `$—`. Replace with real package prices.
- **Web3Forms key** — `index.html` has `REPLACE_WITH_WEB3FORMS_KEY`; form runs in demo mode until set.
- **Directory data** — `assets`/inline truck list is a researched starter set from public info.
  Verify each truck (name, cuisine, area) and the free-directory disclaimer before going live.
- **Domain + host** — register `mauifoodtruckwebsites.com`, set up hosting (Hostinger like the main
  site), then point DNS. The site is `noindex` until launch-ready.

## Roadmap (post-v1)
- Per-truck listing pages + dedicated `/directory`.
- Optional blog/guide engine for long-tail SEO.
- "Claim your listing" → upgrade funnel automation.
