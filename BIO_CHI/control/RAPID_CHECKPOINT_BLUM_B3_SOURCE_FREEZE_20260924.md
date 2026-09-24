# Bio Chi rapid checkpoint - Blum B3 transport source frozen

**Branch:** bio-chi-closure-p0q-20260924

## Frozen before ERK spectrum
Config:
BIO_CHI/config/BLUM_B3_TRANSPORT_SOURCE_FREEZE_v0_1.json

Primary B3 role:
- publication-selected B3 topology
- primary parameterization is the Figure 7 / HSPG model-selection simulation vector
- separate source prediction vector retained as sensitivity

Primary reproduction:
- source experiment sus_2-5ng
- sustained FGF2 input = 2.5
- 15 native states
- 91 source timepoints, 0 to 180 min by 2 min
- independent SciPy BDF reproduction
- frozen pass thresholds:
  max absolute error <= 5e-4
  RMS error <= 5e-5
  all finite

Future generator rule:
- do not interpret raw 15-state Jacobian zero modes
- construct source stoichiometric matrix S
- analyze J_reduced = Q^T J Q on col(S)
- scalar refusal is allowed

Current status:
No ERK eigenspectrum or chi-like quantity has been opened.

Next single gate:
Implement and execute the native B3 trajectory reproduction.

No user intervention required.
