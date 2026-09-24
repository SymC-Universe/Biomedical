# Bio Chi rapid checkpoint - protocol-regime audit

**Branch:** bio-chi-closure-p0q-20260924

## Source-native pulse audit
Published native-output figure mapping is preserved in source order.

- Figure 1: TR=1 from 1 h to 10 h, then off.
- Figure 2: three 5 min pulses beginning at 1 h, 2 h, 3 h.
- Figure 3: three 5 min pulses beginning at 1 h, 2.6667 h, 4.3333 h.
- Figure 4: three 5 min pulses beginning at 1 h, 4.3333 h, 7.6667 h.
- Figure 5: three 22.5 min pulses beginning at 1 h, 1.75 h, 2.5 h.
- Figure 6: three 45 min pulses beginning at 1 h, 2.5 h, 4 h.
- Figure 7: one 2 h pulse from 1 h to 3 h.

## Scientific disposition
The previously discovered candidate chi_bio ~= 0.2131 is derived from the nominal stimulated TR=1 equilibrium generator. Figures 2-7 alternate between TR=1 and TR=0 and therefore are not treated as clean independent ringdown tests of that TR=1 local pole. No mixed-regime comparison will be used to promote chi_bio.

This is a Limit Map result, not a blocker.

## Next safe gate
Qualify the generator-derived two-dimensional real invariant factor itself:
- derive the second-order factor from the unique complex-conjugate pair;
- compute chi_bio = -Re(lambda)/|lambda| for all frozen Jacobian steps;
- quantify numerical spread;
- preserve negative chi for locally amplifying B/C pairs rather than forcing a 0-to-1 scale;
- compare the scalar compression against the full native pole pair and record information loss;
- make no chi=1 biological boundary claim.

No user intervention required.
