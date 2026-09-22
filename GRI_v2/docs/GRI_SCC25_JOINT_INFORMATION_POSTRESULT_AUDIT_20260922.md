# GRI SCC25 joint-information P0-D post-result audit

**Date:** 2026-09-22  
**Run:** 35728155463  
**Head:** `ff2efa11a4e951927aaedb51ab49882dbfb7d927`  
**Artifact:** `GRI_SCC25_JOINT_INFORMATION_P0D_V01`, ID `10694192370`  
**Artifact ZIP SHA-256:** `0f9562b04785414c7eb9d2457b0733a0407537e84b6aba60a81b235e6a1df27b`  
**Status:** P0-D POST-RESULT AUDIT  
**Promotion effect:** NONE

## Result

The frozen pilot executed successfully on the exact hash-bound GSE98812 RNA and GSE98813 methylation sources.

Source/representation checks:
- RNA retained genes: 14,767, matching the frozen R1 gate.
- methylation complete CpGs across all 22 paired states: 485,450.
- scalar biological chi was not assumed or computed.
- all four predeclared RNA-rank × methylation-rank pairs completed without numerical refusal.

| RNA rank | methylation rank | conditional improvement | joint transition win fraction | alignment p | frozen P0-D label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 2 | +0.367238 | 0.70 | 0.0487805 | SYSTEM_CONTEXT_ADDS_INFORMATION |
| 2 | 3 | -1.003317 | 0.50 | 0.7317073 | LOCAL_MODAL_SUFFICIENT_FOR_THIS_TASK |
| 3 | 2 | +0.094386 | 0.55 | 0.1463415 | ALIGNMENT_DEPENDENT_UNRESOLVED |
| 3 | 3 | -1.068757 | 0.35 | 0.7439024 | LOCAL_MODAL_SUFFICIENT_FOR_THIS_TASK |

Cross-representation disposition:

`REPRESENTATION_DEPENDENT`

## What this supports

One predeclared low-dimensional representation, RNA rank 2 plus methylation rank 2, showed a substantial held-out error reduction relative to RNA-local/modal information alone and exceeded the predeclared circular alignment screen.

That is a genuine exploratory signal worth explaining.

## What it does not support

The result cannot be summarized as "methylation context conditions RNA stability" without qualification because the conclusion does not survive the coequal rank representations.

In particular:
- adding the third methylation component sharply worsened held-out prediction at both RNA ranks;
- RNA rank 3 plus methylation rank 2 showed only a modest gain and did not clear the frozen alignment screen;
- therefore the effect is representation-sensitive;
- selecting the favorable r=2,m=2 result as the answer would violate the predeclared coequal-representation rule.

No biological scalar chi, causal methylation->RNA mechanism, capital-Chi ontology, or predictive/diagnostic tool claim is earned.

## Main adversarial explanation opened by the result

The current methylation coordinates may encode **trajectory time / resistance progression** rather than a system context that independently conditions local RNA dynamics.

The within-arm circular-shift null attacks exact temporal alignment, but it also destroys clock-time correspondence. Therefore it cannot distinguish:

`methylation context contains extra biological state information`

from

`methylation PCs are a proxy for week/progression time`.

This is now the highest-priority scientific confound.

## Required next challenge

Before any stronger interpretation, compare:

`RNA_next ~ RNA_now + treatment + time + treatment*time`

against:

`RNA_next ~ RNA_now + methylation_now + treatment + time + treatment*time`.

Use the same frozen source, PBS-only bases, rank-pair grid, leave-one-transition-out evaluation, and no retuning. The time-conditioned challenge is retrospective qualification of a post-result vulnerability, not confirmation.

If methylation still adds held-out information beyond explicit time, the system-context interpretation survives one important alternative explanation. If not, the narrower conclusion is that methylation carries trajectory-position information that the local RNA state omitted.

## Additional limitation

There are only 20 transitions, serially related and derived from pooled weekly states. The model remains small-sample. Any result that survives the time challenge still requires a second system and a native multi-view temporal comparator before promotion.
