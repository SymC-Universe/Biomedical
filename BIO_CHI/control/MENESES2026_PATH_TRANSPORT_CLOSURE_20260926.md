# Meneses 2026 perturbation-path transport closeout

**Date:** 26 September 2026  
**Branch:** `bio-chi-meneses-path-transport-p0q-20260926`  
**Status:** CLOSED PRIMARY GATE; SECONDARY SUBCLASSIFICATION LEFT UNRESOLVED  
**Authority:** SymC GOM v0.8.6

## Status

The genuinely new post-Meneses question was executed after the canonical direct experimental recovery lineage had already closed. This experiment does not repeat the earlier dose-response compression test. It asks whether the multicoordinate motor-recovery representation contains perturbation-path information that generalizes to a concentration omitted from training.

The four frozen path families were standard sucrose, sorbitol, the source-defined sodium/buffer-context assay, and clockwise motor rotation. All four concentrations (200, 300, 400, and 500 mM) were present in every family.

## Source and fit integrity

Sixteen pinned upstream Parquet files from `wadhwalab/2026-Meneses-Osmotic@d14d0caaa07299f13d1b1121d1e4630454fd724b` were retrieved and hashed.

The source-facing fit lane produced 143/143 representation-eligible cells and zero frozen fit failures:

- sucrose: 8, 10, 8, 12 cells across 200--500 mM;
- sorbitol: 8, 8, 8, 8;
- sodium/buffer context: 10, 10, 10, 10;
- clockwise: 8, 8, 9, 8.

No numerical outlier was removed.

## Primary path-transport result

The frozen four-coordinate representation was

[
R=[A_{mathrm{dec}},log	au_{mathrm{dec}},log	au_{mathrm{inc}},G_{mathrm{rec}}].
]

A multinomial classifier was trained on three concentrations and tested on the fourth, repeated over all four held-out concentrations. Path labels were permuted within concentration for the frozen 2,000-replicate null.

Observed full-vector balanced accuracy was **0.3846367**. The concentration-stratified null 97.5th percentile was **0.3272412**, with an upper-tail permutation value of **0.0009995**. The frozen primary disposition is therefore:

`PATH_REORGANIZATION_DETECTED_P0Q`.

The result means that the multicoordinate recovery trajectory contains path information that generalizes across dose. It does not mean that all four paths are cleanly separable, and it does not establish a molecular cause.

Held-out fold balanced accuracies were 0.2500, 0.4875, 0.51875, and 0.2875 at 200, 300, 400, and 500 mM, respectively. The heterogeneity is retained rather than averaged away as a claim of uniform transport.

## Depth-only control

Using only collapse depth `A_dec`, observed balanced accuracy was **0.2967255** versus a frozen null 97.5th percentile of **0.3026514**. The depth-only lane therefore did not satisfy the frozen detection rule.

This is important because the source literature already establishes gross motor-speed effects across these perturbation contexts. The new result is not simply a restatement that larger shocks produce larger slowdown.

## Secondary-rule gap

The full-vector classifier exceeded the depth-only classifier by **0.0879112**. The frozen secondary rule required an increment of at least 0.10 for the label `DYNAMICAL_PATH_INFORMATION_BEYOND_DEPTH_P0Q`.

At the same time, the full-vector lane detected path reorganization while the depth-only lane did not. That exact combination with an increment below 0.10 was not assigned a named secondary class in the prospective freeze.

The correct secondary disposition is therefore:

`SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10`.

No post-result relabeling is used to fill the gap. A separate exploratory diagnostic may investigate which coordinates carry the detected path information, but it cannot alter the primary P0-Q result or retroactively repair the frozen secondary taxonomy.

## Bio Chi interpretation

- biological chi: **path reorganization detected at P0-Q** in the direct motor-recovery event;
- `Chi_bio`: the four-coordinate recovery representation is informative, but the finer secondary path-information subclass is unresolved because the prospective rule omitted the realized edge case;
- `chi_bio`: **not opened / not licensed**. The empirical sigmoid timescales remain response summaries rather than an independently identified modal scalar carrier.

This result strengthens the context/path side of the Bio Chi program without reviving a universal scalar claim.

## Workflow identity

Run: `36284374387`  
Workflow head: `79a098f777a27bb18bcb2c8fb26b69e301ab0e57`  
Artifact: `10919776838`  
Artifact digest: `sha256:71dbba045f674852ae8862cef89013297cbdcd2c16c440e55feea2386c1d35d5`  
Result JSON SHA-256: `f06476bb9daa7fc3f8dcefd8e5eee15ea7d72fead44394b41bae111af8b5a108`

## What happens next and why

The primary transport question is answered for this source. The next low-cost action is a post-result feature-ablation and pairwise diagnostic to identify which recovery coordinates and which path contrasts drive the detected signal. That diagnostic is explanatory only. It cannot promote the primary result or repair the frozen secondary-rule gap.

After that, the more valuable scientific move is cross-system transport: test whether a perturbation-path-sensitive multicoordinate recovery architecture appears in another directly measured biological system rather than continuing to mine one E. coli dataset indefinitely.
