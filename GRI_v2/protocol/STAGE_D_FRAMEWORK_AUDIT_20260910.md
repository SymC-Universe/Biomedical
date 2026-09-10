# Framework reconciliation audit — 2026-09-10

Scope: Stage-D contracts, registry, metadata implementation and tests; upstream README, build status, claim-evidence map, coordinate registry and general feasibility kernel. This is not a reanalysis of closed C1/P0, an exhaustive proof of all historical code, or a completed D0.3 freeze. No numeric biological matrix was opened. All original source records and replicates are preserved.

## Mechanical findings and repairs

1. Metadata CSV silently discarded fields outside its fixed columns, including second-channel information relevant to two-channel arrays. Export now retains all parsed fields. Fresh metadata retrieval is required to recover fields absent from the historical CSV.
2. A sample immediately followed by a SERIES record could be dropped. Parser now flushes it; regression added.
3. A wrong series response could pass if samples existed. Inventory now rejects accession mismatch and missing/invalid GSM identifiers.
4. Metadata response hashes were recorded without the corresponding SOFT text. Future inventories preserve the decoded source text before enrichment. These are text hashes, not assertions about raw HTTP transport bytes.
5. State machine lagged behind current gate. Synchronized to D0_DESIGN_AUDIT; no outcome permission granted.
6. Preserved all three original preflight files and their hashes in provenance/stage_d/preflight_34421899472. A separate listing audit distinguishes record counts from unique GSM accessions, neither of which automatically equals independent biological n.
7. Directory helper files remain source evidence, but are not assay matrices. Their listing counts do not establish usable assay coverage.

## Scientific obstacles: one reconciliation decision, no silent fixes

- D1 source metadata and published Methods both specify day-7 treatment versus day-11 early control. This is a non-time-matched contrast; pure treatment attribution is not established.
- D1 recovery timing conflicts: GEO says day 35 / 28 days after withdrawal, published Methods day 28 / 21 days after withdrawal. Do not select a date by desired model behavior.
- Figure 6 identifies TAMR EPIC pairs as technical replicates. Do not count them as independent biological replication. Cross-assay replicate-number matching alone does not prove common biological provenance.
- D2 combines platforms, cell contexts and patient samples. Second-channel metadata, doses, withdrawal times and control definitions must be reconciled before choosing eligible comparisons. Current raw CSV cannot close this audit.
- D3/D4 assay coverage and replication are uneven. Registry membership does not establish that every frozen detector is evaluable. Preserve datasets and report support/refusal per contrast.
- Q_residual shares an acute denominator with potential acute predictors. Check mathematical coupling explicitly before biological predictive interpretation; raw displacement components provide traceability. No endpoint change is authorized here.
- Label permutations require exchangeable independent units. Generic patient-shuffle code cannot simply be applied to technical repeats or ordered conditions. The exact unrestricted CKA expectation does not automatically apply to restricted permutations.
- Four ordered conditions do not constitute four independent recovery trajectories. Genes, technical repeats, or resampled rows cannot supply missing biological replication.
- Stage D currently has metadata acquisition code, not an implemented recovery engine. Passing preflight establishes neither design sufficiency nor scientific validity.
- Upstream README/build-status/claim-map are historically inconsistent with Stage-D narrative about C1/P0 closure. Exact closure artifact reconciliation is required before importing those claims. Historical frozen files have not been rewritten.
- Source-paper methods lookup exposed published outcome descriptions and figure captions in retrieved pages. No new matrix analysis occurred; however future attestations must distinguish prior published-result awareness from unopened numeric matrices. Do not claim complete outcome blindness.

## Useful structure worth retaining and testing

- Scalar + modal + conglomeration with separate relationship and uncertainty layers is a useful architecture for reporting agreement and disagreement, without requiring a master score.
- Spectral CKA expectation and fixed-spectrum ceiling separate spectral capacity from realized alignment. The stated unrestricted expectation is mathematically consistent; the ceiling is over orthogonal alignment, not necessarily attainable by sample permutation. A_realized may be negative and is not a probability. Denominator collapse is a meaningful nonidentifiability diagnostic.
- Technical replicates can characterize measurement repeatability even where biological generalization is unavailable. Preserve this distinction rather than discard measurements.
- Day-matched late control/recovery comparisons may offer descriptive endpoint information even if acute-normalized recovery remains unsupported. This is a proposed narrowed analysis, not automatic replacement of the primary question.
- D3/D4 remain separately ordered transformation challenges, not substitutes for recovery trajectories. Failure to generalize can delimit the signature's domain.
- In the existing general kernel, PCA is fitted within training folds, a useful leakage safeguard. Its random row folds still require an independent-unit design before reuse in D1.

## Consolidated recommendation awaiting approval

Retain all source data and original contracts. Seek authoritative timing/replicate clarification; retain unresolved facts if unavailable. Propose per-dataset descriptive versus predictive eligibility, independent experimental units, permissible permutation blocks, controls for shared-input coupling, and support/refusal rules together in a D0.3 amendment. Do not implement unapproved thresholds, treat technical precision as biological certainty, or tune toward favorable outcomes. Independent source/provenance repairs and tests can continue.

## Primary sources

- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE216989
- https://www.nature.com/articles/s41594-023-01181-7 (Pharmacological treatments in cell lines)
- https://pubmed.ncbi.nlm.nih.gov/38182927/ (Figure 6 legend)
- Preserved GEO preflight artifact 10131198025, run 34421899472.
- User-supplied CHEMPHYS-D-26-01542_report.pdf: transfer the criticisms about independent estimators, outcome-derived predictors, unsupported dynamics and reproducibility as audit questions; do not assume they prove the same defects in every biomedical component.
