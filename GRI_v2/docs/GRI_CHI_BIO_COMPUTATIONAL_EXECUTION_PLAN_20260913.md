# GRI Chi_bio computational execution plan

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Scientific architecture:** G1-S1-L3 + approved A3/B3/C3  
**Chi_bio:** `NOT_ADMITTED`

## 1. Executive compute assessment

The immediate temporal work is **not compute-limited**. It is identifiability-limited.

The first SCC25 G2 analysis uses only 11 short-term states and 22 chronic main-trajectory states after loading transcript-scale source tables. PCA to `r=2/3`, fitting 2x2/3x3 operators, leave-one-transition diagnostics and hundreds or thousands of synthetic/resampling fits are ordinary laptop CPU work.

The later TCGA transport stage is the first point where memory architecture matters.

No currently justified stage requires a GPU.

## 2. Phase C0: CI / mathematical qualification

### Work

- contracts and regression tests;
- G1/G2 known-truth harnesses;
- A3 rank-robust synthetic pilots;
- treatment-interaction synthetic calibration;
- source/provenance validators.

### Compute

```text
CPU:     1-4 cores sufficient
RAM:     <2 GB expected for the scientific payload
GPU:     none
runtime: seconds to a few minutes
```

GitHub Actions is appropriate for this layer because no protected/local molecular archive is required.

## 3. Phase C1: SCC25 short-term G2 pilot

Frozen processed bulk source:

```text
GSE114446_STCCountsCG.txt.gz
~56,470 genes x 33 sample columns overall
11 SCC25 states used by the first design
```

### Work

1. verify source hash and exact SCC25 columns;
2. apply frozen count transformation;
3. apply frozen feature rule;
4. fit PBS-only PCA basis at `r=2` and `r=3`;
5. project CTX states without refitting;
6. build frozen transition pairs;
7. fit the frozen G2 operator model;
8. calculate spectral and non-normal diagnostics;
9. execute A3 cross-rank agreement and leave-one-transition stability checks;
10. package full provenance and refusal state.

### Compute

```text
CPU:     ordinary laptop
RAM:     <1-2 GB practical working requirement
GPU:     none
runtime: seconds to minutes for one deterministic pass
          minutes for broad synthetic/resampling diagnostics
```

The matrix has many genes but almost no samples. SVD/PCA can be performed through the small sample-space geometry without constructing a large covariance matrix.

## 4. Phase C2: chronic SCC25 transport

Main trajectory:

```text
11 PBS weeks + 11 CTX weeks = 22 states
10 one-step transitions per arm
```

### Work

- same frozen representation discipline;
- weekly operator fit;
- interval/transport audit against daily source;
- local-vs-embedded comparison;
- methylation retained as substrate/context rather than concatenated into the transcriptomic state;
- proliferation/resistant-clone/ATAC/scRNA endpoints remain post-construction tests.

### Compute

Still laptop-scale. Memory and runtime are negligible relative to historical Stage C1.

## 5. Phase C3: B3 regulon qualification

Candidate signed interaction resources contain only tens of thousands of edges, not a dense genome-by-genome matrix.

### Work

- obtain exact CollecTRI and DoRothEA exports;
- byte-hash and inventory schema/sign/evidence metadata;
- map identifiers to SCC25/TCGA expression identifiers;
- quantify duplicate/conflicting edges;
- score candidate regulatory coordinates only after the state-scoring rule is frozen;
- run matched synthetic identifiability tests before empirical G1 state use.

### Compute

```text
CPU:     trivial to modest
RAM:     usually <2-4 GB
GPU:     none
runtime: seconds to minutes at SCC25 scale
```

Provenance and representation choice are far harder than the arithmetic.

## 6. Phase C4: later TCGA/C1 transport

The frozen C1 RNA state is approximately:

```text
9,457 samples x 22,601 genes
= 213,737,657 float values
```

At float64 this is:

```text
~1.71 GB decimal
~1.59 GiB binary
```

