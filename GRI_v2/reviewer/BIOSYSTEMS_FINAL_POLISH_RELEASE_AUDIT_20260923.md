# BioSystems final-polish release audit - 23 September 2026

**Status:** COMPLETE / READ-THROUGH CANDIDATE
**Branch:** `biosystems-final-polish-20260923`
**Immutable parent:** `biosystems-adversarial-r1-v12-final-20260923` @ `c2b0f01337e06387f9898b79edb38c3a305e157c`
**Program authority:** SymC General Operations Manual v0.8.4
**Private manuscript rule:** manuscript/supplement/letters remain private; GitHub retains scientific/provenance/audit records only.

## Purpose

Apply the final minor consistency and calibration changes identified by adversarial review without opening a new scientific analysis lineage.

No new cohort, endpoint, null family, threshold, seed, or biological claim was introduced.

## Changes closed

### 1. H1 claim calibration

The strongest manuscript wording now states the cross-source result as:

> recurrent cross-probe methylation covariance above the specified independence/construction floor and measured linear composition/source-site mean floors

rather than implying that the residual has been isolated as biologically independent organization.

The manuscript now states explicitly that:
- the stronger H1 nulls preserve only measured linear main effects and source-site mean shifts;
- no full technical-preserving null was identifiable under the frozen metadata;
- residual H1 cannot be interpreted as biologically independent of unmeasured composition, nonlinear/interacting effects, within-site acquisition effects, batch/plate/slide structure, subtype, or other latent covariance;
- external H1 is not composition-adjusted because comparable source-bound covariates were unavailable.

### 2. H2 null-floor consequence promoted into main Methods

The main Methods now includes the centered-kernel patient-permutation expectation:

`E <K_M, P K_R P^T>_F = tr(K_M) tr(K_R)/(n-1)`

and therefore

`E CKA_null = sqrt(r_M r_R)/(n-1)`.

The practical consequence is stated directly:
- canonical delta-CKA is a within-cancer observed-versus-shuffle contrast;
- cross-cancer H2 medians/magnitudes are descriptive only;
- the pan-cancer sign test tests directional consistency, not a shared biological effect magnitude.

### 3. H2/H3a external nontransport interpretation

The Discussion and Limitations now state explicitly that TCGA-internal H2/H3a recurrence may include TCGA-specific shared acquisition/processing lineage as well as biology.

External nontransport therefore leaves those contributions unresolved rather than being explained away as biology, platform, or representation.

### 4. Tumor-normal interpretation

The main manuscript, response letter, and cover letter now all state that:
- tumor-normal RNA results are unadjusted bulk tissue-state contrasts;
- broad Hallmark direction does not make the effect tumor-cell intrinsic;
- broad microenvironmental/cell-mixture differences remain plausible contributors.

### 5. P0 consistency repair

The stranded Discussion wording that attributed P0 to held-out “methylation Hallmark architecture” was removed.

P0 is now described only as showing that the frozen methylation representation carried held-out information beyond two measured covariates, while the 47-versus-2 capacity mismatch prevents Hallmark-specific attribution.

P0 is retained primarily for development-lineage transparency and is not part of the revised manuscript's main evidentiary spine.

### 6. RPPA contextualization

The existing supplement-only RNA/RPPA lineage is mentioned once in Discussion:
- RNA/RPPA patient alignment was positive in 31/31 cancers above its row-permutation floor;
- this is used only to show that broad cross-layer alignment is not uniquely methylation-specific;
- RPPA is not promoted into the main evidence hierarchy.

### 7. External H1 heading and wording

The Results heading now reads:

`Independent prostate transport reproduces H1 but not the cross-layer architecture`

rather than “strongly confirms H1.”

Remaining “strongly reproduces/transports” wording was removed from the relevant prose/caption.

### 8. F2 denominator closure

The Supplement now lists all 11 scored F2 behaviors explicitly.

The pre-result bookkeeping repair is stated:
- 12 scenario IDs existed;
- S9 and S10 were prospectively scored as one paired autonomy-ordering behavior;
- therefore the denominator is 11;
- 10/11 passed;
- S8 nonlinear-only was the retained failure.

### 9. Missingness heading and scope

The orphan internal heading `C1-3` was replaced by plain-language wording.

The 5/32 informative S2 scope remains explicit; degenerate S2 cases are not counted as negative evidence.

### 10. Tissue Source Site / TSS200 collision

