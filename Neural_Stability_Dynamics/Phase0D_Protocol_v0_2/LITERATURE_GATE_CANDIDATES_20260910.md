# NSD Domain-Native Evidence Gate, Candidate Sources

Date: 2026-09-10
Status: **P0 SOURCE-OF-RECORD CANDIDATE LOG. NOTHING HERE IS FROZEN AS THE P1 COMPARATOR OR DECISION RULE.**

Purpose: begin the protocol-required native-science review before selecting a P1 comparator, model-adequacy rule, uncertainty method, or real-data interpretation.

## Spectral-state comparator candidate

Donoghue et al., *Parameterizing neural power spectra into periodic and aperiodic components*, Nature Neuroscience 23, 1655-1665 (2020), DOI `10.1038/s41593-020-00744-x`.

Source-of-record check: Nature Neuroscience article page inspected on 2026-09-10. The paper separates periodic peaks from aperiodic structure and reports center frequency, power, bandwidth, aperiodic offset and exponent. It validates the approach on simulation and applies it to electrophysiological data.

Disposition: **COMPARATOR_CANDIDATE_SPECTRAL_STATE_ONLY.** It is not automatically the strongest fair comparator for NSD's multichannel structural-identification question, and it does not validate SSI-COV neural modes.

## Connectivity/system-organization comparator candidates

Stam, Nolte & Daffertshofer, *Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources*, Human Brain Mapping 28, 1178-1193 (2007), DOI `10.1002/hbm.20346`.

Vinck et al., *An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias*, NeuroImage 55, 1548-1565 (2011), DOI `10.1016/j.neuroimage.2011.01.055`.

Source-of-record checks: PubMed / journal records inspected on 2026-09-10. These methods explicitly address multichannel electrophysiological connectivity and the confounding effects of common sources / volume conduction. They therefore belong in the comparator search rather than being silently replaced by a convenient correlation baseline.

Disposition: **COMPARATOR_CANDIDATES_CONNECTIVITY_ONLY.** They are not yet frozen as the strongest comparator for the full NSD task.

## SSI uncertainty-method candidate

Reynders, Maes, Lombaert & De Roeck, *Uncertainty quantification in operational modal analysis with stochastic subspace identification: Validation and applications*, Mechanical Systems and Signal Processing 66-67, 13-30 (2016), DOI `10.1016/j.ymssp.2015.04.018`.

Source-of-record check: journal article page inspected on 2026-09-10. It validates covariance estimation for SSI-derived modal characteristics against variability across repeated structural measurements.

Disposition: **UNCERTAINTY_METHOD_CANDIDATE, NON-NEURAL VALIDATION.** This establishes that principled SSI uncertainty machinery exists. It does not establish that the same assumptions or calibration are valid for EEG, so transfer to NSD requires a separate validity argument and known-truth/neural-data qualification.

## Current conclusion

The search has begun but MFR-05 and MFR-09 remain unresolved. No comparator, uncertainty rule, numerical tolerance, biological mechanism, chi boundary, or regime boundary is frozen from these sources. The next search must determine whether established neural state-space/system-identification methods directly address the same structural-recovery task and must examine model-adequacy diagnostics appropriate to output-only neural time series.
