"""Probe NCHMF salinity bulletin PDFs. Usage: python probe_nchmf.py [YYYY-MM-DD]  (optional: try variants for dates >= this)
Phase 1: listing crawl (post links -> pdf links). Phase 2: canonical URL probe.
'variants' mode: for dates still missing, try other dirs/hours/offsets (slow)."""
import csv, calendar, datetime as dt, os, re, sys, time
import requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "nchmf")
PDF = os.path.join(ROOT, "pdf")
LIST = "https://kttv.gov.vn/kttv/vi-VN/1/xam-nhap-man-20-18.html"
S = requests.Session(); S.headers.update(H)
_last = [0.0]

def req(method, url, **kw):
    for a in range(2):
        time.sleep(max(0, 0.7 - (time.time() - _last[0])))
        _last[0] = time.time()
        try:
            return S.request(method, url, timeout=25, **kw)  # TLS verify stays on
        except requests.RequestException as e:
            err = e
    print("ERR", url, err); return None

def check(url):
    """-> (status, bytes); status 'found' only if real PDF."""
    r = req("GET", url, stream=True)
    if r is None: return "error", 0
    try:
        if r.status_code != 200: return str(r.status_code), 0
        head = next(r.iter_content(8), b"")
        if not head.startswith(b"%PDF"): return "notpdf", 0
        return "found", int(r.headers.get("content-length") or 0)
    finally:
        r.close()

def season(d):
    y = d.year if d.month >= 7 else d.year - 1
    return f"{y}-{str(y+1)[2:]}"

def url_for(d, folder="thuyvan2", dirdate=None, hh="1500"):
    dd = dirdate or d
    return f"https://kttv.gov.vn/upload/{folder}/{dd.year}/{dd.month}/{dd.day}/dbqg_xman_{d:%Y%m%d}_{hh}.pdf"

def canon_dates(y0=2016, y1=2026):
    for y in range(y0, y1 + 1):
        for m in (12, 1, 2, 3, 4, 5, 6):
            yy = y if m == 12 else y + 1
            if yy > y1 or (m != 12 and yy - 1 < y0): continue
            for day in (10, 20, calendar.monthrange(yy, m)[1]):
                yield dt.date(yy, m, day)

def listing():
    out = []
    for p in range(1, 4):
        r = req("GET", LIST + f"?pageindex={p}")
        if r is None or r.status_code != 200: break
        posts = set(re.findall(r'https://kttv\.gov\.vn/kttv/vi-VN/1/[^"]*-post\d+\.html', r.text))
        for u in sorted(posts):
            rp = req("GET", u)
            if rp is None: continue
            for m in re.findall(r'/upload/thuyvan\d/\d+/\d+/\d+/[^"\' ]*\.pdf', rp.text):
                out.append("https://kttv.gov.vn" + m)
        print("listing page", p, len(posts), "posts")
    return sorted(set(out))

def main():
    rows = {}
    for u in listing():
        m = re.search(r"_(\d{8})_", u)
        d = dt.datetime.strptime(m.group(1), "%Y%m%d").date() if m else None
        rows[u] = (d, *check(u))
    done = {r[0] for r in rows.values() if r[0]}
    vfrom = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    for d in canon_dates():
        if d in done: continue
        cands = [url_for(d, f) for f in ("thuyvan2", "thuyvan1")]
        if vfrom and d >= vfrom:
            for off in (-2, -1, 1, 2):
                cands += [url_for(d, f, d + dt.timedelta(off)) for f in ("thuyvan2", "thuyvan1")]
            for hh in ("0900", "1000", "1530", "1600", "1400", "1700"):
                cands += [url_for(d, f, hh=hh) for f in ("thuyvan2", "thuyvan1")]
        best = None
        for u in cands:
            st, n = check(u)
            if st == "found": best = (u, st, n); break
            best = best or (cands[0], st, n)
        rows[best[0]] = (d, best[1], best[2])
        print(d, best[1], best[0], flush=True)
    os.makedirs(PDF, exist_ok=True)
    with open(os.path.join(ROOT, "inventory.csv"), "w", newline="", encoding="utf8") as f:
        w = csv.writer(f); w.writerow(["issue_date", "season", "url", "status", "bytes"])
        for u, (d, st, n) in sorted(rows.items(), key=lambda kv: (kv[1][0] or dt.date(1900, 1, 1))):
            w.writerow([d, season(d) if d else "", u, st, n])
            if st == "found":
                fp = os.path.join(PDF, u.rsplit("/", 1)[1])
                if not os.path.exists(fp):
                    r = req("GET", u)
                    if r is not None and r.content.startswith(b"%PDF"):
                        open(fp, "wb").write(r.content)

if __name__ == "__main__":
    main()
