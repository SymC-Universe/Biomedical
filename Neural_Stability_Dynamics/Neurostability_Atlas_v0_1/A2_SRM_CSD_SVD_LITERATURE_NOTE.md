# A2 SRM CSD-SVD Literature Boundary Note

Date: 2026-09-11
Status: **LITERATURE CROSS-CHECK. DOES NOT MODIFY THE FROZEN A2 METHOD.**

## Relevant method lineage

The classical Frequency Domain Decomposition (FDD) literature establishes spectral-density-matrix decomposition as an output-only frequency-domain modal-analysis technique:

- Brincker, R., Zhang, L., Andersen, P. (2001), *Modal identification of output-only systems using frequency domain decomposition*, Smart Materials and Structures 10(3):441–445, DOI `10.1088/0964-1726/10/3/303`.
- Earlier conference treatments by Brincker, Zhang and Andersen describe the same output-only spectral-density decomposition lineage.

The method decomposes the response spectral-density matrix frequency by frequency. In structural OMA, under the required excitation/system assumptions, singular-value/singular-vector structure can be interpreted in terms of modal contributions and close modes can be separated.

## Why the Atlas claim is deliberately weaker

The SRM Atlas A2 pilot does **not** assume that resting human EEG satisfies the structural OMA excitation assumptions needed to identify every CSD singular vector with a physical eigenmode.

Accordingly, the frozen Atlas language is:

- `observational cross-spectral density matrix SVD`;
- `spectral principal direction` / `spectral carrier direction`;
- `spectral subspace`;
- frequency-resolved observable structure.

It does not promote those objects to literal physical modes merely because the algebra matches an FDD decomposition.

## Damping boundary

FDD damping estimation requires additional construction beyond a frequency-by-frequency CSD eigendecomposition, classically involving isolation of a modal spectral density contribution and transformation/decay estimation in the time domain. See the FDD damping-estimation lineage by Brincker and colleagues.

A2 does not perform that step. Therefore it does not estimate:

- damping ratio;
- continuous-time pole real part;
- decay rate;
- decay time;
- second-order chi.

Those coordinates remain withheld rather than inferred from spectral width or another convenient surrogate.

## Consequence for Atlas v0.1

The literature supports the mathematical use of spectral-density-matrix decomposition while also supporting the claim firewall in `A2_SRM_CSD_SVD_METHOD.md`.

If a later Atlas lane attempts modal damping or second-order coordinates, it requires a separately frozen method and model-eligibility argument. A2 results cannot be retroactively reinterpreted as damping evidence.