Round-1 prose now uses “source site” or “TCGA Tissue Source Site source field” rather than standalone `TSS`.

`TSS200` is reserved for the transcription-start-site promoter mapping terminology.

### 11. Projected-C1 versus Round-1 H1 gate asymmetry

The manuscript now states explicitly:
- projected C1 uses the per-draw all-complete two-covariate rule and excludes COAD, DLBC, KIRC, OV, THYM;
- Round-1 H1 uses a cancer-level composition-complete eligibility gate and excludes only DLBC and THYM.

The denominators therefore arise from different prospectively defined evaluability rules, not outcome-dependent selection.

### 12. H3 mapping scope

The five promoter-core Hallmark refusals are now explicitly described as a source-wide fixed refusal set.

H3a/H3b therefore apply only to the evaluable Hallmark subset and are not complete Hallmark-library coverage.

### 13. Main-text density

Detailed principal-angle values, support correlations, and the H3b cohort-size threshold sweep remain in the Supplement.

The main Results now gives their interpretive consequence only.

### 14. Journal-facing letter calibration

The cover letter is reduced to two pages and uses the same claim ceilings as the Abstract.

Internal “adversarial synchronization” labeling was removed from journal-facing headers.

## PRAD like-for-like external comparator request

A reviewer suggested reporting the frozen TCGA PRAD cancer-level H1 effect beside the external prostate H1 values.

**Disposition: NOT ADDED.**

Reason:
- the exact cancer-level PRAD H1 numerical value was not recoverable from the currently accessible compact machine-readable release artifacts;
- the value is visually represented in an older C1 figure, but figure-reading is not a qualified numerical evidence source under the GOM;
- no scientific rerun was authorized merely to recover one descriptive number.

The manuscript therefore retains the correctly sourced comparison to the TCGA 32-cancer median rather than introducing a lower-provenance point estimate.

## Private read-through candidate

Private main:
- `GRI_BioSystems_working_v14_R1_2026-09-23.tex/.pdf`
- PDF pages: 20
- TeX SHA-256: `ed48276319eb2e4ee9a324f3e705d3bce3acae001732714351b4945fc3fcfa61`
- PDF SHA-256: `625335c344a258fb7ea4af6d1473f7a3fc1f235ed631ec256a2d0c79ab0f2431`

Private supplement:
- `GRI_BioSystems_supplement_working_v12_R1_2026-09-23.tex/.pdf`
- PDF pages: 15
- TeX SHA-256: `9fd0128ea97201ca21f0141c2ae459fbc392e38f57e4b9362e8fefb2dec349a9`
- PDF SHA-256: `e796e9956077270b9782bd94456a538112d4484a46a0db1cac2f07d81f1bb1a5`

Private reviewer response:
- `BioSystems_Response_to_Reviewers_v9_R1_2026-09-23.md/.pdf`
- PDF pages: 9
- Markdown SHA-256: `cae1d3153bf6e9cbdeb70492160420f6605778f010bc9f187b4db66b1e0f9f12`
- PDF SHA-256: `08eadf95a7d969cd4b2caf655f8721efb04494b5a74c9a7f692af10f116553aa`

Private cover letter:
- `BioSystems_Cover_Letter_v8_R1_2026-09-23.md/.pdf`
- PDF pages: 2
- Markdown SHA-256: `7bc6ac229b2249202a47433e103f0f0cc4cc96d8df1f05184a3aad8526166a37`
- PDF SHA-256: `343348ead93d66ed860cdb978b396b77e58e418d2c5a188276497f9a992b58d5`

Private package:
- `BioSystems_Resubmission_FinalPolish_v14_20260923.zip`
- SHA-256: `7336352c3cb215be3341994b9252b0c0725918f39a1f366950772b4565392023`

## PDF QA

Final PDFs were compiled/rendered after the edits.

Verified visually:
- Abstract and title page;
- H2 null-floor derivation in main Methods;
- independent prostate Results heading/body;
- condensed principal-angle/support subsection;
- Limitations/Conclusion claim ceilings;
- stronger H1 source-site null methods and support table;
- explicit 11-behavior F2 table;
- response first/final pages;
- two-page cover letter.

No material clipping, overlap, broken figure placement, or malformed math was found.

## Final disposition

No new scientific gate is open.

**STATUS: COMPLETE / READY FOR USER READ-THROUGH**
