# Neurostability Atlas v0.1 Source Intake Protocol

Date: 2026-09-11
Status: **A1 SOURCE-SELECTION RULES FROZEN BEFORE COORDINATE POPULATION**
System Model: NSD System Model v1.0
Protocol: General v0.7.1 FINAL + authoritative v0.7.1A

## Purpose

The first Atlas source set is selected to populate and challenge the coordinate ontology without targeting a desired chi value, a desired ordering, a diagnosis effect, or a preferred NSD regime.

A source may enter the intake queue because it can inform a predeclared coordinate family and coverage role. It does not enter because its published result agrees with SymC.

## Inclusion priorities

Priority is given to sources that provide one or more of:

1. open or reproducibly accessible raw EEG/MEG time series;
2. explicit acquisition and condition metadata;
3. repeated recordings or paired physiological/experimental conditions;
4. independently defined transition/event annotations when transition context is needed;
5. sufficient duration/channel count for multichannel dynamical reconstruction;
6. stable version/DOI/source identity;
7. published methodological description allowing provenance reconstruction.

Full-text numerical literature without raw data may also enter when it reports a native coordinate with exact table/text provenance.

## Initial coverage design

The first intake deliberately spans:

- `NOMINAL_FUNCTION`: ordinary healthy resting-state and repeatability;
- `PERTURBED_FUNCTION`: cognitive load and sleep deprivation;
- `BOUNDARY_OR_TRANSITION`: natural sleep/wake transitions and seizure transitions;
- `RARE_NATURAL_LIMIT`: **NOT_YET_QUALIFIED**. No rare case is added merely to complete the four-role table.

Counts need not be equal.

## Source-selection firewall

The following are forbidden as intake criteria:

- published or reconstructed chi being near 1 or any other preferred value;
- published direction of a clinical or physiological group difference;
- agreement with prior NSD/GRI/SymC findings;
- whether an Engine run has already produced an appealing interpretation;
- selecting only systems that are easy for SSI-COV, DMD, or another current estimator;
- selecting an event because the Engine itself marked it as unusual when that same event is later presented as independent validation.

## Native-first extraction

For each source, extraction proceeds in this order:

1. source identity/version and population/context;
2. acquisition and preprocessing provenance;
3. source-native model/coordinates;
4. raw-data reconstruction where licensed;
5. exact algebraic/unit conversions;
6. model-conditional derived coordinates only after assumptions are checked;
7. chi last, and only if an independently supported second-order factorization licenses it.

No derived coordinate is used to repair missing native provenance.

## Cohort and analysis counts

Atlas records must distinguish:

- total recruited/published cohort;
- source files/participants actually present in the data release;
- participants/records passing Atlas preprocessing;
- participants/records contributing to a specific coordinate;
- any secondary-paper analyzed subset.

Conflicting source summaries are recorded as discrepancies until reconciled. A single convenient `N` may not replace these distinctions.

## Transition labels

Externally supplied labels such as sleep stages or seizure onset may be used to define Atlas context. Their use creates pathway-specific dependence.

If a label is used to locate the interval whose Engine behavior is then assessed, `outcome_label_independence` for that validation pathway is not independent. This does not make the raw signal unusable; it limits the claim that can be made from the labeled comparison.

A later independent transition-detection claim must use a design in which event eligibility/selection and decisive detection evidence are separated prospectively.

## Preprocessing rule

The Atlas does not impose one universal preprocessing pipeline before source inspection. Instead, each reconstruction pipeline must:

- preserve raw-source identity;
- record every transformation;
- distinguish source-provided cleaned derivatives from Atlas-generated preprocessing;
- define channel exclusions and missing channels;
- avoid diagnosis/outcome-informed cleaning rules;
- preserve enough information to reproduce the coordinate from raw or pinned derivative data.

Any preprocessing choice selected after seeing a coordinate effect is P0-D and carries promotion debt.

## Evidence-tier promotion

A source is not Tier A merely because raw data are downloadable.

`A_FULL_NUMERIC_PROVENANCE` requires a complete path from pinned source bytes or exact source table/text to the coordinate value, including code/derivation and context.

`B_FULL_METHOD_PARTIAL_NUMERIC` may support method/context structure but not decisive numerical coordinates when the exact numeric path is incomplete.

`C_ABSTRACT_OR_SNIPPET_ONLY` and `D_SOURCE_EXISTS_BLOCKED` are discovery records only.

`E_REJECTED_FOR_ATLAS` preserves exclusion reasons.

## Independence grading

For every Atlas entry, grade independently:

- data;
- cohort/system;
- outcome/label;
- parameter/tuning;
- method/estimator;
- Atlas/Engine;
- source/literature;
- temporal decisive evidence.

No overall `independent=true` field is permitted.

## First-pass source set

The initial queue contains deliberately different evidence contexts rather than several near-duplicate healthy rest datasets:

- LEMON / MPI Leipzig Mind-Brain-Body resting EEG;
- SRM Resting-state EEG;
- Dortmund Vital Study pre/post cognitive activity resting EEG;
- sleep-deprivation resting EEG dataset;
- simultaneous EEG/fMRI sleep dataset with sleep/wake stages;
- CHB-MIT long-term scalp EEG with seizure annotations.

Additional sources may be added by the same frozen intake criteria. New sources do not change the coordinate definitions merely because they expose a new value range.
