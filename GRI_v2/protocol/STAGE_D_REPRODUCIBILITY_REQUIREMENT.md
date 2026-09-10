# Stage D Reproducibility Requirement

Every Stage-D package must include a reproducibility guide unless the change is purely cosmetic and cannot affect scientific interpretation, computation, figures, tables, or provenance.

Minimum contents:
- exact source acquisition instructions and hashes;
- exact GitHub branch/commit/config hashes;
- environment/dependency record;
- exact run commands for GitHub/Kaggle/PowerCell as applicable;
- checkpoint/restart instructions;
- expected return artifacts;
- figure/table regeneration commands;
- known limitations and refused branches;
- complete failure/deviation ledger.

Third-party source data are not redistributed merely for convenience. Reproducers obtain them from authoritative sources and verify the frozen identities.
