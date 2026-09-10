# Stage D Checkpoint Policy v0.1

Heavy Stage-D jobs must be restart-safe.

Required checkpoint boundaries:
- source download complete + hashes verified;
- sample manifest normalized;
- each assay matrix normalized/transformed;
- each dataset-layer feature universe frozen/materialized;
- each cancer/condition or experiment block completed;
- each null/permutation batch completed;
- each model family completed;
- each final compact summary generated.

Checkpoint identity must include:
- GitHub commit SHA;
- config hashes;
- source file hashes;
- random-seed namespace;
- software environment identity.

A checkpoint with mismatching science/config/source identity must be refused rather than silently resumed.
