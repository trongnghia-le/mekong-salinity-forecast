"""Parse NCHMF salinity bulletins (data/raw/nchmf/pdf) into data/processed/nchmf_obs.csv and nchmf_fc.csv.
Run: python -I -X utf8 scripts/parse_nchmf.py   (re-runnable; parses whatever PDFs are present)

Layout (2024-2026, all checked): Bang 1 (observed Smax of the dekad ending on the issue date) and Bang 2 (forecast for the
next dekad) are bordered tables, but find_tables() drops rows that spill onto the next page, so we parse the text lines:
a row starts at a line == expected STT followed by a name line; fields follow in order
river, province, km, Smax, then comparison (Bang 1) or time of occurrence (Bang 2, 2026 only).
Periods are derived from the issue date (the stated headers are sometimes stale copies); stated text is kept alongside.
"""
import calendar, csv, glob, os, re, unicodedata
from collections import Counter
from datetime import date, timedelta
import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFS = sorted(glob.glob(os.path.join(ROOT, "data/raw/nchmf/pdf/dbqg_xm*_*.pdf")))
OUT = os.path.join(ROOT, "data/processed")

STATIONS = ["Cát Lái", "Bến Lức", "Xuân Khánh", "Tân An", "Tuyên Nhơn", "Vàm Kênh", "Hòa Bình", "An Định", "Bình Đại",
            "Lộc Thuận", "An Thuận", "Sơn Đốc", "Bến Trại", "Hương Mỹ", "Hưng Mỹ", "Cầu Quan", "Trà Vinh", "Trà Kha",
            "Long Phú", "Đại Ngãi", "Trần Đề", "Thạnh Phú", "Sóc Trăng", "Gành Hào", "Sông Đốc", "Rạch Giá", "Gò Quao",
            "An Ninh"]
# stations of the 2021-23 bulletins that are not among the 28 of 2024+ (kept under their printed names, reported as new)
EXTRA = ["Cầu Nổi", "Xẻo Rô", "Mỹ Tho", "Đồng Tâm", "Ngã 3 Cát Lái", "Cà Mau"]
ALIASES = {"Ngã 3 Cát Lái": "Cầu Nổi"}  # 2022 name of the 2021 "Cầu Nổi" (Vàm Cỏ, km 20): 7/7 identical Smax vs ODV


def norm(s):
    s = unicodedata.normalize("NFC", s).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


CANON = {norm(s).casefold(): s for s in STATIONS}
CANON.update({norm(k).casefold(): v for k, v in ALIASES.items()})
KNOWN = set(CANON) | {norm(x).casefold() for x in EXTRA}
NUM = re.compile(r"^\d+([.,]\d+)?$")
RANGE = re.compile(r"^\d+([.,]\d+)?\s*[-–]\s*\d+([.,]\d+)?$")


def tonum(s):
    return float(s.replace(",", "."))


def periods(d):
    """observed dekad ends on the issue date; forecast = next dekad."""
    o0 = date(d.year, d.month, 1 if d.day <= 10 else 11 if d.day <= 20 else 21)
    f0 = d + timedelta(days=1)
    f1 = date(f0.year, f0.month, 10 if f0.day <= 10 else 20 if f0.day <= 20 else calendar.monthrange(f0.year, f0.month)[1])
    return o0, d, f0, f1


def stated_range(header):
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)/(\d+)/(\d{4})", header)
    return m.group(0) if m else ""


