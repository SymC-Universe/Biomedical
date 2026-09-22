# BioSystems figure/table retirement and regeneration inventory - 22 September 2026

**Source audited:** `SymC_GRIonc.tex` on the frozen oncology lineage  
**Revision branch:** `gri-biosystems-revision-20260922`  
**Rule:** submitted figures are not cosmetically edited when their axes, captions or interpretation depend on retired constructs. They are retired and rebuilt from currently admissible evidence.

## Executive disposition

All three submitted main figures require **retirement and replacement**, not caption-only repair. The submitted driver table also requires **retirement or complete re-derivation** because its selection score depends on historical damping/dispersion/critical-boundary constructs that are no longer admitted.

This closes the old “figures were never regenerated” vulnerability at the planning level: no submitted main visual is grandfathered into the revision.

## Figure 1: `Fig1_Stability_Sig.png` / `fig:signature`

### Submitted content that is no longer admissible
- labels the rank-ordered profile as “time-series analysis”;
- asserts a four-phase mechanical failure sequence;
- treats rank order as compression -> yield -> plastic drift -> terminal divergence;
- uses a biological critical boundary at `chi = 1`;
- claims irreversible overdamped collapse;
- infers an early-warning diagnostic window;
- uses “dispersion energy” `D = Omega * sigma^2` as if physically validated.

### Disposition
**RETIRE ENTIRE FIGURE.**

### Replacement role
A revised Figure 1 should establish the **static, cancer-aware multiomic architecture** actually supported by the rebuilt program. Candidate panels may show:
1. cancer-specific/static RNA organization under finite-sample calibration;
2. measured context/composition contribution;
3. methylation/RNA organization under the frozen C1 construction;
4. clear evidence-class labels: STATIC / INTERNAL / NON-CAUSAL.

No time axis, disease progression sequence, critical-damping boundary or early-warning language is permitted.

## Figure 2: `Fig2_PSTopology.png` / `fig:phasespace`

### Submitted content that is no longer admissible
- plots `Omega` as an “energy” axis without a current biological derivation;
- presents `1/chi` as adaptive susceptibility/inverse damping;
- uses `chi = 1` as a biological phase boundary;
- assigns zones such as underdamped chaos, critical regulation, rigidity lock and captured state;
- describes zone centers as attractors;
- calls a PRH1 point “forensic capture”;
- claims density provides independent thermodynamic validation;
- uses a Poissonian limit as a survival corridor;
- interprets curvature as restoring/repulsive dynamics.

### Disposition
**RETIRE ENTIRE FIGURE.**

### Replacement role
A revised Figure 2 should show the **modal / cross-layer / system organization** without forcing the architecture into a scalar phase plane. Suitable content is a block-preserving view of RNA, methylation, context, genomic and protein evidence with explicit provenance and no master score.

If a low-dimensional visualization is used, it must be labeled as a visualization/representation, not a dynamical phase space unless a native dynamic generator licenses that interpretation.

## Table 1: `tab:culprits`

### Submitted content that is no longer admissible
- ranks “primary drivers of regulatory collapse” using extreme overdamping;
- uses `chi >> 1`, dispersion-energy thresholds and substrate alignment;
- labels genes as bandwidth-exhaustion epicenters/executors.

### Disposition
**RETIRE OR RE-DERIVE FROM A NEW FROZEN QUESTION.**

Do not simply rename the columns. A replacement gene/pathway table is allowed only if the selection rule is based on currently admitted quantities and the biological question is declared before ranking.

## Figure 3: `Fig3_Control_Matrix.png` / `fig:battlemap`

### Submitted content that is no longer admissible
- calls itself a therapeutic control matrix;
- places genes in `(Omega, chi)` sectors;
- maps `chi` regimes directly to mobilization, monitoring or antagonistic treatment;
- implies clinical deployability;
- identifies treatment strategies from static TCGA expression structure.

### Disposition
**RETIRE ENTIRE FIGURE.**

### Replacement role
A revised Figure 3 should be evidence-facing rather than treatment-prescriptive. Strong candidates are:
- internal holdout robustness / sensitivity structure, explicitly labeled internal TCGA evidence; or
- Function Map + Limit Map showing supported architecture beside refusals/non-identifiability; or
- tumor-versus-normal result if prospectively frozen and completed before figure freeze.

A treatment decision matrix is not admissible in the current revision.

## Additional manuscript graphics implied by the submitted prose

The submitted text also contains conceptual claims that should **not** be converted into replacement schematic figures unless new evidence supports them:
- Warning -> Confirmation -> Collapse staging;
- compression -> yield -> drift -> terminal divergence;
- substrate capture as irreversible phase transition;
- exceptional-point crossing as a cancer recovery requirement;
- state-matched treatment guardrails;
- chi-based preventive oncology.

These should be removed or explicitly relocated to future falsifiable hypotheses, not visually reintroduced after being withdrawn from the main claims.

## Required new visual set before submission freeze

At minimum, the revised paper should have a visual sequence that answers the reviewers rather than preserving the old narrative:

1. **Data + evidence architecture.** Cohorts/layers, cancer-specific construction, internal split structure, composition controls and evidence classes.
2. **Static multiomic result.** The strongest frozen RNA/methylation/context result with appropriate null/sensitivity information.
3. **Robustness / Limit Map.** Cancer-specific heterogeneity, failures/refusals and sensitivity rather than only favorable examples.
4. **Tumor-versus-normal control**, if completed and promoted for the revision.
5. **External confirmation**, only if a genuinely untouched cohort passes the prospectively frozen confirmation gate.

Figures 4 and 5 are conditional. If either evidence gate is not completed, the manuscript must state the limitation rather than backfill a weaker visual and call it validation.

## Final visual audit rules

Before release:
- every axis must be a measured or explicitly derived quantity with current derivation;
- every panel must name its evidence class;
- no rank axis may be narrated as time;
- no static association may be captioned as recovery, damping, hysteresis, inheritance or causality;
- no `chi = 1` cancer boundary unless independently re-earned;
- internal TCGA holdout must be labeled internal;
- every plotted source table and generated image must be hash-registered and regenerable.
