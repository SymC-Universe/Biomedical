# BioSystems V29 biological chi continuation checkpoint

**Date:** 26 September 2026  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Reviewer guide:** `GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260926_V29.md`

## Status

The original C1/P1 BioSystems oncology evidence spine is unchanged. V29 reconciles the canonical Meneses direct-experimental lineage, explicitly demotes the timeout-created duplicate to post-result robustness, and adds one genuinely new prospective same-system perturbation-path transport gate.

## Canonical direct Meneses result

The prospective Meneses E. coli osmotic-shock lineage remains the canonical direct experimental record:

- whole-system biological chi: `DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q`;
- modal/vector `Chi_bio`: `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q`;
- scalar `chi_bio`: `NOT_OPENED_NOT_LICENSED`;
- stronger frozen rate-depth invariance rule: failed and preserved.

The later timeout-resume duplicate is not counted as independent confirmation.

## New prospective path-transport result

The path-transport gate used 143 source-facing single-cell motor traces across sucrose, sorbitol, source-defined sodium/buffer context, and clockwise rotation at 200, 300, 400, and 500 mM. All 143 traces were representation-eligible and the frozen fit-failure count was zero.

The four-coordinate representation was
`[A_dec, log(tau_dec), log(tau_inc), G_rec]`.

Observed leave-one-concentration-out balanced accuracy was 0.3846367 versus a concentration-stratified permutation-null 97.5th percentile of 0.3272412 (2,000 permutations; upper-tail p=0.0009995). The primary result is:

`PATH_REORGANIZATION_DETECTED_P0Q`.

Collapse depth alone did not satisfy the frozen detection rule: balanced accuracy 0.2967255 versus null 97.5th percentile 0.3026514.

The full-minus-depth accuracy increment was 0.0879112. Because the prospective secondary taxonomy required at least 0.10 for its strongest label but did not name the realized combination of full-vector detection, depth-only non-detection, and increment below 0.10, the secondary disposition is preserved as:

`SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10`.

No post-result relabel was used.

## Post-result root-cause diagnostic

A separately frozen diagnostic has no promotion rights. It found that collapse depth alone again did not clear its diagnostic threshold, while `log_tau_dec`, `log_tau_inc`, and `G_rec` each did. Every leave-one-coordinate-out three-feature representation remained detectable, so the aggregate path signal is distributed rather than dependent on one unique coordinate.

After BH correction across six pairwise path contrasts, four were detectable: sucrose-vs-sorbitol, sucrose-vs-clockwise, sorbitol-vs-sodium/buffer context, and sorbitol-vs-clockwise. Sucrose-vs-sodium/buffer context and sodium/buffer context-vs-clockwise were not detected. This heterogeneity explains but does not alter the primary result.

## Reproducibility identities

Path-transport run: `36284374387`  
Artifact: `10919776838`  
Artifact digest: `sha256:71dbba045f674852ae8862cef89013297cbdcd2c16c440e55feea2386c1d35d5`

Post-result diagnostic run: `36284508053`  
Artifact: `10919484871`  
Artifact digest: `sha256:0ee429b118b24cba6a2276aae3ba6bac8627ae52f23b4e737903eba461dea0e8`

## What happens next and why

The same E. coli source has now answered the direct recovery-representation question and a same-system perturbation-path transport question. Further mining of this source would add less independent information. The next high-value experiment should therefore move to a second directly measured biological system with explicit perturbation-path or context variation and an accessible native dynamical carrier, testing whether path-sensitive multicoordinate recovery organization transports, reorganizes, or refuses classification.

## What the user needs to do

Nothing at this checkpoint. The public scientific lineage is preserved in GitHub and the private manuscript/Supplementary Information suite is versioned separately.
