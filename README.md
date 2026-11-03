# Probabilistic dekadal salinity forecasts for the Mekong Delta, Vietnam

Code, frozen analysis protocol, aggregated scores and figures for a study of **10-day (dekadal) maximum salinity
forecasts at the 28 stations of the national salinity bulletin** of Vietnam's National Center for
Hydro-Meteorological Forecasting (NCHMF). The study has four parts:

- **Probabilistic forecasts.** Quantile forecasts with conformal 90% intervals, and probabilities of exceeding 1, 2
  and 4 g/L, scored against persistence, station climatology and the **official NCHMF forecast**.
- **Spatial transfer.** The same forecasts tested at stations and provinces left out of training, in addition to
  forward-in-time testing.
- **Economic value.** The relative economic value of the calibrated probabilities, compared with the official
  deterministic forecast.
- **Seasonal decision layer.** A 1 November severe-season forecast at three long-record gauges, its value for the
  early-sowing decision of winter–spring rice (a scenario analysis), and break-even probabilities for crop options.

> **Status:** research code for a manuscript in preparation. It is **not peer reviewed**, **not an official
> forecast** and **not farm advice**.

**Authors:** Trong Nghia Le, Viet Nam Nguyen, Minh Hieu Ho and Thien Bao Nguyen (corresponding author). All are at
the Institute of Intelligent and Interactive Technologies (3ITech), University of Economics Ho Chi Minh City (UEH),
Vietnam.
**Funding:** This research is funded by University of Economics Ho Chi Minh City, Vietnam (UEH).

---

## Contents

