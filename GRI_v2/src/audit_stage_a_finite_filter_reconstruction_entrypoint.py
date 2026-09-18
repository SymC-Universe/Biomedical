from __future__ import annotations

"""Mechanical compatibility entrypoint for the Stage A finite-filter audit.

The frozen Stage C1 JSON stores the Hallmark SHA and download URLs at the
configuration root, while the audit helper originally looked for an obsolete
``inputs`` nesting.  This adapter changes no thresholds, sample rules, hashes,
or analysis logic.  It only presents those same frozen fields in the shape the
existing helper expects.
"""

from src import audit_stage_a_finite_filter_reconstruction as audit


_original_get_hallmark_gmt = audit.get_hallmark_gmt


def _get_hallmark_gmt_compat(cfg, path):
    if "inputs" in cfg:
        return _original_get_hallmark_gmt(cfg, path)
    adapted = {
        "inputs": {
            "hallmark_membership_sha256": cfg["hallmark_membership_sha256"],
            "hallmark_download_urls": cfg["hallmark_download_urls"],
        }
    }
    return _original_get_hallmark_gmt(adapted, path)


audit.get_hallmark_gmt = _get_hallmark_gmt_compat


if __name__ == "__main__":
    audit.main()
