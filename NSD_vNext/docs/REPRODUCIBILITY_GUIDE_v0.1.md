# NSD Reproducibility Guide v0.1

Status: ACTIVE
Date: 24 September 2026
Program authority: SymC General Operations Manual v0.8.6
Working branch: `nsd-rebuild-gom-v0.8.0`

This guide is the executable verification path for the current NSD healthy descriptive and independent-transfer work. It supplements the broader R1/R2/R3 matrix and follows the GOM v0.8.6 V-section format.

## V1. Verify the frozen independent source

[CLAIM] The current ds004148 transfer pilot uses the exact six resting recordings already closed at D4 before any signal-derived transfer result was opened.

Run:

```bash
python NSD_vNext/engine/tools/d4_verify_ds004148_resting_crosssession.py \
  --manifest NSD_vNext/docs/manifests/ds004148_d4_resting_crosssession_v0.1.json \
  --download-dir ./ds004148-d4-payloads \
  --output ./ds004148-d4-report.json
```

Expected:
- 6/6 recordings pass exact identity and raw-layout checks;
- raw payload resolves to 61 channels, 500 Hz, 300 s, IEEE 32-bit float;
- the source JSON 64-channel declaration remains a provenance anomaly rather than being repaired by padding.

Interpretation: this verifies source identity and decoding. It does not verify any neural stability claim.

## V2. Verify the pre-result transfer freeze

[CLAIM] The descriptive transfer task, representation, hierarchy, comparison metrics, refusal rules, and interpretation ceiling were frozen before signal-derived ds004148 transfer outcomes were opened.

Inspect:

```bash
cat NSD_vNext/docs/DS004148_DESCRIPTIVE_TRANSFER_FREEZE_v0.1.md
```

Expected:
- same-state session pairs only;
- frozen Welch and specparam settings reused without retuning;
- no composite transfer score;
- channels remain nested repeated measurements;
- no ds004148-driven threshold choice;
- modal damping, lowercase chi, capital Chi, global chi, diagnosis, recovery, and population inference remain prohibited.

Interpretation: this is the prospective task contract, not a result.

## V3. Verify the committed reference parent

[CLAIM] Transfer labels are referenced to the previously committed ds003775 descriptive P0-D artifact rather than a ds004148-tuned baseline.

Inspect:

```bash
python - <<'PY'
import json
p = "NSD_vNext/atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json"
d = json.load(open(p, encoding="utf-8"))
print(d["atlas_data_id"])
print(d["maturity"])
print(d["subject_count"], d["session_count"])
print(d["population"])
PY
```

Expected:
- atlas_data_id: `ds003775-repeat-p0d-v0.1`;
- maturity: `ATLAS_P0_D`;
- 42 subjects and 84 sessions;
- empirical minimum, median, and maximum values remain unchanged.

Interpretation: the reference is a descriptive Function/Limit artifact. It is not an independent confirmatory Atlas and does not establish a healthy clinical boundary.

## V4. Execute the independent descriptive transfer suite

[CLAIM] The frozen representation can be applied without retuning to the six D4-pinned ds004148 recordings and returns the predeclared metric-by-metric transfer vector plus Limit Map.

Run:

```bash
python -m pip install -e 'NSD_vNext/engine[parameterization_rc7]'

python NSD_vNext/engine/tools/run_ds004148_descriptive_transfer.py \
  --manifest NSD_vNext/docs/manifests/ds004148_d4_resting_crosssession_v0.1.json \
  --atlas NSD_vNext/atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json \
  --matched-reference NSD_vNext/atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_matched59_v0.1.json \
  --output-dir ./nsd-transfer-output
```

Expected outputs:
- `ds004148_descriptive_transfer_result_v0.2.json`;
- `VERIFY_SUMMARY.md`;
- two state blocks, eyes closed and eyes open;
- three same-state session-pair comparisons per state;
- per-recording Limit metrics;
- descriptive labels `WITHIN_PREVIOUS_ENVELOPE`, `OUTSIDE_PREVIOUS_ENVELOPE`, or `REFUSED_OR_NOT_AVAILABLE`.

Interpretation: the labels describe transport relative to a previous empirical envelope. They are not tuned success thresholds. An outside-envelope value is retained as a Limit Map observation.

## V5. Verify the scientific firewalls

[CLAIM] The transfer suite cannot silently promote a descriptive result into damping, chi, capital Chi, diagnosis, or population inference.

Run:

