# Bio Chi C1Q Likelihood-Basin Root-Cause Freeze v1.0

**Status:** APQ-1 QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**Plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_LIKELIHOOD_BASIN_PLAN_v0.1.md\`  
**APQ pass:** \`NSD_vNext/docs/BIO_CHI_C1Q_LIKELIHOOD_BASIN_APQ_PASS_v0.1.md\`

Frozen source:
- Function Map workflow run \`36368579380\`;
- complete artifact \`10948327278\`;
- digest \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`;
- boundary-collapse cells \`0,5,7,8,9,11,12,15\`;
- all 48 rate-level rows in those cells.

Frozen diagnostic:
- generating-coordinate NLL;
- stored-selected-coordinate NLL reproduction;
- one truth-seeded local L-BFGS-B basin;
- one selected-seeded local polish for numerical consistency;
- continuous NLL and parameter displacements;
- no scientific threshold.

Frozen mechanical NLL reproduction tolerance:
\[
10^{-6}\max(1,|\mathrm{NLL}_{artifact}|).
\]

The execution may not modify C1Q, change the source-row set, add an outcome-based cutoff, or promote any estimator. If source reproduction fails, interpretation stops and provenance/mechanical repair takes precedence.
