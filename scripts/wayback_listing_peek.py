import re, sys, time, requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
for ts, u in [("20221207062830","https://kttv.gov.vn/Kttv/vi-VN/1/xam-nhap-man-20-18.html"),
              ("20231004230120","https://kttv.gov.vn/Kttv/vi-VN/1/xam-nhap-man-20-18.html"),
              ("20240303221746","https://kttv.gov.vn/Kttv/vi-VN/1/xam-nhap-man-20-18.html")]:
    time.sleep(12)
    r = requests.get(f"https://web.archive.org/web/{ts}id_/{u}", headers=H, timeout=90)
    t = r.text
    print("==", ts, r.status_code, len(t))
    for m in re.finditer(r'href="([^"]*post\d+\.html)">([^<]*)<span[^>]*>\s*\(\s*([^)]*)\)', t):
        print(m.group(1), "|", m.group(2).strip(), "|", m.group(3))
    print(set(re.findall(r"/upload/[^\"' ]*\.(?:pdf|jpg)", t)))
    print(re.findall(r"_totalrecord = '(\d+)'", t))
