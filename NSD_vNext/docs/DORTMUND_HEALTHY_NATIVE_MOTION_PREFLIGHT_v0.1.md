# Dortmund Healthy Native-Motion Preflight v0.1

**Status:** PROSPECTIVE NATIVE-BASELINE PREFLIGHT  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Dataset:** OpenNeuro ds005385 v1.0.3, DOI 10.18112/openneuro.ds005385.v1.0.3  
**Scientific scope:** independent healthy/reference EEG only. No NSD-derived variable, threshold, or historical control result enters this analysis.

## 1. Purpose

Quantify how much a healthy adult brain normally moves across state, cognitive load, and approximately five years before any NSD stability coordinate is introduced.

The first native baseline separates three quantities:

1. **state displacement:** eyes closed versus eyes open;
2. **short-horizon load displacement:** pre- versus post-cognitive battery;
3. **longitudinal drift:** session 1 versus session 2 at approximately five years.

The analysis does not define pathology or resilience failure.

## 2. Dataset structure

The public Dortmund Vital EEG release contains:
- 608 healthy adults aged 20-70 at session 1;
- 208 with approximately five-year follow-up;
- 64 EEG channels;
- 1000 Hz sampling;
- approximately 3 min per resting condition;
- eyes closed and eyes open;
- recordings before and after an approximately 2 h cognitive test battery.

Published exclusion criteria remove major neurological disease, psychiatric/affective disorder, major head injury/surgery/implants, psychotropic/neuroleptic use, and other severe disease classes described in the source paper.

## 3. Frozen native feature set

The first pass reproduces the four-feature framework of Park et al. 2026 before adding any new feature family.

### N1. Posterior alpha relative power
- preprocessing: 1-40 Hz band-pass;
- re-reference: average reference;
- PSD: Welch, 1-40 Hz;
- alpha band: 8-13 Hz;
- posterior ROI: parietal, parieto-occipital, and occipital electrodes available in the montage;
- value: alpha-band power divided by total 1-40 Hz power.

### N2. Alpha peak frequency
- same PSD;
- frequency of maximum spectral power within 8-13 Hz;
- posterior ROI first; whole-scalp sensitivity analysis only if prospectively added later.

### N3. Theta/beta ratio
- theta: 4-8 Hz;
- beta: 13-30 Hz;
- value: theta-band power / beta-band power;
- channel aggregation rule frozen before outcome inspection.

### N4. Aperiodic exponent
- PSD range: 2-40 Hz;
- FOOOF/specparam-style parameterization;
- peak width limits: 1-8 Hz;
- maximum peaks: 6;
- minimum peak height: 0.1;
- aperiodic mode: fixed.

No alpha peak amplitude or aperiodic offset is primary in v0.1.

## 4. Primary contrasts

For each subject and feature:

### State
[
Delta_{mathrm{EO/EC}} = X_{mathrm{EO,pre}}-X_{mathrm{EC,pre}}.
]

### Cognitive-load displacement
[
Delta_{mathrm{load,EC}} = X_{mathrm{EC,post}}-X_{mathrm{EC,pre}},
]
[
Delta_{mathrm{load,EO}} = X_{mathrm{EO,post}}-X_{mathrm{EO,pre}}.
]

### Longitudinal drift
For participants with session 2:
[
Delta_{5y}=X_{mathrm{ses2}}-X_{mathrm{ses1}}
]
within matched state and acquisition position.

These are distinct. A large EO/EC displacement is not evidence of poor recovery.

## 5. First pilot

Purpose: pipeline qualification only.

Selection:
- deterministic age- and sex-stratified sample from the published participants table;
- selection uses metadata only;
- no EEG outcome is opened to select subjects;
- target pilot size: 40 subjects if all required recordings are available;
- approximately balanced across decades and sex where the public metadata permits.

Required files per pilot subject:
- ses-1 EyesClosed pre;
- ses-1 EyesClosed post;
- ses-1 EyesOpen pre;
- ses-1 EyesOpen post.

The pilot passes pipeline qualification if:
1. all four conditions can be acquired and read reproducibly;
2. QC and feature extraction complete without outcome-dependent parameter changes;
3. expected literature directions for EO/EC are reproduced at the group level:
   - posterior alpha relative power: EC > EO;
   - alpha peak frequency: small EC > EO tendency;
   - theta/beta ratio: EO > EC;
   - aperiodic exponent: EO > EC;
4. numerical values are in plausible proximity to the published healthy results without requiring equality;
5. failures/missing files are preserved rather than silently replaced.

Failure of a literature direction does not license tuning. It triggers preprocessing/method discrepancy investigation.

## 6. Published quantitative comparison anchors

Park et al. 2026 reported at baseline:
- posterior alpha relative power: EC 0.453, EO 0.190, Cohen's d=1.553;
- alpha peak frequency: EC 9.946 Hz, EO 9.702 Hz, d=0.238;
- theta/beta ratio: EC 0.862, EO 1.157, d=-0.342;
- aperiodic exponent: EC 1.288, EO 1.511, d=-0.761.

Five-year ICC(A,1):
- posterior alpha relative power 0.843;
- theta/beta ratio 0.772;
- alpha peak frequency 0.734;
- aperiodic exponent 0.668.

These are external comparison anchors, not thresholds to fit.

## 7. Recovery-language restriction

This dataset directly supports healthy **state displacement**, **post-load displacement**, and **longitudinal drift**.

It does not by itself prove that post-load recordings are continuous recovery trajectories because only pre/post resting snapshots are available. Therefore:
- do not classify DIRECT_CAPTURE, OVERSHOOT, REBOUND, or RECROSSING from this dataset alone;
- use Dortmund to establish allowed healthy displacement and durable position;
- reserve trajectory-class calibration for datasets with sufficient temporal sampling after perturbation.

## 8. Next action after pilot

If the pilot is mechanically sound:
1. freeze exact code/environment;
2. scale the four-feature native analysis across the available session-1 cohort using streaming acquisition;
3. run the five-year matched subset separately;
4. estimate age-conditioned distributions and within-person state/load displacement;
5. only after this native baseline is frozen, compare qualified NSD (chi), (Chi), or (Chi_{mathrm{arc}}).

