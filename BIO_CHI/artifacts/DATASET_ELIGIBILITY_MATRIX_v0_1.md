# Bio Chi P0-D dataset eligibility matrix v0.1

**Date:** 22 September 2026  
**Status:** ACTIVE / SOURCE QUALIFICATION IN PROGRESS  
**Purpose:** select testbeds by design quality and falsifiability rather than agreement with SymC expectations.

Legend: **YES** directly supported; **PARTIAL** supported but sparse/indirect; **NO** absent; **TBD** requires source/data verification.

| Testbed | Domain role | Baseline/reference | Defined perturbation | Removal/recovery | Repeated post-removal observations | Hysteresis/rechallenge | Lineage/carrier | Substrate/chromatin | Native functional endpoint | Public quantitative data | Initial disposition |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sharma et al. Cell 2010, PC9 DTP/DTEP | cancer recovery | YES | YES | YES | YES, passages/doublings | PARTIAL, resensitization/rechallenge | PARTIAL | YES, KDM5A/H3K4 | YES, drug sensitivity/apoptosis | PARTIAL/TBD raw data | **A: cancer recovery candidate** |
| Shaffer et al. Nature 2017, melanoma | recovery -> stable reorganization boundary | YES | YES | YES | PARTIAL | YES, 1-week reversion + 3-week drug holiday | YES, clonal/live-cell | YES, ATAC/transcriptional state | YES, colony resistance | YES, GSE97682 + SRA SRP103406 | **A: boundary candidate** |
| Harmange et al. Nat Commun 2023, scMemorySeq | memory/carrier intervention | YES | YES | YES pretreatment washout | PARTIAL | YES, later targeted-therapy challenge | **YES, barcode lineages** | YES, ATAC/state | YES, resistant colonies | YES, GSE237228 | **A: inheritance/memory candidate** |
| Rehman et al. Cell 2021, CRC diapause-like DTP | in vivo cancer recovery | YES | YES, multi-agent chemo | **YES** | **YES**, regrowth after cessation | **YES**, regrowth-derived tumors rechallenged | **YES**, ~2.6M lentiviral barcodes | PARTIAL, regulatory/metabolic rather than direct chromatin | **YES**, growth, Ki67, sensitivity | **YES**, GSE145356; WES EGAS00001004773 | **A: strongest recovery/rechallenge candidate** |
| Marsolier et al. Nat Genet 2022, TNBC H3K27me3 | substrate/carrier intervention | YES | YES | PARTIAL, recurrence/retreatment rather than dense washout | PARTIAL | YES, recurrence/retreatment | **YES**, barcodes + single-cell | **YES**, H3K27me3/H3K4me3, intervention | YES, persistence/recurrence | **YES**, GSE164716 + public code | **A: strongest substrate-inheritance candidate** |
| Su et al. sequential waves / NF-kB remodeling | hysteresis/reorganization | YES | YES, BRAFi | **YES**, drug removed at D29 | **YES**, DR4-DR35 | **YES**, non-overlapping forward/reverse path + rechallenge | PARTIAL | **YES**, ATAC/ChIP | YES, drug-tolerant/reversible state | TBD exact accession | **A: strongest hysteresis candidate** |
| Lee et al. PNAS 2014, paclitaxel tolerance | sparse recovery | YES | YES | YES | PARTIAL, sparse single-cell | YES, re-exposure hypersensitivity | NO explicit lineage | PARTIAL | YES, IC50/state | YES, SRA SRP040309 | **B: secondary recovery candidate** |
| Jiang et al. Sci Signal 2020, yeast stress memory | known-truth recovery/memory | YES | YES, controlled prime | **YES**, variable break | **YES**, dense 2-min imaging | **YES**, secondary challenge/repeated inputs | NO lineage needed | PARTIAL, mechanistic memory carriers | **YES**, Hog1 recovery/memory metric | TBD exact data package | **A: qualification candidate** |
| McFarland et al. Nat Commun 2020, MIX-Seq | response-only control | YES | YES | **NO** | NO | NO | NO | NO | YES, transcription/viability | YES, Figshare + code | **C: must refuse recovery claims** |
| Srivatsan et al. Science 2020, sci-Plex | response-surface control | YES | YES | **NO** | NO | NO | NO | NO | transcriptional response | YES, GSE139944 + code | **C: must refuse recovery claims** |
| Son et al. Sci Signal 2021, NF-kB | scalar/modal signaling candidate | YES | YES, dynamic TNF/IL-1β | PARTIAL, dynamic inputs/refractory behavior | YES dense 5-min traces | PARTIAL | reporter-defined state | feedback-state, not chromatin | NF-kB dynamics | PARTIAL, traces on request | **B: χ_bio candidate, data-access risk** |
| Jaruszewicz-Błońska et al., identifiable NF-kB model | scalar-model qualification | YES model steady state | YES, 2h TNF + 10h washout protocol | **YES by protocol/model** | YES simulated/experimental design | PARTIAL | six-state model | NO | dynamic adaptation/oscillation | YES code as supplement; exact raw data TBD | **A/B: strongest χ_bio model candidate** |
| Geva-Zatorsky et al. MSB 2006, p53/Mdm2 | scalar limit case | YES | YES, gamma irradiation | NO finite-removal recovery in primary design | long time series | NO | single-cell dynamics | NO | p53/Mdm2 oscillations | PARTIAL, supplementary movies | **B/C: useful limit case, not recovery** |
| Blum et al. MAPK/ERK 2019 | modal/network identification | YES | YES, controlled GF pulses | **YES**, washout/rebound | YES | YES multi-pulse/frequency response | reporter-defined | NO | ERK dynamics | PARTIAL: model/code public, raw data audit TBD | **A/B: modal identification candidate** |

