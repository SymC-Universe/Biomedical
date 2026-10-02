# Bio Chi Single-Series Uncertainty Method Comparison Postresult v1.0

**Status:** COMPLETE / P0-Q METHOD-FAMILY QUALIFICATION  
**Date:** 28 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** `NSD_vNext/docs/BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_PLAN_v0.2.md`  
**Freeze:** `NSD_vNext/docs/BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_FREEZE_v1.0.md`

## Provenance

- Source-of-record workflow: `NSD Single-Series Uncertainty Methods`
- Run: `36373507093`
- Complete artifact: `nsd-single-series-uncertainty-methods-complete`
- Artifact ID: `10950297393`
- Digest: `sha256:d736f1c04196efd95bb3949a8330ce4552a978ff5196a72f52c106c05e398572`
- Repeated-realization reference map: run `36372559076`, artifact `10949349324`, digest `sha256:7331b6781838d3cd4f97f68ecb8dbc301035bfa7cd0f16454ddd80169c16d194`
- Physical-coordinate likelihood equivalence gate: `NSD C1Q-RS Mechanical Contracts`, run `36373236094`

The source-of-record run completed its frozen profile preflights, eight profile/Hessian cases, fitted-model bootstrap cases, and final merge without scientific retuning. The earlier run `36373404832` remains superseded for final aggregation because its artifact-selection pattern could mix preflight and full-profile artifacts.

## Scientific question

Can uncertainty about a fitted local (chi) coordinate be diagnosed from one observed finite record in a way that tracks the known repeated-realization sampling behavior, especially in compact, weak-information, and boundary/nonregular regimes?

The frozen comparison evaluated:

1. target-coordinate profile likelihood in (chi);
2. local observed-Hessian curvature in physical coordinates;
3. fitted-model parametric bootstrap;
4. the immutable 12-realization known-truth sampling distribution as the calibration reference.

No likelihood-ratio cutoff, confidence level, admission threshold, biological prevalence claim, production promotion, C-family membership claim, or real-EEG license was defined.

## Compact and regular cases

Cells 0 and 1 show the expected regular pattern.

For cell 1, profile likelihood has a single well-localized minimum at both rates. The Hessian is positive definite and local (chi) standard error is close to both the fitted-model bootstrap and the repeated-realization spread:

- cell 1 fine: repeated-realization (chi) SD (approx0.0244), bootstrap SD (approx0.0190), Hessian SE (approx0.0176);
- cell 1 coarse: repeated-realization SD (approx0.0312), bootstrap SD (approx0.0258), Hessian SE (approx0.0258).

Cell 0 is also regular but shows somewhat stronger finite-sample realization dependence:

- fine: repeated-realization SD (approx0.0174), bootstrap SD (approx0.0224), Hessian SE (approx0.0224);
- coarse: repeated-realization SD (approx0.0186), bootstrap SD (approx0.0324), Hessian SE (approx0.0285).

The profile remains closed over the frozen search range with one local minimum. The selected observed realization can differ from the population truth even where the estimator sampling distribution is compact, so point error alone is not an uncertainty diagnostic.

## Weak-information case

Cell 6 separates ordinary fine-rate behavior from a substantially weaker coarse-rate regime.

At 256 Hz:

- repeated-realization (chi) SD (approx0.0773);
- bootstrap SD (approx0.0565);
- Hessian SE (approx0.0526);
- profile has one interior minimum and substantial likelihood rise toward both frozen edges.

At 128 Hz:

- repeated-realization (chi) SD (approx0.1422);
- bootstrap SD (approx0.1641);
- Hessian SE (approx0.2376);
- the observed fit is displaced to (chiapprox0.810) from truth (chiapprox0.496);
- the profile becomes shallow toward the high-(chi) side, with right-edge (Deltamathrm{NLL}approx0.20).

Thus the three uncertainty views all signal loss of information at the coarse rate. The profile is especially useful because it exposes the nonquadratic open/flat direction rather than compressing the problem into one local standard error.

## Boundary/nonregular case

