"""Final station coordinates for the map (Fig. 0) and the atlas -> data/meta/station_coords_final.csv.

Coordinates are used for display only; no analysis uses them. Positions are approximate (typically within 1-2 km).
Inputs and precedence (owner, 03/11/2026):
1. Google Maps points picked by Hiếu/Nam (data/meta/station_coords_check.csv: rows marked done, Hòa Bình's corrected
   point, and their choice of Nam's point for Vàm Kênh and Đại Ngãi).
2. Published coordinates, CC BY 4.0 (prefilled in the check sheet): Zenodo 10.5281/zenodo.23497554 (Nguyen H.T.T.
   et al. 2026; source "Station forms (SRHMC)") preferred over Zenodo 10.5281/zenodo.20003854 (Nguyen D.Q.H. et al.
   2026). Hiếu/Nam could not see gauge buildings at these points; accepted as approximate display positions.
3. OpenStreetMap (ODbL, © OpenStreetMap contributors): the point of the named river nearest the same-name locality
   (data/meta/station_coords_osm.csv, built by snapping Nominatim localities to Overpass waterways; panels checked
   by eye). Thạnh Phú: K. Như Gia is not in OSM, so the locality point is used.
Stations left empty: Cầu Nổi (OSM match was a same-name place in Tây Ninh, rejected), Xuân Hòa, Láng Thé (not found).
None of the three is among the 28 NCHMF bulletin stations shown on the map.
"""
import pandas as pd

chk = pd.read_csv("data/meta/station_coords_check.csv", encoding="utf-8-sig", dtype=str).fillna("")
chk = chk[chk["station"].str.strip() != ""].set_index("station")
osm = pd.read_csv("data/meta/station_coords_osm.csv", encoding="utf-8-sig").set_index("station")

NAM_PICK = {"Vàm Kênh": (10.27527689, 106.7377838), "Đại Ngãi": (9.734356059, 106.0739702)}  # from the sheet notes
rows = []
for s, r in chk.iterrows():
    task = r["viec_can_lam"]
    lat = lon = None; src = quality = ""
    if s in NAM_PICK:
        lat, lon = NAM_PICK[s]; src, quality = "Google Maps (Nam), chosen by Hiếu/Nam over the published point", "checked"
    elif task.startswith("XONG"):
        lat, lon = float(r["lat"]), float(r["lon"]); src, quality = "Google Maps (Nam)", "checked"
    elif s == "Hòa Bình":
        lat, lon = float(r["lat"]), float(r["lon"]); src, quality = "Google Maps (Hiếu/Nam), corrected point", "checked"
    elif r["lat"] and task.startswith(("XÁC NHẬN", "KIỂM TRA")):
        lat, lon = float(r["lat"]), float(r["lon"])
        src = r["coord_source"]; quality = "published, approximate"
    elif s in osm.index and str(osm.at[s, "status"]).startswith("OK"):
        lat, lon = float(osm.at[s, "lat"]), float(osm.at[s, "lon"])
        src = f"OpenStreetMap (ODbL): {osm.at[s, 'river_name_osm']} nearest to {osm.at[s, 'loc_name'].split(',')[0]}"
        quality = "approximate (river point nearest the named locality)"
    elif s == "Thạnh Phú" and s in osm.index:
        lat, lon = float(osm.at[s, "loc_lat"]), float(osm.at[s, "loc_lon"])
        src, quality = "OpenStreetMap (ODbL): locality Thạnh Phú (K. Như Gia not in OSM)", "approximate (locality)"
    rows.append(dict(station=s, lat=lat, lon=lon, coord_source=src, coord_quality=quality))

out = pd.DataFrame(rows)
out.to_csv("data/meta/station_coords_final.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    bulletin = list(chk.index[:28])  # the first 28 rows are the NCHMF bulletin stations
    got = out.set_index("station").loc[bulletin, "lat"].notna()
    assert got.all(), list(got[~got].index)
    assert out["lat"].dropna().between(8.5, 11.0).all() and out["lon"].dropna().between(104.4, 107.1).all()
    assert out.set_index("station").loc["Sơn Đốc", "lat"] > 10.05  # station-forms source chosen
    print(out["lat"].notna().sum(), "of", len(out), "stations with coordinates; all 28 bulletin stations present")
    print(out["coord_quality"].value_counts().to_string())
