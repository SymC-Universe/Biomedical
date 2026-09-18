# GRI Conglomerate Chi C1 carrier-contract closure

**Date:** 2026-09-18  
**Branch:** `gri-conglomerate-chi-tool-v1-20260918`  
**Workflow run:** `35337802337`  
**Conclusion:** `success`

## Closed result

The block-preserving C1 carrier schema and materializer passed the known-truth contract suite on GitHub Actions.

The tests verify, at minimum:

- blocks remain distinct rather than being collapsed into a master score;
- missing/refused values cannot masquerade as numeric zero;
- duplicate carrier keys hard-fail;
- forbidden master-score / Chi-value fields hard-fail;
- numeric temporal measurements require directly observed ordering;
- a time index cannot be populated when time order is unknown.

## Consequence

The C1 data contract is mechanically ready. The next task is real block materialization from frozen/public sources and previously earned derived artifacts. Passing this contract does not establish a diagnostic or predictive result.
