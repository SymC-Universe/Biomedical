# NSD Domain-Native Evidence Gate, Candidate Sources

Date: 2026-09-10
Status: **P0 SOURCE-OF-RECORD EVIDENCE LOG. SCIENCE-ADJACENT SELECTIONS BELOW ARE PROPOSED, NOT P1-FROZEN.**

Purpose: satisfy the protocol-required native-science review before selecting a P1 comparator, model-adequacy rule, uncertainty method, unequal-order adjudication rule, or real-data interpretation.

## 1. Direct structural/modal comparator evidence

### Griffith & Hubbard 2021

Tristan D. Griffith & James E. Hubbard, *System identification methods for dynamic models of brain activity*, Biomedical Signal Processing and Control 68, 102765 (2021), DOI `10.1016/j.bspc.2021.102765`.

Source-of-record finding: the paper explicitly adapts and compares Output-Only Modal Analysis (OMA) and Dynamic Mode Decomposition (DMD) for EEG. Both estimate reduced-order state-space/eigenmode descriptions of spatiotemporal neural dynamics. The authors apply them to DEAP and EEGMMI.

Disposition: **DMD_PRIMARY_P1_STRUCTURAL_COMPARATOR_CANDIDATE, NOT FROZEN.** This is a substantially closer comparator to the current NSD structural-recovery question than a spectral-only or connectivity-only feature set. OMA itself overlaps the same broad output-only modal-analysis family as NSD's SSI-COV route and is therefore more useful as lineage/domain precedent than as the sole independent comparator.

### Brunton et al. 2016

Bingni W. Brunton et al., *Extracting spatial-temporal coherent patterns in large-scale neural recordings using dynamic mode decomposition*, Journal of Neuroscience Methods 258, 1-15 (2016), DOI `10.1016/j.jneumeth.2015.10.010`.

Source-of-record finding: DMD is adapted to large-scale human neural recordings as a coupled spatial-temporal modal decomposition and is evaluated on subdural array recordings.

Disposition: **DMD_NEURAL_DOMAIN_SUPPORT.** This strengthens DMD's legitimacy as a neural modal baseline but does not by itself prove that DMD is optimal for the future real-EEG Tool.

## 2. Spectral-state comparator candidate

Donoghue et al., *Parameterizing neural power spectra into periodic and aperiodic components*, Nature Neuroscience 23, 1655-1665 (2020), DOI `10.1038/s41593-020-00744-x`.

Source-of-record finding: separates periodic peaks from aperiodic structure and reports center frequency, power, bandwidth, aperiodic offset and exponent; validated on simulation and electrophysiological data.

Disposition: **COMPARATOR_CANDIDATE_SPECTRAL_STATE_ONLY.** Appropriate for the later EEG spectral-state baseline, not a replacement for a direct structural/modal P1 comparator.

## 3. Connectivity/system-organization comparator candidates

Stam, Nolte & Daffertshofer, *Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources*, Human Brain Mapping 28, 1178-1193 (2007), DOI `10.1002/hbm.20346`.

Vinck et al., *An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias*, NeuroImage 55, 1548-1565 (2011), DOI `10.1016/j.neuroimage.2011.01.055`.

Disposition: **COMPARATOR_CANDIDATES_CONNECTIVITY_ONLY.** These belong in the later real-EEG/native-toolkit baseline panel, not in the synthetic P1 pole/carrier recovery comparison.

## 4. Model-adequacy evidence

### Billinger et al. 2014 / SCoT

M. Billinger et al., *SCoT: a Python toolbox for EEG source connectivity*, Frontiers in Neuroinformatics 8:22 (2014), DOI `10.3389/fninf.2014.00022`.

Source-of-record finding: for EEG MVAR modeling, the authors explicitly require residuals to be serially uncorrelated and implement multivariate portmanteau/Li-McLeod residual-whiteness testing. Because residuals may be non-Gaussian, they estimate the null distribution using temporally permuted surrogate residuals rather than relying only on a Gaussian chi-square approximation.

