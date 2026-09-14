# GRI Regulatory Substrate Atlas v0.2 Chi_bio extension

**Date:** 2026-09-12  
**Status:** P0-D/P0-Q ARCHITECTURE EXTENSION, NOT A LOCKED ATLAS  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Supersedes:** no historical Atlas record; extends `GRI_REGULATORY_SUBSTRATE_ATLAS_V0_1_SCHEMA_20260910.md` prospectively.

## Purpose

This extension prepares the Atlas to receive a future system-level `Chi_bio` coordinate without allowing the Atlas to define, tune, or manufacture that coordinate.

The Atlas and `Chi_bio` program remain separate:

```text
native observables -> System Model / candidate derivation -> Chi_bio candidate
                                                     |
                                                     v
                                        independent Atlas interpretation
```

Atlas placement may not be used upstream to select a formula, rescale unity, suppress discordant cancers, or choose a favored candidate.

## New optional record fields

Every Atlas record may carry the following fields even while `Chi_bio` is not admitted:

- `Chi_bio_status`
- `Chi_bio_candidate_id`
- `Chi_bio_value`
- `Chi_bio_uncertainty`
- `Chi_bio_validity_regime`
- `Chi_bio_refusal_state`
- `Chi_bio_scalar_modal_conglomerate_disagreement`
- `Chi_bio_pre_atlas_freeze_id`
- `Chi_bio_unity_boundary_status`
- `Chi_bio_unity_basis`
- `Chi_bio_independent_boundary_test_id`

Current mandatory values are:

```text
Chi_bio_status = NOT_ADMITTED
Chi_bio_value = null
Chi_bio_unity_boundary_status = NOT_TESTED
```

## Internal 32-cancer development Atlas

The existing TCGA cancers may be plotted now using established non-Chi coordinates and modal/conglomerate overlays. This is a development/historical Atlas and remains non-independent for validating the current Engine.

A future `Chi_bio` column may be added only after the candidate reaches at least `INTERNALLY_QUALIFIED_P0Q` under the Chi_bio admission program.

Before that point, an Atlas may show a **candidate reference line at 1 only in a clearly labeled methodological/schematic panel**, never as an observed biological boundary and never as a label applied to cancer points.

## Unity-boundary firewall

The Atlas renderer or downstream Tool must refuse a biological `Chi_bio = 1` boundary label unless all of the following are true:

1. `Chi_bio_status = UNITY_BOUNDARY_ADMITTED`;
2. a pre-Atlas freeze identifier exists;
3. `CB14` is satisfied;
4. a natural unity basis is recorded;
5. an independent boundary-test identifier is recorded;
6. uncertainty for the plotted record does not make its side of the boundary unresolved;
7. a freely estimated alternative boundary, when scientifically meaningful, has not been hidden.

If uncertainty spans unity, the record is plotted as boundary-unresolved rather than forced above or below.

## Plotting architecture

The primary Atlas should support separate views rather than a single omnibus panel:

1. established architecture scatter using non-Chi coordinates;
2. modal/vector overlays or companion panels;
3. conglomerate/context overlays or companion panels;
4. sensitivity/perturbation trajectories when available;
5. `Chi_bio` view only after admission state permits values;
6. unity-boundary view only after CB14.

No point size, color, axis transformation, or filtering rule may silently convert an established non-Chi metric into `Chi_bio`.

## Appendability

Once the Atlas record and adapter pipeline are fixed, adding another cancer/cohort should be an append-and-revalidate operation when the same representation is used. Representation-changing sources require an explicit adapter and independence audit, but do not require redesigning the Atlas itself.

## Current status

The Atlas can be built and plotted before `Chi_bio` exists. The `Chi_bio` program can advance before the independent Atlas is locked. Their first decisive intersection occurs only after a candidate coordinate is frozen independently and is ready for boundary-blind Atlas placement.