```bash
python - <<'PY'
import json
p = "./nsd-transfer-output/ds004148_descriptive_transfer_result_v0.2.json"
d = json.load(open(p, encoding="utf-8"))
for key in [
    "licenses_modal_damping",
    "licenses_local_chi",
    "licenses_capital_chi",
    "licenses_diagnosis",
    "licenses_population_inference",
]:
    print(key, d[key])
    assert d[key] is False
print("FIREWALL_CHECK=PASS")
PY
```

Expected: every licensing field is `False` and the final line is `FIREWALL_CHECK=PASS`.

Interpretation: descriptive repeat structure remains descriptive. Repeat similarity is not called recovery or resilience.

## V6. Verify suite integrity

[CLAIM] The GitHub Actions suite packages the exact freeze, source manifest, reference artifact, production runner, dependency declaration, result, verification summary, run command, and SHA-256 ledger while excluding downloaded raw EEG payloads.

Workflow:
`.github/workflows/nsd-ds004148-descriptive-transfer.yml`

Expected artifact:
`nsd-ds004148-descriptive-transfer-suite-v0-2`

Required packaged records:
- `DS004148_DESCRIPTIVE_TRANSFER_FREEZE_v0.1.md`;
- `ds004148_d4_resting_crosssession_v0.1.json`;
- `ds003775_repeat_descriptive_reference_p0d_v0.1.json`;
- `run_ds004148_descriptive_transfer.py`;
- `pyproject.toml`;
- `ds004148_descriptive_transfer_result_v0.2.json`;
- `VERIFY_SUMMARY.md`;
- `RUN_COMMAND.txt`;
- `SHA256SUMS.txt`.

Interpretation: the artifact is the compact reviewer-facing reproduction suite for this experiment. It does not redistribute the raw EEG.

## V7. Master smoke test

[CLAIM] A completed suite has the expected hierarchy and preserves every current interpretation firewall.

Run:

```bash
python - <<'PY'
import json
p = "./nsd-transfer-output/ds004148_descriptive_transfer_result_v0.2.json"
d = json.load(open(p, encoding="utf-8"))
assert d["recording_count"] == 6
assert sorted(d["states"]) == ["eyesclosed", "eyesopen"]
assert all(state["pair_count"] == 3 for state in d["states"].values())
assert d["licenses_modal_damping"] is False
assert d["licenses_local_chi"] is False
assert d["licenses_capital_chi"] is False
assert d["licenses_diagnosis"] is False
assert d["licenses_population_inference"] is False
print("MASTER_SMOKE_TEST=PASS")
PY
```

Expected: `MASTER_SMOKE_TEST=PASS`.

Interpretation: a passing smoke test establishes package and contract integrity only. Scientific interpretation remains bounded by the freeze and post-result record.


## V8. Verify corrected exact-label closure

[CLAIM] The promoted ds004148 transfer result uses the exact 59-channel label intersection required by the prospective freeze, and the first 61-versus-64 implementation is retained only as provenance.

Inspect:

```bash
cat NSD_vNext/docs/DS004148_EXACT_LABEL_REFERENCE_REMEDIATION_v0.1.md
cat NSD_vNext/docs/DS004148_DESCRIPTIVE_TRANSFER_POSTRESULT_v0.2.md
```

Expected:
- corrected workflow run `36088323374`;
- artifact `nsd-ds004148-descriptive-transfer-suite-v0-2`;
- artifact digest `sha256:f6ce93029c38d72016c2bfd17f4e1b7bdc74bdc5d3ac0fac780896052bf170ce`;
- exact comparison channel count = 59;
- all nine state-median indicators for eyes closed and all nine for eyes open labeled `WITHIN_PREVIOUS_ENVELOPE`;
- two pair-level Limit Map excursions retained rather than hidden by the state median.

Interpretation: the frozen descriptive representation transported to this independent one-subject source at the state-median level without retuning. The result remains P0-Q and does not license modal damping, lowercase chi, capital Chi, diagnosis, recovery, or population inference.


## V9. Verify checkpoint continuation

[CLAIM] NSD checkpoints automatically hand off to the next already-justified experiment rather than waiting for a new user prompt.

Required behavior:
- checkpoint state and result ceiling are committed before continuation;
- mechanical blockers are repaired without changing frozen science;
- failures/outliers receive root-cause and anomaly disposition;
- the next experiment is prospectively frozen before its target outcome is opened;
- execution stops only at a genuine scientific decision boundary.

Current continuation:
`ds004148 corrected descriptive transfer -> ds004148 eyes-open spatial/state localization`.

Interpretation: this is an operations/reproducibility rule. It cannot be used to silently enlarge scientific claims or retune an experiment after seeing its result.


## V10. Verify spatial/state localization closure

[CLAIM] The sub-01 pair-level excursion was localized with channel-specific parent context before any independent-subject replication outcome was opened.

