# NSD P0 Order / Rank Fairness Investigation

Date: 2026-09-10/11
Status: **P0 INVESTIGATION. NO SELECTION RULE FROZEN.**

## Scientific problem

The current SSI-COV versus Subspace-DMD stress result is conditional on the correct state order/rank being supplied. That is a legitimate estimator-isolation experiment, but it is not yet a fair operational comparison because real data do not reveal the correct rank.

The next question is therefore not "which rank makes each method look best?" It is:

> Which information is available to each method without truth access, and can a predeclared rule use that information to recover or refuse structure reliably enough for a future operational comparison?

## Native-method evidence

Stochastic subspace identification commonly uses **multi-order stabilization diagrams** because the true system order is generally unknown and over-specified models generate spurious modes. Döhler & Mevel, *Efficient multi-order uncertainty computation for stochastic subspace identification*, Mechanical Systems and Signal Processing 38 (2013), DOI `10.1016/j.ymssp.2013.01.012`, explicitly describes physical modes as structures that stabilize across increasing model orders.

DMD rank selection is also not uniquely determined. Published DMD work uses singular-value truncation, energy criteria, hard-threshold rules, mode-selection procedures and other model-selection approaches. A white-noise singular-value hard threshold can be principled under its assumptions, but those assumptions do not automatically cover colored observation noise or process-driven stochastic dynamics.

Therefore **no single common numerical threshold is imposed across SSI-COV and Subspace DMD** merely for symmetry. Fairness means comparable epistemic burden, not identical mathematics.

## Firewall implemented in the P0 sweep

The new sweep layer is deliberately split:

### Data-only layer

Receives only the measured multichannel record and method settings. It exposes:

- the method-native singular spectrum;
- unthresholded singular-gap ratios at each candidate order/rank;
- fitted poles and carriers at each candidate order/rank;
- unstable-pole fraction;
- adjacent-rank candidate assignments, pole distances, MAC values and assignment margins.

It returns:

`selection = None`

for every record.

### P0 truth-evaluation layer

After the data-only sweep is complete, known synthetic truth is attached strictly for development evaluation. Truth may measure how each candidate order/rank behaved, but it does not select the rank.

Any rule invented after inspecting these truth relationships is **DATA_DERIVED / POST_RESULT** and incurs promotion debt. It cannot become P1-confirmatory without a new untouched test.

## Candidate grid

The first common diagnostic grid is ranks/orders `1..6`, because the present stress systems use six observed channels and a true latent order of four. This grid is a P0 characterization device, not a future EEG search space.

Odd ranks are intentionally retained. Removing them because the current truth consists of complex-conjugate oscillator pairs would leak construction knowledge into the sweep.

## What this investigation can establish

It may establish that particular **classes of truth-blind evidence** are useful or useless for future selector qualification. For example:

- a singular gap may or may not align with recoverable structure;
- cross-rank persistence may or may not distinguish real from spurious modes;
- weak observability may present as lower effective rank rather than estimator failure;
- a method may remain numerically stable while its modal content changes radically with rank.

It cannot establish a P1 threshold from the same development records.

## Required consequence

After this sweep is inspected, the project must choose one of three scientifically acceptable paths:

1. **Qualify method-native selectors prospectively** on new P0 development systems, then later freeze them for P1.
2. **Limit the P1 comparator claim to estimator-at-declared-order recovery**, explicitly withholding operational-selector superiority.
3. If no fair operational route can be justified, record that limitation rather than manufacturing a weak comparator.

The choice must be made before MFR-05 is frozen.
