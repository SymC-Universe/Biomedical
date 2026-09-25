# Shaffer 2017 GRI ↔ Bio Chi preanalysis method decision packet

**Date:** 25 September 2026
**Branch:** `gri-biochi-bridge-p0q-20260925`
**Status:** SOURCE QUALIFICATION CLOSED / SCIENCE-ADJACENT METHOD FREEZE NOT YET AUTHORIZED
**Authority:** SymC GOM v0.8.6 + existing GRI/Bio Chi controls

## Inherited constraints that already control this bridge

The current bridge does not restart earlier GRI decisions.

- static covariance is not a native dynamical operator;
- the historical CV/2 route remains closed;
- feature selection is separate from normalization;
- target resistance markers or target outcomes may not define the primary representation;
- a static-to-dynamic bridge must be calibrated against independently licensed dynamic/modal information rather than defining its own target;
- simple/native comparators are mandatory;
- a biological scalar chi_bio is not required for modal or Bio Chi investigation;
- same-publication validation is not external confirmation.

## Shaffer-specific source facts now verified

- GSE97679 development RNA and GSE97681 validation/transfer RNA all share the same 63,682-gene identifier universe.
- The source processed tables are raw HTSeq gene counts.
- The source records state STAR alignment, HTSeq gene counting, and DESeq2 differential-expression analysis.
- GSE97679 has a week-1 overlap across the two sequencing runs, allowing direct run-sensitivity checks.
- GSE97681 exposes WM989 paired drug/no-drug and drug-holiday states plus WM983B paired and longitudinal states.
- no target gene effect, resistance-marker selection, B2 result, or B3 result has been opened for this qualification.

## Consequence for normalization candidates

The earlier SCC25 G2 normalization packet treated DESeq2 VST as a sensitivity/conditional candidate because that source exposed ambiguous tximport-derived processed counts without the original tximport object.

That specific incompatibility does not apply here. Shaffer exposes raw HTSeq count tables and used DESeq2 natively.

Therefore the candidate order for Shaffer is now:

### Candidate S-N1: DESeq2 variance-stabilizing transform
Use the raw-count matrices with a prospectively frozen size-factor/dispersion fit on development data only, then preserve/reapply the fitted transform to source-internal validation where technically valid.

Reason to favor for review:
- source-compatible count semantics;
- established RNA-seq mean/variance handling;
- suitable for sample geometry and downstream multivariate analysis;
- transformation can be frozen and reapplied.

Unresolved before freeze:
- exact fitting subset;
- whether design-blind or design-aware fitting is appropriate for the declared bridge task;
- feature detectability rule;
- explicit run/batch model and week-1 bridge adjudication.

### Candidate S-N2: deterministic library-size normalization + log transform
Retain as the transparent minimal sensitivity/baseline representation.

Reason:
- exact reproducibility from released tables;
- no model fitting dependency.

Risk:
- weaker composition and mean/variance handling than a source-compatible count model.

### Candidate S-N3: TMM/log-CPM
Retain as an optional composition-robust sensitivity if a development-only fitting/reference rule can be frozen cleanly.

## Modal-construction candidates

No modal method is frozen yet.

The lowest-complexity candidate family to review first is an unsupervised PCA/SVD-type sample-state subspace on the frozen transformed development representation, because it provides a simple non-outcome-selected geometry and a natural baseline against which a more elaborate modal object must add value.

A more complex modal construction is not justified merely because it produces richer structure.

## Comparator candidates

At minimum preserve:
- simple persistence / nearest-state or mean-state temporal baseline where the target task is temporal;
- PCA/SVD geometry as a simple multivariate baseline;
- source-native differential-expression/state-description evidence as descriptive context, not automatically a forecast comparator;
- an established transition/state-space comparator only if the frozen question is transition prediction.

No method is allowed to win by answering a different question.

## Current decision boundary

The next scientific freeze must choose:
1. primary normalization and one declared sensitivity;
2. outcome-independent feature universe/filter;
3. batch/run handling;
4. primary modal construction and its epistemic class;
5. B2 statistic;
6. simple/native comparator matched to the same task;
7. exact GSE97681 WM989 validation endpoint;
8. WM983B transfer endpoint;
9. refusal/representation-dependence rule;
10. stopping rule.

Until those are frozen, target molecular effects remain closed.

## Safe continuation

Source-method literature review, executable preprocessing preflight, environment qualification, sample-map checks, and preparation of the decision packet may continue without opening B2/B3 outcomes.
