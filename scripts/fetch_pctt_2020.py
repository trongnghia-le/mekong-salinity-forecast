"""Fetch PCTT daily reports 01/02-31/05/2020 -> data/raw/pctt/. Saves HTML (and the .doc/.docx attachment when the
salinity table is not in the HTML). Misses recorded in data/raw/pctt/misses.txt. Re-runnable (skips files present)."""
import datetime as dt, os, re, time, urllib.parse
import requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "pctt")
BASE = "https://phongchongthientai.mard.gov.vn"
S = requests.Session(); S.headers.update(H)
_last = [0.0]

def get(url):
    for a in range(2):
        time.sleep(max(0, 1.1 - (time.time() - _last[0]))); _last[0] = time.time()
        try:
            return S.get(url, timeout=30)  # TLS verify stays on
        except requests.RequestException as e:
            err = e
    print("ERR", url, err); return None

def slugs(d):
    out = []
    for s in (f"{d.day}-{d.month}-{d.year}", f"{d.day:02d}-{d.month:02d}-{d.year}",
              f"{d.day}-{d.month:02d}-{d.year}", f"{d.day:02d}-{d.month}-{d.year}"):
        if s not in out: out.append(s)
    return out

os.makedirs(OUT, exist_ok=True)
misses = []
d = dt.date(2020, 2, 1)
while d <= dt.date(2020, 5, 31):
    tag = d.isoformat(); hp = os.path.join(OUT, f"{tag}.html")
    if not os.path.exists(hp):
        for s in slugs(d):
            r = get(f"{BASE}/Pages/bao-cao-nhanh-cong-tac-truc-ban-pctt-ngay-{s}.aspx")
            if r is not None and r.status_code == 200 and len(r.content) > 5000:
                open(hp, "wb").write(r.content); break
        else:
            misses.append(tag); d += dt.timedelta(days=1); continue
    t = open(hp, encoding="utf-8", errors="replace").read()
    if "Trạm đo mặn" not in t:
        for link in re.findall(r'/FileUpload/[^"\']+\.docx?', t, flags=re.I)[:1]:
            ext = link.rsplit(".", 1)[1].lower(); ap = os.path.join(OUT, f"{tag}.{ext}")
            if not os.path.exists(ap):
                r = get(BASE + urllib.parse.quote(urllib.parse.unquote(link), safe="/%"))
                if r is not None and r.status_code == 200: open(ap, "wb").write(r.content)
    d += dt.timedelta(days=1)
open(os.path.join(OUT, "misses.txt"), "w").write("\n".join(misses))
print("misses", len(misses))
