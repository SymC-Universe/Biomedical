# Independent-Literature Healthy Brain Baseline Evidence Map v0.1

**Status:** LITERATURE-DERIVED REFERENCE BASELINE / DEVELOPMENT  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Independence rule:** no NSD-derived result, threshold, control mean, simulated figure, or historical \(\chi\) value may define this baseline. NSD quantities may only be compared to the baseline after the external reference is frozen.

## 1. Baseline object

The healthy brain is represented as a conditional distribution plus an allowed motion envelope, not a single point:

\[
B(C)=P(X\mid C)
\]

where \(C\) includes age/development, sex where supported, eyes-open/eyes-closed state, task/rest state, arousal/sleep, recording context, site/device/reference, and other prospectively declared covariates.

For a feature family \(X\), healthy reference requires four distinct quantities:

1. **population position**: expected distribution at a given covariate state;
2. **within-person repeatability**: how much the same person normally changes across repeated measurements;
3. **state displacement**: how far normal task/arousal/eyes-open changes move the feature;
4. **longitudinal drift**: how the same person normally changes across months/years.

A feature cannot define pathological deviation until these four quantities are sufficiently characterized.

## 2. Lifespan normative backbone

### HarMNqEEG

Li et al., NeuroImage 2022, PMID 35398285, DOI 10.1016/j.neuroimage.2022.119190.

Evidence:
- 1,564 neurologically healthy participants;
- 9 countries;
- 12 EEG devices;
- 14 contributing studies;
- lifespan developmental equations for traditional and Riemannian cross-spectral qEEG descriptors;
- explicit site/device batch effects and harmonized z-scores;
- open code/data products for individual normative scoring.

Role:
- primary external lifespan cross-spectral/qEEG reference;
- age-conditioned normative location;
- site/device harmonization;
- cross-spectral/native-connectivity comparator.

Limit:
- primarily eyes-closed resting-state norms; not a complete perturbation/recovery baseline.

### Independent sex/age normative qEEG database

Kim et al., Front Neurosci 2021, PMID 34975376, DOI 10.3389/fnins.2021.766781.

Evidence:
- 1,289 healthy subjects;
- ages approximately 4.5-81;
- age- and sex-differentiated normative database.

Role:
- independent check that age/sex conditioning materially affects qEEG normalization;
- secondary normative reference, not a substitute for HarMN harmonization.

## 3. Healthy trait stability

### Resting spectral fingerprint

Kondacs/Braun-related long-term spectral reliability literature and Näpflin et al., Clin Neurophysiol 2007, PMID 17892969, DOI 10.1016/j.clinph.2007.07.022.

Evidence:
- healthy resting EEG spectral shape can remain sufficiently stable over 12-40 months to identify individuals above inter-individual alternatives;
- alpha peak frequency/shape contribute stable person-specific information.

Interpretation:
- large portions of resting spectral organization are trait-like;
- external perturbations and disease effects should be judged against intra-individual variability, not only group means.

### Parameterized periodic/aperiodic reliability

Pathania et al./Donoghue-method reliability literature; PubMed PMID 38100367 and PMID 39017780.

Evidence:
- aperiodic exponent/offset and periodic alpha/beta parameters commonly show fair-to-good or good reliability depending on state, duration, and method;
- reliability is state- and method-dependent;
- eyes-open parameterization can fail more often at noncentral sites in some datasets.

Role:
- aperiodic and periodic features may enter the healthy baseline only with method/state quality gates.

## 4. Healthy state movement

### Dortmund Vital Study

Getzmann et al., Sci Data 2024, PMID 39256413, DOI 10.1038/s41597-024-03797-w.

Evidence:
- 608 healthy adults ages 20-70;
- 64-channel EEG;
- eyes-open and eyes-closed recordings;
- recordings before and after an approximately two-hour cognitive block;
- approximately five-year follow-up for 208 participants.

Role:
- primary adult state-displacement and longitudinal reference;
- permits separation of EO/EC movement from pre/post cognitive-load movement;
- supports within-person change rather than case-control only.

### State sensitivity and long-term stability

Park et al. 2026, PMID 42395346.

Evidence:
- posterior alpha relative power strongly distinguishes EO/EC but is also highly stable longitudinally;
- alpha peak frequency is less state-sensitive and moderately stable;
- theta/beta ratio and aperiodic exponent show state sensitivity with moderate-to-good long-term stability.

Interpretation:
- a healthy feature can be both trait-like and state-responsive;
- state displacement must not automatically be classified as loss of baseline.

## 5. Healthy longitudinal drift

Dortmund five-year follow-up, PMID 42574751.

Evidence:
- periodic and aperiodic EEG parameters show fair-to-excellent five-year reliability;
- individual alpha peak frequency decreases over time;
- aperiodic exponent flattens over time;
- parameterized alpha power can remain comparatively stable.

Interpretation:
- baseline itself drifts lawfully with aging;
- a static lifetime "healthy point" is invalid;
- disease/progression must be evaluated against expected longitudinal motion.

## 6. Healthy microstate organization

### Normative temporal dynamics

Meta-analysis, PMID 37702825.

Evidence:
- 93 studies;
- 6,583 unique participants;
- normative estimates for resting EEG microstate temporal dynamics;
- substantial effects of development, diagnosis, and methods.

### Lifespan microstate development

Koenig et al. 2002, PMID 11969316.

Evidence:
- normative microstate data from 496 subjects ages 6-80;
- microstate variables change systematically with age.

### Reliability

Khanna et al. 2014, PMID 25479614; large-sample reliability study PMID 37410275.

Evidence:
- durations, occurrences, and coverage can show good-to-excellent repeatability when maps/procedures are held appropriately fixed;
- pairwise transition probabilities are substantially less reliable.