def parse_section(lines, notes):
    starts, exp = [], 1
    for j in range(len(lines) - 1):
        nxt = lines[j + 1]
        if lines[j] == str(exp) and re.search(r"[^\W\d_]", nxt) and not nxt.startswith(("Lớn", "Nhỏ", "Xấp")):
            starts.append(j)
            exp += 1
    rows = []
    for a, j in enumerate(starts):
        end = starts[a + 1] if a + 1 < len(starts) else j + 14
        name, L = lines[j + 1], lines[j + 2:end]
        if norm(name).casefold() not in KNOWN and len(lines) > j + 2 and norm(name + " " + lines[j + 2]).casefold() in KNOWN:
            name, L = norm(name + " " + lines[j + 2]), lines[j + 3:end]  # name wrapped over two lines ("Ngã 3 Cát" / "Lái")
        for c in STATIONS:  # some 2025-26 files print "Xuân Khánh Vàm Cỏ Đông" as one line
            if norm(name).casefold().startswith(norm(c).casefold() + " "):
                name, L = c, [name[len(c):].strip()] + L
                break
        k = next((i for i in range(2, len(L)) if NUM.match(L[i]) or L[i] == "-" or L[i].startswith("Nội đồng")), None)
        if k is None:
            notes.append(f"row {a + 1} {lines[j + 1]}: no km/Smax found")
            continue
        km, kfirst = L[k], k
        if km.startswith("Nội đồng") and k + 1 < len(L) and L[k + 1].startswith("("):
            k += 1
            km += " " + L[k]
        rest = L[k + 1:]
        smax = rest[0] if rest and (NUM.match(rest[0]) or RANGE.match(rest[0]) or rest[0] in ("-", "KQT")) else ""
        if smax and len(rest) > 2 and re.match(r"^(Lớn|Nhỏ) hơn:?$", rest[1]) and NUM.match(rest[2]):
            rest = [rest[0], rest[1] + " " + rest[2]] + rest[3:]  # comparison split over two lines
        rows.append(dict(name=name, river=" ".join(L[:kfirst - 1]), province=L[kfirst - 1], km_raw=km,
                         smax_raw=smax, extra=rest[1] if smax and len(rest) > 1 else ""))
    return rows, (lines[:starts[0]] if starts else [])


MONTH = re.compile(r"(?:tháng|T)\s*(\d{1,2})\s*/\s*(\d{4})")


def cmp_label(header):
    """text of the 'So sánh' column header: everything after the Smax '(g/l)' unit, minus a trailing '(g/l)'"""
    h = norm(" ".join(header))
    parts = re.split(r"\(g/l\)", h, maxsplit=1)
    lab = parts[1] if len(parts) > 1 else ""
    return norm(re.sub(r"\(g/l\)\s*$", "", lab.strip()))


def cmp_fields(label, raw, smax, obs_end):
    """comparison cell -> sign, diff, reference month, back-calculated reference Smax, flag"""
    ms = {(int(a), int(b)) for a, b in MONTH.findall(label)}
    ref, flag = "", ""
    if not label:
        flag = "no_label"
    elif len(ms) != 1:
        flag = "ambiguous_label" if ms else "no_month_in_label"
    else:
        (mo, yr), = ms
        if 1 <= mo <= 12:
            ref = f"{yr:04d}-{mo:02d}"
            off = (obs_end.year * 12 + obs_end.month) - (yr * 12 + mo)
            flag = "ok" if off == 12 else f"offset_{off}m"
        else:
            flag = "unparseable_label"
    m = re.match(r"^(Lớn|Nhỏ) hơn:?\s*(\d+(?:[.,]\d+)?)$", raw)
    sign, diff, refv = "missing", "", ""
    if m:
        sign, diff = ("gt" if m.group(1) == "Lớn" else "lt"), tonum(m.group(2))
        if smax != "":
            refv = round(smax - diff if sign == "gt" else smax + diff, 1)
    elif raw.startswith("Xấp xỉ"):
        sign = "approx"
    elif raw not in ("", "-"):
        sign = "unparsed"
    return dict(cmp_raw=raw, cmp_sign=sign, cmp_diff_gL=diff, cmp_ref_label=label, cmp_ref_month=ref,
                ref_smax_gL=refv, cmp_ref_flag=flag)


def stale(stated, b, e):
    return bool(stated) and not re.match(rf"0?{b.day}\s*[-–]\s*0?{e.day}/0?{e.month}/", stated)


HANMAN = sorted(glob.glob(os.path.join(ROOT, "data/raw/alt_samples/wayback_nchmf_2020/nchmf_hanman_*.pdf")))


