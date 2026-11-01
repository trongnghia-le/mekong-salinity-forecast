# Layer A decision run log (scripts/run_h4.py, seed 20261101, 2000 resamples)

Self-check: passed (perfect information has the highest mean return at every C/L; perfect forecast REV = 1; climatology vs itself REV = 0; break-even solves equality and lies in [0,1]).

## Choices where protocol section 8 / D4 was not explicit
- Parameters: L25-based loss model (pi_bar, b, S_bar per group) from decision_parameters.md, 'Loss model' section, in 2025 VND (x1.197 for slopes); Cost2 20.0 floor; S capped at 14 (10, 20 sensitivity); slope SE: 0.0795 and 0.1358 M VND nominal x 1.197.
- Delta_sev = 10.1 M VND/ha (F22 abstract 10.0-10.2, 2025 VND) for both field types in the main run; 8.3 (L25 gated average) as sensitivity. Delta is a constant (no S dependence; the file says no source for it).
- C/L grid 0.05-0.95 step 0.05; for each r, m = -r*Delta_sev/(1-r) (so m < 0 throughout). The m >= 0 case is reported separately (returns_by_strategy.csv regime=literature_m), where the forecast threshold is set to 0 (always act).
- Strategies: fixed = never act; always; climatology = act if the fold's training base rate of the same station (p_clim column) > C/L; forecast = act if p_severe > C/L; perfect = act iff gain > 0.
- Early-sowing return = max(-Cost2, profit_std + gain) (floor also after acting). The floor never binds in the main run.
- REV in return form: (R_fc - R_ref)/(R_perfect - R_ref); reference = fixed calendar or climatology. Undefined REV (zero denominator, FAO f=0.1 where Delta_i = 0) is set to 0 in areas.
- Tests use the area of the regret reduction (M VND/ha x C/L, a money quantity) as the primary statistic; REV areas are reported alongside.
- Bootstrap: seasons resampled together (all stations), same resamples for gated, ungated and their difference; separate resample set (same seed) for the tercile sample.
- H4 (c) evaluated on the regret-reduction areas vs fixed AND vs climatology (both must have CI > 0). H4 (a), (b) require both field types.
- FAO variant: ECe = 1.56 f S, Y_rel = max(0, 1 - 0.12 (ECe - 3)), loss = 43.4 M x (1 - Y_rel), profit_std = max(-20, 23.4 - loss); gated f = 0.2 x ungated f; early-sowing gain in a severe season = min(Delta_sev, loss) (a recovered amount cannot exceed the loss; my choice). With f = 0.1 field salinity never exceeds the threshold, so Delta = 0 and the forecast has no value by construction.
- Break-even: representative S = pooled mean of capped smax over severe (11.49) / non-severe (7.54) station-seasons (stations differ in level, Son Doc is much higher; not station-specific). Main m = midpoint of the file's range (gated 4.15, ungated 0.25), k = 0.4, F = 3.15 (rent anchor). Option 3 = profit with slope x k, plus 364 kg/ha x 6.62 k VND/kg (price 5.451 x 1.215), minus 458 VND/kg x yield (yield slope also x k). The +364 kg gain is an average over mixed salinity, so it may double count with k: sweep includes a no-yield-gain variant.
- Sweep: m (9 values over the group range) x k (0.2-0.6, 5) x F (0-3.15, 7) x yield-gain on/off; reported min/max p* where a crossing in [0,1] exists and the share of sweep points with a crossing. Delta_sev fixed at 10.1 in the sweep.

## Proposed deviations (not applied; docs/protocol.md untouched)
1. H4 part (c) cannot be tested in a meaningful way with the D4 model as specified: with a constant Delta the REV curve does not depend on the field type (except via the -Cost2 floor at C/L >= 0.75, an artefact), so (c) cannot reflect a real inside/outside effect. Proposal for the owner: either state in the protocol that (c) is evaluated through the plausible C/L range per field type (gated: m >= 0, no tradeoff; ungated: C/L up to about 0.29), or specify an S/field-dependent Delta (no source exists).
2. The tercile run uses the same Delta and loss model; base rate 0.34 so the always-act threshold shifts.

## Fig. 8 redrawn (owner decision 02/11/2026)
The first fig08 fixed m at the midpoint of the literature range, which made early sowing look always best. That m has no direct estimate: the gated range came from Le 2025 calendar-compliance effects, not from an early-sowing estimate. The figure now shows the break-even P(severe) p* = -m/(Delta_sev - m) as a function of m (m < 0; m >= 0 means early sowing is never worse), for Delta_sev 10.1 (Ferrer) and 8.3 (Le), with the out-of-sample P(severe) histogram on the same y axis. p* does not depend on field type (constant Delta), so there is one main panel, not two. Panel b: standard vs salt-tolerant variety break-even over k 0.2-0.6, by field type, with and without the 364 kg/ha yield gain. Skipping the season is dominated in the whole sweep (asserted: True). The breakeven.csv table (main m = range midpoints) is unchanged and should not be read as a result about m.
Thresholds (p*, share of the 70 forecasts above p*): Delta_sev 10.1, m -2: p* 0.165, share above 0.77; Delta_sev 10.1, m -4: p* 0.284, share above 0.70; Delta_sev 8.3, m -2: p* 0.194, share above 0.76; Delta_sev 8.3, m -4: p* 0.325, share above 0.66

## Items for the observation log (controller)
- Specification gap: a gated/ungated split in a cost-loss framework is invariant unless the action effect itself differs by group.
