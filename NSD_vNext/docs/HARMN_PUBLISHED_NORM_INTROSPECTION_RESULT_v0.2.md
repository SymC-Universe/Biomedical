# HarMNqEEG Published Norm Model Introspection Result v0.2

**Date:** 2026-10-01  
**Status:** SOURCE IDENTITY AND MODEL-STRUCTURE QUALIFIED  
**Evidence class:** independent published healthy normative model infrastructure  
**Scientific ceiling:** no NSD variable and no reinterpretation of the HarMN model.

## Source identity

Official public repository: `tperezdevelopment/HarMNqEEG`.

Traditional log-spectrum normative model:
`data/norm/norm_log_gfavfa_bfvf_study.mat`

Published Git-LFS SHA-256:
`dba25f3172b04fb5627083274e8871ef2058bc872217c617fd7cd3bd0859b484`

Kaggle download SHA-256:
`dba25f3172b04fb5627083274e8871ef2058bc872217c617fd7cd3bd0859b484`

Checksum: **PASS**.

File size: 136,146,486 bytes.

## Structural result

The norm is MATLAB v7.3/HDF5 and contains the expected normative prediction objects:
- `tregs`;
- `level`;
- `batch`;
- `resp`;
- `opt`.

Two regression levels are present.

Level 1:
- condition: global / used;
- mean factors: frequency and age;
- variance factors: frequency and age;
- response names begin `globallog1_1`, `globallog2_2`, ... through the channel/response set.

Level 2:
- mean factor: frequency;
- variance factor: frequency;
- response names begin `studylog1_1`, `studylog2_2`, ...;
- this level carries study/batch correction structure.

The regression objects contain MATLAB `griddedInterpolant` instances (`fpp_yhat`) for normative mean/variance prediction.

## Consequence

The official traditional HarMN norm is not a simple table of age bins. It is a hierarchical frequency/age normative regression plus study-level harmonization.

Therefore the baseline program will not approximate HarMN from published figures or fit a replacement model to the same data.

Next action:
1. extract a compact manifest of response names, interpolation grids/breakpoints, and stored normative objects;
2. determine whether exact Python evaluation of MATLAB `griddedInterpolant` objects is demonstrably equivalent;
3. if exact equivalence cannot be established, retain the official MATLAB prediction implementation as the canonical native scorer and wrap it without altering its fitted model.

Kaggle kernels:
- `symcuniverse/nsd-harmn-baseline-introspect-v0-1`;
- `symcuniverse/nsd-harmn-baseline-introspect-v0-2`.
