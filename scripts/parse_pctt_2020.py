"""Parse data/raw/pctt/*.html (or .doc/.docx via antiword when HTML lacks the table) -> data/processed/pctt_daily_2020.csv
and pctt_dekadal.csv. Run: python -I scripts/parse_pctt_2020.py  (then it self-checks)."""
import csv, datetime as dt, glob, html, os, re, subprocess, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "data", "raw", "pctt"); PROC = os.path.join(ROOT, "data", "processed")
ST = re.compile(r"^-?\s*(?P<river>[^:]+):\s*Tại\s+(?P<st>[^(]+?)\s*(?:\((?P<km>[\d.,]+)\s*km\))?$")
DATE = re.compile(r"Ngày\s+(\d\d)/(\d\d)/2020")

def num(s):
    m = re.search(r"\d+(?:[.,]\d+)?", s or "")
    return float(m.group().replace(",", ".")) if m else None

def rows_html(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    i = t.find("Trạm đo mặn")
    if i < 0: return None
    seg = t[t.rfind("<table", 0, i): t.find("</table>", i)]
    return [[re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip()
             for c in re.findall(r"<t[dh].*?</t[dh]>", tr, flags=re.S)] for tr in re.findall(r"<tr.*?</tr>", seg, flags=re.S)]

def rows_doc(path):  # antiword prints tables as |cell|cell|
    out = subprocess.run(["antiword", "-m", "UTF-8.txt", "-w", "0", path], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    return [[c.strip() for c in l.strip().strip("|").split("|")] for l in out.splitlines() if "|" in l]

def parse():
    out = []
    for hp in sorted(glob.glob(os.path.join(RAW, "*.html"))):
        tag = os.path.basename(hp)[:-5]; src = os.path.basename(hp)
        rows = rows_html(hp)
        if rows is None:
            for ap in glob.glob(os.path.join(RAW, tag + ".doc*")):
                rows = rows_doc(ap); src = os.path.basename(ap)
        if not rows: continue
        dm = next((DATE.search(c) for r in rows for c in r if DATE.search(c)), None)
        rd = f"2020-{dm[2]}-{dm[1]}" if dm else tag  # date printed in the table header wins over the page slug
        for r in rows:
            m = ST.match(r[0]) if r else None
            if not m or len(r) < 3: continue
            v = r[1:]
            km = num(v[5]) if len(v) > 5 else num(m["km"])
            out.append(dict(report_date=rd, page_date=tag, station=m["st"].strip(), river=m["river"].strip(), sal_gL=num(v[0]),
                            sal_same_date_2016_gL=num(v[1]) if len(v) > 1 else None,
                            season_max_2016_gL=num(v[3]) if len(v) > 3 else None,
                            len4_km=km, raw_text="|".join(r), source_file=src))
    seen, uniq = set(), []  # same table date on two pages: keep first (HTML page sorted first by name)
    for r in out:
        k = (r["report_date"], r["station"])
        if k in seen: print("DUP", k, r["page_date"]); continue
        seen.add(k); uniq.append(r)
    return uniq

def dekad(d):
    a = 1 if d.day <= 10 else 11 if d.day <= 20 else 21
    end = d.replace(day=10 if a == 1 else 20) if a < 21 else (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return d.replace(day=a), end

def main():
    rows = parse(); os.makedirs(PROC, exist_ok=True)
    cols = ["report_date", "page_date", "station", "river", "sal_gL", "sal_same_date_2016_gL", "season_max_2016_gL", "len4_km", "raw_text", "source_file"]
    with open(os.path.join(PROC, "pctt_daily_2020.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
    g = collections.defaultdict(list)  # (station, year, dekad_start, dekad_end) -> values
    for r in rows:
        d = dt.date.fromisoformat(r["report_date"]); a, b = dekad(d)
        for yr, k in ((2020, "sal_gL"), (2016, "sal_same_date_2016_gL")):
            if r[k] is not None: g[(r["station"], yr, a.replace(year=yr), b.replace(year=yr))].append(r[k])
    with open(os.path.join(PROC, "pctt_dekadal.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["station", "year", "dekad_start", "dekad_end", "n_days", "smax_gL", "complete"])
        for (s, y, a, b), v in sorted(g.items()):
            w.writerow([s, y, a, b, len(v), max(v), int(len(v) >= 7)])
    print(len(rows), "rows,", len({r["report_date"] for r in rows}), "days")
    return rows

def check(rows):
    q = {(r["report_date"], r["station"]): r for r in rows}
    a = q[("2020-03-10", "Tân An")]; assert (a["sal_gL"], a["sal_same_date_2016_gL"], a["season_max_2016_gL"]) == (6.9, 2.4, 11.8), a
    b = q[("2020-02-12", "Cầu Quan")]; assert (b["sal_gL"], b["sal_same_date_2016_gL"], b["season_max_2016_gL"]) == (14.0, 9.5, 16.5), b
    print("self-check OK")

if __name__ == "__main__":
    check(main())
