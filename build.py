#!/usr/bin/env python3
"""Embed the CSVs in data/ into src/page.html and write index.html."""
import argparse, csv, json, pathlib
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--site-url", default="https://harssha6.github.io/upi-study/")
args = parser.parse_args()
site_url = args.site_url.rstrip("/") + "/"
if urlparse(site_url).scheme not in {"http", "https"} or not urlparse(site_url).netloc:
    parser.error("--site-url must be an absolute HTTP(S) URL")

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"


def num(s):
    s = (s or "").strip().replace(",", "").rstrip("%")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return s


def load(name, numeric):
    rows = []
    with open(DATA / name, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out = {}
            for k, v in r.items():
                out[k] = num(v) if k in numeric else v.strip()
            rows.append(out)
    return rows


data = {
    "monthly": load("upi_monthly.csv", {"banks_live", "volume_mn", "value_cr"}),
    "p2p": load("upi_p2p_p2m_monthly.csv", {"total_vol_mn", "total_val_cr", "p2p_vol_mn", "p2p_val_cr", "p2m_vol_mn", "p2m_val_cr"}),
    "apps": load("upi_apps_top8_monthly.csv", {"rank", "volume_mn", "value_cr", "month_total_vol_mn", "apps_count"}),
    "states": load("upi_states_sep2026.csv", {"districts", "volume_mn", "value_cr"}),
    "districts": load("upi_top_districts_sep2026.csv", {"volume_mn", "vol_share", "value_cr", "val_share"}),
    "banks": load("upi_top50_banks_sep2026.csv", {"rank", "volume_mn", "value_cr"}),
    "mcc": load("upi_mcc_sep2026.csv", {"volume_mn", "value_cr"}),
}

template = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
assert "/*__DATA__*/" in template
html = template.replace("/*__DATA__*/", json.dumps(data, separators=(",", ":"))).replace("__SITE_URL__", site_url)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html), "bytes;", {k: len(v) for k, v in data.items()})