def parse_hanman(notes):
    """5-day bulletin (not a dekad, kept out of the main tables): only its comparison column goes to the reference table"""
    out = []
    for f in HANMAN:
        base = os.path.basename(f)
        with fitz.open(f) as doc:
            lines = [x for x in (norm(y) for p in doc for y in p.get_text().split(chr(10))) if x]
        lo = next((i for i, x in enumerate(lines) if re.match(r"^Bảng \d: Bảng độ mặn cao nhất", x)), None)
        hi = next((i for i, x in enumerate(lines) if i > (lo or 0) and x.startswith("Hình 1")), None)
        m = re.search(r"đến ngày|từ ngày\s*\d+-(\d+)/(\d+)/(\d{4})", lines[lo] if lo is not None else "")
        if lo is None or hi is None or not m:
            notes.append(f"{base}: salinity table not found")
            continue
        end = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        rows, header = parse_section(lines[lo + 1:hi], notes)
        lab = cmp_label(header)
        for r in rows:
            st = CANON.get(norm(r["name"]).casefold(), r["name"])
            smax = tonum(r["smax_raw"]) if NUM.match(r["smax_raw"]) else ""
            c = cmp_fields(lab, r["extra"] if r["extra"][:3] in ("Lớn", "Nhỏ", "Xấp") else "", smax, end)
            out.append(dict(station=st, issue_date=end.isoformat(), source_file=base, smax_obs_gL=smax, **c))
        notes.append(f"{base}: {len(rows)} stations, 5-day bulletin, comparison label '{lab}' (not in the dekad tables)")
    return out


