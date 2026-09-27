# NSD Finite-Sample Structural-Order Literature Control v0.1

Status: LITERATURE CONTROL / NO THRESHOLD FREEZE
Date: 27 September 2026
Authority: GOM v0.8.6

The failed combined refusal map is consistent with established system-identification literature: noise makes empirical Hankel matrices effectively full rank, so raw singular-value magnitude is not a principled finite-data order rule.

Relevant controls:

- [Cam01] directly treats statistical rank testing of Hankel covariance matrices when the blocks are estimated rather than exact.
- [Bar88] identifies minimal stochastic state order from Hankel correlation structure using sampling-distribution information rather than exact rank.
- [Tsi19] provides finite-sample stochastic subspace-identification error bounds and shows estimation uncertainty decays with sample size.
- [Sun25] extends finite-sample stochastic subspace analysis to pole errors and highlights conditioning dependence.
- [Alt25] proposes a split-sample, data-dependent singular-value noise threshold for noisy Hankel order estimation, but its stated setting is Markov-parameter estimation rather than the present autocovariance-Hankel problem.

Program consequence: do not transfer a fixed singular-value cutoff into N-B1. The next structural-order route should be uncertainty-aware and should validate any covariance-Hankel statistical or split-sample construction prospectively on C, D, S, colored extra-pole, and genuine multimode known truths before real EEG.

No paper above licenses a universal biological closure or order threshold.
