# BioSystems adversarial Round 1 - external P1 Monte Carlo precision audit

**Date:** 23 September 2026
**Status:** CLOSED / R1_P1_PRECISION_CONCORDANT
**Branch:** `biosystems-adversarial-r1-20260923`
**Freeze:** `BIOSYSTEMS_ADVERSARIAL_R1_P1_PRECISION_FREEZE_20260923.md`
**Workflow:** `35815566680`
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_P1_PRECISION_V01`
**Artifact ID:** `10731477329`
**Artifact digest:** `sha256:c4a54434de5584be0f2d42defc10b82f5c3af4c9584a941ed6391f01bdaa6c65`

## Role

Post-result numerical-resolution sensitivity only. The original B=999 P1 decision and final `P1_REPRESENTATION_DEPENDENT` label remain immutable.

The B=9,999 streams use the same source identities, participant sets, endpoint definitions, seed namespace, null constructions and BH family. Repetitions 0..998 are nested from the original deterministic stream; only additional repetitions were appended.

## Primary 450K n=30, B=9,999

Primary-publication track:

| Endpoint | Observed | Null median | Effect | p | BH q | Status |
|---|---:|---:|---:|---:|---:|---|
| H1 | 0.303894 | 0.000802 | +0.303092 | 0.0001 | 0.0003 | PASS |
| H2 | 0.257193 | 0.239201 | +0.017992 | 0.2952 | 0.4428 | unresolved |
| H3a | 0.077197 | 0.119021 | -0.041824 | 0.8212 | 0.8212 | no transport |

Masked-technical track preserves the same endpoint statuses:
- H1 q=0.0003;
- H2 q=0.4416;
- H3a q=0.8293.

## EPIC n=26, B=9,999

Primary-publication track:

| Endpoint | Observed | Null median | Effect | p | BH q | Status |
|---|---:|---:|---:|---:|---:|---|
| H1 | 0.359251 | 0.000856 | +0.358395 | 0.0001 | 0.0003 | PASS |
| H2 | 0.218066 | 0.232855 | -0.014789 | 0.6662 | 0.6662 | unresolved |
| H3a | 0.161709 | 0.131624 | +0.030085 | 0.3505 | 0.52575 | unresolved |

Masked-technical track again preserves status:
- H1 q=0.0003;
- H2 q=0.6613;
- H3a q=0.5697.

## Adjudication

All H1/H2/H3a pass/non-pass statuses match the original B=999 P1 result in both platform lanes and both technical tracks.

Machine disposition:

`R1_P1_PRECISION_CONCORDANT`

The Round-1 criticism was correct that the original H1 q=0.003 sat at the B=999 Monte Carlo floor. The higher-resolution test now shows H1 at the B=9,999 floor, p=0.0001 and BH q=0.0003, while H2/H3a remain clearly unresolved/nontransporting.

This strengthens numerical precision only. It does **not** strengthen the biological null, remove composition/batch confounding, or change the original P1 classification.

## Reviewer-facing wording

Use:

> The original external P1 used the prospectively frozen B=999 permutation family, for which H1 reached the Monte Carlo resolution floor (p=0.001; BH q=0.003). A post-result numerical-resolution sensitivity extended the same deterministic null stream to B=9,999 without changing any sample, feature, endpoint or null definition. H1 remained at the finer resolution floor on both 450K and EPIC (p=0.0001; BH q=0.0003), whereas H2/H3a remained unresolved. The original P1 decision was not reclassified.

## Claim ceiling

This audit answers only Monte Carlo resolution. The canonical H1 null remains an independence/construction floor.
