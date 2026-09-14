# P0-D22 Identifiability Null-Floor Challenge Result

Date: 2026-09-14
Status: **P0-D exploratory known-truth result. Not confirmatory. P1 remains closed.**
Governing interpretation: General Protocol v0.8.0, with the run itself executed under the then-current v0.7.7 construction.

## Execution identity

- GitHub Actions run: `34807746168`
- Artifact ID: `10333193921`
- Downloaded artifact SHA-256: `41ef01992f3b81a30a3f2eb0d498d100e33416e4185352feca0facd1a40a4692`
- Scientific JSON: `identifiability_null_floor_v1.json`
- Scientific JSON SHA-256: `f99c88d9a21486ed27dd83ef88d650a63d55900c0bdec770d89a2b1a163c0761`
- Environment JSON SHA-256: `07fce4cb6553ee33132f5519f6459eba2523ce2e38c354ef85f17db2db98d75d`
- Workflow/process result: completed successfully.

## Frozen P0-D construction preserved

The latent four-state generator, latent trajectory within replicate, and absolute measurement-noise realization within replicate remained fixed across observation conditions. Only observation access to the second modal pair was weakened over scales `[1.0, 0.3, 0.1, 0.03, 0.01, 0.003]`. SSI-COV remained fixed at order 4 and block rows 18. Eight deterministic replicates were run. Atlas information and the prospective preferred-chi note were excluded.

## Aggregate result

All 48 estimator executions returned `OK`, so the challenge did not expose a simple execution/refusal boundary. It did expose a strong and orderly loss of observation geometry while latent truth remained invariant.

Across weak-observation scale from `1.0` to `0.003`:

- median observability singular-value ratio fell from `0.4396126499` to `0.0014244666`;
- median weak-to-strong observation-column norm ratio fell from `1.0943943419` to `0.0032831830`;
- median Hankel effective-rank proxy fell from `4.2546016368` to approximately `2.8684` and then plateaued;
- median matched modal-chi MAE increased from `0.2495599444` at scale 1.0 to `0.3332603203` at scale 0.003, with non-monotonic intermediate variation;
- median asymptotic-time-constant absolute error increased from `0.0733706596` at scale 1.0 to `0.1268442514` at scale 0.003, also with non-monotonic intermediate variation.

The matched-mode count itself changes with observation condition, so the chi-error sequence is not interpreted as a clean scalar dose-response. That changing support is part of the identifiability result rather than something to suppress.

## Scientific interpretation

Because the latent generator, exact poles, exact modal chi values, spectral abscissa, and latent asymptotic recovery time were invariant by construction, the observed movement in estimated modal/recovery quantities is attributable to measurement geometry / effective identifiability in this known-truth testbed rather than a change in the underlying dynamics.

This result therefore **supports the need for an explicit identifiability / observation-geometry null floor before any empirical NSD chi-recovery relationship is eligible for promotion.** It does not define the control yet, and it does not freeze an observability, effective-rank, chi-error, or recovery-error threshold.

The strongest result is not that the estimator catastrophically fails. It is that an estimator can continue returning finite, apparently usable outputs while the information available about a latent mode is being progressively removed and its derived coordinates drift. That makes identifiability a required companion to coordinate estimation and recovery interpretation.

## Nonclaims and firewalls preserved

- No neural chi-recovery law is confirmed.
- No empirical Atlas zone or preferred chi value is tested.
- No `chi_system` is defined.
- Failure to recover or match a mode is not treated as physical mode absence or chi equal to zero.
- No admission threshold is selected from this result.
- This run remains P0-D and cannot confirm the control it motivates.

## Consequence for the next gate

Any recovery-related P0-Q proposal that uses estimated modal chi, spectral-abscissa-derived recovery, or related coordinates across systems must explicitly address observation geometry / identifiability. The exact P0-Q control, admission rule, or null-floor treatment remains a scientific decision to be specified prospectively rather than inferred from these six observed scales.
