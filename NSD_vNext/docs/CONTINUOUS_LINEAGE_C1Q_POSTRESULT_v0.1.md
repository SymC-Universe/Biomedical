# NSD C1Q Nonzero-g Qualification Postresult v0.1

Status: QUALIFICATION-ONLY KNOWN-TRUTH RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD State-Space Lineage Sampling Contracts`  
Run: `36354967663`  
Conclusion: SUCCESS  
Source head: `73f5d881ed4af4eabd8f6381487d4e1ac2e8503f`

Artifact: `nsd-continuous-lineage-nonzero-g-probe`  
Artifact ID: `10943194616`  
Digest: `sha256:713be00f0e252c2db8196a11e17de7c2ebb986dc6e9872b54ad87941f26845c6`  
Expiry: 26 December 2026

## Purpose

The probe repeated the previously established one-mode continuous-lineage truths but added C1Q as a separate k=4 qualification candidate. Production A0/A1/A2 remained unchanged.

## Results

For every nonzero-g cell, C1Q had the lowest BIC among A0/A1/A2/C1Q.

g = -0.75:

- seed 0 fine: C1Q margin to second 57.309; fitted chi 0.312662; fitted g -0.769001;
- seed 0 coarse: margin 32.947; chi 0.311710; g -0.737583;
- seed 1 fine: margin 52.524; chi 0.330157; g -0.751063;
- seed 1 coarse: margin 25.716; chi 0.322374; g -0.731585.

g = +0.75:

- seed 0 fine: C1Q margin 39.937; chi 0.288485; g 0.680911;
- seed 0 coarse: margin 6.151; chi 0.294743; g 0.529396;
- seed 1 fine: margin 35.257; chi 0.345599; g 0.802167;
- seed 1 coarse: margin 26.910; chi 0.352099; g approximately 0.999963.

For g = 0, simpler A1 remained the extended-family BIC winner in all four fine/coarse comparisons:

- seed 0 fine: A1 over C1Q by 7.788 BIC;
- seed 0 coarse: A1 over C1Q by 7.177;
- seed 1 fine: A1 over C1Q by 8.757;
- seed 1 coarse: A1 over C1Q by 8.170.

## Interpretation

C1Q resolves the first qualification problem cleanly:

- it absorbs the nonzero-g one-mode nuisance structure that caused false A2 pressure;
- it does not automatically replace A1 when g=0;
- the A1 -> C1Q nesting behaves in the intended BIC direction.

The result also exposes the next qualification issue. Fitted g and chi remain realization-dependent, and one coarse positive-g cell reached the practical g boundary. Therefore model-order repair is not equivalent to parameter-identifiability closure. Uncertainty, boundary proximity, paired-sampling recovery, and refusal behavior still require qualification before any production promotion.

## Claim boundary

This result advances C1Q on the promotion ladder but does not promote it into production. Genuine two-mode, colored-process, D\C, S\D, near-critical, A2-collision, and predictive-closure controls remain required.

Real-EEG local chi remains unlicensed.
