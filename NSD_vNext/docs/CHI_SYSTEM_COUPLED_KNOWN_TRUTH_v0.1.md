# NSD joint local-chi / embedded-system known-truth extension v0.1

Date: 22 September 2026  
Status: ACTIVE P0-Q KNOWN-TRUTH EXTENSION  
Program authority: SymC General Operations Manual v0.8.3

## Purpose

GOM v0.8.3 requires the relationship between any licensed local/modal lowercase chi and the broader reconstructed system architecture to be investigated directly.

NSD already had 2x2 first-order fixtures showing that local and embedded stability can differ. This extension makes the relationship explicit in the same native second-order language used for local modal chi.

Each isolated subsystem is:

`q'' + 2*zeta*omega_n*q' + omega_n^2*q = 0`

Thus `zeta_i` is the native modal damping ratio and can correspond to local `chi_i` only where the SymC equivalence is licensed.

The two local oscillators are then embedded into a coupled four-state system. No whole-system chi scalar is defined.

## Frozen exact questions

### CVX-01 / CVX-06: same local chi, same full eigenvalues, different transient behavior

Use identical local oscillators and one-way feed-forward coupling.

Because the full state matrix is block triangular, the coupled and uncoupled systems retain the same full eigenvalues. Coupling nevertheless changes non-normality, reactivity, transient gain and sustained return.

This is a direct falsifier of:
- local damping ratios as a complete system descriptor;
- eigenspectrum alone as a complete transient descriptor.

### CVX-05: same local chi, different embedded modal organization

Hold `omega_n` and `zeta` fixed for both isolated modes, then introduce reciprocal position coupling.

Question:
does the full eigenspectrum reorganize while local modal damping ratios remain unchanged?

### CVX-03: locally stable, globally unstable

Hold both isolated modes stable at `zeta=0.20`, then increase reciprocal coupling beyond the stiffness-stability boundary.

Question:
can locally stable modal chi coexist with an unstable embedded system?

## Native outputs

The Engine records:
- local natural frequencies;
- local damping ratios;
- isolated local poles;
- full-system eigenspectrum;
- spectral abscissa;
- numerical abscissa/reactivity;
- non-normality;
- eigenvector conditioning;
- finite-time maximum propagator gain;
- sustained return time of the induced norm below a fixed known-truth diagnostic threshold.

The return-time threshold is a fixture diagnostic, not a biological boundary.

## Scientific ceiling

These exact fixtures establish only mathematical non-equivalence among:
- local modal damping;
- embedded asymptotic stability;
- transient amplification;
- recovery.

They do not establish which system object best describes human neurophysiology, and they do not license a whole-brain chi.

The forward empirical question remains whether measured neural data contain enough information to identify analogous local and embedded objects reproducibly.
