# P0-D8 Subspace-DMD Tail-Gap Forensics Result

Date: 2026-09-11
Status: P0-D RESULT. RETROSPECTIVE / MECHANISM MAPPING. NOT P0-Q. NOT P1.
Workflow run: `34611271875`
Job: `103302084304`
Artifact ID: `10268033447`
Artifact ZIP SHA256: `d43f5a94b380a95e29605ca800ba53d0a404f6b7767e61ae42adbf87c75cd63f`

## Historical firewall

The frozen P0Q1 result is unchanged:

- SSI-COV: `SURVIVES_P0Q1`
- Subspace DMD: `FAILS_P0Q1`

P0-D8 does not rescore or repair P0Q1. It diagnoses a mechanism capable of producing the observed comparator failure and replay fragility.

## Design

Two known-truth synthetic families were tested:

1. two stable real poles, continuous state dimension 2, no oscillatory truth;
2. one stable oscillatory conjugate pair, continuous state dimension 2, one positive-frequency oscillatory truth mode.

For each family, Subspace DMD was swept over ranks 1 through 8 at record lengths 1300, 2600, 5200 and 10400 samples, with 8 independent replicates per length. The frozen P0Q1 largest-adjacent-gap gate was overlaid retrospectively only. Each generated input record was SHA256 hashed.

## Central result

The frozen largest-gap gate selected **rank 4 in 8/8 replicates for every record length in both families**. Thus the selected rank exceeded the known continuous state dimension in 100% of tested records.

The critical point is not merely the over-rank selection. It is *where the selected gap occurred*.

### Two-real-pole family

| samples | median selected `s4/s1` | median `s5/s1` | median selected gap `s4/s5` |
|---:|---:|---:|---:|
| 1300 | 1.215e-3 | 5.158e-16 | 2.993e12 |
| 2600 | 5.179e-4 | 6.938e-16 | 9.208e11 |
| 5200 | 4.642e-4 | 9.121e-16 | 5.536e11 |
| 10400 | 3.250e-4 | 1.107e-15 | 2.822e11 |

### One-oscillatory-pair family

| samples | median selected `s4/s1` | median `s5/s1` | median selected gap `s4/s5` |
|---:|---:|---:|---:|
| 1300 | 6.014e-4 | 5.778e-16 | 1.049e12 |
| 2600 | 8.115e-4 | 7.601e-16 | 8.635e11 |
| 5200 | 3.859e-4 | 9.954e-16 | 3.842e11 |
| 10400 | 2.488e-4 | 1.579e-15 | 1.599e11 |

The selected fourth direction therefore carries only roughly `2.5e-4` to `1.2e-3` of the leading singular value in the median record, while the next direction is at approximately machine precision. The raw adjacent ratio becomes enormous because the denominator collapses, not because the selected direction itself has large absolute or relative support.

## False-complexification behavior

The over-rank selections frequently produced unstable or extra complex poles.

For the two-real-pole family, where no complex mode exists in truth, the frozen retrospective gate decisions were:

- 1300 samples: 3 admit, 4 unstable refusals, 1 method exception;
- 2600: 4 admit, 4 unstable refusals;
- 5200: 4 admit, 4 unstable refusals;
- 10400: 1 admit, 7 unstable refusals.

For the genuine one-oscillatory-pair family, rank 4 was still selected in every replicate and often produced extra complex or unstable structure beyond the one true oscillatory pair.

## Interpretation

P0-D8 strongly supports the bounded mechanism statement:

**The largest adjacent singular-value gap is not, by itself, evidence of supported dynamic rank. A huge gap can occur at the boundary between a weak finite-sample projected direction and an effectively numerical-zero tail.**

This explains why the frozen P0Q1 Subspace-DMD gate can be attracted to rank 4 and then create false complexification or unstable fits. It also explains why per-replicate outcomes can be fragile when the fit depends on weak near-null directions.

The result does **not** establish that a correct operational rank must equal the continuous state dimension in a stochastic finite-sample problem. The safe conclusion is narrower: raw largest-gap selection can elevate weak tail structure and requires additional support/robustness evidence before it can serve as a qualified rank rule.

## Reproducibility consequence

For near-singular prospective synthetic tests, source code + seed + package versions are not enough for ideal forensic replay. Future decisive runs should also retain either the exact generated input arrays or strong cryptographic hashes plus richer numerical-backend provenance. P0-D8 now writes an input SHA256 for every generated record.

## What remains unfrozen

- no normalized-support floor;
- no effective-rank rule;
- no stable-rank rule;
- no denoising threshold;
- no cross-rank persistence threshold;
- no revised Subspace-DMD selector;
- no final comparator identity.

Any revised rule inspired by P0-D8 must receive a new version and untouched P0-Q evidence.