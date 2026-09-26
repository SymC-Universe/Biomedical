# Meneses 2026 E. coli PMF recovery Bio Chi closure

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Primary evidence class:** P0-Q, literature-open direct experimental qualification

## Status

The direct experimental whole-event gate is admitted at P0-Q. The source-released E. coli osmotic-shock data reproduce the frozen bead trace inventories and the orthogonal TMRM/cell-area population summaries. A first executable artifact produced a false-negative whole-event disposition because it introduced an unfrozen finite-normalized-track-count veto; that artifact remains preserved, and a pre-rerun implementation audit documents the repair.

The repaired primary result is pinned in `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`. A separate post-result source-method reconciliation against the manuscript-facing sucrose fitting lane is pinned in `BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`.

## Source reproduction

Immediate motor trace counts reproduced exactly: 8, 10, 8, and 12 traces at 200, 300, 400, and 500 mM. Sustained-adaptation counts reproduced exactly: 8, 8, 8, and 4.

All frozen TMRM and cell-area population summaries reproduced within the specified tolerances. Raw source-track counts were 40 per orthogonal-assay condition. TMRM finite-normalized contributing-track counts were 39, 40, 39, 39, and 38 for control through 500 mM; this difference is a normalization diagnostic, not a frozen admission gate.

The original freeze inherited a DOI-like PII string from repository metadata. Publication metadata are corrected here without changing the source data identity: Meneses et al., *Biophysical Journal* (2026), DOI `10.1016/j.bpj.2026.04.014`.

## Primary P0-Q result

The shock-depth coordinates changed monotonically with dose. In the frozen primary fit lane, median collapse amplitude increased from 0.2850 at 200 mM to 0.9119 at 500 mM (Spearman rho = 1.0), while sustained adaptation plateau decreased from 0.8159 to 0.4065 (rho = -1.0).

The stronger frozen hypothesis that depth could vary while all three rate coordinates remained dose-robust **failed**. Collapse tau, post-removal recovery tau, and sustained-adaptation tau did not jointly satisfy the fixed rho and max/min-ratio rule. The disposition is `FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q`. This failure is retained and is not rewritten as a positive timescale-invariance result.

The nine-coordinate condition representation also refused one-dimensional compression. PC1 explained 0.6621 of standardized variance and the maximum absolute standardized one-dimensional reconstruction residual was 1.1145, versus frozen adequacy requirements of at least 0.95 and at most 0.10, respectively. The retained lower representation is therefore `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q`.

Scalar `chi_bio` remains `NOT_OPENED_NOT_LICENSED`. The source sigmoid/exponential time constants summarize response kinetics but are not independently licensed mechanistic modal carriers.

The whole-system result is `DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q`.

## Fit anomaly and root cause

The unconstrained four-parameter primary lane returned one sign-reversed but finite 200 mM collapse fit for `cell8`: (A_{dec}=-0.269898), (	au_{dec}=-1.54594). Because simultaneous amplitude/tau sign reversal is an algebraically equivalent sigmoid parameterization with a shifted offset, the trace is not deleted. The anomaly motivated the independent source-method reconciliation rather than a post-result filter.

## Source-method reconciliation

The manuscript-facing source lane fixes collapse amplitude from the 155--175 s and 215--235 s windows and fits positive (	au_{dec}) and (t_0). It produced no immediate or sustained fit failures.

The representation conclusion survived. PC1 explained 0.7720, the maximum standardized one-dimensional reconstruction residual was 1.2037, and one-dimensional adequacy again failed. The multicoordinate `Chi_bio` disposition is therefore `SOURCE_METHOD_ROBUST_AT_P0Q`.

The stronger rate-depth rule also failed in the manuscript-facing lane. In particular, post-removal recovery tau decreased monotonically with dose (rho = -1.0), and sustained-adaptation tau remained strongly variable (rho = 0.8; max/min ratio 3.46). This reconciliation cannot promote the primary evidence but demonstrates that the central multicoordinate/refusal result is not an artifact of the older four-parameter fit path.

## Joint interpretation

This experiment supplies the direct experimental layer that the preceding HOG model qualification lacked. It supports a whole-event biological chi relation between osmotic perturbation, energetic/physical organization, and realized recovery while refusing both a one-coordinate `Chi_bio` compression and an unlicensed scalar `chi_bio`.

The result is not a universal biological chi law. It is one directly measured E. coli perturbation system, literature-open at P0-Q, with source-method robustness for the representation conclusion.

## Workflow identities

Primary repaired run: `36216252676`  
Primary artifact: `10897836350`  
Primary artifact digest: `sha256:33e2c253ffb19abe1d3679116df768e08012cc6181cd910a38c3976b4bf77c3f`

Preserved false-negative run: `36216125834`  
Preserved false-negative artifact: `10898060524`  
Preserved false-negative digest: `sha256:0e6d640aae38c5e2d906b4dbce7a887e89628d9d97176fb6df5cc8141683ea09`

Source-method reconciliation run: `36216368561`  
Reconciliation artifact: `10897991063`  
Reconciliation digest: `sha256:0534f1173b51a4d4fc4459bdb28a800a7759968f96119434d5f7ea35c1308dc9`

## What happens next and why

The next experiment should not repeat another dose-response compression attack. This source has already shown that collapse depth, rapid recovery, sustained adaptation, membrane-potential displacement, and cell-size recovery do not behave as one coordinate. The next useful Bio Chi test is a **same-system perturbation-path comparison** or a **cross-system transport test** that can ask whether the multicoordinate recovery architecture itself is conserved, reorganized, or refused.

No user intervention is required before that next freeze.
