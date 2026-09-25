# GRI ↔ Bio Chi autonomous continuation checkpoint

**Last updated:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** SHAFFER SOURCE QUALIFICATION CLOSED / METHOD-SELECTION GATE ACTIVE  
**Authority:** SymC General Operations Manual v0.8.6 + GRI controls + Bio Chi three-object nomenclature.

## Resume here

The active bridge source is Shaffer et al. 2017.

### Completed
- Harmange direct bridge refused for current source-materialization limits without inventing lineage identity.
- GSE97679 source schema PASS.
- GSE97679 metadata/common-gene audit PASS: 63,682 genes shared exactly across both processed RNA runs.
- week-1 states span both GSE97679 sequencing runs and remain the internal run-sensitivity bridge.
- GSE97681 metadata-only audit PASS on run 36157584442.
- all five GSE97681 processed tables are retrievable and share the same 63,682-gene universe/hash as GSE97679.
- WM989 source material mechanically supports the frozen source-internal validation role with paired drug/no-drug plus 48-hour and 7-day holiday states.
- WM983B source material mechanically supports the frozen same-source transfer role with paired and longitudinal drug-state records.
- no target-gene effect, resistance-marker selection, B2 result, B3 result, or chi_bio calculation was used to qualify these sources.

### Inherited scientific constraints
Do not restart closed GRI routes:
- historical CV/2 is closed;
- static covariance is not a native dynamical operator;
- feature filtering is separate from normalization;
- target outcomes may not define the primary representation;
- same-source validation is not external confirmation;
- chi_bio scalar admission is not required for Chi_bio modal or Bio Chi investigation.

### Current method-selection gate
The Shaffer source uses raw HTSeq counts and source-native DESeq2 analysis. This removes the tximport-count ambiguity that made DESeq2 VST a conditional/sensitivity candidate in the earlier SCC25 normalization packet.

Candidate method packet:
`BIO_CHI/control/SHAFFER2017_PREANALYSIS_METHOD_DECISION_PACKET_20260925.md`

Current candidates only, not frozen:
- DESeq2 VST as source-compatible primary candidate for review;
- deterministic library-size + log transform as minimal sensitivity/baseline;
- TMM/log-CPM as optional composition-robust sensitivity if a clean development-only reference rule is established;
- PCA/SVD-type unsupervised geometry as the first low-complexity modal candidate/baseline.

### Immediate safe continuation
Continue:
1. source-method and comparator literature review;
2. executable preprocessing/environment preflight without target-effect interpretation;
3. exact sample-role and batch/run mechanics;
4. refinement of the candidate decision packet.

Stop before:
- freezing normalization/filter/modal/comparator/B2/B3/endpoint choices without scientific adjudication;
- opening target molecular effects;
- constructing chi_bio without a qualifying dynamical carrier.

The hourly continuation check should advance only the safe work above and surface the method freeze as a scientific decision once the candidate packet is sufficiently resolved.
