# Stage D Randomization Policy v0.1

All stochastic Stage-D procedures must be deterministic and namespace-separated.

Base namespace: `GRI_STAGE_D_20260908`.

Subnamespaces must include at minimum:
- dataset stage ID (D1-D4);
- detector family;
- null/control family;
- replicate index;
- assay/layer;
- analysis version.

Seeds must be generated from the full namespace by a stable documented hash-to-integer procedure. Reusing one random stream across directly compared sensitivity variants is preferred when dimensions permit because it reduces Monte Carlo noise in paired comparisons. Independent scientific null families retain separate namespace components.

Exact replicate counts remain to be frozen at D0.3 after design/sample support is known and before biological outcome inspection.
