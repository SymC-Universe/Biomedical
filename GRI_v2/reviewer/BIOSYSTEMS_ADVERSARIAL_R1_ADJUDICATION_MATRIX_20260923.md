# BioSystems adversarial Round 1 adjudication matrix

**Date:** 23 September 2026
**Status:** ACTIVE
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4

## Rule

Round 1 is an adversarial post-release audit. A reviewer comment is not accepted merely because it is plausible and is not rejected merely because the parent package disagrees. Each item is classified against code, source provenance, frozen contracts and reproducible outputs.

Status vocabulary:

- `VALID / CLOSED BY NEW TEST`
- `VALID / CLAIM NARROWED`
- `VALID / EDIT REQUIRED`
- `PARTLY VALID / LIMIT RETAINED`
- `REVIEWER HYPOTHESIS FALSE`
- `NOT IDENTIFIABLE FROM CURRENT SOURCE`
- `OPEN SCIENTIFIC CONTROL`

## A. External prostate P1

| Round-1 issue | Adjudication | Evidence / action |
|---|---|---|
| H1 may have pooled tumor and adjacent samples | **REVIEWER HYPOTHESIS FALSE** | Code audit establishes H1/H2/H3a use tumor samples only. Adjacent samples enter symmetric probe eligibility and the separately declared TN contrast. |
| External H1 magnitude (~+0.303 to +0.358) greatly exceeds internal median (~+0.128) | **VALID / EXPLANATION INCOMPLETE** | Pooled tissue state is excluded. AA/EA axis is excluded as a sufficient explanation. Remaining technical/composition/subtype factors require bounded investigation; manuscript must not present effect-size equivalence. |
| AA/EA mixture could inflate external H1 | **VALID / CLOSED BY NEW TEST** | `R1_H1_RACE_ROBUST`: race residualization retained 104.6% of primary effect; AA-only also positive; all-EA EPIC remains positive. This excludes race label as sufficient explanation, not all ancestry structure. |
| H1 construction null is weak because independent CpG permutation destroys all real covariance | **VALID** | Canonical H1 is relabeled an independence/construction floor. New TCGA composition-preserving null passes 30/30 cancers but does not eliminate batch/latent structure. |
| H1 lacks measured composition attack | **VALID / CLOSED BY NEW TEST WITH LIMIT** | `R1_H1_MEASURED_COMPOSITION_ROBUST`: 30/30 composition-complete cancers positive against a null preserving linear purity/leukocyte covariance; median +0.09998, p=1.86e-9. Claim ceiling explicitly excludes full composition independence. |
| H1 lacks batch/center/plate/age/sex attack | **OPEN SOURCE-IDENTIFIABILITY AUDIT** | Metadata-only workflow `BioSystems adversarial R1 external metadata audit` inventories what is actually source-bound before any further molecular adjustment. |
| H2 should not be described as weak positive/power-limited transport | **VALID / CLAIM NARROWED** | External +0.019724 is ~8.6% of internal median +0.2295 with q=0.4065. Wording becomes “no detectable external H2 transport.” |
| `P1_REPRESENTATION_DEPENDENT` overreads sign flips between null-compatible H2/H3a estimates | **VALID INTERPRETIVE LIMIT** | Frozen label is retained for provenance, but explicitly described as a procedural conflict label, not evidence of a real representation-specific effect. |
| RNA representation was not transported unchanged | **VALID / LIMIT RETAINED** | TCGA uses EB++ batch-adjusted RSEM with log2(max(x,0)+1); external uses raw counts with median-ratio normalization then log2(+1). H2/H3a nontransport cannot be assigned uniquely to cohort biology versus RNA representation. |
| Recompute TCGA with DESeq-style median-ratio normalization | **NOT A VALID SAME-OBJECT TEST** | Median-ratio size factors require count-like inputs; TCGA EB++ batch-adjusted RSEM is not raw counts. Applying DESeq-style normalization to EB++ values would create a different invalid preprocessing operation. A legitimate alternative transform may be tested only if source-compatible. |
| B=999 makes p=0.001/q=0.003 the Monte Carlo resolution floor | **VALID / POST-RESULT PRECISION CONTROL ALLOWED** | Higher-B repetition may refine Monte Carlo precision but cannot rewrite the frozen B=999 P1 decision. If executed, it is a separate post-result numerical-resolution sensitivity. |
| External prostate-only validation limits generalization | **VALID LIMIT** | No new cohort will be selected because it is favorable. Breast and other families prequalified before P1 remain candidates only under a separately frozen same-question extension. |

## B. Tumor-normal controls

| Round-1 issue | Adjudication | Evidence / action |
|---|---|---|
| TN RNA weakening is composition-unadjusted | **VALID LIMIT / FURTHER SOURCE TEST UNDER REVIEW** | Same-participant pairing does not remove tissue-state composition. Purity is not symmetric in adjacent normal. Language must identify the result as an unadjusted state contrast unless a valid symmetric composition sensitivity is source-supported. |
| Effect may be concentrated in immune/inflammatory Hallmarks | **ATTACKED / NOT SUPPORTED** | Post-hoc Hallmark breadth: TN-A1 pairwise 49/50, PC1 47/50, C_out 50/50 Hallmark medians lower in tumor; TN-P20 48/50, 48/50, 50/50. This argues against concentration in a small immune subset but does not remove composition confounding. |
| Naive composition direction could predict higher tumor coherence | **PLAUSIBLE ARGUMENT, NOT A CONTROL** | May be stated only as an interpretive observation, not treated as confound removal. |
| 12 TN-A1 and 13 TN-P20 cancers are unnamed | **VALID / EDIT REQUIRED** | Add exact rosters to Methods/Supplement/response. |
| TN-C1 5/5 abstract result omits finite exact-test resolution | **VALID / EDIT REQUIRED** | Any abstract mention must state p=0.0625 / BH q=0.125 or describe the result as directional consistency rather than significance. |
| External prostate TN RNA did not confirm the internal pan-cancer shift | **VALID LIMIT** | First two effects same-signed but much smaller; C_out ~0. No power rescue is asserted. A second external cohort requires a prospective extension, not post-result shopping. |

