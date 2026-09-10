# Stage D Backend Equivalence Rule v0.1

Kaggle, PowerCell, and GitHub are execution environments only.

A result is backend-equivalent only if:
- the same GitHub commit is used;
- the same config hashes are used;
- source file hashes are identical;
- deterministic seeds/namespaces match;
- floating-point differences remain within a predeclared numerical tolerance;
- no backend-specific preprocessing or scientific branch exists.

If equivalent runs disagree beyond tolerance, the result is held until the discrepancy is explained. No backend is chosen because it gives the favorable biological result.
