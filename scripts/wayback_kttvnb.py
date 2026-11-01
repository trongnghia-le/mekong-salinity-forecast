"""Wayback-only enumeration of kttv-nb.org.vn han-man posts. Never contacts kttv-nb.org.vn.
python -I wayback_kttvnb.py cdx    -> data/raw/kttvnb/cdx/*.txt
"""
import os, re, sys, time, requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "kttvnb")
CDX = "https://web.archive.org/cdx/search/cdx"
FL = "timestamp,original,statuscode,mimetype,length"
LINE = re.compile(r"^\d{14} ")
last = [0.0]

def get(url, params=None, **kw):
    """polite GET to web.archive.org only; backoff 60/300 s on outage page"""
    assert url.startswith("https://web.archive.org/")
    for wait in (0, 60, 300, 600):
        time.sleep(max(wait, 12 - (time.time() - last[0])))
        try:
            r = requests.get(url, params=params, headers=H, timeout=120, **kw)
        except requests.RequestException as e:
            print("ERR", str(e)[:80], flush=True); last[0] = time.time(); continue
        last[0] = time.time()
        if r.status_code in (200, 404) and not (r.content[:5].lower() == b"<html" and b"Temporarily Offline" in r.content[:3000]):
            return r
        print("BACKOFF", r.status_code, wait, flush=True)
    return None

def cdx(url, name, extra=None):
    out = os.path.join(D, "cdx", name)
    if os.path.exists(out): return open(out, encoding="utf8").read()
    p = {"url": url, "matchType": "prefix", "output": "txt", "fl": FL, "collapse": "urlkey"}
    p.update(extra or {})
    r = get(CDX, p)
    if r is None: print("GIVE UP", url); return None
    t = r.text
    if t.strip() and not all(LINE.match(l) for l in t.splitlines()):
        print("BAD", url, t[:80]); return None
    open(out, "w", encoding="utf8").write(t)
    print("ok", url, len(t.splitlines()), flush=True)
    return t

if __name__ == "__main__" and sys.argv[1] == "cdx":
    os.makedirs(os.path.join(D, "cdx"), exist_ok=True)
    cdx("www.kttv-nb.org.vn/index.php/thong-tin-kttv/han-man", "han_man_www.txt")  # positive control
    cdx("kttv-nb.org.vn/index.php/thong-tin-kttv/han-man", "han_man_nowww.txt")
    cdx("www.kttv-nb.org.vn/images/", "images_www.txt")
    cdx("kttv-nb.org.vn/images/", "images_nowww.txt")
