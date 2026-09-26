# GSE342354 U2OS CCCP recovery source-qualification preflight

**Date:** 25 September 2026  
**Branch:** `bio-chi-u2os-cccp-recovery-p0q-20260925`  
**Status:** FROZEN BEFORE EXPRESSION EXTRACTION  
**Authority:** SymC GOM v0.8.6

## Why this source

The Meneses E. coli source family is closed after direct recovery, source-method reconciliation, context transport, transport refusal, and root-cause analysis. The next experiment must therefore cross acquisition lineage rather than continue mining the same source.

GEO GSE342354 is an independent human U2OS mitochondrial-damage/washout time series. The study contains 12 RNA-seq samples in four biological-triplicate states: untreated, 50 uM CCCP for 30 minutes, 1 hour after CCCP washout, and 6 hours after washout. This provides a direct state-displacement/recovery architecture with a different organism, assay, perturbation, and acquisition lineage from the Meneses motor/TMRM/cell-area experiment.

The public GEO summary was visible during selection and describes recovery-related transcriptional programs. The experiment is therefore literature-open P0-Q, not blinded discovery.

## Frozen sample identity

- WT: GSM9929032--GSM9929034
- CCCP: GSM9929035--GSM9929037
- W1H: GSM9929038--GSM9929040
- W6H: GSM9929041--GSM9929043

No expression values have been opened for the SymC-specific test.

## Source gate

The immediate task is source qualification only:

1. resolve the NCBI GEO supplementary and series-matrix directories;
2. record every candidate processed expression file;
3. hash any downloaded processed source before parsing values;
4. verify that the 12 frozen sample identities can be mapped without inference;
5. stop as SOURCE_LIMITED if no unambiguous processed gene-level matrix is available.

A biological recovery analysis will be frozen only after this source gate closes.

## Representation hierarchy

- biological chi: future whole transcriptomic damage-to-recovery event;
- modal/vector Chi_bio: future minimum transcriptomic state representation;
- scalar chi_bio: not opened and not implied by RNA-seq replicate statistics.

## What happens next

Run the source enumerator and preserve its manifest. If the processed source is unambiguous, freeze the state-geometry analysis before opening expression values.
