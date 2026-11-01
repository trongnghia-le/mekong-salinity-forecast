import sys, requests
for u in sys.argv[1:]:
    try:
        r = requests.get(u, headers={"User-Agent": "mekong-salinity-research/0.1"}, timeout=25, stream=True)
        print(r.status_code, r.headers.get("content-type"), r.headers.get("content-length"), next(r.iter_content(8), b""), u)
    except Exception as e: print("ERR", type(e).__name__, str(e)[:100], u)
