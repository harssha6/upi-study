# Bengaluru does more UPI than 31 states

A live, interactive report built from NPCI's public UPI statistics, April 2016 to October 2026.

**Live:** https://now.harssha.design/upi-study/

A UPI study from NPCI's public statistics. 712 million payments in one month from one district. UPI is 25 billion payments a month and it is lopsided: a few cities, two apps and a flood of tiny payments. Seven charts, one claim each.

1. In most states, one city does most of the paying.
2. UPI adds the same four billion payments every year.
3. Only one month in ten years went backwards: April 2020.
4. The average payment is shrinking. Shop payments are the reason.
5. Shops get many tiny payments. Finance gets a few big ones.
6. Every app, bank and state, ranked by the size of one payment.
7. PhonePe and Google Pay own 79%. The rest is growing anyway.

## Layout

```
data/        CSVs scraped from NPCI's JSON endpoints (Nov 2026)
src/page.html  the page: HTML, CSS and D3 charts, with a /*__DATA__*/ slot
src/page-v1.html  the first, table-like version, kept for comparison
build.py     embeds the CSVs into src/page.html and writes index.html
shoot.py     Playwright pass: renders every chapter, both themes, checks tooltips
assets/      photos (Unsplash) and the UPI mark
index.html   the built page
```

Rebuild after editing the template or data:

```sh
python3 build.py
python3 shoot.py 1280   # optional: screenshots into shots/
```

## Data

NPCI's site blocks plain HTTP clients, so the tables were fetched from inside a browser session against the same JSON API the site uses. Headline volume and value run to October 2026. App, merchant and state tables run to September 2026. Average ticket is value divided by volume. Merchant categories use NPCI's MCC grouping. 44% of state-wise volume is unclassified in the source.

## Credits

Photos by Rudra Gupta, Urip Dunker and rupixen on Unsplash. Type is Fraunces and Inter. Charts are D3.

## Share assets

`python3 share-assets.py` regenerates the 1200×630 card from the checked-in NPCI CSVs, using the page's Fraunces/Inter fonts, and the favicon set from the UPI arrow mark. It uses puppeteer-core (`PUPPETEER_MODULE` can point to an installed copy), Chromium (`CHROMIUM_PATH` overrides the path), and Pillow.

`python3 build.py` targets GitHub Pages. For ownnow, build with `python3 build.py --site-url https://now.harssha.design/<slug>/`, then publish only `index.html` and `assets/` to that slug. Use a separate noindex test slug for review.
