# NSD T0 Engine Qualification Execution Ledger v0.1

Date opened: 14 September 2026
Status: ACTIVE
Target: T0 exit for the Neurophysiology Decision-Support Tool program

## 1. T0 exit definition

T0 exists to prove that the label-blind representation layer can recover known structure, refuse invalid reductions, preserve provenance, and operate on traceable real neurophysiology before any clinical model is allowed to matter.

T0 does **not** claim diagnosis, prognosis, a healthy chi range, or a universal neural stability scalar.

Provisional exit requirements:

1. deterministic provenance/hierarchy contracts;
2. metadata-role firewall;
3. signal-payload identity/readability gate;
4. generic label-blind signal QC;
5. descriptive spectral layer qualified on fixtures and real healthy data;
6. known-truth modal recovery for at least one native dynamical route;
7. scalar admission/refusal only after modal qualification;
8. local-versus-embedded stability known-truth tests;
9. nuisance/adversarial Limit Map;
10. repeat-session healthy qualification;
11. CI regression coverage;
12. versioned Engine outputs ready for Atlas serialization.

## 2. Mechanical verification

Latest confirmed full Engine contract suite before the optional parameterization work:

- GitHub Actions workflow: `NSD Engine Contracts`
- run: `34925476505`
- result: SUCCESS
- tests: **73 passed**
- runtime: 0.83 s

The suite includes provenance, hierarchy, metadata firewall, descriptive spectral/modal contracts, exact second-order fixtures, scalar admission/refusal, serialization, generic signal QC, local-versus-embedded 2x2 stability fixtures, EDF-header tests, EDF digital-to-physical sample access, and Welch PSD known-truth tests.

A separate exact-version descriptive parameterization qualification suite has also passed:

- workflow: `NSD specparam rc7 Qualification`
- run: `34925860672`
- result: SUCCESS
- tests: **7 passed**
- exact dependency: `specparam==2.0.0rc7`
- numerical stack in that successful run: NumPy 2.4.6 / SciPy 1.17.1

The specparam tests are deliberately isolated from the main contract suite because release-candidate parameterization software must not become a silent core dependency.

### Mechanical issues caught by CI rather than normalized away

Two useful failures occurred during this push:

1. adding a qualification-test directory initially broke setuptools automatic package discovery; package discovery was then explicitly frozen to `nsd_engine*`;
2. an earlier eager import of the PSD stack caused D4 payload tools to fail when NumPy/SciPy were absent; the package import surface was corrected so payload/provenance utilities remain dependency-light.

A third reproducibility issue was caught empirically: consecutive qualification workflows resolved NumPy 2.4.4 and then 2.4.6 under an open version range. The T0 numerical stack is therefore now explicitly frozen to:

- `numpy==2.4.6`;
- `scipy==1.17.1`.

This is a qualification freeze, not a claim that these versions are universally optimal.

## 3. Local-versus-embedded stability program

Executable native-system fixtures cover:

- same isolated local rates and same eigenspectrum with different coupling/non-normality and different reactivity;
- locally stable isolated components whose coupled system is globally unstable;
- an isolated unstable component whose coupled system is asymptotically stabilized;
- distinction between spectral abscissa and numerical-abscissa/reactivity behavior.

Implemented in:

`engine/nsd_engine/system_stability.py`

These fixtures operationalize the GOM rule:

`LOCAL DYNAMICAL IDENTITY != EMBEDDED REALIZED BEHAVIOR`

without introducing a project-branded whole-system parameter.

## 4. Generic signal QC

Implemented in:

`engine/nsd_engine/qc.py`

Current capabilities:

- per-channel finite/missing fraction;
- amplitude range;
- flat-channel detection;
- repeated numerical-extreme occupancy as a clipping/saturation indicator;
- channel-count accounting;
- conservative usable-duration bookkeeping;
- explicit caller-supplied thresholds;
- no hidden universal EEG-quality cutoffs.

The scientific rule is measurement first, task-specific admission threshold second.