Interpretation:
- microstate occupancy/duration are better candidates for normative baseline than raw transition counts unless transition reliability is independently established.

## 7. Connectivity and dynamic-state baseline

### EEG/MEG connectivity

Resting connectivity can be reproducible, but reliability depends on metric, band, preprocessing, and connection.

### fMRI dynamic connectivity

Zhang et al., NeuroImage 2018, PMID 30120987.

Evidence:
- in 820 healthy subjects with repeated scans, dynamic FC was generally less reliable than static FC;
- reliability depends strongly on windowing/statistic.

### Connectome reliability

Tozzi et al. 2020, PMID 33615097.

Evidence:
- only a minority of individual functional-connectivity edges show good/excellent day-to-day reliability;
- network-level averages can be more reliable than individual edges;
- preprocessing choices materially change reliability.

Interpretation:
- a network feature cannot enter the normative baseline merely because it is popular;
- reliability filtering is mandatory before disorder deviation is calculated.

## 8. Healthy perturbation and homeostatic response

### Human homeostatic plasticity

Wittkopf et al., Eur J Neurosci 2021, PMID 34251703, DOI 10.1111/ejn.15389.

Evidence:
- systematic review/meta-analysis of 37 reports, 55 experiments, 700 healthy participants;
- repeated non-invasive stimulation can produce compensatory/homeostatic changes in corticospinal excitability;
- after repeated excitatory stimulation, response can shift in the inhibitory direction relative to a single block;
- after repeated inhibitory stimulation under some intervals, response can shift in the excitatory direction;
- pooled post-protocol MEPs did not necessarily remain different from baseline;
- substantial protocol heterogeneity and repeatability limitations remain.

Interpretation:
- healthy recovery is not necessarily monotonic;
- compensatory movement opposite the initial perturbation is biologically plausible;
- overshoot/rebound must be distinguished from incomplete return;
- there is no literature basis for one universal human recovery threshold.

### rTMS repeatability limitation

Systematic review/meta-analysis PMID 37771347.

Interpretation:
- perturbation aftereffects themselves can be variable in healthy people;
- any resilience margin must include protocol-specific and person-specific uncertainty.

## 9. Perturbational state dependence

TMS-EEG / perturbational-complexity literature (PMID 23946194; PMID 31133480) demonstrates that healthy wakefulness, sleep, and pharmacologically altered states produce different spatiotemporal responses to perturbation.

Criticality/PCI work (PMID 37994368) further shows that resting dynamical regime relates to perturbational response.

Interpretation:
- the same physical perturbation need not have the same healthy response in different brain states;
- recovery baselines must be state-conditioned.

## 10. Literature-derived recovery trajectory taxonomy

The following classes are operational hypotheses motivated by independent perturbation/homeostasis literature. They are not yet assigned numerical healthy thresholds.

- **DIRECT_CAPTURE**: displacement followed by sustained return to the prior healthy region;
- **DELAYED_CAPTURE**: sustained return after longer-than-usual recovery;
- **INCOMPLETE_RETURN / UNDERSHOOT**: trajectory approaches but never re-enters the prior healthy region;
- **OVERSHOOT_AND_CAPTURE**: crosses past the prior region, then returns and remains captured;
- **OVERSHOOT_AND_SHIFT**: crosses past the prior region and establishes a persistent state on the opposite side;
- **TRANSIENT_RETURN_REBOUND**: enters the prior region but subsequently exits again before sustained capture;
- **OSCILLATORY_CAPTURE**: repeated crossings with diminishing displacement followed by sustained capture;
- **PERSISTENT_RECROSSING**: repeated exits/re-entries without durable capture;
- **NEW_ADAPTIVE_BASELINE**: persistent new region with maintained/improved function and reproducibility;
- **NEW_MALADAPTIVE_BASELINE**: persistent new region associated with impaired function/reduced future resilience;
- **NONIDENTIFIABLE**: recording duration, noise, context, or measurement reliability cannot distinguish the class.

First crossing of the prior baseline region is explicitly not equivalent to recovery.

## 11. What is established versus open

### Established strongly enough to seed baseline construction

- age materially changes healthy EEG;
- site/device effects matter and can be harmonized;
- resting spectral organization contains stable trait-like structure;
- several periodic and aperiodic measures have useful test-retest reliability;
- healthy state changes such as EO/EC and cognitive load produce lawful displacement;
- healthy longitudinal aging produces measurable drift;
- microstate duration/coverage can be reasonably stable while transitions are less stable;
- network measures vary widely in reliability;
- healthy homeostatic responses can be compensatory and non-monotonic.

### Not established and therefore not to be assumed

- a universal healthy \(\chi\);
- one universal brain-recovery time constant;
- one universal perturbation amplitude at which recovery fails;
- one universal overshoot threshold;
- one universal number of failed recoveries that causes baseline migration;
- a single healthy attractor;
- that all new baselines are pathological;
- that the same recovery architecture applies across pain, mood disorders, ADHD, autism, Parkinson's, and addiction.

## 12. Construction order

1. freeze the independent literature evidence ledger;
2. reproduce HarMNqEEG age-conditioned native norms where accessible;
3. reproduce Dortmund EO/EC and pre/post-task healthy displacement;
4. quantify long-term drift using published/Dortmund follow-up structure;
5. establish reliability filters for spectral, aperiodic, microstate, and connectivity variables;
6. define healthy state-conditioned motion envelopes;
7. only after those native baselines are frozen, introduce qualified NSD \(\chi\), \(\Chi\), and \(\Chi_{\mathrm{arc}}\);
8. compare each target condition to the external normative baseline;
9. use historical NSD results only as secondary comparison, never as baseline construction evidence.