Cell 2 is the strongest limit result.

At 128 Hz the selected fit is driven to (chiapprox0.9999) and (gapprox0.9998), with raw parameters on numerical bounds. The physical-coordinate Hessian correctly refuses the optimum as invalid/nonregular. The profile remains effectively open toward the high-(chi) boundary.

The fitted-model bootstrap is not a reliable representation of the source known-truth sampling distribution in this case:

- repeated-realization (chi) SD (approx0.1630), median (approx0.703);
- bootstrap SD (approx0.0723), median (approx0.9999).

The bootstrap reproduces the fitted boundary model rather than the broader known-truth behavior. This is a direct example of why fitted-model resampling cannot by itself license a local coordinate when the observed optimum is nonregular or boundary-attracted.

At 256 Hz cell 2 is less severe in (chi) but the fitted (g) remains numerically boundary-adjacent. The Hessian refuses the boundary case, while the profile remains informative about the likelihood geometry. This preserves the distinction between a usable target-coordinate profile and invalid regular-Wald/Hessian assumptions.

## Method-family disposition

The completed evidence supports the following hierarchy for future Bio Chi qualification:

1. **Profile likelihood:** primary single-record practical-identifiability diagnostic for local (chi), because it exposes open, flat, boundary-limited, or nonquadratic likelihood geometry without assuming local normality.
2. **Observed Hessian/Fisher curvature:** useful cheap secondary diagnostic only when the optimum is interior and the Hessian is valid/positive definite. Boundary or invalid-optimum refusal is scientifically informative and must be preserved.
3. **Fitted-model parametric bootstrap:** useful finite-sample secondary calibration in regular interior cases, but not self-validating. It can be seriously misleading when the observed fitted model sits on a nonregular/boundary branch.
4. **Repeated known-truth realizations:** remain the qualification/calibration reference for evaluating whether the single-record diagnostics behave correctly. They are not available for real observations and therefore are not themselves a deployable admission rule.

The completed Undermind methods-control search independently supports this hierarchy: profile likelihood is standard for practical identifiability; local Fisher/Hessian methods are limited to local regular geometry; finite-sample LR or bootstrap calibration requires validation; and boundary/nonregular points invalidate naive regular approximations.

## Claim consequences

- **Profile likelihood as primary P0-Q uncertainty diagnostic:** SUPPORTED.
- **Local Hessian as universal uncertainty method:** REFUSED; retain only as interior/regular secondary diagnostic.
- **Fitted-model bootstrap as universal admission method:** REFUSED; retain as conditional secondary calibration.
- **C1Q-RS production promotion:** NO.
- **C-family membership from fit/uncertainty quality:** NO.
- **Real-EEG local chi admission:** NO.
- **Scientific admission threshold:** NONE.
- **Biological prevalence:** NOT ESTIMATED.

## Post-execution deviation audit

The frozen scientific comparison was preserved.

- Frozen cells 0, 1, 6, and 2 were retained.
- Frozen observed seed and both sampling rates were retained.
- The profile grid and nuisance optimization recipe were retained.
- Hessian calculations used the frozen physical-coordinate formulation.
- Bootstrap used the frozen fitted-model route and seed set.
- No unfavorable case was removed.
- No LR cutoff, confidence level, or admission threshold was introduced.
- The earlier aggregation implementation defect was corrected mechanically by a superseding workflow before final source-of-record interpretation.

No material scientific deviation occurred.

## Next scientific requirement

The next gate is prospective calibration of a **profile-based refusal/uncertainty architecture** across a broader known-truth Function/Limit set, including regular C interiors, weak-information C interiors, near-critical/near-boundary C cases, alias-sensitive cases, D\\C and S\\D family boundaries, colored-process/memory controls, and genuine multimode controls.

The purpose is not to choose a numerical likelihood-ratio cutoff from the current four cases. It is to determine which profile-shape features are reliably diagnostic of practical identifiability versus semantic model misspecification, and which features must trigger REFUSE or NEED_MORE_INFORMATION before any empirical local-(chi) admission rule is frozen.