## 5. First healthy real-data source: ds003775

Dataset identity:

- OpenNeuro `ds003775`;
- DOI `10.18112/openneuro.ds003775.v1.2.1`;
- NEMAR mirror `on003775/v1.0.0`;
- 111 subjects;
- 153 sessions;
- 42 repeat-session subjects;
- 64-channel BioSemi EEG;
- four-minute eyes-closed rest;
- 1024 Hz;
- average reference in the pinned raw release metadata.

### Gate state

- D0 discovery: CLOSED
- D1 provenance for pinned release: CLOSED FOR CURRENT SCOPE
- D2 hierarchy: VERIFIED
- D3 metadata/join: **VERIFIED FOR T0 HEALTHY QUALIFICATION**
- D4 signal input: **FROZEN 42-SUBJECT REPEAT POPULATION VERIFIED (84 recordings); non-repeat remainder not yet promoted**
- D5 analysis ready: OPEN

### D3 artifact

`atlas/manifests/ds003775_metadata_role_manifest_v0.1.json`

Canonical manifest-body SHA-256:

`28d71314e720eb4be799525c27c89f1f5a6090f2464e8d82e0c071effe1afe1d`

Only identity/acquisition/recording-state metadata may enter structural feature construction. Age, sex, and all participant cognitive scores are downstream.

## 6. D4 payload and sample decoding

### Single-file pilot

`sub-001 / ses-t1 / task-resteyesc`

Verified against the pinned NEMAR payload:

- exact annex MD5: PASS;
- exact expected byte count: PASS;
- EDF internal byte-count consistency: PASS;
- 64 channels: PASS;
- exact channel-label sequence: PASS;
- 1024 Hz on all channels: PASS;
- 240 s duration: PASS.

Confirmed workflow run:

`NSD ds003775 D4 Pilot` / `34924760163`

### Real repeat pair

Frozen repeat subject:

`sub-069`

Public hierarchy:

- `ses-t1`, acquisition `2017-10-17T10:33:20`;
- `ses-t2`, acquisition `2018-10-16T11:12:04`.

Pinned identities:

- t1: 31,473,920 bytes; MD5 `656b7184b5ed01e36601b79a3bf38c52`;
- t2: 31,473,920 bytes; MD5 `0ecea6e69394a865f2fca83086f1b947`.

Both files passed exact payload/header checks in workflow run `34924915222`.

A dependency-light EDF sample reader now verifies the digital-to-physical conversion explicitly and can read bounded physical-unit channel windows without loading an entire recording.

### First real signal-integrity probe

A 10-second, all-64-channel, label-blind physical-sample probe on the real repeat pair completed successfully.

Observed only as descriptive integrity facts:

- t1: 0 flat channels; 0 missing fraction; maximum repeated numerical-extreme occupancy 0.000390625;
- t2: 0 flat channels; 0 missing fraction; maximum repeated numerical-extreme occupancy 0.00029296875.

This does **not** mean the data are artifact-free or scientifically preprocessed. It shows the payload can be decoded into plausible non-flat finite physical samples and is suitable for the next qualification layer.

## 7. Descriptive Welch PSD layer

Implemented in:

`engine/nsd_engine/psd.py`

Frozen primitive characteristics:

- SciPy Welch;
- exact method/version recorded;
- explicit window length;
- explicit overlap;
- explicit detrending;
- explicit density/spectrum convention;
- explicit frequency range and resolution;
- no damping license;
- no natural-frequency license;
- no chi license.

Known-truth tests recover a known sinusoidal frequency, check integrated PSD power against signal variance, and enforce input/frequency/window validity.

### Real repeat-session PSD pilot

`sub-069`, full four-minute t1/t2 recordings, all 64 channels, 1–45 Hz.

Initial 4-second-window run:

- Hann window;
- 50% overlap;
- constant detrend;
- density scaling;
- 0.25 Hz frequency resolution;
- 119 Welch segments.

Single-subject descriptive repeat result:

