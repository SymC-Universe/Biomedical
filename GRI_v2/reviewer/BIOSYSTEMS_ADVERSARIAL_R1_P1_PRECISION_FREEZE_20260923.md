# BioSystems adversarial Round 1 - external P1 Monte Carlo precision freeze

**Date:** 23 September 2026
**Status:** FROZEN BEFORE B=9,999 PRECISION OUTCOME
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Role:** post-result numerical-resolution sensitivity only.

## Motivation

The frozen external P1 used B=999, making the minimum attainable endpoint p-value 0.001 and the three-endpoint BH floor 0.003 when H1 has zero exceedances. Round-1 review correctly notes that this means the reported H1 q-value is partly limited by Monte Carlo resolution.

## Frozen question

Using the exact original P1 sources, participants, preprocessing, probe carrier, Hallmark mapping, statistics and null definitions, what endpoint p/q values are obtained when the deterministic null stream is extended from B=999 to B=9,999?

## Lanes

Run only the two publication-relevant platform lanes:

1. `PRIMARY_450K_N30`
2. `SENSITIVITY_EPIC_N26`

For each lane retain both:
- `PRIMARY_PUBLICATION`
- `MASKED_TECHNICAL`

The full n=32 lane is not required for the Monte Carlo-resolution question because it is a participant-count sensitivity, not a publication-primary p-value.

## Exact nesting rule

Use the original P1 seed namespace and exact seed functions. Set only the number of null repetitions to 9,999.

Therefore repetitions 0..998 are exactly the same deterministic null stream used in the original B=999 analysis; repetitions 999..9998 are an extension, not a new randomization scheme.

No participant, source, feature, preprocessing rule, null, endpoint, multiplicity family, direction, threshold, or interpretation is changed.

## Endpoint family

Recompute the original primary family:
- H1;
- H2;
- H3a.

BH correction remains across the same three endpoint p-values separately within each lane/track.

H3b may be computed internally by inherited code but has no inferential role in this precision gate.

## Disposition

This test does not change:
- the original P1 primary class;
- the original final `P1_REPRESENTATION_DEPENDENT` label;
- any preregistered decision.

It reports only higher-resolution p/q values and whether the original pass/non-pass statuses remain unchanged.

Outcome classes:
- `R1_P1_PRECISION_CONCORDANT`: all H1/H2/H3a q<0.05 statuses match original P1 in both lanes/tracks;
- `R1_P1_PRECISION_STATUS_CONFLICT`: any status changes;
- `R1_P1_PRECISION_HOLD`: source/identity/reconstruction failure.

## Claim ceiling

A smaller H1 p/q at B=9,999 means only that H1 lies deeper in the same frozen null tail than B=999 could resolve. It does not strengthen the biological null, remove confounding, or upgrade external generality.
