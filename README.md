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
7. Quote — Web3Forms quick lead form. Primary CTAs route to the multi-step intake (`intake.html`).
8. Footer — Frontline sub-brand + cross-link.

## ⚠ Confirm BEFORE launch
- **Directory** — deep-dived & verified against public sources (Yelp / Maui guides, 2026). Give it a
  final local eyeball before publishing real businesses. Framed as a free community directory with a
  claim / update / remove path.
- **Domain + host** — register `mauifoodtruckwebsites.com`, set up Hostinger, point DNS, then flip the
  page off `noindex`. (A temporary `*.hostingersite.com` subdomain is fine for review.)

## Done / wired
- **Pricing** — real packages: Single Page **$249**, Full Site **$449**, Pro **$699**, plus optional
  Monthly Maintenance **$49/mo** (3-month minimum).
- **Intake form** (`intake.html`) — multi-step React brief; the primary CTAs route here. On submit it
  emails the completed brief to FrontlineWebDesigns@gmail.com via Web3Forms (live key).
- **Quick quote form** (`#quote`) — Web3Forms, same inbox (live).
- **Brand assets** — favicon set, `og-image.png` social card, `ProfessionalService` schema.org JSON-LD.

## Roadmap (post-v1)
- Per-truck listing pages + dedicated `/directory`.
- Optional blog/guide engine for long-tail SEO.
- "Claim your listing" → upgrade funnel automation.