## Current ranking by question

### Recovery / reorganization
1. **Rehman 2021** — strongest complete cancer treatment -> DTP -> withdrawal -> regrowth -> rechallenge chain.
2. **Su sequential-waves melanoma** — strongest time-resolved hysteresis/reverse-path architecture.
3. **Sharma 2010** — clean historical reversibility with chromatin-linked resensitization.
4. **Shaffer 2017** — especially valuable because transient pre-resistance and later stable resistance separate recoverable from reorganized states.
5. **Lee 2014** — useful but sparse.

### Stability Inheritance / substrate
1. **Marsolier 2022** — pre-existing H3K27me3 state, lineages, chromatin intervention, persistence outcome.
2. **Harmange 2023** — lineage-resolved memory and intervention.
3. **Su sequential-waves** — chromatin remodeling plus forward/reverse path.
4. **Sharma 2010** — mechanistically suggestive but older/sparser.

### χ_bio scalar discovery
1. **Identifiable NF-kB reduced model** — strongest model-identifiability route; local complex poles can be tested without calling them mechanical damping by default.
2. **ERK temporal perturbation** — strong system identification and washout/rebound, probably more naturally modal/transfer-function than scalar.
3. **p53/Mdm2** — valuable adversarial case because single-cell oscillations are often sustained and population damping can be a synchronization artifact.
4. **Son 2021 NF-kB differentiator** — dense trajectories but the native mechanism is multi-state and may refuse one-pair compression.

## Immediate source-qualification tasks

- verify exact accession/file identities and download paths for Rehman, Marsolier, Harmange, Shaffer, Lee, and any Su dataset;
- verify whether Jiang raw single-cell traces are downloadable or only figure/supplement level;
- verify raw-data access for the identifiable NF-kB model and ERK experiments;
- record licenses and redistribution constraints;
- record exact native comparator/model used by each study;
- identify which datasets can be analyzed entirely from public files without author request.

## Gate rule

A testbed may be scientifically interesting yet still be rejected for execution if source identity, time ordering, recovery definition, or quantitative data access cannot be frozen cleanly.

No favorable biological result can upgrade a testbed retrospectively.
