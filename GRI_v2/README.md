# GRI v2 / Cancer Stability Atlas

**Status:** DEVELOPMENT PROGRAM, NOT A VALIDATED CANCER TOOL  
**Active phase:** Stage B2 orthogonal static integration  
**Status date:** 2026-08-29

## Objective

The active objective is to build the most predictive, falsifiable cancer-stability tool supported by the data and by the updated Chemistry and Stability Arc methodology.

The historical GRI manuscript is not the target model. It is provenance: a source of observations, failed claims, and candidate ideas. The new tool is not required to reproduce its variables, mechanisms, gene rankings, or conclusions.

If the mathematics retains an old component, it must earn retention prospectively. If the mathematics rejects it, the rejected component remains archived.

## Notation used in this program

- **V**: expression-adjusted variability/fluctuation structure. `V` is a static measured coordinate, not a damping quantity.
- **L**: lineage/context dependence. `L` measures how strongly a feature depends on cancer lineage/context.
- **C_in**: read “C sub in.” Internal Hallmark-module coherence, measured from within-module expression relationships.
- **C_out**: read “C sub out.” Coupling of a Hallmark module to the external Hallmark-union background.
- **chi**: reserved for a genuine dynamical balance coordinate of the form `Gamma/(2*Omega)`. No valid biological chi has yet been admitted in this cancer program.
- **Gamma**: capital gamma. If chi is ever admitted, Gamma must be an independently meaningful relaxation/damping/recovery/decay rate for the same dynamical coordinate.
- **Omega**: capital omega. If chi is ever admitted, Omega must be an independently meaningful intrinsic response/restoring rate or frequency for that same coordinate.

## Active scientific rules

- `CV/2` is the historical scalar comparator. It is not chi.
- Static RNA and multiomic observables remain independent map axes rather than being folded into chi.
- `chi = 1`, if a valid chi is eventually measured, is a dynamical regime-balance boundary of the applicable model. It is not a presumed cancer optimum, maximum organization point, healthy state, or therapeutic target.
- No feature receives privileged status because it appeared in the historical manuscript.
- Higher `C_in` or lower `C_out` is not inherently better, healthier, or more stable.
- Model selection is driven by predictive performance, calibration, robustness, ablation, appropriate baselines, and external validation.
- Manuscript reconstruction is downstream of a validated tool architecture and must not steer feature selection or interpretation.

## Completed development layers

### Historical scalar closure

The historical `CV/2` experiment was reconstructed and audited. A pronounced mean/variability geometry exists in PanCanAtlas RNA expression, but the frozen construction-aware primary test did not distinguish the scalar pattern from processed-expression mean/standard-deviation structure. `CV/2` therefore remains a historical descriptive comparator only.

### Stage A: static measurement map

Stage A is closed as a development measurement layer.

The retained static observables are `V`, `L`, `C_in`, and `C_out`. They are not combined into a master stability score.

Stage A1.1 fixed-sample-size calibration removed the finite-sample inflation in absolute-correlation magnitudes while preserving the module topology. This supports retention of the network coordinates as reproducible static observables, not as evidence of a dynamical mechanism.

### Stage B1: composition/context decomposition

Stage B1 is closed.

Independent ABSOLUTE tumor purity and DNA-methylation-derived leukocyte fraction explain a real but concentrated portion of the Stage A network geometry. They do not erase the broader topology.

Under joint independent adjustment:

- module ordering remains strongly preserved for internal coherence and external coupling;
- the inverse relationship between pairwise `C_in` and `C_out` remains negative in all 30 jointly eligible cancers;
- the strongest composition-sensitive effects are concentrated in immune/inflammatory Hallmarks, including allograft rejection, interferon responses, IL6/JAK/STAT3, inflammatory response, and TNF/NF-kB.

Both unadjusted and context-adjusted information are retained. Composition-sensitive modules are carried as context/decomposition information rather than deleted or assigned a better/worse direction.

See `docs/STAGE_B1_AUDIT_20260829.md`.

## Current phase: Stage B2

Stage B2 tests orthogonal static biological layers that were reserved before seeing the B1 result.

Current source families:

1. aneuploidy / loss-of-heterozygosity genomic context;
2. copy-number burden;
3. reverse-phase protein array protein abundance;
4. DNA methylation as a deeper substrate/state layer, subject to source-size and coverage review before full acquisition.

The first B2 source probe successfully downloaded and hashed the small genomic and protein sources. A legacy GDC metadata-route issue was identified separately and is being repaired for deferred methylation size/provenance inspection. No B2 biological association has yet been interpreted.

## What comes after the static program

After B2 static integration closes, the program advances to genuine ordered perturbation/time-course benchmarking. That phase will compare the new stability-map machinery against established dynamic and predictive baselines.

Only after a same-coordinate relaxation rate and intrinsic response rate satisfy the admission gates may a biological chi coordinate be tested. The data are free to place any response optimum below, at, above, or unrelated to `chi = 1`.

## Where to look

- `notes/BUILD_STATUS.md` — canonical current handoff and next step
- `docs/TOOL_OBJECTIVE.md` — predictive-tool objective
- `docs/EPISTEMIC_CONSTITUTION.md` — scientific guardrails
- `docs/CHI_ADMISSION_RULES.md` — conditions required before chi may be used
- `docs/STAGE_A1_AUDIT_20260829.md` — Stage A1 audit
- `docs/STAGE_B1_AUDIT_20260829.md` — Stage B1 composition/context audit
- `artifacts/MILESTONE_ARTIFACTS.md` — artifact hashes and provenance

## Repository role

GitHub is the durable reproducible spine: code, configs, tests, scientific specifications, compact summaries, audits, and milestone hashes. Large raw datasets and bulky derived tables are not duplicated in repository history when they are reproducible from recorded source artifacts.