- global median log-PSD correlation: approximately **0.99**;
- median channel log-PSD correlation: approximately **0.98**;
- minimum channel correlation in that run: approximately **0.89**.

Interpretation ceiling:

> one healthy subject, one acquisition family, descriptive PSD similarity only. This is not an ICC, population reliability estimate, trait claim, or clinical result.

## 8. Welch-window nuisance / Limit-Map probe

A prespecified 2 s / 4 s / 8 s comparison was run with no model-selection rule and no attempt to choose whichever window looked best.

All settings used:

- 1–45 Hz;
- Hann;
- 50% overlap;
- constant detrending;
- density scaling.

### Repeat-session log-PSD similarity

| Window | Resolution | Segments | Global median-PSD correlation | Median channel correlation | Minimum channel correlation |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 s | 0.5 Hz | 239 | 0.9950 | 0.9929 | 0.9262 |
| 4 s | 0.25 Hz | 119 | 0.9937 | 0.9905 | 0.9235 |
| 8 s | 0.125 Hz | 59 | 0.9934 | 0.9869 | 0.9179 |

These numbers are a nuisance map, **not** evidence for selecting 2 s as “best.”

### Cross-window behavior within each recording

PSD *shape* was extremely similar on the common 0.5-Hz grid across all window pairs, with median channel log-shape correlations above 0.996 in both sessions.

Integrated 1–45-Hz power was more window-sensitive than shape. Median symmetric relative differences were:

- t1: 2 s vs 4 s = 0.0847; 2 s vs 8 s = 0.0991; 4 s vs 8 s = 0.0172;
- t2: 2 s vs 4 s = 0.0494; 2 s vs 8 s = 0.0757; 4 s vs 8 s = 0.0268.

The maximum channel-level differences were substantially larger in some comparisons. Therefore absolute integrated power cannot be treated as configuration-invariant merely because spectral shape is highly correlated.

Next required scale-up is the 42-repeat-subject population, where configuration effects can be quantified subject-aware rather than inferred from one person.

## 9. Periodic/aperiodic parameterization qualification

The project has **not** promoted a periodic/aperiodic parameterizer into the Atlas yet.

Current qualification route:

- exact isolated dependency: `specparam==2.0.0rc7`;
- adapter: `engine/nsd_engine/specparam_adapter.py`;
- known-truth tests: `engine/qualification_tests/test_specparam_adapter.py`;
- exact-version qualification CI: PASS, **7 tests passed**;
- raw Welch PSD remains independently available beneath the parameterizer;
- returned peak bandwidth remains descriptive only.

The first passing tests cover:

- pure fixed aperiodic truth with no invented peak;
- one separated Gaussian peak;
- two separated Gaussian peaks;
- knee truth versus a misspecified fixed model;
- broad Gaussian bump kept descriptive;
- exact release-candidate version freeze;
- invalid/nonpositive power rejection.

A broader known-truth failure-boundary map is now active for:

- overlapping-peak separation;
- weak-peak detection under deterministic noise;
- frequency-resolution sensitivity;
- knee misspecification with periodic fitting enabled;
- broad-bump behavior.

No real healthy periodic/aperiodic result is admitted until this failure map is inspected and the operating region is declared.

## 10. 42-subject repeat-population result

Workflow:

- `NSD ds003775 42-Subject Repeat Population`
- run `35304835270`
- result: **SUCCESS**
- 42 independent repeat subjects;
- 84 exact pinned recordings re-verified at D4 before analysis.

The authoritative result note is:

`docs/DS003775_REPEAT_POPULATION_T0_RESULT_v0.1.md`

Key descriptive population findings:

- median global median-log-PSD repeat correlation: **0.99146**;
- median channel log-PSD repeat correlation: **0.97946**;
- median of each subject's minimum channel correlation: **0.74840**, with a minimum subject value of **-0.80173**;
- median subject-level absolute aperiodic-exponent difference: **0.20476**;
- median exact same peak-count fraction: **0.46094**;
- median exact same zero-peak-state fraction: **0.97656**;
- median fixed-versus-knee model-family disagreement across the 84 sessions: **0.42188**.

