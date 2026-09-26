# Umeki 2025 EGF-SOS-RAF depth-versus-temporal Bio Chi freeze v0.1

**Date:** 25 September 2026  
**Branch:** `bio-chi-erk-egf-depth-rate-p0q-20260925`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct single-cell representation qualification

## Source

Umeki N, Kabashima Y, Sako Y. *Evaluation of information flows in the RAS-MAPK system using transfer entropy measurements*. eLife. 2025;14:e104432. DOI: `10.7554/eLife.104432`.

Pinned source repository:

- repository: `YasushiSako/transfer_entropy_2`
- upstream commit: `3467850de2e45dfc2b7766ba4dce0d7af8839a00`
- README blob: `80d5e6fea3ac83493a6d905a16806376e8d3755e`

The source reports simultaneous single-cell SOS and RAF membrane-translocation trajectories, sampled at 1-minute intervals, under four EGF doses. The source publication and qualitative dose-response behavior were inspected during candidate selection. Therefore this experiment does not claim blinded discovery of an EGF dose effect.

## Frozen source files

Wild-type, no-MEK-inhibitor dose series only:

| EGF dose | SOS file / blob | RAF file / blob |
| --- | --- | --- |
| 0.1 ng/mL | `EGF dose dynamics data/SOS_wt_EGF01ng.csv` / `157404e86adf690e67fa0d52fcaed553023a2ed6` | `EGF dose dynamics data/RAF_wt_EGF01ng.csv` / `1994dd3dd45f59110bb37257e7411e9fa5232c71` |
| 1 ng/mL | `EGF dose dynamics data/SOS_wt_EGF1ng.csv` / `69e15154cd06db9489872811a05f889ecf669665` | `EGF dose dynamics data/RAF_wt_EGF1ng.csv` / `17e81faafa8b6a32c8f8ad77c2e9fa4d35b16e2a` |
| 10 ng/mL | `EGF dose dynamics data/SOS_wt_EGF10ng.csv` / `5b1eda54b292fb60b2d66058cef08f40cb988d77` | `EGF dose dynamics data/RAF_wt_EGF10ng.csv` / `61b5f598347b29a1d084c9e8c1239b05070fb375` |
| 100 ng/mL | `EGF dose dynamics data/SOS_wt_EGF100ng.csv` / `b21c017747e6856e30391d45e71f3f36da06a1a9` | `EGF dose dynamics data/RAF_wt_EGF100ng.csv` / `a866a47924026b06c89a834359a236126abb9dcc` |

The README states that the first column contains time in minutes and subsequent columns are single-cell signals, with the same cell index pairing SOS and RAF measured simultaneously.

## Whole biological event

The frozen event is:

[
	ext{EGF input magnitude}
ightarrow
	ext{paired SOS/RAF recruitment dynamics}
ightarrow
	ext{temporal persistence / return organization}.
]

The experiment asks whether the temporal organization of the response is fully determined by early response depth, or whether input magnitude contains additional predictive information after early depth is accounted for.

## Source preprocessing

The published source trajectories are already downstream response signals after the source image-processing pipeline. No new smoothing, baseline subtraction, sign flip, clipping of the raw trajectory, or outcome-dependent cell filtering is permitted.

For each dose:
1. parse the first column as time in minutes;
2. pair SOS and RAF columns by exact source cell index;
3. retain time points from 0 through 60 min inclusive;
4. require at least 90% finite paired time points for a cell;
5. no cell is removed for numerical extremeness.

## Frozen per-cell depth coordinates

For each paired cell:

- `SOS_peak_early`: maximum SOS response from 0-15 min;
- `RAF_peak_early`: maximum RAF response from 0-15 min.

These two coordinates define the early response-depth vector (D).

They are descriptive source-response coordinates and are not scalar `chi_bio`.

## Frozen temporal-organization coordinates

For each channel (X in {SOS,RAF}), define positive response
[
X_+(t)=max(X(t),0).
]

Then define:

1. **late persistence fraction**
[
P_X=
rac{int_{30}^{60}X_+(t)dt}
{int_{0}^{60}X_+(t)dt}.
]

2. **late response centroid**
[
C_X=
rac{int_{15}^{60}tX_+(t)dt}
{int_{15}^{60}X_+(t)dt}.
]

