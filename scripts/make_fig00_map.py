"""Fig. 0 study-area map. Run: python -I -X utf8 scripts/make_fig00_map.py  (from repo root).

Basemap: Natural Earth 1:10m (public domain), data/raw/naturalearth/. Stations: first 28 rows of
data/meta/station_meta.csv (NCHMF bulletin stations). Kratie: GloFAS cell used as discharge predictor.
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from shapely.geometry import shape, box
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.makedirs("figures", exist_ok=True)
MM = 1 / 25.4
W2 = 190 * MM
NE = "data/raw/naturalearth/"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7.5, "axes.labelsize": 7.5, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "svg.fonttype": "none", "figure.facecolor": "white",
})
INK, MUTED = "#0b0b0b", "#52514e"
C_ST, C_LONG, C_RIVER = "#eb6834", "#2a78d6", "#4f8fc9"
C_LAND, C_SEA, C_PROV, C_BORDER = "#f2f0ea", "#e9f1f7", "#b9b8b2", "#6b6a66"

EXT = (104.4, 107.1, 8.5, 11.0)          # lon0, lon1, lat0, lat1 of main panel
INS = (100.0, 111.0, 7.5, 16.0)          # inset extent
KRATIE = (105.975, 12.425)               # lon, lat
LONG = {"Cầu Quan", "Sơn Đốc", "Trà Vinh"}


def save(fig, name):
    for ext in ("png", "svg", "pdf"):
        fig.savefig(f"figures/{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def load(fn, bbox):
    d = json.load(open(NE + fn, encoding="utf8"))
    out = []
    for f in d["features"]:
        g = shape(f["geometry"])
        if g.intersects(bbox):
            out.append((f["properties"], g.intersection(bbox)))
    return out


def polys(g):
    if g.is_empty:
        return []
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def fill(ax, g, **kw):
    for p in polys(g):
        if p.geom_type != "Polygon":
            continue
        x, y = p.exterior.xy
        ax.fill(x, y, **kw)


def lines(ax, g, **kw):
    for p in polys(g):
        if p.geom_type == "LineString":
            ax.plot(*p.xy, **kw)
        elif hasattr(p, "geoms"):
            lines(ax, p, **kw)


def outline(ax, g, **kw):
    for p in polys(g):
        if p.geom_type == "Polygon":
            lines(ax, p.boundary, **kw)


# ---------------- data ----------------
st = pd.read_csv("data/meta/station_meta.csv").iloc[:28].copy()
chk = pd.read_csv("data/meta/station_coords_check.csv").iloc[:28]
assert list(st.station) == list(chk.station), "station order differs from coords check sheet"
assert st[["lat", "lon"]].notna().all().all()
assert LONG <= set(st.station)

bb = box(EXT[0] - 0.5, EXT[2] - 0.5, EXT[1] + 0.5, EXT[3] + 0.5)
bbi = box(INS[0] - 1, INS[2] - 1, INS[1] + 1, INS[3] + 1)
land = unary_union([g for _, g in load("ne_10m_land.geojson", bb)])
countries = load("ne_10m_admin_0_countries.geojson", bb)
vn = unary_union([g for p, g in countries if p["ADMIN"] == "Vietnam"])
kh = unary_union([g for p, g in countries if p["ADMIN"] == "Cambodia"])
border = kh.boundary.intersection(vn.buffer(0.01))
prov = [(p["name_vi"], g) for p, g in load("ne_10m_admin_1_states_provinces.geojson", bb)
        if p["admin"] == "Vietnam" and p["name"] != "Đông Nam Bộ"]
rivers = [g for p, g in load("ne_10m_rivers_lake_centerlines.geojson", bb)]

# ---------------- figure ----------------
fig = plt.figure(figsize=(W2, 168 * MM))
ax = fig.add_axes([0.07, 0.07, 0.91, 0.91])
ax.set_facecolor(C_SEA)
ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3])
ax.set_aspect(1 / np.cos(np.radians((EXT[2] + EXT[3]) / 2)))
fill(ax, land, fc=C_LAND, ec="none", zorder=1)
for _, g in prov:
    outline(ax, g, color=C_PROV, lw=0.4, zorder=2)
lines(ax, border, color=C_BORDER, lw=0.9, zorder=3)
for g in rivers:
    lines(ax, g, color=C_RIVER, lw=0.6, zorder=3)

# province labels (only provinces that contain stations); nudges in degrees
PL = {"Thành phố Hồ Chí Minh": ("Ho Chi Minh City", (0.12, 0.10)), "Long An": ("Long An", (-0.25, -0.15)),
      "Tiền Giang": ("Tiền Giang", (-0.02, 0.0)), "Bến Tre": ("Bến Tre", (0.05, 0.0)),
      "Trà Vinh": ("Trà Vinh", (0.12, -0.2)), "Sóc Trăng": ("Sóc Trăng", (0.0, 0.0)),
      "Bạc Liêu": ("Bạc Liêu", (0.0, 0.0)), "Cà Mau": ("Cà Mau", (0.0, 0.0)),
      "Kiên Giang": ("Kiên Giang", (0.0, 0.0))}
for name, g in prov:
    if name in PL:
        lab, (dx, dy) = PL[name]
        gg = g.intersection(box(*[EXT[0], EXT[2], EXT[1], EXT[3]]))
        pt = max(polys(gg), key=lambda p: p.area).representative_point()
        ax.text(pt.x + dx, pt.y + dy, lab.upper(), fontsize=5.5, color="#8d8c86", ha="center", va="center",
                zorder=4, fontweight="bold")
ax.text(106.95, 9.5, "South China Sea", fontsize=6.5, style="italic", color="#5a7f9c", ha="right", zorder=4)
ax.text(104.5, 9.45, "Gulf of\nThailand", fontsize=6.5, style="italic", color="#5a7f9c", ha="left", zorder=4)

# station labels: (dx, dy) in points from marker; leader line when long
OFF = {
    "Cát Lái": (6, 1), "Bến Lức": (-6, -4), "Xuân Khánh": (-6, 2), "Tân An": (-6, -5), "Tuyên Nhơn": (-6, 2),
    "Vàm Kênh": (6, -2), "Hòa Bình": (0, 9), "An Định": (-6, 4), "Bình Đại": (6, -2), "Lộc Thuận": (-6, -3),
    "An Thuận": (26, 0), "Sơn Đốc": (-8, 7), "Bến Trại": (20, -12), "Hương Mỹ": (-8, -11), "Hưng Mỹ": (-8, -12),
    "Cầu Quan": (-8, 10), "Trà Vinh": (-10, 3), "Trà Kha": (6, 4), "Long Phú": (-6, -6), "Đại Ngãi": (-6, -7),
    "Trần Đề": (6, -4), "Thạnh Phú": (-6, -5), "Sóc Trăng": (-6, 5), "Gành Hào": (6, -4), "Sông Đốc": (6, 4),
    "Rạch Giá": (-6, 3), "Gò Quao": (6, 1), "An Ninh": (-6, 5),
}
halo = [pe.withStroke(linewidth=1.8, foreground="white")]
for r in st.itertuples():
    lg = r.station in LONG
    if lg:
        ax.plot(r.lon, r.lat, "*", ms=9, color=C_LONG, mec="white", mew=0.5, zorder=6)
    else:
        ax.plot(r.lon, r.lat, "o", ms=4, color=C_ST, mec="white", mew=0.5, zorder=5)
    dx, dy = OFF[r.station]
    ha = "left" if dx > 0 else "right" if dx < 0 else "center"
    long_off = np.hypot(dx, dy) > 12
    ax.annotate(r.station, (r.lon, r.lat), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                fontsize=5.5, color=INK, fontweight="bold" if lg else "normal", path_effects=halo, zorder=7,
                arrowprops=dict(arrowstyle="-", lw=0.35, color=MUTED, shrinkA=0, shrinkB=2) if long_off else None)

ax.set_xticks([104.5, 105, 105.5, 106, 106.5, 107])
ax.set_xticklabels([f"{v:g}°E" for v in [104.5, 105, 105.5, 106, 106.5, 107]])
ax.set_yticks([9, 9.5, 10, 10.5, 11])
ax.set_yticklabels([f"{v:g}°N" for v in [9, 9.5, 10, 10.5, 11]])
ax.tick_params(length=2.5, width=0.5)

# scale bar (50 km) + north arrow, bottom-right in the sea
lat0 = 8.68
km_deg = 111.32 * np.cos(np.radians(lat0))
x1 = 106.25; x0 = x1 - 50 / km_deg
ax.plot([x0, x1], [lat0, lat0], color=INK, lw=1.6, solid_capstyle="butt", zorder=8)
ax.plot([x0, x0], [lat0 - 0.012, lat0 + 0.012], color=INK, lw=0.6, zorder=8)
ax.plot([x1, x1], [lat0 - 0.012, lat0 + 0.012], color=INK, lw=0.6, zorder=8)
ax.text((x0 + x1) / 2, lat0 + 0.03, "50 km", ha="center", va="bottom", fontsize=6.5, zorder=8)
ax.annotate("", xy=(106.98, 9.35), xytext=(106.98, 9.12), arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8), zorder=8)
ax.text(106.98, 9.37, "N", ha="center", va="bottom", fontsize=7, fontweight="bold", zorder=8)

# legend
h = [Line2D([], [], marker="o", ls="", ms=4, color=C_ST, mec="white", label="NCHMF bulletin station"),
     Line2D([], [], marker="*", ls="", ms=9, color=C_LONG, mec="white", label="long-record gauge (seasonal layer)"),
     Line2D([], [], color=C_RIVER, lw=0.8, label="river (Natural Earth)"),
     Line2D([], [], color=C_BORDER, lw=0.9, label="Vietnam-Cambodia border"),
     Line2D([], [], color=C_PROV, lw=0.6, label="province boundary")]
ax.legend(handles=h, loc="lower right", bbox_to_anchor=(0.995, 0.012), frameon=True, framealpha=0.95,
          edgecolor="#d0cfca", fancybox=False, borderpad=0.5, handletextpad=0.5, fontsize=6.5).set_zorder(9)

# ---------------- locator inset ----------------
ia = fig.add_axes([0.09, 0.70, 0.27, 0.27])
ia.set_facecolor(C_SEA)
ia.set_xlim(INS[0], INS[1]); ia.set_ylim(INS[2], INS[3])
ia.set_aspect(1 / np.cos(np.radians(12)))
ic = load("ne_10m_admin_0_countries.geojson", bbi)
for p, g in ic:
    isv, isk = p["ADMIN"] == "Vietnam", p["ADMIN"] == "Cambodia"
    fill(ia, g, fc="#e4e2db" if isv else C_LAND, ec="none", zorder=1)
    outline(ia, g, color=C_BORDER if (isv or isk) else C_PROV, lw=0.4, zorder=2)
ia.add_patch(Rectangle((EXT[0], EXT[2]), EXT[1] - EXT[0], EXT[3] - EXT[2], fill=False, ec=C_ST, lw=1.0, zorder=5))
ia.plot(*KRATIE, "^", ms=5, color=INK, mec="white", mew=0.4, zorder=6)
ia.annotate("Kratie\n(GloFAS cell)", KRATIE, xytext=(7, -3), textcoords="offset points", ha="left", va="center",
            fontsize=5.5, path_effects=halo, zorder=7)
ia.text(104.2, 13.0, "CAMBODIA", fontsize=5, color=MUTED, ha="center")
ia.text(107.7, 13.6, "VIETNAM", fontsize=5, color=MUTED, ha="center", rotation=-70)
ia.set_xticks([]); ia.set_yticks([])
for s in ia.spines.values():
    s.set_linewidth(0.8)

# ---------------- self-check ----------------
assert len(st) == 28 and st.station.is_unique
assert st.lon.between(EXT[0], EXT[1]).all() and st.lat.between(EXT[2], EXT[3]).all()
assert INS[0] <= KRATIE[0] <= INS[1] and INS[2] <= KRATIE[1] <= INS[3]
assert len(ax.lines) >= 28 and sum(1 for ln in ax.lines if ln.get_marker() in ("o", "*")) == 28
assert sum(1 for ln in ax.lines if ln.get_marker() == "*") == 3

save(fig, "fig00_study_area")
print("ok: 28 stations plotted, 3 long-record")
