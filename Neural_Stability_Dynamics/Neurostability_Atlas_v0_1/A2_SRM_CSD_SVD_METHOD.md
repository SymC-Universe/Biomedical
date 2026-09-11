# Atlas A2 SRM Cross-Spectral SVD Reconstruction Method

Date: 2026-09-11
Status: **P0-D ATLAS RECONSTRUCTION METHOD FROZEN BEFORE EEG VALUE INSPECTION**
Source: `ATLAS-SRC-002-SRM`, OpenNeuro `ds003775`, snapshot `1.2.1`
System Model: NSD System Model v1.0

## Scientific purpose

The first numerical Atlas reconstruction asks a deliberately narrow question:

> Are frequency-resolved observable spectral/carrier coordinates reproducible within a resting session and across the source-defined repeat sessions, without using the NSD Structural Engine, participant age, cognitive scores, diagnosis, or a desired chi value?

This is a `NOMINAL_FUNCTION` Atlas pilot. It is not an Engine validation and not P1.

## Why this method is separate from the Engine

The pilot uses a **cross-spectral density matrix singular-value decomposition (CSD-SVD)**. At each frequency bin, it decomposes the empirical multichannel cross-spectral matrix into orthogonal spectral principal directions.

This is related mathematically to frequency-domain decomposition, but the Atlas pilot uses the decomposition in the weaker observational sense only:

- singular values describe frequency-resolved multichannel spectral strength;
- singular vectors describe frequency-resolved observable carrier directions/subspaces;
- no claim is made that every singular vector is a physical eigenmode;
- no white/broadband excitation assumption is used to convert this EEG decomposition into a mechanical OMA claim;
- no damping ratio is inferred;
- no pole real part is inferred;
- no chi value is inferred.

This keeps the first Atlas coordinate path methodologically distinct from SSI-COV and Subspace DMD.

## Pinned source layer

The primary A2 pilot uses the **source-provided `derivatives/cleaned_epochs` files**, not raw EDF, and labels the resulting coordinates `NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE`.

Source-provided preprocessing recorded in the dataset README/sidecars includes:

- BioSemi ActiveTwo, 64 channels;
- average reference;
- 4-second epochs;
- 1024 Hz sampling;
- automated 1–45 Hz band-pass filtering;
- automatic bad-channel handling/interpolation as documented by the source pipeline;
- resting eyes closed;
- nominal 240-second recording duration before epoch rejection/cleaning.

The pilot does **not** silently call this raw data.

## Atlas-side preprocessing frozen for the pilot

For every retained source-provided epoch:

1. use all 64 channels in the derivative-provided order;
2. refuse the paired comparison if `t1` and `t2` channel names/order differ;
3. preserve the source channel-status files and count bad/interpolated channels as provenance metadata;
4. do not perform additional filtering, re-referencing, ICA, ASR, channel rejection, or artifact rejection;
5. subtract each channel's epoch mean;
6. apply a Hann window to each 4-second epoch;
7. use the real FFT on the full 4096-sample epoch.

The source's cleaned derivative already encodes substantial preprocessing, so Atlas-side transformations are deliberately minimal.

## Cross-spectral matrix

For epoch `e`, frequency bin `f`, and complex channel Fourier vector `z_e(f)`, form

`G(f) = mean_e [ z_e(f) z_e(f)^H ]`

with a fixed one-sided Hann-window spectral scaling recorded in code.

At every retained frequency, perform the Hermitian eigendecomposition/SVD

`G(f) = U(f) S(f) U(f)^H`

with singular/eigenvalues sorted descending.

Because `G(f)` is Hermitian positive semidefinite up to numerical precision, the eigendecomposition is the primary implementation path. Negative numerical eigenvalues at round-off scale are retained in diagnostics and clipped only for normalized nonnegative shares if necessary; material negativity causes refusal.

## Frequency grid

The source derivative has 4-second epochs at 1024 Hz, giving an exact DFT-bin spacing of `0.25 Hz`.

