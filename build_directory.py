#!/usr/bin/env python3
"""Generate the food truck directory from data/trucks.json.

Writes:
  directory.html                     the hub, every truck, filterable
  food-trucks/<area>/index.html      one page per area, the real SEO targets
  sitemap.xml                        rebuilt so it can never drift from the pages

DO NOT HAND-EDIT ANY OF THOSE FILES. Edit data/trucks.json and re-run:
    python build_directory.py

Why per-area pages exist at all: people search "food trucks kahului", not
"maui county food truck directory". One filterable page can rank once. Seven
pages can rank seven times. The filter on the hub stays for humans; the links
are what Google can follow.
"""
import json
import html
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://mauifoodtruckwebsites.com"
TODAY = date.today().isoformat()

# Bump when assets/site.css or assets/site.js changes. Matches the other pages.
ASSET_V = "3"

PAGE_CSS = """/* Page-specific only. The shared system lives in assets/site.css. */
@layer components, responsive;

@layer components {
  main:focus{outline:none}
  .intro h1{font-size:var(--fs-xxl);max-width:13ch;line-height:1.04}
  .intro h1 em{font-style:italic;color:var(--mango)}
  .intro .mono{color:#cfc0ae;max-width:56ch;margin-top:1.4rem}

  .filters{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.9rem}
  .fbtn{
    appearance:none;background:none;border:1px solid var(--hair);color:var(--ink);
    font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:var(--fs-mono);
    letter-spacing:.16em;text-transform:uppercase;padding:.7rem 1.1rem;cursor:pointer;
    transition:background var(--dur-fast) var(--ease),color var(--dur-fast) var(--ease),border-color var(--dur-fast) var(--ease);
  }
  .fbtn:hover{border-color:var(--ink)}
  .fbtn[aria-pressed="true"]{background:var(--volcanic);border-color:var(--volcanic);color:var(--cream)}
  .count{color:var(--ash);margin-bottom:2.4rem}

  .dgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 3rem}
  .truck{padding:1.6rem 0;border-top:1px solid var(--hair)}
  .t-top{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1rem}
  .t-name{font-size:var(--fs-lg);line-height:1.15}
  .t-area{margin-left:auto;color:var(--ember)}
  .t-cuisine{display:block;color:var(--ash);margin:.35rem 0 .6rem}
  .t-desc{color:var(--quiet);margin-bottom:.7rem}
  .t-claim{display:inline-block;text-transform:none;letter-spacing:.03em;font-size:13px;text-decoration:none;color:var(--ink);border-bottom:1px solid var(--hair);padding-bottom:2px;
           transition:border-color var(--dur-fast) var(--ease),color var(--dur-fast) var(--ease)}
  .t-claim:hover{color:var(--ember);border-color:var(--ember)}

  .empty{padding:2.5rem 0;color:var(--quiet)}
  .disc{margin-top:2.6rem;padding-top:1.4rem;border-top:1px solid var(--hair);color:var(--ash);max-width:70ch}
  .disc a{color:var(--ember)}

  /* Area navigation. These links are the crawlable path the filter buttons are not. */
  .areas{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0 3rem;margin-bottom:1rem}
  .area-card{display:block;padding:1.5rem 0;border-top:1px solid var(--hair);text-decoration:none;color:inherit}
  .area-card:hover .area-name{color:var(--ember)}
  .area-name{font-size:var(--fs-lg);line-height:1.15;transition:color var(--dur-fast) var(--ease)}
  .area-meta{display:block;color:var(--ash);margin-top:.3rem}
  .area-blurb{color:var(--quiet);margin-top:.5rem;font-size:.97rem}
  /* A real breadcrumb, not a decorative eyebrow. `impeccable detect` flags a
     tracked-caps label above an oversized h1 as the default AI hero shape, and
     names "run it as a navigation breadcrumb instead" as the fix. So it is one:
     a nav, an ordered list, aria-current on the leaf, and BreadcrumbList schema. */
  .crumb{margin-bottom:1.1rem;color:#cfc0ae}
  .crumb ol{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem}
  .crumb li+li::before{content:"/";margin-right:.5rem;opacity:.55}
  /* inline-block plus padding, because a bare inline anchor's box is only the
     font's content height. Measured live 2026-08-27 at 217x18, under the WCAG 2.2
     AA 2.5.8 floor of 24x24. These are standalone nav links, not links inside a
     sentence, so 2.5.8's inline exception does not cover them. 18 + 8 = 26px.
     devices.js reported these as "sub-44 but >=24 (AAA only)", which is wrong;
     trust a measured rect over that note. */
  .crumb a{display:inline-block;padding-block:4px;color:var(--mango)}
  .elsewhere{margin-top:3rem;padding-top:1.6rem;border-top:1px solid var(--hair)}
  .elsewhere .mono{color:var(--ash);margin-bottom:.8rem}
  .elsewhere-list{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem}
  .elsewhere-list a{display:inline-block;padding-block:4px;color:var(--ink)}
}

@layer responsive {
  @media (max-width:800px), (max-height:500px) and (max-width:1100px){
    .dgrid{grid-template-columns:1fr;gap:0}
  }
}"""