Inspect:

```bash
cat NSD_vNext/docs/DS004148_SPATIAL_LOCALIZATION_FREEZE_v0.1.md
cat NSD_vNext/docs/DS004148_SPATIAL_LOCALIZATION_POSTRESULT_v0.1.md
```

Expected:
- workflow run `36139756523`;
- suite `nsd-ds004148-spatial-localization-suite-v0-1`;
- artifact digest `sha256:2a8db256d431f8a436c66229accb633c2d5511709388f1bbd31485de5e9b7ea0`;
- parent reference rebuilt from 42 frozen ds003775 subject artifacts;
- 59 exact matched labels;
- target eyes-open session2-session3: 11/21 eligible channels above channel-specific parent q95;
- eyes-open session1-session3: 10/19 high;
- eyes-open session1-session2: 8/35 high;
- modal/damping/chi/capital-Chi firewalls remain false.

Interpretation: the localization identifies a session-3 eyes-open descriptive pattern and model-family coupling in sub-01. It is explanatory discovery and does not establish an independent-subject effect.

## V11. Verify untouched MFR-14 handoff

[CLAIM] The next checkpoint proceeds automatically into an untouched independent-subject replication without reusing sub-01 or retuning the representation.

Inspect:

```bash
cat NSD_vNext/docs/DS004148_EYESOPEN_MFR14_REPLICATION_FREEZE_v0.1.md
cat NSD_vNext/docs/manifests/ds004148_eyesopen_mfr14_replication_v0.1.json
```

Expected:
- subjects `sub-02` through `sub-15`;
- 14 independent subjects;
- all three eyes-open sessions per subject;
- exact source/D4 gate before features;
- no replacement subjects after signal outcomes;
- subject-level paired contrasts;
- exact sign tests with Holm correction for the two predeclared high-shift-fraction contrasts;
- no modal, chi, capital-Chi, clinical, recovery, or broad population promotion.

Interpretation: this is the first untouched independent-subject test of the session-3 descriptive pattern within ds004148.


## V12. Verify white-process pole-identifiability predecision record

[CLAIM] The modal qualification branch has an analytic predecision record that separates identifiable oscillator-pole structure from non-identifiable latent process-noise covariance and does not license real-EEG local chi.

Inspect:

```bash
cat NSD_vNext/docs/STATE_SPACE_WHITE_PROCESS_POLE_IDENTIFIABILITY_PREFLIGHT_v0.1.md
```

Expected:
- current frozen A1 remains `F = rho R(theta)`, scalar `G = [1,0]`, isotropic `Q = q I`;
- arbitrary white process covariance preserves the same generic second-order positive-lag covariance recurrence and therefore does not by itself destroy pole identifiability;
- latent `Q` remains non-unique and must not be biologically interpreted;
- the broader standardized one-oscillator white-process observable class adds exactly one covariance-phase/numerator shape degree relative to current A1;
- exact scalar admissibility is enforced analytically through nonnegative residual spectral numerator over `x = cos(omega) in [-1,1]`, not through an empirical cutoff;
- colored process noise remains a separate augmented-model family;
- the document is PREDECISION ANALYTIC PREFLIGHT ONLY and authorizes no estimator-family change.

Current provenance:
- preflight introduction commit: `e6280d145a91e50cdc143ec65587776f6a655b35`;
- exact observable-admissibility refinement commit: `fdafa412a2f53198a9887ba5efc2b3d175da3c26`.

Interpretation: this record refines the candidate packet and refusal logic only. It does not change A0/A1/A2, define a production threshold, license modal damping or local chi on real EEG, or alter N-B2/N-B3.

## V13. Verify lineage, sampling, and substrate-closure qualification contracts

[CLAIM] The NSD Bio Chi predecision branch contains executable, threshold-free known-truth contracts for continuous-lineage sampling behavior and substrate/projection closure without changing A0/A1/A2 or licensing real-EEG local chi.

Run:

```bash
cd NSD_vNext/engine
python -m pip install pytest numpy
python -m pytest -q \
  tests/test_state_space_lineage_sampling.py \
  tests/test_substrate_closure_contracts.py
```

Expected:
- exact m-fold covariance decimation contracts pass across underdamped, critical, and stable positive-real overdamped regimes;
- continuous-lineage coordinate `g` is invariant under alias-safe exact decimation;
- sample-rate-specific discrete exact-image coordinate `h` contracts under canonical coarsening;
- exact Hankel transport and the underdamped alias/order-collapse control pass;
- the constructive `S\\D -> D\\C` coarse-graining witness remains valid;
- substrate closure fixtures distinguish exact closed, hidden-input exposed, leaky-without-return, and bidirectional return-memory classes;
- the Schur-complement self-energy reproduces the exact projected resolvent for bidirectionally coupled known truths.