Decision:

- raw Welch spectral shape is population-useful as a descriptive layer, with important subject/channel Limit-Map outliers;
- the descriptive periodic/aperiodic layer is retained for Atlas/Limit-Map use but is **not** promoted as a standalone trait biomarker;
- no configuration is retuned after inspecting these results;
- channel-wise subject-aware repeatability is now closed for this frozen output: exponent ICC(A,1) median **0.65882** across 64 channels (range **0.40278–0.83557**), exact peak-count agreement median **0.53571**, and exact zero-peak-state agreement median **0.90476**; no reliability threshold was tuned from these observations.

## 11. M2 adversarial model-adequacy result

Workflow:

- `NSD Latent Oscillator Adversarial Map`
- run `35304835293`
- result: **SUCCESS**.

The current M2 single-latent-oscillator covariance gate admitted every tested misspecified adversary, including close/separated two-mode mixtures, colored observation noise, frequency drift, bursts, nonoscillatory AR(1), and white noise.

A close two-mode generator achieved median covariance-fit R-squared approximately **0.9403**, slightly above the valid single-mode truth at approximately **0.9382**. Therefore fit quality alone cannot license a unique single oscillator.

Current decision:

`M2_LATENT_COVARIANCE = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED`

The next modal work is explicit model adequacy/order qualification, frozen in:

`docs/M2_MODEL_ADEQUACY_PLAN_v0.1.md`

## 12. Immediate execution order from here

1. convert the closed 42-subject descriptive/repeatability outputs into the first versioned Atlas-P0-D reference artifact without inventing a healthy cutoff;
2. preserve channel heterogeneity, model-family disagreement, zero-peak state, and refusal/open-channel rates in that artifact rather than reducing them to one score;
3. continue the modal P0-Q adequacy program with formal nonoscillatory / one-oscillator / multi-oscillator model competition plus stationarity, colored-noise, residual/innovation, and identifiability tests;
4. keep real-EEG modal damping ratios disabled until that modal route survives the frozen adequacy program;
5. define the first research-grade individual assessment rendering against the versioned Atlas artifact, with diagnostic and prognostic modules explicitly disabled;
6. expand to the larger adult Function/Limit dataset only after the first ds003775 Atlas-P0-D artifact and report contract are reproducible;
7. keep all clinical labels downstream until T0/T1 gates are closed.

## 13. Stop lines

Still prohibited at T0:

- clinical classification;
- ASD feature selection;
- diagnosis-informed region selection;
- prognosis;
- treatment guidance;
- universal healthy stability boundaries;
- direct bandwidth-to-damping conversion;
- whole-brain chi;
- any claim that repeated-session similarity alone proves trait biology.

The intended T0 outcome is a trustworthy measurement and representation engine. Clinical usefulness is tested downstream rather than assumed upstream.


## 14. GOM v0.8.0 live-alignment checkpoint - 18 September 2026

Purpose tag: QUALIFICATION

The authoritative SymC GOM v0.8.0 was re-read against the live NSD branch after the M2 adversarial work and 42-subject repeat population.

Alignment retained:
- T0 remains P0-Q / label-blind qualification, not P1 confirmation;
- Function Map and Limit Map are coequal;
- descriptive spectral structure remains distinct from dynamical/modal interpretation;
- no whole-system chi is manufactured;
- local dynamical identity remains distinct from embedded/system behavior;
- Atlas information remains read-only with respect to Engine construction;
- clinical labels remain downstream of structural qualification;
- open-channel failures, absent features, model disagreement, and poor-reliability regions remain visible;
- real-EEG modal damping/local chi remains disabled until model adequacy is frozen and qualified.

GOM gap closed:
- added docs/P0Q_QUALIFICATION_SEARCH_LEDGER_v0.1.md so substantial iterative qualification records candidate families, reused evidence, targeted failures, complexity increases, search history, and stopping rationale.