def esc(s):
    return html.escape(s or "", quote=True)


def head(title, desc, canonical, depth, og_title, og_desc, extra_ld="", is_hub=False):
    """depth is how many directories deep the page sits, for relative asset paths.

    The site's convention is that the nav omits the page you are on (index.html
    drops Home, samples.html drops See real sites), so the hub drops its own link
    and shows How it works in its place."""
    up = "../" * depth
    second = (
        f'<a href="{up}index.html#how">How it works</a>'
        if is_hub
        else f'<a href="{up}directory.html">Truck directory</a>'
    )
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(og_title)}">
<meta property="og:description" content="{esc(og_desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(og_title)}">
<meta name="twitter:description" content="{esc(og_desc)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#241f1b">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" sizes="32x32" href="{up}favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{up}apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=Instrument+Serif:ital@0;1&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css?v={ASSET_V}">
<style>
{PAGE_CSS}
</style>
{extra_ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head stuck" id="head">
  <a class="brand" href="{up}index.html">Maui Food Truck Websites</a>
  <button class="navbtn mono" id="navBtn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="site-nav mono" id="nav" aria-label="Primary">
    <a href="{up}index.html">Home</a>
    {second}
    <a href="{up}samples.html">See real sites</a>
    <a class="go" href="{up}intake.html">Get your free sample</a>
  </nav>
</header>

<main id="main" tabindex="-1">
"""


def tail(depth):
    up = "../" * depth
    return f"""</main>

<footer class="dark site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="brand">Maui Food Truck Websites</p>
        <p class="blurb">Websites for Maui County food trucks that show people you are open and where. Built on island.</p>
      </div>
      <div>
        <p class="mono foot-h">Explore</p>
        <nav class="mono" aria-label="Explore">
          <a href="{up}index.html">Home</a>
          <a href="{up}directory.html">Truck directory</a>
          <a href="{up}samples.html">Our work</a>
        </nav>
      </div>
      <div>
        <p class="mono foot-h">Get started</p>
        <nav class="mono" aria-label="Get started">
          <a href="{up}intake.html">Free sample</a>
          <a href="mailto:FrontlineWebDesigns@gmail.com">Email us a question</a>
        </nav>
      </div>
    </div>
    <p class="foot-mark" aria-hidden="true">Maui Food Truck</p>
    <div class="mono foot-bot">
      <span>&copy; 2026 Maui Food Truck Websites &middot; Maui, Hawai&#699;i</span>
      <span>Built by <a href="https://frontlinewebdesign.tech" rel="noopener nofollow">Frontline Web Designs</a></span>
    </div>
  </div>
</footer>

<aside class="callbar" aria-label="Get started">
  <a class="cta" href="{up}intake.html">Get your free sample</a>
</aside>

<script src="{up}assets/site.js?v={ASSET_V}" defer></script>
"""


def truck_card(t, area_lookup, depth, show_area=True):
    up = "../" * depth
    name = esc(t["name"])
    bits = [f'<div class="t-top"><span class="t-name">{name}</span>']
    if show_area:
        labels = " &middot; ".join(area_lookup[a]["name"] for a in t["areas"])
        bits.append(f'<span class="mono t-area">{labels}</span>')
    bits.append("</div>")
    if t.get("cuisine"):
        bits.append(f'<span class="mono t-cuisine">{esc(t["cuisine"])}</span>')
    if t.get("desc"):
        bits.append(f'<p class="t-desc">{esc(t["desc"])}</p>')
    bits.append(
        f'<a href="{up}intake.html" class="mono t-claim" '
        f'aria-label="Claim the {name} listing and get a free sample site">Is this your truck? Claim it</a>'
    )
    areas_attr = " ".join(t["areas"])
    return f'<article class="truck" data-area="{areas_attr}">' + "".join(bits) + "</article>"


def itemlist_ld(trucks, name, url):
    """ItemList is the honest schema here. We are listing OTHER people's businesses,
    so we describe the LIST, and never emit LocalBusiness or reviews we do not own."""
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": t["name"],
        }
        for i, t in enumerate(trucks)
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "url": url,
        "numberOfItems": len(trucks),
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "itemListElement": items,
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def breadcrumb_ld(area_name, url):
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Maui food truck directory",
             "item": f"{SITE}/directory.html"},
            {"@type": "ListItem", "position": 2, "name": area_name, "item": url},
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def build():
    with open(os.path.join(ROOT, "data", "trucks.json"), encoding="utf-8") as f:
        data = json.load(f)
    areas = data["areas"]
    trucks = data["trucks"]
    lookup = {a["slug"]: a for a in areas}

    known = set(lookup)
    for t in trucks:
        bad = set(t["areas"]) - known
        if bad:
            raise SystemExit(f"ERROR: {t['name']} names unknown area(s): {sorted(bad)}")
        if not t.get("source"):
            raise SystemExit(f"ERROR: {t['name']} has no source. Every truck must be sourced.")

    by_area = {a["slug"]: [t for t in trucks if a["slug"] in t["areas"]] for a in areas}
    written = []

    # ---------- the hub ----------
    cards = "\n        ".join(truck_card(t, lookup, 0) for t in trucks)
    area_cards = "\n        ".join(
        f'<a class="area-card" href="food-trucks/{a["slug"]}/">'
        f'<span class="area-name">{esc(a["name"])}</span>'
        f'<span class="mono area-meta">{esc(a["region"])} &middot; {len(by_area[a["slug"]])} trucks</span>'
        f'</a>'
        for a in areas
    )
    filter_btns = "\n        ".join(
        f'<button type="button" class="fbtn" data-area="{a["slug"]}" aria-pressed="false">{esc(a["name"])}</button>'
        for a in areas
    )
    hub_url = f"{SITE}/directory.html"
    hub = head(
        "Maui County Food Truck Directory | Maui Food Trucks",
        f"A free directory of {len(trucks)} Maui County food trucks by area and cuisine, from Kahului to Hana. Own a truck? Claim your listing and get a free website sample.",
        hub_url,
        0,
        "Maui County food truck directory",
        f"A free community guide to {len(trucks)} Maui County food trucks, by area. Own one? Claim your listing.",
        itemlist_ld(trucks, "Maui County food trucks", hub_url),
        is_hub=True,
    )
    hub += f"""
  <section class="dark intro below-head">
    <div class="wrap">
      <h1>Maui County <em>food trucks.</em></h1>
      <p class="mono plain">A free community directory of {len(trucks)} trucks across {len(areas)} areas of Maui County. Own one of these? Claim your listing and let us build you a free website sample.</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2 class="mono">Browse by area</h2>
      <div class="areas">
        {area_cards}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2 class="mono">Every truck</h2>
      <div class="filters" role="group" aria-label="Filter by area">
        <button type="button" class="fbtn" data-area="all" aria-pressed="true">All</button>
        {filter_btns}
      </div>
      <p class="mono count" id="count" role="status"></p>

      <div class="dgrid" id="grid">
        {cards}
      </div>
      <p class="empty" id="empty" hidden>No trucks listed in that area yet.</p>

      <p class="disc mono plain">This directory is free and community-run. We are a web design company, not a review site, so nothing here is paid placement. Spotted a truck that has closed, moved or is missing? <a href="mailto:FrontlineWebDesigns@gmail.com">Tell us</a> and we will fix it.</p>
    </div>
  </section>
"""
    hub += tail(0)
    hub += """<script>
(function(){
  "use strict";
  var trucks = [].slice.call(document.querySelectorAll(".truck")),
      btns   = [].slice.call(document.querySelectorAll(".fbtn")),
      empty  = document.getElementById("empty"),
      count  = document.getElementById("count");

  /* A truck can work more than one area, so data-area holds a SPACE-SEPARATED
     list and this must test membership, never equality. */
  function inArea(t, area){
    return area === "all" || (" " + t.dataset.area + " ").indexOf(" " + area + " ") > -1;
  }

  function apply(area, label){
    var n = 0;
    trucks.forEach(function(t){
      var show = inArea(t, area);
      t.hidden = !show;
      if (show) n++;
    });
    empty.hidden = n > 0;
    /* Counted from the DOM, never hard-coded, so it cannot drift from the list. */
    count.textContent = n === 0 ? "" : (area === "all" ? "Showing all " + n + " trucks" : "Showing " + n + " in " + label);
  }

  btns.forEach(function(b){
    b.addEventListener("click", function(){
      btns.forEach(function(x){ x.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      apply(b.dataset.area, b.textContent);
    });
  });

  apply("all", "All");
})();
</script>
</body>
</html>
"""
    with open(os.path.join(ROOT, "directory.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(hub)
    written.append(("directory.html", len(trucks)))

    # ---------- one page per area ----------
    for a in areas:
        mine = by_area[a["slug"]]
        url = f"{SITE}/food-trucks/{a['slug']}/"
        title = f"{a['name']} Food Trucks | Maui Food Truck Websites"
        desc = (
            f"{len(mine)} food trucks in {a['name']}, Maui, and what each one serves. "
            f"Free community directory. Own one? Claim your listing."
        )
        page = head(
            title,
            desc,
            url,
            2,
            f"{a['name']} food trucks",
            f"{len(mine)} food trucks in {a['name']}, Maui, and what each one serves.",
            itemlist_ld(mine, f"Food trucks in {a['name']}, Maui", url) + breadcrumb_ld(a["name"], url),
        )
        others = "\n        ".join(
            f'<a href="../{o["slug"]}/">{esc(o["name"])} ({len(by_area[o["slug"]])})</a>'
            for o in areas
            if o["slug"] != a["slug"]
        )
        cards = "\n        ".join(truck_card(t, lookup, 2, show_area=False) for t in mine)
        page += f"""
  <section class="dark intro below-head">
    <div class="wrap">
      <nav class="mono plain crumb" aria-label="Breadcrumb">
        <ol>
          <li><a href="../../directory.html">Maui food truck directory</a></li>
          <li aria-current="page">{esc(a['name'])}</li>
        </ol>
      </nav>
      <h1>{esc(a['name'])} <em>food trucks.</em></h1>
      <p class="mono plain">{esc(a['blurb'])}</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <p class="mono count">{len(mine)} trucks listed in {esc(a['name'])}</p>
      <div class="dgrid">
        {cards}
      </div>

      <div class="elsewhere">
        <p class="mono">Food trucks elsewhere on Maui</p>
        <nav class="mono elsewhere-list" aria-label="Other areas">
        {others}
        </nav>
      </div>

      <p class="disc mono plain">This directory is free and community-run. We are a web design company, not a review site, so nothing here is paid placement. Spotted a truck that has closed, moved or is missing? <a href="mailto:FrontlineWebDesigns@gmail.com">Tell us</a> and we will fix it.</p>
    </div>
  </section>

  <section class="close">
    <div class="wrap wrap-narrow">
      <h2>Own a truck in <em>{esc(a['name'])}</em>?</h2>
      <p>We build websites for Maui food trucks that show people you are open and where you are parked. Tell us three things and we will build you a free sample. No cost, no card.</p>
      <a class="cta" href="../../intake.html">Get your free sample</a>
    </div>
  </section>
"""
        page += tail(2)
        page += "</body>\n</html>\n"
        out_dir = os.path.join(ROOT, "food-trucks", a["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
        written.append((f"food-trucks/{a['slug']}/index.html", len(mine)))

    # ---------- sitemap, rebuilt so it cannot drift ----------
    urls = [(f"{SITE}/", "1.0"), (f"{SITE}/samples.html", "0.8"), (f"{SITE}/directory.html", "0.8")]
    urls += [(f"{SITE}/food-trucks/{a['slug']}/", "0.7") for a in areas]
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, p in urls
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap)

    for path, n in written:
        print(f"  wrote {path:38s} {n} trucks")
    print(f"  wrote {'sitemap.xml':38s} {len(urls)} urls")
    print(f"\n{len(trucks)} trucks across {len(areas)} areas.")


def selftest():
    """Prove the two things that would silently ship wrong: the multi-area filter
    predicate, and that no generated page claims a truck it does not list."""
    import glob

    ok = True

    # 1. The JS membership test, mirrored in Python. A naive equality test must FAIL here.
    def in_area(attr, area):
        return area == "all" or (" " + attr + " ").find(" " + area + " ") > -1

    assert in_area("kahului kihei", "kihei"), "membership test broken"
    assert in_area("kahului kihei", "kahului"), "membership test broken"
    assert not in_area("kahului kihei", "hana"), "membership test too loose"
    assert not in_area("north-shore", "shore"), "must not match a partial slug"
    assert ("kahului kihei" == "kihei") is False, "control: equality would have dropped this truck"
    print("  pass  multi-area filter predicate (and equality would have failed it)")

    # 2. Every area page's stated count must equal the cards it actually renders.
    with open(os.path.join(ROOT, "data", "trucks.json"), encoding="utf-8") as f:
        data = json.load(f)
    for a in data["areas"]:
        p = os.path.join(ROOT, "food-trucks", a["slug"], "index.html")
        if not os.path.exists(p):
            print(f"  FAIL  {a['slug']}: page not generated")
            ok = False
            continue
        s = open(p, encoding="utf-8").read()
        rendered = s.count('<article class="truck"')
        claimed = int(re.search(r'(\d+) trucks listed in', s).group(1))
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
        if rendered == claimed == ld["numberOfItems"] == len(ld["itemListElement"]):
            print(f"  pass  {a['slug']:12s} {rendered} cards = stated count = schema count")
        else:
            print(f"  FAIL  {a['slug']}: {rendered} cards, says {claimed}, schema {ld['numberOfItems']}")
            ok = False

    # 3. CONTROL: a deliberately wrong count must be caught by the check above.
    probe = "<article class=\"truck\"></article> 99 trucks listed in Nowhere"
    assert probe.count('<article class="truck"') != int(re.search(r'(\d+) trucks listed in', probe).group(1)), \
        "control failed: the count check cannot detect a mismatch"
    print("  pass  CONTROL, a wrong count is detectable")

    # 4. No em dash or en dash anywhere in the generated HTML.
    for p in [os.path.join(ROOT, "directory.html")] + glob.glob(os.path.join(ROOT, "food-trucks", "*", "index.html")):
        s = open(p, encoding="utf-8").read()
        n = s.count(chr(8212)) + s.count(chr(8211))
        if n:
            print(f"  FAIL  {os.path.basename(os.path.dirname(p))}: {n} em/en dash(es)")
            ok = False
    print("  pass  no em or en dashes in generated HTML")

    print("\nALL SELFTESTS PASS" if ok else "\nSELFTESTS FAILED")
    return 0 if ok else 2


if __name__ == "__main__":
    import sys

    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    build()
