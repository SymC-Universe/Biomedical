# HOG1 input-context Bio Chi qualification freeze v0.1

**Date:** 25 September 2026  
**Branch:** `bio-chi-hog1-input-context-p0q-20260925`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC RESULT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q source-native model qualification

## Biological system and source

The test uses the source-released four-node HOG signaling Model 3 and source parameter object from Jashnsaz et al. The source repository is `neuertlab/Jashnsaz_STARProtocols_2021`. Model 3 is explicitly designated the true model in the source simulation workflow and is driven by time-varying NaCl input profiles.

Pinned source identities:

- `Jashnsaz_et_al_dir01_Models/get_models.m`: blob `a31de158ff7474648c0d48a2994eaa25b10cc610`
- `Jashnsaz_et_al_dir02_simData/Get_ODE.m`: blob `1ede4299ec77dc8cfffeec8381b7ae2ccf4b205b`
- `Jashnsaz_et_al_dir02_simData/get_simData.m`: blob `8a2a99b8a1193fc35a86437c251b17d8e82cad03`
- `Jashnsaz_et_al_dir02_simData/Models_and_TrueParams/FP_OBJ_FIM.mat`: blob `7b152c6aa33018970dcd689244864fcb595f1f52`

## Frozen question

For the same four-node HOG network and source parameterization, does changing only the temporal shape of the NaCl input alter realized Hog1 response organization enough that no single local scalar can represent the whole response family?

The system is held fixed. The perturbation context is the input trajectory.

## Frozen input family

At final NaCl concentration 0.3 M, compare six source-defined input kinetics used in the source workflow:

1. step, (t^0)
2. root2, (t^{1/2})
3. linear, (t^1)
4. quadratic, (t^2)
5. quintic, (t^5)
6. heptic, (t^7)

Treatment horizon is 50 minutes, ramp completion time 25 minutes, source initial state is ([0.05,0.05,0.05,0]), and basal parameter is 0.1.

## Representation hierarchy

- **Bio Chi:** realized relation between a fixed HOG network, temporal input context, and the Hog1 output trajectory.
- **Chi_bio:** candidate response-organization vector ((peak, time\_to\_peak, AUC, endpoint, postpeak\_return)), reduced only if redundancy supports it.
- **chi_bio:** not licensed at freeze. A scalar may be considered only if a source-native local dynamical reduction is independently identifiable and then passes the whole-event transport test.

## Frozen tests

1. Reproduce the six source-native deterministic trajectories at 0.3 M using the released Model 3 equations and source parameters.
2. Extract the five response-organization coordinates without retuning.
3. Standardize coordinates across the six contexts and test intrinsic rank by singular values of the centered six-by-five representation matrix.
4. A one-dimensional compression is considered adequate only if PC1 explains at least 95 percent of variance **and** each original coordinate is reconstructed with maximum normalized absolute residual at or below 0.10.
5. If one-dimensional adequacy fails, the scalar-compression route is refused for this whole event.
6. Independently compute the local Jacobian spectrum at each context's final state. Any scalar built from a complex pair is descriptive only unless the same mode can be tracked across all six contexts and the scalar predicts the frozen response-organization ordering without retuning.
7. Failure of source reproduction, parameter extraction, or a stable same-mode carrier is preserved as a refusal or source/model limitation, not repaired by selecting a convenient mode post hoc.

## Claim ceiling

This is a source-native model qualification, not experimental biological validation and not a general HOG law. Its role is to test context dependence and representation adequacy in a biologically motivated signaling model under a fixed network and parameterization.