The frozen temporal vector is
[
T=[C_{SOS},P_{SOS},C_{RAF},P_{RAF}].
]

If either required denominator is zero or nonfinite, the corresponding cell is recorded as a representation failure and excluded only from tests requiring that coordinate.

## Primary depth-versus-input test

The primary question is whether log EGF dose improves held-out prediction of (T) beyond early depth (D).

Use leave-one-dose-out cross-validation across 0.1, 1, 10, and 100 ng/mL.

Within every fold, standardize all predictors and outcomes using training cells only.

### M0: early-depth model

For each temporal coordinate:
[
T_j =
eta_0+
eta_1 z_{SOSpeak}+
eta_2 z_{RAFpeak}+
eta_3 z_{SOSpeak}^{2}+
eta_4 z_{RAFpeak}^{2}+
eta_5 z_{SOSpeak}z_{RAFpeak}.
]

### M1: early depth plus input magnitude

Add:
[
eta_6 z_{log_{10}dose}+
eta_7 z_{log_{10}dose}z_{SOSpeak}+
eta_8 z_{log_{10}dose}z_{RAFpeak}.
]

Fit by ordinary least squares. No regularization or feature selection is permitted in the primary analysis.

Primary statistic:
[
I=(MSE_{M0}-MSE_{M1})/MSE_{M0}
]
using all held-out cells and all four temporal coordinates.

### Bootstrap

Use 2,000 nonparametric block-bootstrap resamples, seed `20260925`, resampling paired cells with replacement within each dose while preserving dose sample sizes. Re-run the complete leave-one-dose-out analysis for every resample.

Frozen disposition:

- `INPUT_MAGNITUDE_ADDS_TEMPORAL_INFORMATION_P0Q` if observed (I ge 0.25) and bootstrap 95% CI lower bound > 0;
- `EARLY_DEPTH_SUFFICIENT_FOR_TEMPORAL_ORGANIZATION_P0Q` if observed (I le 0.10) and bootstrap 95% CI upper bound <= 0.10;
- otherwise `DEPTH_VS_INPUT_TEMPORAL_ORGANIZATION_UNRESOLVED_P0Q`.

Coordinate-level improvements are descriptive only and cannot override the aggregate rule.

## Secondary representation-adequacy test

Construct the six-coordinate paired response vector
[
R=[
SOS_{peak},
RAF_{peak},
C_{SOS},
P_{SOS},
C_{RAF},
P_{RAF}
].
]

Using the same leave-one-dose-out folds:
1. standardize coordinates from training cells only;
2. fit PCA rank 1 on training cells;
3. reconstruct held-out cells.

A one-coordinate compression is adequate only if:
- total held-out standardized MSE <= 0.25; and
- every coordinate has held-out RMSE <= 0.75.

Otherwise the response requires a multicoordinate `Chi_bio` representation at this evidence level.

This is a representation adequacy test, not a mechanistic PCA claim.

## Three-object hierarchy

- **Biological chi:** the whole EGF-input -> paired SOS/RAF recruitment -> temporal organization relation.
- **Chi_bio:** the minimum supported multicoordinate paired signaling representation.
- **chi_bio:** **NOT OPENED at freeze**. The source trajectories and transfer-entropy analysis do not independently identify a damping-mode scalar. Empirical response times, PCA scores, EGF dose, or response amplitude may not be renamed `chi_bio`.

No `chi_bio=1` boundary is tested.

## Source-reproduction gates

Before any SymC-specific interpretation:
- source file blobs must match the frozen identities;
- SOS and RAF time axes must match within dose;
- paired cell-index intersection must be nonempty;
- source cell counts must be recorded and compared with publication-reported approximate totals;
- all four doses must be present.

A source gate failure returns a preserved source/refusal record and lower-level mathematics cannot rescue the experiment.

## Failure and outlier handling

Every parse failure, missing pair, insufficient finite trajectory, zero-denominator temporal coordinate, or numerical failure is retained by dose and cell identity.

No outlier is removed solely because it weakens a relationship or lies far from the population mean.

## Claim ceiling

This is one direct single-cell RAS-MAPK signaling system in SOS-knockout HeLa cells expressing the source probes. It can qualify representation and depth-versus-temporal organization only within this source. It cannot establish a universal biological chi law, a universal RAS-MAPK stability scalar, a cancer-wide mechanism, or a universal substrate-inheritance rule.
