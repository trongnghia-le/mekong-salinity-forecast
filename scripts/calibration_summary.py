"""Quantitative calibration of the exceedance probabilities (forward design, main variant, pooled test seasons).

Reads results/core_b/reliability.csv (10 equal-width probability bins, as in Fig. 4) and writes
results/core_b/calibration_summary.csv with, per model and threshold:
  rel      reliability term of the binned Murphy (1973) decomposition, sum_k n_k (p_k - o_k)^2 / N
  res      resolution term, sum_k n_k (o_k - o)^2 / N
  unc      uncertainty term, o (1 - o)
  ece      count-weighted mean |p_k - o_k| over bins
  n_extreme  forecasts in the two extreme bins (0.0-0.1, 0.9-1.0)
  ece_mid  count-weighted mean |p_k - o_k| over the eight intermediate bins
  bins_out_wilson95  non-empty bins whose mean probability lies outside the 95% Wilson interval of o_k
  n_bins   non-empty bins
  brier    Brier score of the model (metrics.csv), for scale
Run from the repository root: python -X utf8 scripts/calibration_summary.py
"""
import math
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "results", "core_b")
Z = 1.959964


def wilson(k, n):
    p, d = k / n, 1 + Z * Z / n
    c, h = (p + Z * Z / (2 * n)) / d, Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return c - h, c + h


def main():
    rel = pd.read_csv(os.path.join(R, "reliability.csv"))
    met = pd.read_csv(os.path.join(R, "metrics.csv"))
    sel = (rel.design == "forward") & (rel.variant == "main") & (rel.scope == "pooled")
    rows = []
    for (model, thr), g in rel[sel].groupby(["model", "threshold"]):
        g = g[g.n > 0]
        n, p, o = g.n.to_numpy(float), g.mean_prob.to_numpy(float), g.obs_freq.to_numpy(float)
        N = n.sum()
        obar = (n * o).sum() / N
        ext = g.bin.isin(["0.0-0.1", "0.9-1.0"]).to_numpy()
        out = sum(not (lo <= pk <= hi) for pk, (lo, hi) in zip(p, (wilson(round(ok * nk), nk) for ok, nk in zip(o, n))))
        brier = met[(met.design == "forward") & (met.variant == "main") & (met.scope == "pooled")
                    & (met.model == model) & (met.metric == f"brier_model_{thr}")].value.item()
        r = dict(model=model, threshold=thr, n=int(N), base_rate=obar,
                 rel=(n * (p - o) ** 2).sum() / N, res=(n * (o - obar) ** 2).sum() / N, unc=obar * (1 - obar),
                 ece=(n * abs(p - o)).sum() / N, n_extreme=int(n[ext].sum()),
                 ece_mid=(n[~ext] * abs(p[~ext] - o[~ext])).sum() / n[~ext].sum(),
                 bins_out_wilson95=int(out), n_bins=len(g), brier=brier)
        # self-check: binned REL - RES + UNC approximates the Brier score (exact up to within-bin variance terms)
        assert N == 732 and abs(r["rel"] - r["res"] + r["unc"] - brier) < 0.01, r
        rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(R, "calibration_summary.csv"), index=False, float_format="%.6g")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
