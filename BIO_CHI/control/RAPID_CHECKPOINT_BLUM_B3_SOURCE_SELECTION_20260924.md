# Bio Chi rapid checkpoint - Blum B3 source-selected transport route

**Branch:** bio-chi-closure-p0q-20260924
**Active gate:** NF-kB modal conditioning still running. No ERK outcome-bearing analysis opened.

## Publication-defined ERK model selection

Blum et al. 2019 evaluated 12 deterministic candidate FGF2/MAPK topologies.
- Training retained multiple models, with D3 the only candidate stringently reproducing every training feature.
- Held-out pulse validation retained B2, B3, C3, and D3.
- Independent HSPG perturbation then selected **B3** as the only model reproducing that experiment.

Therefore B3 is source-selected and no user/post-result topology choice is required for an independent Bio Chi transport lane.

## Pinned B3 source

Repository: Mijan/LFNS_MSB
Commit: 5c917abda0618d75c00c9cab45f24ed893dd71f1
Tree: cbb79d66f79a84bc8af28ca85f1678295348da83

Files:
- FGF2_models/Fgf_B3/FGF_Model_B3.txt
- FGF2_models/Fgf_B3/config_fgf_sus_3_20.xml
- FGF2_models/Fgf_B3/initial_states_B3.txt
- FGF2_models/Fgf_B3/measurement_FRET_B3.txt

Native model facts:
- type DET
- CVODE ODE simulation
- 15 states
- ERK-to-RAF negative feedback
- competitive joint FGF2/HSPG/FGFR activation
- explicit FRET map through Erk/Erk_star
- source configuration contains publication simulation and likelihood parameter records

## Guard
No B3 eigenvalues, chi_bio, Chi_bio, or Bio Chi quantities have been calculated yet. Transport will open only after the current NF-kB modal qualification closes.
