import re, sys, time, requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
for u in sys.argv[1:]:
    time.sleep(12)
    r = requests.get(f"https://web.archive.org/web/2id_/{u}", headers=H, timeout=90)
    print("==", u[-50:], r.status_code, len(r.text), r.url[:70])
    t = r.text
    print(sorted(set(re.findall(r"[^\"'\s(]*(?:upload|Upload|\.pdf|\.doc|\.jpg|\.png)[^\"'\s)]*", t)))[:25])