Inspect:

```bash
cat NSD_vNext/docs/STATE_SPACE_LINEAGE_SAMPLING_QUALIFICATION_SUITE_v0.1.md
cat NSD_vNext/docs/SUBSTRATE_CLOSURE_QUALIFICATION_PREFLIGHT_v0.1.md
```

Interpretation: passing V13 establishes analytic and known-truth contract integrity only. It does not define an empirical closure threshold, change the production estimator family, license local chi on real EEG, or alter N-B2/N-B3.

## V14. Execute the exploratory nonzero-g continuous-lineage probe

[CLAIM] The unchanged A0/A1/A2 likelihood machinery can be exercised on exact nonzero-g continuous-lineage known truths and on deterministic decimations of the same realized path without changing the production estimator or licensing real EEG.

Run:

```bash
cd NSD_vNext/engine
python -m pip install -e .
python tools/probe_continuous_lineage_nonzero_g.py \
  --output ../../continuous-lineage-probe/continuous_lineage_nonzero_g.json
```

Expected output:
- status `EXPLORATORY_KNOWN_TRUTH_ONLY`;
- `licenses_real_eeg_local_chi=false`;
- `changes_production_estimator=false`;
- paired fine/coarse results generated from the same realized continuous-lineage path;
- descriptive A0/A1/A2 BIC, innovation diagnostics, and fitted parameters for each known-truth cell.

Interpretation: V14 is an exploratory model-adequacy probe. A1 or A2 preference is not itself an admission or refusal rule. Its purpose is to determine whether current A1's H=0/B=0 restriction remains adequate inside the intended continuous-lineage C family before any estimator-family modification is considered.

## V15. Map predictive approximate closure without defining an admission threshold

[CLAIM] The approved predictive-closure policy can be exercised on exact known-truth projection mechanisms while keeping raw leakage, hidden-state sensitivity, return memory, pole displacement, chi displacement, and resolved predictive error distinct.

Run:

```bash
cd NSD_vNext/engine
python tools/probe_predictive_closure_calibration.py \
  --output ../../predictive-closure-probe/predictive_closure_calibration.json
```

Expected:
- status `EXPLORATORY_KNOWN_TRUTH_ONLY`;
- `licenses_real_eeg_local_chi=false`;
- `defines_closure_threshold=false`;
- exact closed, P-to-Q leakage-only, Q-to-P hidden-input-only, and bidirectional return-memory classes;
- separate resolved prediction error, hidden-initial-state sensitivity, memory-kernel magnitude, pole displacement, and chi displacement fields;
- leakage-only fixtures can retain exact resolved prediction despite nonzero P-to-Q leakage;
- hidden-input and return-memory effects remain distinguishable.

Inspect:

```bash
cat NSD_vNext/docs/PREDICTIVE_APPROXIMATE_CLOSURE_POLICY_v0.1.md
cat NSD_vNext/docs/SUBSTRATE_CLOSURE_QUALIFICATION_PREFLIGHT_v0.1.md
```

Interpretation: V15 maps how known substrate/projection mechanisms affect the specific N-B1 local-mode claim. It does not define the empirical closure tolerance. Any future predictive-error, memory-decay, pole-displacement, chi-displacement, or uncertainty threshold must be prospectively calibrated and frozen before real EEG is opened.

## V16. Quantify spectral model-order pressure from nonzero-g C truths

[CLAIM] A valid single-mode continuous-lineage C truth with nonzero covariance-phase coordinate H can be compared against the best spectra reachable by the unchanged A1 and A2 families without fitting real EEG or modifying either family.

Run:

```bash
cd NSD_vNext/engine
python tools/probe_continuous_lineage_spectral_kl.py \
  --output ../../continuous-lineage-probe/continuous_lineage_spectral_kl.json
```

Expected output:
- status `PREDECISION_ANALYTIC_ONLY`;
- `licenses_real_eeg_local_chi=false`;
- `changes_production_estimator=false`;
- exact C-family truth cells at the declared g values;
- best reachable A1 and A2 spectral KL rates under the current optimizer parameter box;
- fitted A1 chi for comparison with truth chi;
- expected A1-to-A2 likelihood improvement and descriptive BIC implication at the declared effective sample count.

Interpretation: V16 tests whether current A1's H=0 restriction creates model-order pressure inside the scientifically intended C family. An A2 advantage in this probe is evidence of model-family misspecification pressure, not evidence for two physical modes and not authorization to promote a new estimator. Any nuisance-family expansion remains a separate qualification and promotion step.
