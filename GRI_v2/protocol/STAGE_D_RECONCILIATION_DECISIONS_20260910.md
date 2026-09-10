# Consolidated reconciliation: proposed, not frozen

Executed offline metadata index: 179 rows retained; 24 D2 and eight D4 rows have second-channel metadata. Preserved snapshot is the local refresh, not a downloaded GitHub artifact. All source records remain unchanged; distinct GSM counts are not biological sample sizes.

D2 processing metadata describes red/green log ratios. Do not treat these as absolute expression or subtract controls again. GSM843853–GSM843857 titles identify leukemia but channel characteristics say Breast Cancer. Several mock-channel treatment protocols say DAC. Preserve conflicting assertions until authoritative clarification. D4 reference-channel design also requires reconciliation.

## Consolidated proposal for scientific approval

- D1: retain a descriptive endpoint/repeatability branch while timing and biological independence remain unresolved; no recovery-rate or biological predictive claim. This narrowing requires approval.
- D2/D4: define assay-specific representations only after reference-channel identity and ratio orientation are established. Source contradictions cannot be resolved by approval alone.
- Prediction: define independent experimental units and grouped validation/permutation before fitting. Technical repeats must not cross train/test boundaries. Minimum support remains unchosen pending design facts.
- Circularity: propose a synthetic shared-denominator null and separate reporting of acute/recovered displacements. These are proposed controls, not silently approved changes.
- D3/D4: preserve frozen challenge roles and report nonidentifiability per unsupported contrast.
- If the registered datasets cannot support prediction, prepare an independent-data amendment rather than replace the primary dataset silently.

All six recommendations form one reconciliation package. D0.3 remains unfrozen. No new thresholds or outcome calculations were introduced. No author contact was sent.

## Mechanical reproduction

Extract `GRI_v2/provenance/stage_d/refresh_and_design_a5902b7.zip` into `GRI_v2/provenance/stage_d/` first. From repository root:

    python GRI_v2/src/stage_d_design_inventory.py --source GRI_v2/provenance/stage_d/local_refresh_a5902b7 --out /tmp/stage_d_design_audit

Preflight now runs this index automatically and uploads it with source metadata. The index records every source row and input hashes, without selecting scientific eligibility.