Execution-governance repair:
- the long-lived PR could retrigger the expensive 42-subject population workflow from cumulative pull-request path matching after unrelated commits;
- .github/workflows/nsd-ds003775-repeat-population.yml now includes current-synchronize diff gating and concurrency cancellation so obsolete/redundant population executions do not consume compute;
- this repair changes execution control only, not scientific inputs or analysis rules.

M2 interim diagnostic result:
- A0-like AR(1) covariance competition correctly exposes the explicit nonoscillatory AR(1) adversary;
- split-half stability exposes strong mid-record frequency change;
- the covariance two-oscillator pseudo-BIC improves the criterion for true two-mode adversaries but also for valid single-mode truth;
- therefore no pseudo-BIC or post-hoc combined cutoff is frozen;
- the proper A0/A1/A2 state-space likelihood/innovation route remains the next modal qualification task.

Current safe resume point:
1. maintain the existing 42-subject descriptive/repeatability result as P0-Q evidence;
2. allow one current guarded population run when the repeatability code itself changes, without repeated unrelated reruns;
3. implement the proper M2/A0-A1-A2 adequacy layer;
4. build the first versioned descriptive Atlas artifact only from already qualified layers;
5. do not open clinical labels or real-EEG damping until their upstream gates close.

User action: NONE.


## 15. First Atlas and report milestone — 18 September 2026

The first two items in the prior execution order are now closed at P0-D.

### Atlas serialization

Committed Atlas version:

`ds003775-repeat-p0d-v0.1`

Canonical artifacts:

- `atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json`;
- `atlas/manifests/ds003775_repeat_atlas_p0d_release_v0.1.json`;
- `atlas/release_records/ds003775_repeat_p0d_v0.1.md`.

The artifact preserves population repeatability, channel heterogeneity, model-family disagreement, zero-peak behavior, and explicit Limit-Map quantities rather than compressing them into one score.

Evidence-path grade for the decisively used ds003775 descriptive reference family:

`NON_INDEPENDENT_FOR_ENGINE_VALIDATION`

because the same source cohort contributed to T0 qualification and this P0-D reference build. It is therefore not used as independent P1 evidence.

### First real-recording report path

The reporting layer now contains a real pinned-recording example for `sub-069 / ses-t1`:

- machine-readable JSON report;
- human-readable research rendering;
- reproducible report builder.

The report remains:

`RESEARCH_STRUCTURE_ONLY`

and visibly disables:

- individual abnormality scoring;
- modal damping / local chi;
- screening;
- diagnosis;
- prognosis.

This establishes the product/reporting plumbing without inventing clinical capability.

### Proper modal adequacy route

A formal A0/A1/A2 state-space candidate-model layer using steady-state Kalman innovations likelihood and BIC is now implemented on the branch with:

- A0 nonoscillatory relaxation;
- A1 single latent oscillator;
- A2 two latent oscillators;
- innovation autocorrelation diagnostics;
- split-half comparison;
- held-out scoring.

The corresponding adequacy workflow is active. The first test-file collection failure was mechanical (a literal escaped newline in the import statement) and was corrected immediately. Engine contract CI subsequently returned to green on the corrected branch lineage.

No BIC winner is treated as a real-EEG admission rule. The known-truth/adversarial map must close before modal parameters can move downstream.

### Current resume point

1. allow the A0/A1/A2 likelihood adequacy map to complete and inspect the exact adversarial confusion pattern;
2. freeze only the diagnostics that distinguish known truth for principled reasons; if close-mode, burst, colored-noise, or nonstationarity failures remain unresolved, keep explicit refusal states;
3. keep real-EEG modal damping disabled until the model-adequacy operating region is declared;
4. use the committed Atlas-P0-D and reporting contract to design the next broader, more independent reference build;
5. advance ds005385 toward the adult Function/Limit Atlas only after its metadata and signal-input gates are explicitly closed;
6. keep all diagnostic and prognostic models empty until T1/T2 maturity gates are earned.

User action: NONE.
