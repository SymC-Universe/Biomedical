# NSD State-Space Hardened Rerun Provenance v0.1

Date: 19 September 2026
Status: P0-Q QUALIFICATION / PROVENANCE ONLY
Program authority: SymC General Operations Manual v0.8.0
Branch: `nsd-rebuild-gom-v0.8.0`

## Scope

This record preserves provider-side workflow state and artifact identity for the hardened state-space adequacy and operating-region qualification lane. It does not alter the A0/A1/A2 models, likelihood, admission/refusal rules, thresholds, interpretation ceiling, or real-EEG firewall.

## Scientific source run

The first hardened operating-region result was produced by:

- workflow: NSD State-Space Operating Region
- run: `35343001336`
- head SHA: `8f707861890ba6fadcca25f62cb62e48a6335a71`
- artifact: `nsd-state-space-operating-region`
- artifact id: `10545788992`
- ZIP digest: `sha256:4fcd36f82fc82817ebda71f7e7d3ab23d7b8905c6f75d2adeaf0155fd2e01886`
- extracted JSON SHA-256: `0b016ef77e938ef53a00a426740d8609e8cf9d3dbcc56ea2dd9245120a14d264`

The paired adequacy result was:

- workflow: NSD State-Space Adequacy Map
- run: `35343001303`
- head SHA: `8f707861890ba6fadcca25f62cb62e48a6335a71`
- artifact id: `10546226542`
- ZIP digest: `sha256:943cdea62b8d35e74dc57219bae28172a8d8797178b55e8d90a615e98e32f47f`

## Hardened operating-region observations

Single-mode grid: 162 rows across 5/10/20 Hz natural frequency, damping ratios 0.2/0.5/0.8, 10/30 s duration, observation-noise ratios 0/0.5/1.0, and three deterministic seeds.

- A1 selected by BIC in 141/162 rows.
- damping 0.2: A1 54/54.
- damping 0.5: A1 54/54.
- damping 0.8: A1 33/54, A0 21/54.
- all 162 A1 fits reported optimizer success and 12 converged starts.
- among the 21 A1 nonselections, the fitted A1 latent fraction was approximately 0.464 to 1.000 and rho approximately 0.628 to 0.912.

Therefore the previously documented near-zero-latent-fraction/lower-rho-boundary collapse does not explain the current 21 high-damping nonselections. This is candidate Limit-Map evidence only; no operating boundary is frozen from it.

Two-mode grid: 45 rows across separations 0.5/1/2/5/10 Hz, second:first amplitude ratios 0.35/0.60/1.00, and three deterministic seeds.

- A2 selected 8/45 overall.
- separation 0.5 Hz: 0/9.
- separation 1 Hz: 0/9.
- separation 2 Hz: 0/9.
- separation 5 Hz: 1/9.
- separation 10 Hz: 7/9.
- at 10 Hz separation, A2 selected 1/3 at amplitude ratio 0.35 and 3/3 at ratios 0.60 and 1.00.

These observations do not define a frozen minimum resolvable separation or amplitude rule.

## Adequacy observations retained

Across three deterministic seeds per adversarial generator, full-record BIC selected:

- valid stationary single oscillator: A1, 3/3;
- separated simultaneous two-mode truth: A2, 3/3;
- nonoscillatory AR(1): A0, 3/3;
- white noise: A0, 3/3;
- close two-mode truth: A1, 3/3;
- colored observation-noise truth: A1, 3/3;
- finite-burst truth: A1, 3/3;
- mid-record frequency-shift truth: A2, 3/3.

For valid single-oscillator truth, median natural-frequency relative error was approximately 0.0101 and median damping-ratio absolute error approximately 0.0206.

White-noise held-out scoring returned `INDETERMINATE` for all 3/3 interpretable decisions when per-sample likelihood differences were computationally negligible. The numerical-indeterminate state is a computational safeguard, not a scientific effect threshold.

Close modes, colored observation noise, finite bursts, and temporal frequency shifts remain unresolved by whole-record model order alone. Real-EEG modal damping and local chi remain disabled.

## Current provider-side rerun audit

Current branch head at audit time:

- SHA: `efb5480e42cb4a29927435ba08bf027f7abc0d6f`
- commit: `Harden NSD workflow triggers against long-lived-PR reruns`

Latest adequacy workflow:

- run: `35422339362`
- provider conclusion: success;
- prepare/guard job: success;
- adequacy-map job: skipped;
- artifact count: 0.

This is a correct guarded no-op, not evidence of a new adequacy computation.

Latest operating-region workflow:

- run: `35422336560`
- provider conclusion: success;
- operating-region job: success;
- artifact id: `10578390906`
- ZIP digest: `sha256:a99c9657fe20f5a26da139436674bbf2d4607ed506e49aea6ed53ba2afd18baa`
- extracted JSON SHA-256: `0b016ef77e938ef53a00a426740d8609e8cf9d3dbcc56ea2dd9245120a14d264`

The extracted JSON is byte-for-byte identical to the first hardened operating-region result from run `35343001336`. The differing ZIP artifact digests therefore do not represent a scientific result change.

## GOM v0.8.0 disposition

- classification remains P0-Q qualification;
- prior failures remain visible;
- Function Map and Limit Map remain coequal;
- no viewed qualification result is promoted to untouched confirmation;
- no production threshold or operating region is frozen here;
- no real-EEG modal damping, local chi, biological mode interpretation, diagnosis, prognosis, or P1 claim is licensed.

## Next scientific gate

Before a production operating region or modal admission/refusal rule can be frozen, the unresolved qualification lanes remain:

1. colored observation-noise adequacy/refusal;
2. burst and temporal-stationarity discrimination;
3. identifiability/uncertainty around the high-damping and mode-resolution regions;
4. remaining sampling-rate/process-noise operating-region extensions required by the adequacy plan;
5. isolated standard-toolkit comparison against the pinned comparator lane.

A science-adjacent decision is required before interpreting the current high-damping and mode-resolution patterns as a frozen Limit Map. This record intentionally preserves state without making that decision.
