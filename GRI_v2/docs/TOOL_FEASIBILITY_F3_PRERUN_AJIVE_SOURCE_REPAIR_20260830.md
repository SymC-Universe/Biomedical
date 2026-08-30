# F3 pre-run comparator source repair: AJIVE implementation

**STATUS: RECORDED BEFORE AJIVE BASELINE EXECUTION**

Date: 2026-08-30

`TOOL_FEASIBILITY_F3_BASELINE_FREEZE_20260830.md` named the `idc9/py_jive` Python implementation for the AJIVE comparator.

Inspection of that repository before comparator execution showed that its own README marks the package as deprecated and directs users to `https://github.com/idc9/mvdr` for the new AJIVE code.

## Repair

The F3 comparator remains **AJIVE**. Only the implementation lineage changes:

- deprecated source: `idc9/py_jive`
- replacement source: `idc9/mvdr`

The replacement repository describes itself as an sklearn-compatible multi-view dimensionality-reduction package including AJIVE and multiview CCA. Its AJIVE path also requires `idc9/ya_pca`.

This repair is based only on upstream package-maintainer deprecation guidance. No AJIVE comparison result had been generated when the source was changed.

If the replacement implementation cannot run in the current Python environment for a documented dependency/API reason, record the comparator as mechanically blocked or use a separately documented compatible environment. Do not substitute a weaker method and label it AJIVE.
