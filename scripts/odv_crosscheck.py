"""Compare NCHMF Bảng 1 Smax with the ODV CSV (VN) for dekads present in both. Matching by station name only
(ODV 2022 river/province columns are shifted). Block 1 of 30 rows = 2021, block 2 = 2022 (the Year cell is blank for some rows).
Run: python -I -X utf8 scripts/odv_crosscheck.py"""
import csv, os, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from parse_nchmf import norm  # noqa: E402

with open(os.path.join(ROOT, "data/raw/odv/salinization_2021_2022_vi.csv"), encoding="utf-8-sig") as fh:
    rows = list(csv.reader(fh))
hdr, rows = rows[0], rows[1:]
odv = {}  # (year, station, col label) -> value text
for y, blk in ((2021, rows[:30]), (2022, rows[30:])):
    for r in blk:
        for c in range(4, 13):
            odv[(y, norm(r[0]), hdr[c].replace(" ", ""))] = r[c].strip()
with open(os.path.join(ROOT, "data/processed/nchmf_obs.csv"), encoding="utf-8") as fh:
    obs = list(csv.DictReader(fh))

ALT = {}  # (Ngã 3 Cát Lái is now aliased to Cầu Nổi in the parser)
for alt in (False, True):
    eq, diff, ex, nores, only_n, only_o = 0, 0, [], 0, 0, 0
    for r in obs:
        b, e = date.fromisoformat(r["obs_start"]), date.fromisoformat(r["obs_end"])
        label = f"{b.day:02d}/{b.month:02d}-{e.day:02d}/{e.month:02d}"
        st = ALT.get(r["station"], r["station"]) if alt else r["station"]
        v = odv.get((b.year, st, label))
        if v is None:
            continue
        n = r["smax_obs_gL"]
        o = "" if v in ("", "-") else v
        if n == "" and o == "":
            continue
        if n == "" or o == "":
            only_n += n != ""
            only_o += o != ""
            continue
        if abs(float(n) - float(o)) < 1e-9:
            eq += 1
        else:
            diff += 1
            if len(ex) < 12:
                ex.append((r["issue_date"], r["station"], n, o))
    print(f"alias Ngã 3 Cát Lái -> Cầu Nổi: {alt}: equal {eq}, different {diff}, NCHMF only {only_n}, ODV only {only_o}")
    for x in ex:
        print("   diff", x)
