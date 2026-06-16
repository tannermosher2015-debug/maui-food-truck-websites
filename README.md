# Maui Food Truck Websites — by Frontline Web Designs

A niche **lead-generation property** that sells websites to Maui County food-truck **owners**.
The homepage is a complete, gorgeous **"demo-as-pitch"** food-truck site for a fictional truck
(**Pā'ina Maui**) — it answers every question a food truck's customers have (where, hours, menu,
photos, story, ordering, catering, social) and is framed throughout as *"this is a free sample
we built — get one for your truck."* Every conversion CTA → the intake form.

- **Live:** `mauifoodtruckwebsites.com` — **soft launch, `noindex`** until the full public launch.
- **Deploy:** GitHub `tannermosher2015-debug/maui-food-truck-websites` is connected to **Hostinger
  Git**, so **a push to `main` auto-deploys** to `public_html`. *(Push = publish.)*
- **Stack:** lightweight static HTML/CSS/JS, no build step.

## Design system (Laurel-inspired)
- **Palette:** warm ivory `#F7F1E4` · forest green `#2E3A2B` · gold `#B98A3C` · espresso `#2A211A` (WCAG-AA).
- **Type:** Playfair Display (display serif) · Karla (body/UI) · Ephesis (script accents).
- **Icons:** inline SVG (no emoji). Appetizing photography (Unsplash; real client builds swap their own).

## Pages
- **`index.html`** — the Pā'ina Maui demo-as-pitch homepage: sticky "free sample" bar, hero,
  find-us + Google map, menu w/ prices, today's special + review, gallery, owner story,
  order/catering, and the closing pitch (*"that's the free sample"*) with the $249 / $449 / $699
  packages (+ $49/mo maintenance).
- **`directory.html`** — free community directory of ~14 real Maui County food trucks (area filter,
  "claim your listing" → intake).
- **`intake.html`** — multi-step React brief (recolored to match). On submit it emails the brief to
  FrontlineWebDesigns@gmail.com via Web3Forms (live key). Primary CTAs route here.

## Going fully public (later)
Flip `index.html` + `directory.html` off `noindex`, add `robots.txt` + `sitemap.xml`, then push.

## Notes
- "Pā'ina Maui" is a **fictional sample** — labeled as such in the sample bar and footer.
- Directory listings are public-info; a final local verify before wide promotion is wise.
