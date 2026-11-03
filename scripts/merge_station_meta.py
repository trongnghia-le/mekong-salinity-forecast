"""Merge two independent station-metadata passes (data/meta/station_meta_A.csv, _B.csv) into station_meta.csv.
Province: agreed values. Coordinates: from data/meta/station_coords_final.csv (scripts/build_station_coords.py;
display only, approximate; sources and quality per station there). Sluice status: kept only when both passes agree
on a non-unknown value; still 'reasoned', not map-based."""
import pandas as pd

a = pd.read_csv("data/meta/station_meta_A.csv", encoding="utf-8-sig").set_index("station")
b = pd.read_csv("data/meta/station_meta_B.csv", encoding="utf-8-sig").set_index("station")
c = pd.read_csv("data/meta/station_coords_final.csv", encoding="utf-8-sig").set_index("station")
out = b[["river", "km_from_mouth", "province_old", "province_new"]].copy()
out["province_old"] = out["province_old"].str.replace("TP Hồ Chí Minh", "Hồ Chí Minh")
out["lat"] = c["lat"].reindex(out.index)
out["lon"] = c["lon"].reindex(out.index)
out["coord_source"] = c["coord_source"].reindex(out.index).fillna("none")
out["coord_quality"] = c["coord_quality"].reindex(out.index).fillna("none")
sa, sb = a["sluice_status"].reindex(out.index), b["sluice_status"]
agree = sa.eq(sb) & sb.ne("unknown")
out["sluice_status"] = sb.where(agree, "to_verify")
out["sluice_basis"] = agree.map({True: "both passes agree (reasoning, no boundary map)", False: "passes disagree or unknown"})
out.to_csv("data/meta/station_meta.csv", encoding="utf-8")

if __name__ == "__main__":
    assert len(out) == 37 and out["province_new"].notna().all()
    assert out["lat"].notna().sum() == 34, out["lat"].notna().sum()
    print(out["lat"].notna().sum(), "stations with coordinates;",
          out["sluice_status"].eq("to_verify").sum(), "sluice to verify")