A second dense matrix of the same shape doubles that before any temporary arrays, dataframe overhead, decompression, resampling or score matrices are created.

### Recommended machine envelope

```text
RAM minimum:       16 GB, only with mmap/chunking and disciplined copies
RAM recommended:   32 GB
RAM comfortable:   64 GB if parallel resampling is desired
CPU:               modern 8-16 logical threads is ample
GPU:               not required
storage headroom:  20-50 GB for current processed workflow
SSD:               strongly preferred
```

If raw sequencing is deliberately reprocessed later, storage and runtime move into a different class and should be budgeted separately.

## 7. Required memory architecture for TCGA

Do not repeatedly materialize transcriptome-scale copies.

Preferred pattern:

```text
read-only/memmap source
-> chunk samples or genes
-> compute compact fixed regulon/module coordinates
-> persist compact score matrix
-> perform downstream resampling in compact state space
```

Avoid:

- dense gene x TF weight matrices when the regulon graph is sparse;
- per-bootstrap copies of the full RNA matrix;
- loading RNA + methylation + multiple transformed copies into RAM merely for convenience;
- DataFrame conversions of large numeric arrays when ndarray/memmap is sufficient.

The post-reduction matrices should be tiny compared with the C1 transcriptome source.

## 8. Expected scaling of repeated fits

Once the state is `r=2/3`, a transition fit is microscopic. Even thousands of refits are cheap.

Therefore resampling should be structured so that expensive transcriptomic preprocessing is performed **once** under the frozen representation, followed by compact-state resampling.

Expected order:

```text
source validation / transform        once
fixed-state score construction       once
compact-state transition fitting     cheap repeated operation
A3 / LOTO / perturbation checks      cheap repeated operation
later per-cancer compact mapping      moderate
large bootstrap grid                 CPU-parallel but not HPC-class
```

## 9. What could make compute materially larger

Only a few scientifically optional choices would substantially increase resource requirements:

1. reprocessing GSE114446/GSE98812 from raw FASTQ instead of frozen processed tables;
2. adopting a high-dimensional nonlinear latent model instead of the current low-order operator program;
3. thousands of full-transcriptome bootstrap reconstructions rather than compact-state resampling;
4. raw methylation reprocessing across large cohorts;
5. broad hyperparameter/model-family searches, which the protocol would treat as additional multiplicity/model-selection debt anyway.

None is currently required for the first legitimate G2 test.

## 10. Software stack

Current repo requirements are intentionally small:

```text
numpy
pandas
statsmodels
pytest
```

Current G2 PCA/operator mechanics use NumPy directly and do not require scikit-learn or CUDA.

Potential additional tools only if scientifically selected:

- R/Bioconductor DESeq2 if VST becomes the frozen count transformation;
- edgeR if TMM/log-CPM becomes the frozen transformation;
- decoupler/OmniPath-compatible tooling for a frozen CollecTRI/DoRothEA export or activity method;
- scipy sparse operations if later regulon scoring benefits from sparse matrices.

Package/version hashes should be frozen at empirical execution.

## 11. Cloud/HPC decision

### Not needed now

SCC25 G2 + B3 qualification should stay local/CI-scale. Moving it to cloud/HPC would add orchestration and provenance complexity without scientific benefit.

### Potentially useful later

A cloud/workstation CPU run becomes useful only for:

- large per-cancer resampling grids;
- parallel representation sensitivities;
- raw sequencing reconstruction;
- large external P1 cohorts.

Even then, CPU and memory matter much more than GPU acceleration.

## 12. Practical recommendation

For the current program:

```text
SCC25 stage: use the existing laptop
TCGA transport: 32 GB RAM target if available
16 GB machine: still feasible with mmap/chunking
GPU purchase/cloud GPU: unnecessary
fast SSD + power stability: more useful than a GPU
```

The architecture should be written so the scientific result is identical whether run on the laptop or a larger CPU machine.
