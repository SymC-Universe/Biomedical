# Subspace DMD Comparator Reconciliation

Date: 2026-09-10
Status: **P0 COMPARATOR SEARCH ADVANCEMENT. NOT P1-FROZEN.**

## Trigger

The first common P0 stress matrix showed an important mismatch between noise-aware total-least-squares DMD and the NSD synthetic process family. TLS-DMD improved the fixed deterministic sensor-noise construction, but on stochastically driven state-space records it frequently returned unstable modes and degraded decay estimates. That result is preserved rather than tuned away.

The literature search was therefore narrowed to DMD variants explicitly intended for **random dynamical systems with observation noise**, rather than deterministic systems with snapshot error alone.

## Source-of-record result

Naoya Takeishi, Yoshinobu Kawahara & Takehisa Yairi, *Subspace dynamic mode decomposition for stochastic Koopman analysis*, Physical Review E 96, 033310 (2017), DOI `10.1103/PhysRevE.96.033310`.

The paper states that popular DMD implementations are inaccurate for random dynamical systems with observation noise and proposes Subspace DMD. The method projects future snapshots onto the space of past snapshots before estimating the reduced operator, and the authors establish convergence to stochastic Koopman spectra under their assumptions.

The authors also published a MATLAB implementation. The corrected `subdmd.m` implementation was inspected directly. The NSD P0 Python translation follows that algorithmic sequence rather than reconstructing the method from memory.

## Updated comparator hierarchy

For the present synthetic family:

1. **SSI-COV**: NSD candidate structural estimator.
2. **Subspace DMD**: strongest currently identified independent DMD-family candidate specifically aligned to random dynamics + observation noise.
3. **TLS-DMD**: useful deterministic/snapshot-noise diagnostic and assumption-sensitivity control, not automatically the primary stochastic comparator.
4. **Exact DMD**: transparent baseline, known to carry observation-noise bias.
5. **Optimized/robust DMD**: remains in the comparator search space if future P1 noise/outlier assumptions require it.

This hierarchy is a P0 research disposition, not an MFR-05 freeze.

## Immediate P0 test

Subspace DMD will be run on the **same fixed condition generator, replicate identities, oracle rank, truth objects, and metrics** already used in `comparator_stress_matrix.json`. This isolates method behavior without redesigning the challenge after seeing results.

## Nonclaims

- The stochastic Koopman operator is not assumed to be the literal neural mechanism.
- Subspace DMD is not yet the frozen P1 comparator.
- Better P0 performance would not by itself prove incremental value for NSD.
- The current P0 oracle-rank comparison does not solve fair rank/order selection.
- No EEG, phenotype, mechanism, chi coordinate, or neural regime boundary is tested here.