def write_ref_monthly(obs, extra):
    """one row per station-month of the reference column: ref Smax = observed -/+ stated difference"""
    g = {}
    for r in list(obs) + extra:
        if r["cmp_ref_month"] and r["ref_smax_gL"] != "":
            g.setdefault((r["station"], r["cmp_ref_month"]), []).append((r["ref_smax_gL"], r["source_file"], r["cmp_ref_flag"]))
    rows = []
    for (st, mo), v in sorted(g.items()):
        vals = [x[0] for x in v]
        mode = max(set(vals), key=vals.count)
        rows.append(dict(station=st, ref_month=mo, ref_smax_gL=mode, n_bulletins_agreeing=vals.count(mode),
                         n_bulletins=len(vals), values_seen=";".join(f"{x:g}" for x in vals),
                         max_spread_gL=round(max(vals) - min(vals), 1), flags=";".join(sorted({x[2] for x in v})),
                         source_files=";".join(x[1] for x in v)))
    with open(os.path.join(OUT, "nchmf_ref_monthly.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    dis = [r for r in rows if r["max_spread_gL"] > 0.1]
    okdis = []
    for (st, mo), v in sorted(g.items()):
        ok = [float(x[0]) for x in v if x[2] == "ok"]
        if len(ok) > 1 and max(ok) - min(ok) > 0.1:
            okdis.append((st, mo, ok, [x[1] for x in v if x[2] == "ok"]))
    print(f"nchmf_ref_monthly.csv: {len(rows)} station-months; {len(dis)} with bulletins disagreeing by > 0.1 g/L "
          f"(all labels); {len(okdis)} when only flag=ok bulletins are used")
    for st, mo, ok, fs in okdis:
        print("   DISAGREE(ok only)", st, mo, ok, fs)


def main():
    obs, fc, notes = [], [], []
    tokens, unmapped, counts = Counter(), Counter(), []
    for f in PDFS:
        names1 = set()
        base = os.path.basename(f)
        m = re.search(r"_(\d{8})_", base)
        d = date(int(m.group(1)[:4]), int(m.group(1)[4:6]), int(m.group(1)[6:]))
        with fitz.open(f) as doc:
            lines = [norm(x) for p in doc for x in p.get_text().split("\n")]
        lines = [x for x in lines if x]
        i1 = next((i for i, x in enumerate(lines) if re.match(r"^Bảng 1\.", x)), None)
        i2 = next((i for i, x in enumerate(lines) if re.match(r"^Bảng 2\.", x)), None)
        if i1 is None or i2 is None:
            notes.append(f"{base}: Bảng 1/2 header not found")
            continue
        o0, o1, f0, f1 = periods(d)
        for sec, lo, hi in ((1, i1, i2), (2, i2, len(lines))):
            hdr = stated_range(lines[lo])
            if sec == 1:
                if stale(hdr, o0, o1): notes.append(f"{base}: Bảng 1 header says '{hdr}', derived {o0}..{o1} (derived kept)")
            elif stale(hdr, f0, f1):
                notes.append(f"{base}: Bảng 2 header says '{hdr}', derived {f0}..{f1} (derived kept)")
            rows, header = parse_section(lines[lo + 1:hi], notes)
            if sec == 1:
                names1 = {norm(r["name"]) for r in rows}
            if sec == 1:
                counts.append(len(rows))
            if len(rows) != 28:
                notes.append(f"{base}: Bảng {sec} has {len(rows)} rows")
            for r in rows:
                st = CANON.get(norm(r["name"]).casefold())
                if sec == 2 and st == "Cát Lái" and ("Ngã 3 Cát Lái" in names1):
                    st = "Cầu Nổi"  # 2021-22 Bảng 2 prints row 1 as "Cát Lái (Sài Gòn, 58)"; Bảng 1 row 1 is "Ngã 3 Cát Lái" (same STT, obs 5.8 vs fc 6.0)
                if st is None:
                    unmapped[r["name"]] += 1
                    st = r["name"]
                raw, low, high = r["smax_raw"], "", ""
                if NUM.match(raw) or RANGE.match(raw):
                    parts = [tonum(x) for x in re.split(r"[-–]", raw)]
                    low, high = min(parts), max(parts)
                    if high > 45:  # e.g. An Định "202" in 20260420 Bảng 2: typo (seawater ~35; Sông Đốc 2020 prints 42, kept)
                        tokens[(sec, f"implausible>45:{raw}")] += 1
                        low = high = ""
                else:
                    tokens[(sec, raw or "<blank>")] += 1
                kmn = re.search(r"\d+([.,]\d+)?", r["km_raw"])
                if r["km_raw"] == "-":
                    tokens[("km", "-")] += 1
                if sec == 1:
                    obs.append(dict(issue_date=d.isoformat(), station=st, river=r["river"], province=r["province"],
                                    km_from_mouth=tonum(kmn.group(0)) if kmn else "",
                                    inland_canal=int(r["km_raw"].startswith("Nội đồng")), smax_obs_gL=low, smax_raw=raw,
                                    obs_start=o0.isoformat(), obs_end=o1.isoformat(), obs_header_stated=stated_range(lines[i1]),
                                    source_file=base, **cmp_fields(cmp_label(header), r["extra"] if r["extra"][:3] in ("Lớn", "Nhỏ", "Xấp") or r["extra"] == "-" else "", low, o1)))
                else:
                    fc.append(dict(issue_date=d.isoformat(), station=st, fc_raw=raw, fc_low_gL=low, fc_high_gL=high,
                                   fc_start=f0.isoformat(), fc_end=f1.isoformat(), fc_header_stated=stated_range(lines[i2]),
                                   fc_time_of_max=r["extra"] if re.match(r"^\d", r["extra"]) else "",
                                   river=r["river"], province=r["province"], source_file=base))
    ref5 = parse_hanman(notes)
    os.makedirs(OUT, exist_ok=True)
    write_ref_monthly(obs, ref5)
    for name, rows in (("nchmf_obs.csv", obs), ("nchmf_fc.csv", fc)):
        if rows:
            with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
    cs = sorted(counts)
    if cs:
        print(f"{len(PDFS)} PDFs; obs rows {len(obs)}, fc rows {len(fc)}; stations per Bảng 1: "
              f"min {cs[0]} median {cs[len(cs) // 2]} max {cs[-1]}")
    print("unmapped station names:", dict(unmapped) or "none")
    print("missing/odd tokens {(table, token): n}:", dict(tokens) or "none")
    for n in notes:
        print("NOTE", n)


def selfcheck():
    """values read by eye from the text layer of dbqg_xman_20240320_1500.pdf"""
    def rows(name):
        with open(os.path.join(OUT, name), encoding="utf-8") as fh:
            return {r["station"]: r for r in csv.DictReader(fh) if r["issue_date"] == "2024-03-20"}
    o, p = rows("nchmf_obs.csv"), rows("nchmf_fc.csv")
    assert len(o) == 28 and len(p) == 28
    assert o["Cát Lái"]["smax_obs_gL"] == "10.4" and o["Vàm Kênh"]["smax_obs_gL"] == "26.0"
    sd = o["Sông Đốc"]
    assert sd["smax_obs_gL"] == "31.6" and sd["km_from_mouth"] == "1.5" and sd["province"] == "Cà Mau"  # decimal comma
    tp = o["Thạnh Phú"]
    assert tp["smax_obs_gL"] == "1.1" and tp["km_from_mouth"] == "58.0" and tp["inland_canal"] == "1"
    assert o["Rạch Giá"]["smax_obs_gL"] == "0.5" and o["Bến Trại"]["river"] == "Cổ Chiên (cửa Cổ Chiên)"
    assert o["Cát Lái"]["obs_start"] == "2024-03-11" and o["Cát Lái"]["obs_end"] == "2024-03-20"
    assert p["Cát Lái"]["fc_raw"] == "9.3" and p["Bến Lức"]["fc_low_gL"] == "3.6"
    assert p["Sông Đốc"]["fc_high_gL"] == "30.0" and p["An Ninh"]["fc_raw"] == "6"
    assert p["Cát Lái"]["fc_start"] == "2024-03-21" and p["Cát Lái"]["fc_end"] == "2024-03-31"
    assert o["Cát Lái"]["cmp_sign"] == "gt" and o["Cát Lái"]["cmp_diff_gL"] == "4.4" and o["Cát Lái"]["cmp_ref_month"] == "2023-03"
    assert o["Cát Lái"]["ref_smax_gL"] == "6.0" and o["Cát Lái"]["cmp_ref_label"] == "So sánh T3/2023"  # 10.4 - 4.4 = Mar 2023 max
    assert o["Cát Lái"]["cmp_ref_flag"] == "ok" and o["Thạnh Phú"]["cmp_sign"] == "approx" and o["Thạnh Phú"]["ref_smax_gL"] == ""
    assert o["Đại Ngãi"]["cmp_sign"] == "lt" and o["Đại Ngãi"]["ref_smax_gL"] == "9.5"  # 8.9 + 0.6
    print("self-check OK (dbqg_xman_20240320_1500.pdf)")


def selfcheck_2022():
    """values read by eye from dbqg_xmnb_20220320_1530.pdf (text layer): 27 stations, decimal dots, wrapped names/rivers"""
    def rows(name):
        with open(os.path.join(OUT, name), encoding="utf-8") as fh:
            return {r["station"]: r for r in csv.DictReader(fh) if r["issue_date"] == "2022-03-20"}
    o, p = rows("nchmf_obs.csv"), rows("nchmf_fc.csv")
    assert len(o) == 27 and len(p) == 27
    assert o["Cầu Nổi"]["smax_obs_gL"] == "5.8" and o["Cầu Nổi"]["km_from_mouth"] == "20.0"  # name wraps over two lines
    assert o["Bến Lức"]["smax_obs_gL"] == "1.4" and o["Vàm Kênh"]["smax_obs_gL"] == "21.1" and o["Cầu Quan"]["smax_obs_gL"] == "8.8"
    assert o["Thạnh Phú"]["smax_obs_gL"] == "2.0" and o["Thạnh Phú"]["inland_canal"] == "1"  # "Nội đồng" with no km number
    assert o["Sông Đốc"]["smax_obs_gL"] == "33.6" and o["Sông Đốc"]["km_from_mouth"] == ""  # km printed "-"
    assert o["Rạch Giá"]["km_from_mouth"] == "0.0" and o["Rạch Giá"]["smax_obs_gL"] == "0.4" and o["An Ninh"]["smax_obs_gL"] == "8.3"
    assert o["Bến Trại"]["river"] == "Cổ Chiên (cửa Cổ Chiên)"  # river wrapped over two lines
    assert o["Cầu Quan"]["obs_start"] == "2022-03-11" and o["Cầu Quan"]["obs_end"] == "2022-03-20"
    assert p["Cầu Nổi"]["fc_raw"] == "6.0" and p["Bến Lức"]["fc_low_gL"] == "1.6" and p["Cầu Quan"]["fc_raw"] == "8.9"
    assert p["Sông Đốc"]["fc_raw"] == "33.7" and p["Rạch Giá"]["fc_raw"] == "0.5" and p["Cầu Quan"]["fc_start"] == "2022-03-21"
    print("self-check OK (dbqg_xmnb_20220320_1530.pdf)")


if __name__ == "__main__":
    main()
    if os.path.exists(os.path.join(ROOT, "data/raw/nchmf/pdf/dbqg_xman_20240320_1500.pdf")):
        selfcheck()
    if os.path.exists(os.path.join(ROOT, "data/raw/nchmf/pdf/dbqg_xmnb_20220320_1530.pdf")):
        selfcheck_2022()
