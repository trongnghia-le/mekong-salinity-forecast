import re, sys, time, requests
H = {"User-Agent": "mekong-salinity-research/0.1"}
B = "https://kttv.gov.vn/Kttv/vi-VN/1/"
for ts, p in [("20220601", "ban-tin-du-bao-xam-nhap-man-khu-vuc-nam-bo-tu-ngay-11-20-5-2022-post26810.html"),
              ("20230601", "tin-du-bao-xam-nhap-man-tren-khu-vuc-nam-bo-tu-ngay-21-den-ngay-31-3-2023-post31331.html")]:
    time.sleep(12)
    r = requests.get(f"https://web.archive.org/web/{ts}id_/{B}{p}", headers=H, timeout=90)
    print(r.status_code, r.url[:80], len(r.text))
    print(sorted(set(re.findall(r"[^\"'\s]*(?:thuyvan|\.pdf|\.docx?|Article)[^\"'\s]*", r.text))))
