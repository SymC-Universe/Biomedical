# HarMNqEEG Normative Model Anatomy v0.1

**Status:** INDEPENDENT BASELINE MODEL INTAKE  
**Date:** 2026-10-01  
**Source:** official HarMNqEEG public repository, traditional log-spectrum normative model  
**Norm file SHA-256:** `dba25f3172b04fb5627083274e8871ef2058bc872217c617fd7cd3bd0859b484`  
**Checksum:** PASS against official Git-LFS object identity  
**Scientific ceiling:** native lifespan qEEG normative model only; no NSD interpretation.

## Model structure recovered from the published file

The official model is a MATLAB v7.3 / HDF5 object.

### Regression level 1: biological/global normative surface

Condition:
- `global`.

Mean factors:
- frequency;
- age.

Variance factors:
- frequency;
- age.

Responses:
- 18 traditional log-spectrum dimensions:
  `globallog1_1` through `globallog18_18`.

Interpretation:
- the expected healthy log-spectrum position and its variance are modeled jointly as functions of frequency and age;
- this is the appropriate external source for age-conditioned native spectral centering and dispersion.

### Regression level 2: study/batch layer

Condition:
- `study`.

Number of study conditions in the stored model:
- 14.

Mean factor:
- frequency.

Variance factor:
- frequency.

Interpretation:
- study/site/device-related effects are represented separately from the age/frequency normative surface;
- baseline construction must preserve this distinction rather than folding acquisition differences into biological deviation.

## Consequence for the NSD healthy baseline

The external native reference should be represented schematically as:

[
X_{mathrm{native}}
=
mu(mathrm{age},f)
+
B_{mathrm{study}}(f)
+
epsilon,
]

with variance also conditioned on age/frequency and study/frequency according to the published model hierarchy.

The exact HarMN implementation uses nonlinear regression/interpolation objects rather than the simple additive shorthand above. The equation is conceptual only.

## What remains to reproduce

1. decode the stored interpolants/regression surfaces;
2. evaluate expected mean and variance over an age-frequency grid;
3. reproduce published z-score behavior on synthetic probe spectra;
4. compare a held-out/public healthy spectrum against the official MATLAB scoring path if an executable reference path is available;
5. freeze extracted normative surfaces and their provenance before any NSD feature is introduced.

## Prohibitions

- do not infer a healthy (chi) from HarMN;
- do not collapse the 18 spectral dimensions to one scalar without an independent native rationale;
- do not interpret batch/study correction as biology;
- do not tune the external norm using disorder outcomes.

