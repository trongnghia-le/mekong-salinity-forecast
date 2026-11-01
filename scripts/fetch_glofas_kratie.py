"""Daily GloFAS v4 river discharge at Kratie (Mekong main stem) via the Open-Meteo Flood API.

The gauge coordinate falls on a tributary cell, so we scan the 0.05 deg grid around it and keep the
cell with the largest mean discharge (the main stem). Output: data/raw/glofas/kratie_glofas_daily.csv
Source: GloFAS (Copernicus EMS) via Open-Meteo, CC BY 4.0 - cite both.
"""
import csv
import json
import time
import urllib.request
from datetime import date
from pathlib import Path

KRATIE = (12.481, 106.018)  # MRC gauge 014901
API = "https://flood-api.open-meteo.com/v1/flood"
UA = {"User-Agent": "mekong-salinity-research/0.1"}
OUT = Path(__file__).resolve().parents[1] / "data/raw/glofas/kratie_glofas_daily.csv"


def get(lat, lon, start, end):
    url = f"{API}?latitude={lat:.3f}&longitude={lon:.3f}&daily=river_discharge&start_date={start}&end_date={end}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return json.load(r)


def main():
    best = None
    steps = [i * 0.05 for i in range(-3, 4)]
    for dlat in steps:
        for dlon in steps:
            d = get(KRATIE[0] + dlat, KRATIE[1] + dlon, "2023-01-01", "2023-12-31")
            q = [v for v in d["daily"]["river_discharge"] if v is not None]
            mean = sum(q) / len(q) if q else 0
            print(f"{d['latitude']:.3f} {d['longitude']:.3f} mean2023={mean:10.1f}")
            if best is None or mean > best[0]:
                best = (mean, d["latitude"], d["longitude"])
            time.sleep(0.3)
    mean, lat, lon = best
    print(f"main-stem cell: {lat:.3f}, {lon:.3f} (2023 mean {mean:.0f} m3/s)")
    # Plausibility: Mekong at Kratie averages roughly 13,000-14,000 m3/s.
    assert 5000 < mean < 30000, "best cell is not the Mekong main stem"

    d = get(lat, lon, "1984-01-01", date.today().isoformat())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "q_m3s", "lat", "lon"])
        for t, v in zip(d["daily"]["time"], d["daily"]["river_discharge"]):
            if v is not None:
                w.writerow([t, v, lat, lon])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
