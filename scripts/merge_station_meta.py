"""Merge two independent station-metadata passes (data/meta/station_meta_A.csv, _B.csv) into station_meta.csv.
Province: agreed values. Coordinates: left empty for every station until a human check (owner, 01/11/2026:
Zenodo/OSM points not trusted); filled later from data/meta/station_coords_check.csv.
Sluice status: kept only when both passes agree on a non-unknown value; still 'reasoned', not map-based."""
import pandas as pd

a = pd.read_csv("data/meta/station_meta_A.csv", encoding="utf-8-sig").set_index("station")
b = pd.read_csv("data/meta/station_meta_B.csv", encoding="utf-8-sig").set_index("station")
out = b[["river", "km_from_mouth", "province_old", "province_new"]].copy()
out["province_old"] = out["province_old"].str.replace("TP Hồ Chí Minh", "Hồ Chí Minh")
out["lat"] = float("nan")
out["lon"] = float("nan")
out["coord_source"] = "to_verify"
sa, sb = a["sluice_status"].reindex(out.index), b["sluice_status"]
agree = sa.eq(sb) & sb.ne("unknown")
out["sluice_status"] = sb.where(agree, "to_verify")
out["sluice_basis"] = agree.map({True: "both passes agree (reasoning, no boundary map)", False: "passes disagree or unknown"})
out.to_csv("data/meta/station_meta.csv", encoding="utf-8")

if __name__ == "__main__":
    assert len(out) == 37 and out["province_new"].notna().all()
    assert out["lat"].isna().all()
    print(out["coord_source"].eq("to_verify").sum(), "coords to verify;",
          out["sluice_status"].eq("to_verify").sum(), "sluice to verify")
