import requests,re,sys
h={"User-Agent":"mekong-salinity-research/0.1"}
u=sys.argv[1]
r=requests.get(u,headers=h,timeout=30)
print(r.status_code,len(r.text))
t=r.text
open(sys.argv[2],"w",encoding="utf8").write(t)
for m in sorted(set(re.findall(r'href="([^"]+)"',t))):
    if 'xman' in m or 'upload' in m or 'xam-nhap' in m or 'page' in m.lower(): print(m)
