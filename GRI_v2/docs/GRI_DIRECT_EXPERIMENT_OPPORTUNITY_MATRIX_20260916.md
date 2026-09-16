# GRI direct-experiment opportunity matrix

**Date:** 2026-09-16  
**Status:** DESIGN SPACE, NOT A FROZEN EXPERIMENT  
**Purpose:** define physically/biologically testable residual questions before manuscript convenience or available datasets choose the science.

## Governing rule

These are **question-first experiment sketches**. They do not authorize a state representation, model dimension, threshold, estimator, restoration law, or biological unity boundary. Where existing public studies already collide with an experiment design, that collision is recorded as an opportunity to answer part of the question computationally before commissioning new wet-lab work.

A design becomes a real experiment only after a separate prospective freeze defines its endpoint, comparator, uncertainty model, sample structure, analysis plan, and falsifier.

## Opportunity matrix

| ID | Residual question | Direct experiment concept | Required measurements | Strong falsifier / informative negative | Existing source collision already in GRI | Residual value if literature/source collision is strong |
| --- | --- | --- | --- | --- | --- | --- |
| EXP-R1 | Can transcript restoration/degradation be identified separately enough from regulatory interaction to normalize G1? | pulse-label or transcription-block/release experiment under matched control and treatment, with repeated RNA measurement over decay/recovery window | gene/transcript abundance at sufficiently dense times; condition labels; technical/biological replicates; viability/total-RNA controls; ideally an orthogonal RNA-stability readout | plausible restoration models or replicates yield materially different normalized G1 conclusion; effective decay is strongly transcript-/state-dependent in a way that defeats a common restoration family | current SCC25 G2 provides transition structure but not restoration decomposition; existing external RNA-stability measurements may constrain plausibility but are not condition-matched | identify what restoration information is truly missing and whether a common normalized G1 is scientifically tenable at all |
| EXP-R2 | Does removal of a perturbation reveal recovery/resilience information that continued-exposure trajectories cannot identify? | perturb cells to an altered state, remove drug, then follow return/non-return across multiple times rather than only continued exposure | RNA time course before/during/after washout; phenotype/viability; optionally methylation or ATAC context; replicate lineages | no reproducible return trajectory; multiple stable post-washout states; recovery ordering depends strongly on representation; treatment withdrawal does not restore the pre-treatment basin | chronic SCC25 source is continued cetuximab, so it cannot establish washout recovery; short-term source is also continued exposure | leaves a clean residual experimental question even after existing SCC25 temporal data are exhausted |
| EXP-R3 | Is the local transcriptomic dynamical identity preserved when embedded substrate/context changes? | hold nominal perturbation/state protocol fixed while measuring transcript dynamics and an orthogonal substrate layer in the same biological system | RNA plus ATAC and/or methylation at matched states/times; phenotype; replicate cultures/subjects | RNA transition structure changes qualitatively with substrate context, or substrate relation is not transportable across cell lines/conditions | `GSE135604` already supplies day-5 ATAC in the HNSCC cetuximab program; `GSE98813` supplies chronic methylation paired to RNA | existing data can test limited local-vs-embedded relations; new experiment would be justified only for missing temporal matching, replication, or washout |
| EXP-R4 | Does a distributed/modal description transport better than a forced scalar compression? | prospectively freeze multiple representation classes before perturbation, then compare their out-of-sample transport across matched systems without selecting on outcome | repeated RNA trajectories in at least two systems/cell lines; same perturbation; predefined representation outputs; independent phenotype axis | scalar and modal/system descriptions are equally nontransportable, or apparent modal advantage vanishes under a fair complexity/uncertainty comparison | short-term SCC25/SCC1 and chronic SCC25 create a natural cross-system/cross-timescale challenge, but SCC25 has already contributed to development | useful for designing a future untouched transport experiment after representation classes are frozen elsewhere |
| EXP-R5 | Is there a measurable temporal precursor to an independently defined phenotypic transition? | collect dense molecular trajectory while phenotype is measured independently, with the molecular coordinate frozen before phenotype inspection | RNA trajectory; phenotype such as proliferation/response; optionally substrate layer; enough temporal density to order molecular vs phenotype changes | molecular changes do not precede phenotype, ordering is unstable under uncertainty, or candidate refuses exactly where prediction would be needed | chronic HNSCC cetuximab has independently measured proliferation during acquired resistance; short-term study also contains phenotype data | can test timing hypotheses internally now, but an untouched system would be required for strong confirmation after any predictor is constructed |
| EXP-R6 | Are apparent system-level states driven by changing cell composition rather than within-cell regulation? | pair bulk multiomic measurements with single-cell profiling from the same specimens/states | bulk RNA/methylation/protein where possible; scRNA/scATAC; exact specimen identity; cell fractions; longitudinal pairing if available | bulk state movement is almost entirely reconstructable from composition, or within-cell state shifts do not reproduce bulk organization | CGGA CCell_4083 has multi-layer + scRNA potential but exact intersections are incomplete; IDH dual-capture offers same-nucleus methylation/RNA | source qualification may answer much of this without new wet-lab work; new experiment is valuable only if exact matched layers/order remain unavailable |
| EXP-R7 | Does within-patient tumor progression preserve, reorganize, or bifurcate cross-layer regulatory architecture? | serial tumor sampling with exact patient pairing and joint or tightly matched RNA/substrate measurements | primary/recurrent ordered specimens; RNA; methylation/ATAC; clinical/treatment interval; hierarchical patient structure | patient-specific trajectories diverge so strongly that a shared transition/state law is not identifiable; bulk result disappears under within-patient analysis | 2026 IDH dual-capture source provides 15 longitudinal patients and joint single-nucleus methylation/RNA; CARE provides another longitudinal multiomic family | likely a literature-first/computational opportunity before new collection; residual experiment need depends on treatment metadata and representation transport |
| EXP-R8 | Does a state coordinate learned in one perturbation family retain meaning under a mechanistically different perturbation? | freeze state construction on one treatment/system, then apply unchanged to a second perturbation with independent phenotype | matched molecular time courses for two perturbation classes; independent phenotype; no retuning | coordinate ordering or meaning reverses/vanishes; refusal rate becomes dominant; mode identities reorganize completely | no current source in the qualified set provides an untouched mechanistically distinct perturbation under the same frozen GRI coordinate | potentially high-value future experiment, but only after a representation survives current admission work |
| EXP-R9 | Can a scalar be shown to be unnecessary rather than merely unavailable? | predeclare scalar and distributed representations, then test whether system-level decisions/transport remain identifiable when scalar compression refuses | time-resolved molecular data; independent endpoint; formal refusal outputs; complexity-matched evaluation | distributed representation adds no transport/identifiability or its advantage is only extra capacity | B3 compact refusal plus current G2/modal architecture motivates the question but does not answer it prospectively | establishes a legitimate experimental route for `NO_COHERENT_LOW_DIMENSIONAL_STATE` as a positive architectural result rather than a fallback |
| EXP-R10 | What aspects of apparent recovery are inherited from substrate state? | perturb-and-release with RNA plus slower substrate measurement before perturbation, at peak response, and through recovery | RNA densely sampled; methylation/ATAC at fewer predeclared anchor times; phenotype; clone/lineage control if possible | RNA recovery is independent of measured substrate history or substrate state has no reproducible relation to recovery path | current SCC25 chronic methylation/RNA is continued-exposure and therefore cannot isolate substrate inheritance during recovery | remains a genuinely new wet-lab opportunity unless a matched washout multiomic dataset is found |

