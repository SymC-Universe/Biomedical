# NSD Native Comparator Selection Plan

Status: **DIRECT STRUCTURAL COMPARATOR IDENTIFIED AS P0 PROPOSAL; P1 COMPARATOR NOT YET FROZEN.**

The scientific comparison question must be frozen before decisive comparator performance is inspected.

Candidate P1 method-scope comparison question for review:

> On known-truth multichannel stochastic systems within a declared local-linear/output-only validity regime, does the NSD SSI-COV Structural Engine recover poles, modal/carrier structure and admissible system organization at least as reliably as the strongest fair independent structural/modal baseline addressing the same target objects, while preserving valid refusals and uncertainty?

## Current leading structural comparator

**Dynamic Mode Decomposition (DMD)** is the leading primary comparator candidate because it:

- estimates reduced-order spatiotemporal eigenmodes;
- has peer-reviewed neural-recording applications;
- has been directly adapted to EEG and compared with output-only modal analysis;
- targets a structural/modal object closer to NSD's P1 method-scope question than spectral-only or connectivity-only baselines;
- is sufficiently distinct from SSI-COV to provide an informative independent comparison.

This status is **proposed, not frozen**. P0 development may implement DMD using the same synthetic inputs and known-truth scoring objects, but no decisive P1 comparison may be inspected until the full MFR-14 and challenge matrix are frozen.

## Later real-EEG baseline panel

The real-data tool will still require multiple domain-native baselines because no single comparator spans every NSD layer:

- periodic/aperiodic spectral parameterization for spectral state;
- PLI/wPLI-class measures or another independently justified established connectivity baseline for multichannel organization;
- DMD or another directly comparable state-space/modal method for structural dynamics;
- simple-feature baseline(s) for downstream classification/prediction.

A weak baseline will not be manufactured merely to create an ADDS result. See `LITERATURE_GATE_CANDIDATES_20260910.md` and `FOUR_HOLD_DECISION_PACKET_20260910.md`.
