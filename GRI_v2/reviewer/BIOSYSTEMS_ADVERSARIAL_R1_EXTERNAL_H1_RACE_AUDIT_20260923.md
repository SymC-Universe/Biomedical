# BioSystems adversarial Round 1 external H1 race sensitivity audit

**Date:** 23 September 2026
**Status:** COMPLETE / POST-RESULT ADVERSARIAL SENSITIVITY
**Parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Round-1 branch:** `biosystems-adversarial-r1-20260923`
**Workflow:** `35812295850`
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_V01`
**Artifact ID:** `10730720732`
**Artifact ZIP SHA-256:** `654ad38c91ae2ba479c20641e06055465220dcf73d4fffe6734a1053f418bd94`

## Question

Adversarial review identified the mixed AA/EA composition of the primary external 450K cohort as one plausible source of the unusually large external H1 effect.

The original P1 architecture endpoints were already verified to use **tumor samples only**, not pooled tumor+adjacent states. This sensitivity therefore tests the remaining known race-label axis.

## Prospective freeze and mechanical amendment

The Round-1 sensitivity was frozen before its numerical outcome was opened in:
`BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_FREEZE_20260923.md`.

The first execution failed mechanically because EPIC contains only EA-labeled participants, making a two-level race regression unidentified. No endpoint result was written or printed before that failure.

A pre-outcome implementation amendment then froze:
- explicit AA/EA residualization only in mixed-race lanes;
- refusal of race regression in a single-race lane;
- EPIC retained as a race-homogeneous supporting sensitivity and unable to rescue the mixed-race primary.

No participant, probe, null, B, threshold, or endpoint changed.

## Primary 450K n=30

Source composition: 25 AA / 5 EA tumors.

Primary-publication track:

| Analysis | H1 effect | empirical p |
|---|---:|---:|
| Original raw reconstruction | +0.3030902452 | 0.001 |
| Race-residualized | +0.3169520962 | 0.001 |
| AA-only, n=25 | +0.3062264585 | 0.001 |

Race-residualized effect retention relative to raw:
**1.045735** (104.6%).

Masked-technical track:

| Analysis | H1 effect | empirical p |
|---|---:|---:|
| Raw | +0.3061725789 | 0.001 |
| Race-residualized | +0.3199770391 | 0.001 |
| AA-only, n=25 | +0.3094796350 | 0.001 |

## Full 450K n=32

Source composition: 27 AA / 5 EA tumors.

Primary track:
- raw: +0.3170451231;
- race-residualized: +0.3289833299;
- AA-only n=27: +0.3169687259;
- all empirical p=0.001.

The masked track gives the same qualitative result.

## EPIC n=26

All 26 EPIC participants are EA-labeled.

Therefore AA/EA regression is not identifiable and is explicitly refused.

Race-homogeneous raw H1:
- primary-publication: +0.3583937311, p=0.001;
- masked-technical: +0.3595136537, p=0.001.

## Disposition

`R1_H1_RACE_ROBUST`

Removing the known AA/EA axis does not attenuate the external 450K H1 signal. The effect is also present within AA tumors alone and in the all-EA EPIC cohort.

This falsifies **race label as a sufficient explanation** for the external H1 magnitude under this source representation.

It does **not** establish a biological mechanism for H1 and does not eliminate:
- tumor purity;
- leukocyte/stromal composition;
- age or sex;
- center/plate/array/batch effects;
- molecular subtype;
- other structured sample-level covariance.

The original P1 classification remains `P1_REPRESENTATION_DEPENDENT`; this post-result sensitivity cannot rescue or upgrade it.

## Manuscript consequence

Permissible:
> The unusually large external H1 effect is not explained by the source AA/EA axis: per-CpG race residualization retained 104.6% of the primary H1 effect, and H1 remained present within AA tumors alone. Other composition and technical sources remain unresolved.

Not permissible:
> H1 is composition independent.