## C. P0 internal held-out branch

| Round-1 issue | Adjudication | Evidence / action |
|---|---|---|
| P0 used a 24-cancer promotion floor but only 19 were eligible | **VALID / CLAIM NARROWED** | P0 is bounded internal evidence below the pan-cancer promotion floor. Remove it from central Abstract promotion language. |
| 47 predictors vs 2 covariates is a capacity mismatch | **VALID** | Existing result establishes additional held-out methylation information beyond two measured covariates, not Hallmark-specific superiority. Historical capacity-control freeze is provenance-unverified. |
| Manuscript said a capacity control was already frozen | **INACCURATE / CORRECTED** | `GRI_POSTFINAL_CAPACITY_CONTROL_PROVENANCE_DISCREPANCY_20260911.md` establishes REFERENCED_BUT_NOT_RECOVERED. Do not invent historical preregistration. |
| Run a capacity-matched control | **OPEN P0-Q FEASIBILITY** | Scientifically useful only as a new post-FINAL adversarial comparator. It cannot upgrade the original untouched holdout and must use the same data/task with an equal-capacity representation. |
| Reviewer 2 asks for clinical utility beyond existing predictors | **DECLINED / NOT CLAIMED** | Current paper makes no diagnostic/prognostic/treatment decision claim. |

## D. Alternative methods / representation

| Round-1 issue | Adjudication | Evidence / action |
|---|---|---|
| No benchmark against MOFA/SNF/DIABLO/CCA | **PARTLY VALID** | These tools answer different latent-factor/fusion/supervised questions than the exact H1 construction-null transport task. A comparator should be run only if it can be aligned to the same question; paper cannot claim superiority over them. |
| Custom representations may obscure simpler explanations | **VALID LIMIT** | Add a concise necessity/function map and keep claims at the level each endpoint tests. |
| H3b promoter-core mapping may be definition-sensitive | **VALID LIMIT** | Retain as support-sensitive/refused semantic promotion; do not broaden. |

## E. Technical/reporting consistency

| Round-1 issue | Adjudication | Action |
|---|---|---|
| Title names cross-layer recurrence that did not externally transport | **VALID / EDIT REQUIRED** | Candidate title: *Recurrent Methylation Organization Across Human Cancers with Context-Dependent Methylation-RNA Coupling*. |
| Abstract overweights H1 without naming weak canonical null | **VALID / EDIT REQUIRED** | State that H1 is above an independence/construction floor and that Round-1 measured-composition attack is separate. |
| Stale “raw-state sensitivity remains pending” text | **VALID / EDIT REQUIRED** | Remove/update everywhere. |
| “No scientific gate remains” conflicts with optional future P0-Q | **VALID WORDING ISSUE** | Say no evidence gate remains **for the original revision package**; Round-1 controls are new adversarial work. |
| First-person abstract / mixed singular-plural cover pronouns | **VALID / EDIT REQUIRED** | Normalize to single-author neutral/singular wording. |
| TeX en-dash markup regression | **VALID / EDIT REQUIRED** | Replace unnecessary range/compound `--` usage consistently; retain mathematical minus signs. |
| Response promises protein/phosphoprotein evidence not present in main | **VALID / RESPONSE FIX** | Either point explicitly to supplementary B2 evidence if retained or remove the claim from the response. Do not imply analyses absent from the paper. |
| Lingering biological chi / exceptional-point vocabulary | **VALID FRAMING RISK** | Remove from current Abstract/Conclusion except minimal historical nonclaim where strictly necessary. |
| RSEM preprocessing clarity | **VALID / EDIT REQUIRED** | State EB++ source is already normalized/batch-adjusted RSEM and log2(max(x,0)+1) is the downstream transform; do not describe it as raw-count normalization. |
| Small-cohort draw dependence | **VALID / SUPPLEMENT CLARITY** | Report source pool sizes and emphasize deterministic draws are robustness summaries, not independent observations. |

## F. Reviewer citations

- Reviewer-1 oncology/chromatin citations PMID 39485254, 39617063 and 38409266: **relevant; engage/cite after bibliographic verification**.
- Reviewer-2 converter/EV-control/drilling-control references: **outside current static oncology scope after withdrawal of the control-theory analogy; explicitly decline in response instead of silently ignoring**.

## G. Reproducibility/public record

**VALID concern, mechanically closable.**

The manuscript itself remains private until submission. The following are public/versioned in GitHub:
- freezes;
- configs;
- code;
- workflows;
- source identities;
- result audits;
- reviewer adjudication;
- claim ceilings;
- checkpoint state.

Before Round-1 submission release, add:
1. a public reviewer/reproducibility index binding all Round-1 commits/run/artifact hashes;
2. a frozen release snapshot branch/tag equivalent;
3. Zenodo-ready public package manifest excluding third-party redistributability-prohibited data and the private manuscript text.

## Current highest-priority unresolved items

1. external metadata/technical source identifiability;
2. TN composition sensitivity if a symmetric source-supported route exists;
3. P0-Q capacity comparator feasibility;
4. optional higher-B P1 Monte Carlo precision;
5. synchronized manuscript/response/cover/reproducibility release.

No chi_bio/recovery/SCC25 extension belongs in this revision.
