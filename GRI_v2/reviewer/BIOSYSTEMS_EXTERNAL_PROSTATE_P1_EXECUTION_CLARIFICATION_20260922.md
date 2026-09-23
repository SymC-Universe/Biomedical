# BioSystems independent prostate P1 execution clarification - 22 September 2026

**Status:** FROZEN BEFORE EXTERNAL GRI OUTCOME OPENING  
**Parent:** `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`  
**Source-only preflight:** run `35801003396` PASS; no GRI biological outcome computed.

This note resolves two implementation details that were not numerically explicit in the parent freeze. It does not change the transported scientific claim.

## Primary tissue state

The transported C1 claim is a tumor-architecture claim. Therefore:

- primary P1-H1/H2/H3a are evaluated on the frozen 30 **tumor** samples from the primary 450K paired participant set;
- the paired adjacent samples are retained for the separately frozen external tumor--normal corroboration;
- adjacent tissue cannot rescue a failed primary tumor transport endpoint.

## H1 repeated construction null

The parent freeze requires an H1 probe-marginal construction null distribution but did not state its Monte-Carlo count.

Before outcome opening, freeze:

- H1 construction-null replicates: **B=999**;
- each replicate independently permutes patient order within every retained CpG column;
- H1 effect: observed `S_spec - median(S_spec_null)`;
- H1 upper-tail Monte-Carlo p: `(1 + count(S_spec_null >= S_spec_observed))/(B+1)`.

This matches the already-frozen B=999 resolution of H2/H3a and makes all three primary endpoint p-values eligible for the single frozen BH family.

## Exact transported methylation carrier

The primary and EPIC sensitivity methylation carriers are restricted to the exact 22,601 PanCan C1 probe IDs recovered from the frozen PanCan methylation source under the exact C1A source-only inventory. External probes outside this carrier are not used for P1-H1/H2/H3a.

The C1 PROMOTER_CORE map and technical mask are reconstructed from the same frozen C1A annotation/Chen source identities before external values are analyzed.

## RNA normalization carrier

For the primary 450K lane, RNA size factors are fitted once using the 60 selected paired RNA samples (30 tumor + 30 adjacent), without using tissue labels in the normalization formula. The resulting normalized/log2 values are then subset to the 30 tumor samples for P1-H2/H3a and to both states for the secondary tumor-normal RNA corroboration.

EPIC sensitivity analogously fits its RNA normalization on all 52 paired samples (26 + 26).

No normalization parameter is selected from P1 endpoint results.

## Sensitivity conflict rule

Before outcome opening, define a material conflict for a primary endpoint as either:

- reversal of the sign of its null-corrected effect relative to the primary 450K publication track; or
- disagreement in BH-q<0.05 endpoint status between the primary track and the mandatory sensitivity being compared.

The full-n=32 450K analysis and the EPIC lane remain sensitivities and cannot rescue the frozen n=30 primary. A conflict is reported as representation/platform dependence rather than averaged away.
