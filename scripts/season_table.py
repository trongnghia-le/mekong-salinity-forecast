import csv, calendar, collections, datetime as dt
rows = list(csv.DictReader(open("data/raw/nchmf/inventory.csv", encoding="utf8")))
found = {r["issue_date"]: r for r in rows if r["status"] == "found"}
def canon(d):
    return d.day in (10, 20, calendar.monthrange(d.year, d.month)[1])
c = collections.Counter(); x = collections.Counter(); w = collections.Counter(); seas = set()
for k, r in found.items():
    d = dt.date.fromisoformat(k); s = r["season"]; seas.add(s)
    if canon(d): c[s] += 1
    else: x[s] += 1
    w[s] += r["source"] == "wayback"
for s in sorted({r["season"] for r in rows if r["season"] and r["issue_date"] <= "2026-06-30"}):
    print(s, "canonical", c[s], "/21", "| off-canonical extra", x[s], "| from wayback", w[s])
print("total found", len(found), "wayback", sum(w.values()))
print("extras:", sorted(k for k in found if not canon(dt.date.fromisoformat(k))))