Disposition: **MODEL_ADEQUACY_COMPONENT_SUPPORTED: RESIDUAL/INNOVATION WHITENESS.**

### Courellis et al. 2017

H. S. Courellis et al., *EEG-Based Quantification of Cortical Current Density and Dynamic Causal Connectivity Generalized across Subjects Performing BCI-Monitored Cognitive Tasks*, Frontiers in Neuroscience 11:180 (2017), DOI `10.3389/fnins.2017.00180`.

Source-of-record finding: fitted MVAR models were stable and had >90% consistency, yet none passed residual-whiteness tests. The authors explicitly interpret this as uncaptured temporal structure.

Disposition: **MODEL_ADEQUACY_FIREWALL_SUPPORTED.** Stability or high reconstruction/consistency alone cannot license model adequacy.

### Cross-validated neural self-prediction

Sani et al., *Dissociative and prioritized modeling of behaviorally relevant neural dynamics using recurrent neural networks*, Nature Neuroscience (2024), article `s41593-024-01731-2`.

Source-of-record finding: model quality includes cross-validated one-step-ahead prediction of neural activity using past neural observations, termed neural self-prediction.

Disposition: **MODEL_ADEQUACY_COMPONENT_SUPPORTED: OUT-OF-SAMPLE PREDICTIVE ADEQUACY.** This supports predictive checking as a neural-native model test; it does not require NSD to adopt the DPAD model itself.

## 5. SSI uncertainty evidence

Edwin Reynders, Rik Pintelon & Guido De Roeck, *Uncertainty bounds on modal parameters obtained from stochastic subspace identification*, Mechanical Systems and Signal Processing 22, 948-969 (2008), DOI `10.1016/j.ymssp.2007.10.009`.

Source-of-record finding: derives single-record uncertainty/covariance estimates for SSI-COV/ref modal parameters using first-order sensitivity to perturbations of measured output-only data, and treats stabilization-diagram bias separately from variance.

Reynders, Maes, Lombaert & De Roeck, *Uncertainty quantification in operational modal analysis with stochastic subspace identification: Validation and applications*, Mechanical Systems and Signal Processing 66-67, 13-30 (2016), DOI `10.1016/j.ymssp.2015.04.018`.

Disposition: **UNCERTAINTY_METHOD_CANDIDATE, METHOD-NATIVE BUT NON-NEURAL VALIDATION.** Analytical SSI uncertainty is a principled candidate for the estimator layer. It still requires known-truth calibration for NSD and must not be presented as already validated for EEG.

## 6. Unequal-order / mode-persistence evidence

Edwin Reynders, Jeroen Houbrechts & Guido De Roeck, *Fully automated (operational) modal analysis*, Mechanical Systems and Signal Processing 29, 228-250 (2012), DOI `10.1016/j.ymssp.2012.01.007`.

Source-of-record finding: stabilization-diagram interpretation explicitly identifies recurring physical modes across models of differing order, clustering similar modal properties and separating closely spaced modes using carrier/mode-shape information such as MAC.

Disposition: **UNEQUAL_ORDER_TRACKING_CONCEPT_SUPPORTED, EXACT NSD RULE NOT FROZEN.** Observable-order change need not force blanket refusal of every shared modal claim. Exact cross-segment matching costs, uncertainty handling, crowding rules and thresholds still require P0 qualification.

## Current evidence-gate conclusion

The previous four scientific holds are no longer evidence-empty. The literature now supports a coherent candidate architecture:

1. **P1 structural comparator:** DMD is the leading direct neural comparator candidate.
2. **Model adequacy:** use multiple logically distinct checks; stable poles or high reconstruction alone are insufficient.
3. **Uncertainty:** SSI-native first-order covariance/sensitivity is a principled primary candidate, with known-truth resampling/calibration as an independent check.
4. **Unequal order:** shared/added/lost mode reporting is defensible in principle; ambiguous assignments must remain unresolved/indeterminate.

No numerical tolerance, comparator identity, weighting, uncertainty confidence level, resampling count, challenge matrix, P1 seed, P1 system list, biological mechanism, chi boundary, or regime boundary is frozen by this evidence log.
