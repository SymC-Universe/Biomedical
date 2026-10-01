# Healthy-Brain Quantitative Literature Ledger v0.1

**Status:** INDEPENDENT NATIVE BASELINE / DEVELOPMENT  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Independence rule:** no NSD-derived value may define this ledger. All numeric anchors below come from external healthy/reference neuroscience literature.

## Purpose

This ledger records quantitative healthy-brain reference facts that constrain later baseline, recovery, and migration analyses. These values are not diagnostic thresholds. They define observed reliability, state sensitivity, lifespan/longitudinal motion, or homeostatic response under specific methods and populations.

## Quantitative anchors

| ID | Feature / construct | Healthy/reference sample and interval | Quantitative result | Baseline role | Source |
| --- | --- | --- | --- | --- | --- |
| HB-Q01 | absolute alpha power | Dortmund subgroup n=370, four recordings in session 1 | ICC 0.92-0.94 EC; 0.87-0.90 EO | strong short-term trait/repeatability anchor; state-specific | Getzmann et al. 2024 dataset descriptor, PMID 39256413; Metzen et al. 2022 |
| HB-Q02 | posterior alpha relative power | healthy adults, five-year longitudinal analysis | EO/EC state effect Cohen's d=1.553; five-year ICC=0.843 | example of a feature that is both strongly state-sensitive and longitudinally stable | Park et al. 2026, PMID 42395346 |
| HB-Q03 | alpha peak frequency | same five-year analysis | EO/EC d=0.238; five-year ICC=0.734 | comparatively state-insensitive but moderately trait-stable | Park et al. 2026, PMID 42395346 |
| HB-Q04 | theta/beta ratio | same five-year analysis | EO/EC d=-0.342; five-year ICC=0.772; outlier sensitivity noted | state-sensitive candidate with caution on individual stability | Park et al. 2026, PMID 42395346 |
| HB-Q05 | aperiodic exponent | same five-year analysis | EO/EC d=-0.761; five-year ICC=0.668 | moderate-longitudinal stability plus substantial state movement | Park et al. 2026, PMID 42395346 |
| HB-Q06 | parameterized periodic/aperiodic metrics | healthy adults, approximately five-year follow-up | ICC range 0.51-0.88; alpha peak frequency decreased, aperiodic exponent flattened, parameterized alpha power unchanged | establishes lawful longitudinal drift | PMID 42574751 |
| HB-Q07 | aperiodic components | healthy young adults, 90 min and one month; multiple states/durations/methods | reliability range 0.53-0.91; >3 min, EC/mental arithmetic, and LMER gave better reliability | method/state/duration-specific reliability floor | Li et al. 2024, PMID 39017780 |
| HB-Q08 | microstate duration/occurrence/coverage | Dortmund-like large healthy sample, day 1 n=583, day 2 n=542 | short-term average ICC 0.874-0.920; longer-term average ICC 0.671-0.852 | reliable state-organization features | Kleinert et al. 2024, PMID 37410275 |
| HB-Q09 | microstate transitions | same sample | poor retest reliability | transition probabilities cannot define a baseline without additional reliability qualification | Kleinert et al. 2024, PMID 37410275 |
| HB-Q10 | normative microstate dynamics | meta-analysis, 93 studies, 6,583 unique participants | population-level normative estimates with systematic developmental/methodological heterogeneity | broad external distribution reference; not a single universal mean | PMID 37702825 |
| HB-Q11 | homeostatic corticospinal response | 37 reports, 55 experiments, 700 healthy participants | repeated excitatory NIBS decreased MEP relative to single block at 0-30 min; repeated inhibitory stimulation with <=10 min interval increased MEP; pooled MEP not different from baseline | evidence that healthy response can reverse/compensate rather than return monotonically | Wittkopf et al. 2021, PMID 34251703 |
| HB-Q12 | HarMNqEEG lifespan norm | 1,564 neurologically healthy participants, 9 countries, 12 devices, 14 studies | age/frequency-dependent mean and SD models for traditional and Riemannian qEEG DPs with batch harmonization | primary external lifespan population baseline | Li et al. 2022, PMID 35398285 |

## Immediate constraints these anchors impose

1. **First crossing is not recovery.** A feature can make substantial state-dependent excursions while remaining trait-stable over years.
2. **State sensitivity and trait stability are separate axes.** HB-Q02 and HB-Q05 demonstrate that both can coexist.
3. **Feature reliability is heterogeneous.** Microstate occupancy/duration can be much more reliable than pairwise transition probabilities.
4. **Longitudinal drift is normal.** Healthy ageing changes some periodic and aperiodic features.
5. **Healthy response can be non-monotonic.** Homeostatic stimulation studies support compensatory reversal, so overshoot/rebound cannot be collapsed with incomplete return.
6. **Methods matter.** Recording duration, state, fitting method, montage/site/device, and preprocessing can materially change baseline reliability.
7. **No universal scalar baseline is licensed.** These studies constrain native neural variables only.

## Recovery trajectory taxonomy for later healthy calibration

The quantitative threshold for each class remains unfrozen until appropriate healthy data are analyzed.

- DIRECT_CAPTURE
- DELAYED_CAPTURE
- INCOMPLETE_RETURN / UNDERSHOOT
- OVERSHOOT_AND_CAPTURE
- OVERSHOOT_AND_SHIFT
- TRANSIENT_RETURN_REBOUND
- OSCILLATORY_CAPTURE
- PERSISTENT_RECROSSING
- NEW_ADAPTIVE_BASELINE
- NEW_MALADAPTIVE_BASELINE
- NONIDENTIFIABLE

A trajectory must remain inside a prospectively derived healthy capture region for a prospectively derived dwell period before it counts as recovered.

## Next quantitative work

1. inspect and reproduce HarMNqEEG traditional log-spectrum age/frequency norm surfaces;
2. build an independent Dortmund native-feature pipeline for EC/EO and pre/post-cognitive displacement;
3. estimate population, within-person state, and five-year drift components separately;
4. derive reliability-aware native healthy motion envelopes;
5. only after those are frozen, introduce NSD \(\chi\), \(\Chi\), and \(\Chi_{\mathrm{arc}}\).

