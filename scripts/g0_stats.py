"""Gate G0 statistics from data/processed/nchmf_obs.csv, nchmf_fc.csv (+ ODV CSV shown separately).
Run: python -I -X utf8 scripts/g0_stats.py
Season = Dec-Jun, labelled by the Dec year (Dec 2023..Jun 2024 = 2023-24). Season is taken from the ISSUE date.
Two denominators are shown per season:
  present = bulletins actually in the CSV that season (a station passes with >= 80% of them)
  of 21   = the 21 canonical issue dates (Dec 10/20/31 ... Jun 10/20/30; a station passes with >= 17 values)
G0 needs >= 20 stations passing; the 'of 21' column is the strict one when PDFs are missing.
"""
import calendar, csv, os
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def season(d):
    return f"{d.year}-{str(d.year + 1)[2:]}" if d.month == 12 else f"{d.year - 1}-{str(d.year)[2:]}"


def canonical(y0):
    out = []
    for y, m in [(y0, 12)] + [(y0 + 1, m) for m in range(1, 7)]:
        out += [date(y, m, 10), date(y, m, 20), date(y, m, calendar.monthrange(y, m)[1])]
    return set(out)


def rd(name):
    with open(os.path.join(ROOT, "data/processed", name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    obs, fc = rd("nchmf_obs.csv"), rd("nchmf_fc.csv")
    ds = lambda r: date.fromisoformat(r["issue_date"])
    S = defaultdict(lambda: dict(dates=set(), n=defaultdict(int), f=defaultdict(int)))
    for r in obs:
        s = S[season(ds(r))]
        s["dates"].add(ds(r))
        if r["smax_obs_gL"] != "":
            s["n"][r["station"]] += 1
    for r in fc:
        if r["fc_low_gL"] != "":
            S[season(ds(r))]["f"][(r["issue_date"], r["station"])] += 1
    print(f"{'season':8} {'bulletins':>9} {'of21':>5} {'extra':>5} {'stn>=80% present':>17} {'stn>=17 of 21':>14}  {'Bang2: bulletins with >=20 fc values':>38}")
    for k in sorted(S):
        s = S[k]
        y0 = int(k[:4])
        can = canonical(y0)
        nb = len(s["dates"])
        thr = 0.8 * nb
        pres = sum(1 for v in s["n"].values() if v >= thr)
        of21 = sum(1 for v in s["n"].values() if v >= 17)
        per_b = defaultdict(int)
        for (d, _), v in s["f"].items():
            per_b[d] += 1
        okb = sum(1 for c in per_b.values() if c >= 20)
        print(f"{k:8} {nb:9d} {len(s['dates'] & can):5d} {len(s['dates'] - can):5d} {pres:17d} {of21:14d}  {okb:3d}/{nb:<3d} {'parsed' if okb == nb else 'PARTIAL'}")
    print("\nMissing canonical dates per season (first 25):")
    for k in sorted(S):
        miss = sorted(canonical(int(k[:4])) - S[k]["dates"])
        print(f"  {k}: {len(miss)} missing" + (f" e.g. {', '.join(d.isoformat() for d in miss[:25])}" if len(miss) <= 25 else ""))
    odv()


def odv():
    """ODV wide CSV (VN): one 30-row block per year (2021, then 2022), 9 dekad columns Jan-Mar. Stations mapped by name."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from parse_nchmf import CANON, norm
    p = os.path.join(ROOT, "data/raw/odv/salinization_2021_2022_vi.csv")
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    hdr, rows = rows[0], rows[1:]
    blocks = {"2021": rows[:30], "2022": rows[30:]}  # the Year cell is blank for 4 rows of 2021, so use position
    print("\nODV (separate; Jan-Mar dekads only, 9 columns):")
    mapped_all, unm = set(), set()
    for y, b in blocks.items():
        cnt = {}
        for r in b:
            st = CANON.get(norm(r[0]).casefold())
            if st is None:
                unm.add(norm(r[0]))
                continue
            mapped_all.add(st)
            cnt[st] = sum(1 for x in r[4:13] if x.strip().replace(".", "", 1).isdigit())
        popcols = sum(1 for c in range(4, 13) if any(r[c].strip() not in ("", "-") for r in b))
        print(f"  Year {y}: {len(b)} rows, {len(cnt)} map to the 28; populated dekad columns {popcols}/9; "
              f"stations with >=80% of 9 columns: {sum(1 for v in cnt.values() if v >= 7.2)}; of populated columns: "
              f"{sum(1 for v in cnt.values() if v >= 0.8 * popcols)}")
    from parse_nchmf import STATIONS
    print("  ODV names not in the 28:", sorted(unm))
    print("  28-list stations absent from ODV:", [s for s in STATIONS if s not in mapped_all])


if __name__ == "__main__":
    main()