The frozen pilot grid is every native FFT bin from **1.0 through 45.0 Hz inclusive**.

No peak picking is used. No frequency band is selected because it gives a favorable result.

## Per-session reconstructed objects

The full numerical artifact preserves, for each frequency bin:

- `frequency_hz`;
- first four singular values;
- first four trace-normalized singular-value shares;
- leading spectral carrier vector `u1(f)`;
- leading two-dimensional spectral subspace `U2(f)`;
- leading-carrier participation vector `|u1(f)|^2 / sum |u1(f)|^2`;
- trace of `G(f)`;
- numerical Hermitian/PSD diagnostics.

Large complex vectors are stored in a reconstruction artifact and referenced from sparse Atlas entries rather than copied into every JSON entry.

## Within-session stability

Epochs are split deterministically by source order into odd-indexed and even-indexed epochs. No random split is chosen after seeing results.

At each frequency, compare the two split-half CSD-SVD reconstructions using:

- leading-carrier MAC: `|u_a^H u_b|^2` for unit vectors;
- two-dimensional subspace similarity: mean squared singular value of `Q_a^H Q_b`;
- leading-carrier participation total-variation distance: `0.5 * sum |p_a - p_b|`;
- Pearson correlation of the log leading singular-value curves across the full frozen frequency grid, reported as a session-level summary.

No pass threshold is defined.

## Across-session repeatability

For each preselected repeat participant, compare full-session `t1` vs `t2` at exactly matched frequency bins and channel basis using the same quantities:

- frequency-resolved leading-carrier MAC;
- frequency-resolved two-dimensional subspace similarity;
- frequency-resolved participation total-variation distance;
- correlation of trace-normalized leading singular-value-share curves;
- correlation of log total cross-spectral power curves.

No frequency is shifted to improve matching. No participant is removed because repeatability is poor.

## Missingness/refusal

A session or paired comparison is preserved as `UNRESOLVED`/refused rather than repaired if:

- source derivative cannot be retrieved or byte provenance cannot be established;
- file cannot be parsed reproducibly;
- channel basis is not 64 channels as declared or does not match between paired sessions;
- fewer than two cleaned epochs remain;
- cross-spectral matrices contain material non-finite values;
- eigendecomposition fails;
- source preprocessing provenance is missing.

Bad repeatability is **not** a reason for exclusion.

## Atlas coordinates populated by this pilot

Eligible objects:

- `frequency_hz` (`DERIVED_EXACT`, fixed FFT grid);
- `observable_strength_descriptor` (`NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE`);
- `carrier_representation_type` (`NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE`);
- `carrier_vector_or_reference` (`NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE`);
- `channel_participation_vector` (`NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE`);
- paired `MAC`;
- paired `subspace_similarity`;
- paired `participation_distance`;
- `uncertainty_status = PARTIAL` because split-half and repeat-session variability are mapped, but no calibrated sampling interval is yet claimed.

Explicitly withheld/not applicable in this lane:

- `pole_real_per_s`;
- `decay_rate_per_s`;
- `decay_time_s`;
- second-order damping parameter;
- `chi_value`;
- SSI/Engine model-adequacy status.

## Independence disposition

For this pilot:

- the subject roster is selected solely by repeat-session file availability and lexicographic ID order before EEG values are opened;
- age, sex, cognitive scores and expected physiological ordering are not used;
- the reconstruction code is Atlas-specific and does not import the NSD Structural Engine;
- Atlas outputs remain `engine_selector_eligible=false`;
- the source's authors' cleaning pipeline is a data-preprocessing dependency and is preserved as such;
- any later Engine-vs-Atlas agreement on this same source must be graded pathway-specifically rather than called generically independent.

## Promotion firewall

A strong test–retest pattern would establish only that these **Atlas CSD-SVD coordinates are reproducible in this tested source/pilot**. It would not validate NSD's state-space poles, establish a healthy universal range, or license chi.

A weak result remains valuable Limit-Map evidence and does not trigger participant deletion or parameter retuning on the same pilot.
