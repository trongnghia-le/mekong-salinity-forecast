"""Tidy the two open long salinity records (CC BY 4.0). Run: python -I -X utf8 scripts/tidy_long_records.py
Units: both sources state g/l, so no conversion. Outputs in data/processed/."""
import sys, csv, glob
from pathlib import Path
sys.path.append(r"C:\Users\ASUS\AppData\Roaming\Python\Python310\site-packages")  # -I hides user site; openpyxl only
import pandas as pd, openpyxl

R = Path(__file__).resolve().parent.parent
RAW, OUT = R / "data/raw", R / "data/processed"

# --- GFZ Son Doc (';' separated, '#' comment lines, BOM) ---
sd = pd.read_csv(glob.glob(str(RAW / "gfz_sondoc/*SONDOC*.csv"))[0], sep=";", comment="#",
                 encoding="utf-8-sig", parse_dates=["DATETIME"])
sd.columns = ["t", "s"]
sd["s"] = pd.to_numeric(sd.s, errors="coerce")  # 12 blank cells in source (2000-05-31, 2002-03-31)
sd = sd.dropna()
# NB source has 2008-02-02 twice (24 readings, two different series); kept, n_obs=24 flags it
sd["date"] = sd.t.dt.normalize()
daily = sd.groupby("date").s.agg(smax_gL="max", n_obs="count").reset_index()
daily.to_csv(OUT / "long_sondoc_daily_max.csv", index=False)
m = daily.assign(year=daily.date.dt.year, month=daily.date.dt.month).groupby(["year", "month"]) \
         .agg(smax_gL=("smax_gL", "max"), n_days=("date", "count")).reset_index()
m.to_csv(OUT / "long_sondoc_monthly_max.csv", index=False)

# --- GFZ Tan Chau monthly Q (m3/s) ---
qf = glob.glob(str(RAW / "gfz_sondoc/*Qmonthly*.csv"))[0]
lines = open(qf, encoding="utf-8-sig").read().splitlines()
q = pd.DataFrame([l.split(";")[:3] for l in lines[[l.startswith("year;") for l in lines].index(True) + 1:] if l.strip()],
                 columns=["year", "month", "q_m3s"]).astype(int)
q.astype(int).to_csv(OUT / "long_tanchau_monthly_q.csv", index=False)

# --- Mendeley Binh 2019, sheet 'Max. salinity' ---
ws = openpyxl.load_workbook(glob.glob(str(RAW / "mendeley_binh2019/*.xlsx"))[0], data_only=True)["Max. salinity"]
rows, SH = [], "Max. salinity"
for r in ws.iter_rows(min_row=2, max_col=3, values_only=True):
    if isinstance(r[0], (int, float)):
        rows += [("Trà Vinh", int(r[0]), "", r[1], SH), ("Cầu Quan", int(r[0]), "", r[2], SH)]
mon = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6}
yrs = [c.value for c in ws[2][6:9]]  # 1998, 2010, 2016 (header row sits in row 2)
for r in ws.iter_rows(min_row=3, min_col=6, max_col=9, values_only=True):
    if r[0] in mon:
        rows += [("Cầu Quan", int(y), mon[r[0]], v, SH) for y, v in zip(yrs, r[1:])]
mx = pd.DataFrame(rows, columns=["station", "year", "month", "smax_gL", "source_sheet"])
mx.to_csv(OUT / "long_mendeley_max.csv", index=False, encoding="utf-8")

# --- self-check (values read by eye from the source files) ---
d0 = daily.set_index("date")
assert d0.loc[pd.Timestamp("1996-02-01"), "smax_gL"] == 4.3 and d0.loc[pd.Timestamp("1996-02-01"), "n_obs"] == 12   # first day, 12 readings
assert d0.loc[pd.Timestamp("1996-02-03"), "smax_gL"] == 4.6
assert q[(q.year == 1980) & (q.month == 2)].q_m3s.iloc[0] == 4575
a = mx[(mx.station == "Cầu Quan") & (mx.year == 2016)]
assert a[a.month == ""].smax_gL.iloc[0] == 16.5 and a[a.month == 3].smax_gL.iloc[0] == 14.6
assert mx[(mx.station == "Trà Vinh") & (mx.year == 1993)].smax_gL.iloc[0] == 4.5
print("self-check OK")

# --- coverage ---
if __name__ == "__main__":
    print("Son Doc: %s .. %s, %d days, %d obs" % (daily.date.min().date(), daily.date.max().date(), len(daily), len(sd)))
    p = m.pivot(index="year", columns="month", values="n_days").reindex(columns=range(1, 13))
    print("n_days with data per month (Son Doc):\n", p.dropna(how="all", axis=1).fillna(0).astype(int).to_string())
    print("Feb&Mar both present:", sorted(p.index[(p[2] > 0) & (p[3] > 0)]))
    print("Feb&Mar >=10 days each:", sorted(p.index[(p[2] >= 10) & (p[3] >= 10)]))
    print("Mendeley annual years:", mx[mx.month == ""].year.min(), mx[mx.month == ""].year.max(), "n =", mx[(mx.month == "") & (mx.station == "Cầu Quan")].shape[0])
    print("Mendeley monthly rows:", sorted(set(mx[mx.month != ""].year)))
    o = pd.read_csv(OUT / "nchmf_obs.csv", parse_dates=["obs_end"])
    o = o[o.station.isin(["Sơn Đốc", "Cầu Quan", "Trà Vinh"])]
    c = o.assign(ym=o.obs_end.dt.to_period("M")).groupby(["station", "ym"]).size().unstack(0)
    c = c[[i.month in (2, 3) for i in c.index]]
    print("Bulletin dekads per month (3 = full month), Feb/Mar:\n", c.to_string())
