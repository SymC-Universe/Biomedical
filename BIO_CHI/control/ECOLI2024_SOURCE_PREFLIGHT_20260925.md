# E. coli sensory-diversity Bio Chi source preflight

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-sensory-p0q-20260925`  
**Status:** FROZEN BEFORE RAW OUTCOME EXTRACTION  
**Evidence class:** P0-Q, literature-open representation qualification  
**Authority:** SymC GOM v0.8.6

## Status

A new independent biological system is opened under the top-down Bio Chi contract. The source is Moore et al., *Cell Systems* (2024), DOI `10.1016/j.cels.2024.06.003`, with raw data at Dryad DOI `10.5061/dryad.nvx0k6dzz` and author analysis code in `emonetlab/SensoryDiversityTuningAnalysis`.

The publication's qualitative claim about sensory-diversity tuning was visible during candidate selection. This experiment therefore does not claim blinded discovery or P1 confirmation. Its job is narrower: reproduce the source-defined whole biological event and determine the minimum representation needed to describe it without forcing a scalar.

## Frozen biological question

Does sustained MeAsp background context reorganize the single-cell sensory-sensitivity distribution in a way that requires more information than a one-coordinate shift in central sensitivity?

The frozen same-ligand series is 0, 0.1, 0.3, 1, 10, and 100 uM MeAsp background using only the file lists already selected by the authors in `datasets.m`.

## Three-object disposition at freeze

- `Bio Chi`: the whole background-conditioned population reorganization event.
- `Chi_bio`: candidate minimum internal vector representation, initially the source-native lognormal distribution state `(mu_logK, sigma_logK)`.
- `chi_bio`: **not opened**. A dose-response sensitivity coordinate is not a licensed damping/stability scalar by itself.

A location-only sensitivity coordinate will be tested strictly as a scalar-compression control and will not be renamed `chi_bio`.

## Source-native processing locked before extraction

The author pipeline uses seven responses per stimulus, median response summaries, the source cell-quality threshold `a0 >= 0.15`, and a CDF based on the fraction of cells whose normalized post-stimulus activity is below 0.5. The primary reanalysis preserves those semantics and records any Python/MATLAB implementation difference as an interface issue rather than silently changing the biological object.

## Cross-project lessons inherited as method, not evidence

Foundations D02F requires target-observable power rather than generic perturbation response. Chemistry CP/Cu(111) shows that identical local scalar structure can coexist with different embedded recovery, so local coordinates do not automatically determine whole-system behavior. NSD separates nuisance nonidentifiability from carrier identifiability. Economics and AIF preserve scalar refusal as a valid endpoint. These results constrain the analysis design but do not count as biological evidence for this experiment.

## Next action

Retrieve and hash the frozen Dryad files, reproduce the source-native response/CDF objects, execute the representation comparison without retuning, and preserve success, failure, refusal, or source limitation unchanged.
