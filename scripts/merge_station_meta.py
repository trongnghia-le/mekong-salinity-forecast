"""Merge two independent station-metadata passes (data/meta/station_meta_A.csv, _B.csv) into station_meta.csv.
Province: agreed values. Coordinates: pass B only when sourced (medium); everything else marked to_verify.
Sluice status: kept only when both passes agree on a non-unknown value; still 'reasoned', not map-based."""
import pandas as pd

a = pd.read_csv("data/meta/station_meta_A.csv", encoding="utf-8-sig").set_index("station")
b = pd.read_csv("data/meta/station_meta_B.csv", encoding="utf-8-sig").set_index("station")
out = b[["river", "km_from_mouth", "province_old", "province_new"]].copy()
out["province_old"] = out["province_old"].str.replace("TP Hồ Chí Minh", "Hồ Chí Minh")
med = b["coord_confidence"].eq("medium")
out["lat"] = b["lat"].where(med)
out["lon"] = b["lon"].where(med)
out["coord_source"] = b["coord_source"].where(med, "to_verify")
sa, sb = a["sluice_status"].reindex(out.index), b["sluice_status"]
agree = sa.eq(sb) & sb.ne("unknown")
out["sluice_status"] = sb.where(agree, "to_verify")
out["sluice_basis"] = agree.map({True: "both passes agree (reasoning, no boundary map)", False: "passes disagree or unknown"})
out.to_csv("data/meta/station_meta.csv", encoding="utf-8")

if __name__ == "__main__":
    assert len(out) == 37 and out["province_new"].notna().all()
    assert out.loc["Sơn Đốc", "coord_source"] != "to_verify"
    print(out["coord_source"].eq("to_verify").sum(), "coords to verify;",
          out["sluice_status"].eq("to_verify").sum(), "sluice to verify")
