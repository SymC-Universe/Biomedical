# GRI Conglomerate Chi C1 public-source probe closure

**Date:** 2026-09-18  
**Branch:** `gri-conglomerate-chi-tool-v1-20260918`  
**Workflow run:** `35337654254`  
**Conclusion:** `success`  
**Artifact:** `gri-conglomerate-chi-c1-public-source-probe-20260918`  
**Artifact ID:** `10543676669`  
**Artifact SHA-256:** `9e68efaf0962c43bc829621c35802917a9b5591b5d8ebc3322e39dce3230d2c0`

## Closed result

```text
status = C1_PUBLIC_SOURCE_PATHS_VERIFIED
sources_total = 7
failed_or_error_sources = []
```

Five smaller PanCanAtlas sources were fully downloaded in GitHub Actions and matched their frozen SHA-256 identities:

- ABSOLUTE purity
- leukocyte fraction
- aneuploidy/LOH
- CNV burden
- RPPA

The two large primary sources were range-probed without consuming the full files:

- RNA PANCAN source: observed total size matched 1,882,540,959 bytes
- merged HM27/HM450 methylation source: public endpoint and total size verified

The source probe opened no biological outcome and fit no model.

## Mechanical failure record

The first workflow attempt `35337566190` failed before the source probe because pytest had not been installed. The dependency step was added without changing scientific state. The repaired run above passed.

## Consequence

Cloud reconstruction is source-feasible. User-local computation is not required to obtain the seven primary raw sources. Heavy RNA and methylation materialization should use a cloud environment suited to multi-gigabyte data, while GitHub Actions can continue source qualification, compact adapters, tests, and smaller-source materialization.
