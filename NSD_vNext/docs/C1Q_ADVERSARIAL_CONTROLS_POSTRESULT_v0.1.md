# NSD C1Q Adversarial Controls Postresult v0.1

Status: QUALIFICATION-ONLY ADVERSARIAL RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD C1Q Adversarial Controls`  
Run: `36355157685`  
Conclusion: SUCCESS  
Source head: `f3c2b36fd103b93e5fddc25596989c826718acca`

Artifact: `nsd-c1q-adversarial-controls`  
Artifact ID: `10943900668`  
Digest: `sha256:7c762a2f755cdaeeab93258835cc8a5de50737eedb062da972e5210018fd34d7`  
Expiry: 26 December 2026

## Results

Nested isotropic one-mode controls behaved correctly:

- seed 0: current A1 remained extended winner; A1 over C1Q by 8.924 BIC;
- seed 1: current A1 remained extended winner; A1 over C1Q by 7.618.

Genuine separated two-mode controls also behaved correctly:

- seed 0: A2 remained extended winner; margin 62.596;
- seed 1: A2 remained extended winner; margin 33.166.

The known one-mode white-forcing shape controls that previously caused false A2 pressure were absorbed by C1Q:

- anisotropic 4:1 seed 0: C1Q winner, margin 25.216;
- anisotropic 4:1 seed 1: C1Q winner, margin 49.971;
- rank-1 axis drive seed 0: C1Q winner, margin 62.780;
- rank-1 axis drive seed 1: C1Q winner, margin 78.170.

This supports the interpretation that these A2 wins can arise from the missing one-mode covariance-phase degree rather than genuine multimodality.

The colored-process control exposed a remaining failure:

- colored phi=0.7 seed 0: C1Q winner, margin 45.356;
- colored phi=0.7 seed 1: C1Q winner, margin 44.297.

The colored truth contains an additional real process pole and is not a white-driven second-order C-family truth. C1Q therefore cannot be admitted solely because it wins BIC.

## Interpretation

C1Q passes the first model-family specificity checks but fails a crucial closure/refusal check.

It distinguishes:
- simpler isotropic one-mode truth -> A1;
- genuine separated two-mode truth -> A2;
- one-mode nonzero-phase white forcing -> C1Q.

However, ordinary A0/A1/A2/C1Q BIC competition does not distinguish C1Q-compatible second-order lineage from colored-process higher-order/memory contamination.

Therefore C1Q promotion requires an independent structural-order or memory/refusal diagnostic. Model selection alone is insufficient.

## Claim boundary

The next qualification target is to distinguish genuine second-order C lineage from extra-pole/memory structure without using a raw sample-rate-dependent Hankel threshold. Exact known-truth work should begin with recurrence/Hankel rank before finite-sample calibration.

C1Q remains qualification-only. Real-EEG local chi remains unlicensed.
