"""Wayback enumeration + download for NCHMF salinity bulletins.
python wayback_nchmf.py cdx       -> data/raw/wayback/cdx_*.txt (one query at a time, >=10 s apart, backoff 60 s/300 s)
python wayback_nchmf.py download  -> fetch missing bulletin PDFs into data/raw/nchmf/pdf, rewrite inventory.csv"""
import csv, datetime as dt, os, re, sys, time
import requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
WB, PDF, INV = os.path.join(B, "wayback"), os.path.join(B, "nchmf", "pdf"), os.path.join(B, "nchmf", "inventory.csv")
CDX = "https://web.archive.org/cdx/search/cdx"
FL = "timestamp,original,statuscode,mimetype,length"
LINE = re.compile(r"^\d{14} ")

def cdx(url, out, extra=None):
    if os.path.exists(out) and LINE.match(open(out, encoding="utf8").readline() or "x") or os.path.exists(out + ".empty"):
        return
    p = {"url": url, "matchType": "prefix", "output": "txt", "fl": FL}
    p.update(extra or {})
    for wait in (0, 60, 300, None):
        if wait is None: print("GIVE UP", url); return
        time.sleep(wait)
        try:
            r = requests.get(CDX, params=p, headers=H, timeout=120)
        except requests.RequestException as e:
            print("ERR", url, e); continue
        t = r.text
        if r.status_code == 200 and (not t.strip() or all(LINE.match(l) for l in t.splitlines())):
            if t.strip(): open(out, "w", encoding="utf8").write(t)
            else: open(out + ".empty", "w").write("")
            print("ok", url, len(t.splitlines()), flush=True); time.sleep(12); return
        print("BACKOFF", r.status_code, url, t[:60].replace("\n", " "), flush=True)

def do_cdx():
    os.makedirs(WB, exist_ok=True)
    for f in ("thuyvan1", "thuyvan2"):
        for y in range(2016, 2027):
            cdx(f"kttv.gov.vn/upload/{f}/{y}/", os.path.join(WB, f"cdx_{f}_{y}.txt"))
    cdx("kttv.gov.vn/kttv/vi-VN/1/xam-nhap-man", os.path.join(WB, "cdx_listing_kttv.txt"))
    cdx("nchmf.gov.vn/", os.path.join(WB, "cdx_nchmf_man.txt"),
        {"filter": "original:.*(xman|xam-nhap|mannhap|man).*", "limit": "500"})

def do_cdx2():
    """older domain thoitietvietnam.gov.vn (bulletins pre-2024 use dbqg_xmnb / dbqg_xmtb names)"""
    os.makedirs(WB, exist_ok=True)
    for f in ("thuyvan2", "thuyvan1"):
        cdx(f"thoitietvietnam.gov.vn/upload/{f}/", os.path.join(WB, f"cdx_tt_{f}.txt"),
            {"filter": "original:.*\.pdf"})

def season(d):
    y = d.year if d.month >= 7 else d.year - 1
    return f"{y}-{str(y+1)[2:]}"

def do_download():
    import glob, calendar
    best = {}  # issue date -> (rank, ts, original)
    for fn in glob.glob(os.path.join(WB, "cdx_*thuyvan*.txt")):
        for l in open(fn, encoding="utf8"):
            p = l.split()
            if len(p) < 4: continue
            ts, orig, sc, mt = p[:4]
            m = re.search(r"dbqg_xm(?:an|nb|tb)_(\d{8})_(\d{4})(?:-\d)?\.pdf", orig)
            if not m: continue
            d = dt.datetime.strptime(m.group(1), "%Y%m%d").date()
            rank = (sc == "200", mt == "application/pdf", ts)
            if d not in best or rank > best[d][0]: best[d] = (rank, ts, orig)
    rows = {}
    for r in csv.DictReader(open(INV, encoding="utf8")):
        r.setdefault("source", "live" if r["status"] == "found" else ""); r.setdefault("wayback_ts", "")
        rows[r["issue_date"]] = r
    have = {os.path.basename(x) for x in glob.glob(os.path.join(PDF, "*.pdf"))}
    for d, (rank, ts, orig) in sorted(best.items()):
        name = orig.rsplit("/", 1)[1]
        if rows.get(str(d), {}).get("status") == "found" and rows[str(d)].get("source") == "live": continue
        if name not in have:
            r = None
            for wait in (4, 120, 300, 600):  # Wayback refuses connections when throttled
                time.sleep(wait)
                try: r = requests.get(f"https://web.archive.org/web/{ts}id_/{orig}", headers=H, timeout=90); break
                except requests.RequestException as e: print("BACKOFF", name, type(e).__name__, flush=True)
            if r is None: print("GIVE UP", name); continue
            if not r.content.startswith(b"%PDF"): print("notpdf", name, r.status_code); continue
            open(os.path.join(PDF, name), "wb").write(r.content)
        n = os.path.getsize(os.path.join(PDF, name))
        rows[str(d)] = dict(issue_date=str(d), season=season(d), url=f"https://web.archive.org/web/{ts}id_/{orig}",
                            status="found", bytes=n, source="wayback", wayback_ts=ts)
        print("got", name, n, flush=True)
    cols = ["issue_date", "season", "url", "status", "bytes", "source", "wayback_ts"]
    with open(INV, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
        for k in sorted(rows): w.writerow(rows[k])

if __name__ == "__main__":
    {"cdx": do_cdx, "cdx2": do_cdx2, "download": do_download}[sys.argv[1]]()