1. [Repository layout](#repository-layout)
2. [Study design in brief](#study-design-in-brief)
3. [Pre-registration: the frozen protocol](#pre-registration-the-frozen-protocol)
4. [Data sources and licences](#data-sources-and-licences)
5. [Reproducing the results](#reproducing-the-results)
6. [Outputs](#outputs)
7. [Interactive atlas](#interactive-atlas)
8. [What is not in this repository, and why](#what-is-not-in-this-repository-and-why)
9. [Citation and licence](#citation-and-licence)

---

## Repository layout

```
docs/
  protocol.md                 Frozen analysis protocol (git tag protocol-v1) and its "Deviations after freeze" log
  paper_notes.md              Dated log of every result, decision, figure and number used in the manuscript
  ke_hoach_trien_khai.md      Project plan (Vietnamese)
  huong_dan_kiem_tra_toa_do.md  Guide for the manual station-coordinate check (Vietnamese)
  background/                 Data-source survey, novelty checks, venue notes, decision-parameter sources
data/
  meta/                       Station metadata and coordinates (see "Station coordinates" below)
  raw/        (not tracked)   Downloaded source files
  processed/  (not tracked)   Parsed tables and the feature matrix
scripts/                      Every step of the pipeline (see "Reproducing the results")
results/
  core_b/                     Dekadal forecasts: metrics, bootstrap CIs, reliability, value curves, verdicts
  layer_a/                    Seasonal severe-season forecast: leave-one-season-out forecasts and scores
  layer_a_decision/           Sowing-decision value (H4) and crop-option break-even
figures/                      Figures (PNG 300 dpi, SVG, vector PDF) and captions.md
atlas/                        Static interactive atlas (Leaflet + JSON), scores only
```

## Study design in brief

| Item | Choice |
|---|---|
| Target | Maximum salinity of the next dekad (g/L) at each bulletin station, one dekad ahead (the official forecast's horizon) |
| Stations | The 28 stations of the NCHMF bulletin (Table 1 of each bulletin); 9 provinces before the 2025 merger; 1.5–120 km from the river mouth, plus 2 inland canals |
| Predictors | Values known on the issue date only: the current dekadal maximum and its change; GloFAS v4 discharge at Kratie (Cambodia), lagged by an assumed 5-day latency; ENSO (ONI); astronomical spring–neap and perigee indices; static station attributes |
| Models | Linear quantile regression (QR) and gradient-boosted quantile regression (HGB) on log(1+S), 19 quantile levels |
| Intervals | Conformalized quantile regression (CQR) with cross-conformal (CV+) calibration over season folds; Mondrian variant by distance-to-mouth group |
| Test designs | Forward-by-season (test seasons 2023–24 to 2025–26; 27 issue dates, 732 station-dekads); leave-station-out; leave-province-out; an exploratory 2020 extreme-season check |
| Benchmarks | Persistence, station climatology and the **official NCHMF forecast** (Table 2 of each bulletin) |
| Value | Relative economic value (Richardson 2000) at 4 g/L over cost/loss ratios 0.1–0.9 |
| Seasonal layer | Logistic severe-season forecast issued on 1 November at Cầu Quan, Sơn Đốc and Trà Vinh, leave-one-season-out; regret-based cost/loss evaluation of early sowing; break-even probabilities for crop options |
| Inference | Paired bootstrap 95% CIs (issue dates resampled within seasons, 2,000 resamples) |

### Hypotheses and verdicts

The verdicts follow the frozen protocol's criteria literally. Full numbers are in `results/core_b/verdicts.md` and
`results/layer_a_decision/verdict_h4.md`.

| Hypothesis | Verdict |
|---|---|
| H1: the pooled model beats persistence, climatology and the official forecast on MAE | Not supported. The model matches the official forecast and persistence but does not beat them |
| H2a: conformal 90% intervals are calibrated in forward testing | Supported for HGB |
| H2b: plain conformal coverage drops under spatial transfer and Mondrian calibration restores it | Not supported. Coverage did not drop, so the premise did not occur |
| H3: calibrated 4 g/L probabilities have a higher economic value than the official forecast | Supported |
| H4: the seasonal forecast reduces regret relative to (a) a fixed calendar and (b) climatology | Not supported. Part (a) holds; part (b) does not |

## Pre-registration: the frozen protocol

`docs/protocol.md` was frozen before any model was scored on a test season. It is tagged **`protocol-v1`**
(commit `1d72a22`). Every later change is dated and justified in its "Deviations after freeze" section, entries
D1–D6. Rules that the code enforces:

- Only information available at bulletin issue time may enter a forecast. A self-check in
  `scripts/build_features.py` asserts this.
- Every model is scored against persistence and the official forecast, and unsupported hypotheses are reported.

## Data sources and licences

| Source | Used for | Licence or terms | In this repository |
|---|---|---|---|
| NCHMF salinity bulletins, 2019–2026 (live archive and Internet Archive copies) | Target, and the official-forecast benchmark | © NCHMF; no reuse terms found | **Transcribed values are not redistributed** (permission requested). Code and aggregated scores only |
| Open Development Vietnam CSV, Jan–Mar 2021 dekads | Training rows; cross-check of the parser | CC BY-SA 4.0 | Not redistributed raw. Derived files share CC BY-SA |
| GloFAS v4 river discharge (Copernicus), via the Open-Meteo Flood API | Discharge predictors | CC BY 4.0 | Fetched by script |
| NOAA CPC Oceanic Niño Index | ENSO predictor | Public domain | Fetched by script |
| Apel et al. (2024), GFZ Data Services: Sơn Đốc salinity 1996–2016 and Tân Châu discharge | Seasonal-layer target and predictor | CC BY 4.0 | Download manually (see below) |
| Binh et al. (2019), Mendeley Data: Cầu Quan and Trà Vinh salinity 1990–2016 | Seasonal-layer target | CC BY 4.0 | Download manually |
| PCTT daily reports, Feb–May 2020 (4 stations) | Exploratory 2020 check | No terms stated | Scores only |
| Published farm-economics estimates (Le et al. 2025; Ferrer et al. 2022; Mills et al. 2022, 2025) | Decision-layer parameters | Cited | `docs/background/decision_parameters.md` |
| Natural Earth 1:10m | Basemap of the study-area map | Public domain | Downloaded by `make_fig00_map.py` |

No data from the Mekong River Commission portal are used.

### Station coordinates

Coordinates are used **for display only** (the map and the atlas); no analysis uses them. Positions are
approximate, typically within 1–2 km. `scripts/build_station_coords.py` writes `data/meta/station_coords_final.csv`,
which gives the source and quality of every station. The sources, in order of precedence:

1. Google Maps points checked by hand by the authors (`station_coords_check.csv`).
2. Published coordinates, CC BY 4.0:
   - Zenodo [10.5281/zenodo.23497554](https://doi.org/10.5281/zenodo.23497554), from station forms of the Southern
     Regional Hydro-Meteorological Centre;
   - Zenodo [10.5281/zenodo.20003854](https://doi.org/10.5281/zenodo.20003854).
3. OpenStreetMap: the point on the named river nearest the same-name locality (`station_coords_osm.csv`).
   **© OpenStreetMap contributors. These derived coordinates are available under the
   [ODbL](https://opendatacommons.org/licenses/odbl/).**

## Reproducing the results

### Environment

Windows 11 was used, with Python 3.10.9 and the following packages:

| Package | Version |
|---|---|
| scikit-learn | 1.7.2 |
| numpy | 1.26.4 |
| pandas | 2.2.3 |
| matplotlib | 3.10.3 |
| PyMuPDF | 1.28.0 |
| shapely | 2.1.2 |

There is no virtual environment. Run every script from the repository root. Use `-X utf8` because file names and
station names are Vietnamese, and `-I` for scripts that read downloaded files.

```bash
pip install scikit-learn==1.7.2 numpy==1.26.4 pandas==2.2.3 matplotlib==3.10.3 PyMuPDF==1.28.0 shapely==2.1.2
```

### Pipeline

| Step | Script | Output |
|---|---|---|
| 1. NCHMF bulletins | `probe_nchmf.py` (live archive), `wayback_nchmf.py` (Internet Archive) | `data/raw/nchmf/pdf/`, `inventory.csv` |
| 2. Parse bulletins | `parse_nchmf.py` (self-checks against two hand-read bulletins) | `data/processed/nchmf_obs.csv`, `nchmf_fc.csv` |
| 3. Cross-check | `odv_crosscheck.py`, `g0_stats.py` | Gate G0 statistics |
| 4. Discharge | `fetch_glofas_kratie.py` | `data/raw/glofas/kratie_glofas_daily.csv` |
| 5. 2020 daily reports | `fetch_pctt_2020.py`, `parse_pctt_2020.py` | `data/processed/pctt_daily_2020.csv` |
| 6. Long records | `tidy_long_records.py` | `data/processed/long_*.csv` |
| 7. Features | `build_features.py` (downloads the ONI) | `data/processed/features.csv` |
| 8. Dekadal forecasts (H1–H3) | `run_core_b.py` | `results/core_b/` |
| 9. Seasonal layer | `run_layer_a.py` | `results/layer_a/` |
| 10. Sowing decision (H4) and crop options | `run_h4.py` | `results/layer_a_decision/`, Figs. 8–9 |
| 11. Calibration summary | `calibration_summary.py` | `results/core_b/calibration_summary.csv` |
| 12. Station metadata | `build_station_coords.py`, `merge_station_meta.py` | `data/meta/station_meta.csv` |
| 13. Figures | `make_fig00_map.py`, `make_figures.py` | `figures/` |
| 14. Tables | `make_tables.py` | LaTeX tables (manuscript, not tracked) |
| 15. Atlas | `build_atlas_data.py` | `atlas/data/*.json` |

Download these files by hand first:

- the ODV CSV, to `data/raw/odv/salinization_2021_2022_vi.csv`;
- the GFZ data set, to `data/raw/gfz_sondoc/`;
- the Mendeley workbook, to `data/raw/mendeley_binh2019/binh2019_salinity.xlsx`.

The bootstrap and model seeds are fixed. `run_log.md` in each results folder records the settings of the run.

## Outputs

- `results/core_b/`:
  - `metrics.csv` and `bootstrap_ci.csv`: every metric for every design, variant, model and season;
  - `reliability.csv` and `rev_curve.csv`: reliability diagrams and value curves;
  - `verdicts.md`: the protocol verdicts;
  - `calibration_summary.csv`: reliability term and calibration error.
- `results/layer_a/`: leave-one-season-out severe-season probabilities (main run and sensitivity runs) and their
  scores.
- `results/layer_a_decision/`: regret, relative economic value, bootstrap CIs, break-even tables and the H4 verdict.
- `figures/`: Fig. 1 (study area) to Fig. 9 (break-even). The file names (`fig00`–`fig08`) predate the final
  numbering. Each figure comes as `.png`, `.svg` and `.pdf`; captions are in `figures/captions.md`.

## Interactive atlas

`atlas/` is a static Leaflet page. It shows station-level scores, reliability and value curves, and approximate
station positions. It holds **aggregated scores only** and no NCHMF values. To view it locally:

```bash
python -m http.server --directory atlas 8000
# then open http://localhost:8000
```

It will be published on GitHub Pages when the paper is published.

## What is not in this repository, and why

- **Transcribed NCHMF bulletin values** (`data/processed/`, `results/**/predictions*.csv`, `results/layer_a/extension.csv`).
  The bulletins carry no reuse terms. Permission to redistribute has been requested from NCHMF. Until it is granted,
  only code and aggregated scores are public.
- **Raw downloads** (`data/raw/`), **PDFs** and **papers**: third-party copyright.
- **The manuscript**: it will be shared through the journal after peer review. No preprint is posted.

## Citation and licence

Please cite the article once it is published; this README will be updated with the reference. Until then, cite
this repository and the commit you used.

Data keep their source licences (see the table above). Files derived from the ODV CSV are CC BY-SA 4.0, and
coordinates derived from OpenStreetMap are ODbL. No licence has yet been chosen for the code in this repository.