## Minimal experiment architecture that should survive across future choices

Regardless of which residual question is eventually selected, the experiment should preserve several design features:

1. **Independent phenotype or physical readout.** Do not define the biological transition from the same coordinate later claimed to detect it.
2. **Ordering or perturbation.** Recovery, resilience, temporal inheritance, and transition claims require real ordering rather than cross-sectional pseudo-time.
3. **Replication at the biological unit that supports the claim.** Pooled material may be useful, but it cannot manufacture biological replicate uncertainty.
4. **Refusal as an allowed result.** The analysis must be able to return no coherent scalar, no identifiable restoration, no transport, or representation dependence.
5. **Representation frozen before decisive outcome.** Scalar/modal/system comparisons must not be selected after seeing which one looks best.
6. **Local versus embedded outputs separated.** RNA dynamics, substrate/context, and their relationship should be recorded independently before integration.
7. **Matched controls and explicit intervention timing.** Treatment-only trajectories without time-matched controls can confound ordinary drift with perturbation response.
8. **A release/recovery arm when recovery is the claim.** Continued exposure cannot substitute for washout.

## Existing-source collision summary

The current source audits already collide strongly with several experimental ideas:

- chronic SCC25 answers part of the continued-exposure temporal question and provides paired RNA/methylation plus phenotype;
- short-term SCC25/SCC1 answers part of the fast-response/cross-cell-line question;
- day-5 HNSCC ATAC answers part of the orthogonal substrate/context question;
- IDH dual-capture and CARE answer parts of the within-patient longitudinal multiomic question;
- melanoma MAPKi provides another ordered acquired-resistance family;
- CGGA provides a potential composition/protein/substrate cross-layer system if exact modality overlap is reconstructed.

Therefore the strongest reason for a new wet-lab experiment is **not** “we need another cancer dataset.” It is to measure a variable the existing sources structurally cannot identify, especially restoration/degradation, perturbation release/recovery, or a prospectively untouched transport test after a representation is frozen.

## What is not frozen here

This document deliberately does not choose:

- cell line or cancer type;
- drug or dose;
- sample count;
- time grid;
- transcriptomic state basis;
- scalar formula;
- operator dimension;
- regularization family;
- restoration model;
- response threshold;
- confirmatory endpoint;
- winning experiment.

Those are scientific design choices. This matrix narrows why an experiment would be worth doing without letting current results choose the answer in advance.
