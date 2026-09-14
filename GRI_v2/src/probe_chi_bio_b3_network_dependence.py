from __future__ import annotations

"""Outcome-free B3 network dependence and algebraic-capacity probe.

This probe advances the B3 representation audit without opening any expression
values or selecting a TF panel. It uses only the already-qualified mapped
GSE98812 gene namespace and frozen external CollecTRI/DoRothEA network bytes.

The analysis is deliberately representation-level:
  * determine the regulator universe that independently clears tmin=5 in both
    network resources;
  * quantify target-set dependence using unsigned membership only, so no
    unresolved DoRothEA duplicate/sign aggregation rule is smuggled in;
  * quantify cross-resource signed-pair agreement without resolving ambiguous
    multi-sign pairs;
  * record the exact unregularized D1/D2 algebraic state-dimension ceilings for
    the frozen 20-transition chronic geometry.

It does NOT read SCC25/TCGA expression, score TF activity, choose a panel,
select a state dimension, fit an operator, compute G1/G2, or compute Chi_bio.
"""

from io import BytesIO
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.probe_chi_bio_b3_network_gene_overlap import (
    DOROTHEA_LEVELS,
    TMIN,
    _eligibility,
)
from src.probe_chi_bio_b3_network_symbol_mapping import (
    _download_gse,
    _mapped_gene_universe,
)
from src.probe_chi_bio_collectri_export import (
    _apply_decoupler_220_human_semantics,
    _canonicalize as _canonicalize_collectri,
    _download_exact_source as _download_collectri,
)
from src.probe_chi_bio_dorothea_export import (
    _canonicalize as _canonicalize_dorothea,
    _download_exact_source as _download_dorothea,
    _read_rda,
)


CHRONIC_TRANSITIONS = 20
CHRONIC_LOTO_TRAIN_ROWS = 19
D1_DESIGN_COLUMNS_FORM = "r+2"
D2_DESIGN_COLUMNS_FORM = "2r+2"
D1_MAX_UNREGULARIZED_RANK_LOTO = CHRONIC_LOTO_TRAIN_ROWS - 2
D2_MAX_UNREGULARIZED_RANK_LOTO = (CHRONIC_LOTO_TRAIN_ROWS - 2) // 2


def _membership_summary(
    frame: pd.DataFrame,
    source_col: str,
    target_col: str,
    regulators: list[str],
    mapped_targets: set[str],
) -> dict:
    sub = frame.loc[
        frame[source_col].astype(str).isin(regulators)
        & frame[target_col].astype(str).isin(mapped_targets),
        [source_col, target_col],
    ].drop_duplicates()
    targets = sorted(sub[target_col].astype(str).unique().tolist())
    target_index = {target: idx for idx, target in enumerate(targets)}
    regulator_index = {reg: idx for idx, reg in enumerate(regulators)}
    matrix = np.zeros((len(regulators), len(targets)), dtype=np.float64)
    for source, target in sub.itertuples(index=False, name=None):
        matrix[regulator_index[str(source)], target_index[str(target)]] = 1.0

    singular = np.linalg.svd(matrix, compute_uv=False) if matrix.size else np.asarray([], dtype=float)
    numerical_rank = int(np.linalg.matrix_rank(matrix)) if matrix.size else 0
    nonzero = singular[singular > 0.0]

    intersections = matrix @ matrix.T
    counts = np.diag(intersections)
    unions = counts[:, None] + counts[None, :] - intersections
    with np.errstate(divide="ignore", invalid="ignore"):
        jaccard = np.divide(intersections, unions, out=np.zeros_like(intersections), where=unions > 0)
    tri = jaccard[np.triu_indices(len(regulators), k=1)] if len(regulators) > 1 else np.asarray([])

    row_bytes: dict[bytes, list[str]] = {}
    packed = np.packbits(matrix.astype(np.uint8), axis=1)
    for reg, row in zip(regulators, packed, strict=True):
        row_bytes.setdefault(bytes(row), []).append(reg)
    duplicate_sets = [sorted(group) for group in row_bytes.values() if len(group) > 1]
    duplicate_sets.sort()

    return {
        "regulator_count": len(regulators),
        "measured_target_count": len(targets),
        "unique_source_target_pairs": int(sub.shape[0]),
        "unsigned_membership_matrix_rank": numerical_rank,
        "unsigned_membership_full_row_rank": bool(numerical_rank == len(regulators)),
        "singular_value_max": float(singular[0]) if len(singular) else None,
        "singular_value_min_nonzero": float(nonzero[-1]) if len(nonzero) else None,
        "nonzero_singular_condition_ratio": (
            float(nonzero[0] / nonzero[-1]) if len(nonzero) else None
        ),
        "pairwise_target_jaccard_median": float(np.median(tri)) if len(tri) else None,
        "pairwise_target_jaccard_p95": float(np.quantile(tri, 0.95)) if len(tri) else None,
        "pairwise_target_jaccard_max": float(np.max(tri)) if len(tri) else None,
        "regulator_pairs_jaccard_ge_0_80": int(np.sum(tri >= 0.80)) if len(tri) else 0,
        "regulator_pairs_jaccard_ge_0_90": int(np.sum(tri >= 0.90)) if len(tri) else 0,
        "exact_duplicate_target_set_group_count": len(duplicate_sets),
        "exact_duplicate_target_set_groups": duplicate_sets,
        "note": "Unsigned target membership only; no TF activity or network-weight aggregation is performed.",
    }


def _sign_set(value: float) -> int:
    x = float(value)
    return -1 if x < 0 else (1 if x > 0 else 0)


def _cross_resource_sign_summary(
    collectri: pd.DataFrame,
    dorothea: pd.DataFrame,
    regulators: list[str],
    mapped_targets: set[str],
) -> dict:
    c = collectri.loc[
        collectri["source"].astype(str).isin(regulators)
        & collectri["target"].astype(str).isin(mapped_targets),
        ["source", "target", "weight"],
    ].copy()
    d = dorothea.loc[
        dorothea["tf"].astype(str).isin(regulators)
        & dorothea["target"].astype(str).isin(mapped_targets),
        ["tf", "target", "mor"],
    ].copy()

    c_sets = {
        (str(source), str(target)): frozenset({_sign_set(weight)})
        for source, target, weight in c.itertuples(index=False, name=None)
    }
    d_sets: dict[tuple[str, str], set[int]] = {}
    for source, target, mor in d.itertuples(index=False, name=None):
        d_sets.setdefault((str(source), str(target)), set()).add(_sign_set(mor))

    common = sorted(set(c_sets) & set(d_sets))
    unambiguous_same = 0
    unambiguous_opposite = 0
    ambiguous_dorothea = 0
    zero_involved = 0
    for pair in common:
        cs = c_sets[pair]
        ds = frozenset(d_sets[pair])
        if 0 in cs or 0 in ds:
            zero_involved += 1
        if len(ds) != 1:
            ambiguous_dorothea += 1
        elif cs == ds:
            unambiguous_same += 1
        else:
            unambiguous_opposite += 1

    return {
        "common_source_target_pair_count": len(common),
        "unambiguous_same_sign_pair_count": unambiguous_same,
        "unambiguous_opposite_sign_pair_count": unambiguous_opposite,
        "dorothea_multi_sign_common_pair_count": ambiguous_dorothea,
        "zero_sign_involved_common_pair_count": zero_involved,
        "aggregation_rule_applied": False,
        "note": "Sign sets are inventoried only; ambiguous duplicate DoRothEA pairs are not collapsed or rescued.",
    }


def run_probe(output_dir: Path) -> dict:
    collectri_payload, collectri_history = _download_collectri()
    collectri_raw = pd.read_csv(BytesIO(collectri_payload))
    collectri = _canonicalize_collectri(_apply_decoupler_220_human_semantics(collectri_raw))

    dorothea_payload, dorothea_history = _download_dorothea()
    dorothea = _canonicalize_dorothea(_read_rda(dorothea_payload))
    dorothea_abc = dorothea.loc[dorothea["confidence"].isin(DOROTHEA_LEVELS)].copy()

    gse_payload, gse_history = _download_gse()
    symbols, namespace = _mapped_gene_universe(gse_payload)
    mapped_targets = set(symbols)

    c_eligibility = _eligibility(collectri, "source", "target", mapped_targets)
    d_eligibility = _eligibility(dorothea_abc, "tf", "target", mapped_targets)
    regulators = sorted(
        set(c_eligibility["eligible_sources_tmin5"])
        & set(d_eligibility["eligible_sources_tmin5"])
    )
    if len(regulators) != 249:
        raise RuntimeError(f"frozen B3 eligible-regulator intersection drift: {len(regulators)} != 249")

    result = {
        "status": "PASS_B3_OUTCOME_FREE_NETWORK_DEPENDENCE_AUDIT",
        "eligible_regulator_intersection_count": len(regulators),
        "eligible_regulator_intersection_sha256": hashlib.sha256(
            "\n".join(regulators).encode("utf-8")
        ).hexdigest(),
        "tmin": TMIN,
        "namespace": namespace,
        "collectri_unsigned_dependence": _membership_summary(
            collectri, "source", "target", regulators, mapped_targets
        ),
        "dorothea_abc_unsigned_dependence": _membership_summary(
            dorothea_abc, "tf", "target", regulators, mapped_targets
        ),
        "cross_resource_sign_inventory": _cross_resource_sign_summary(
            collectri, dorothea_abc, regulators, mapped_targets
        ),
        "chronic_unregularized_algebraic_capacity": {
            "transition_rows_full": CHRONIC_TRANSITIONS,
            "transition_rows_per_loto_fit": CHRONIC_LOTO_TRAIN_ROWS,
            "d1_design_columns": D1_DESIGN_COLUMNS_FORM,
            "d2_design_columns": D2_DESIGN_COLUMNS_FORM,
            "d1_max_state_rank_from_row_count_only": D1_MAX_UNREGULARIZED_RANK_LOTO,
            "d2_max_state_rank_from_row_count_only": D2_MAX_UNREGULARIZED_RANK_LOTO,
            "warning": (
                "These are necessary row-count ceilings, not sufficient identifiability and not a selected state dimension. "
                "Conditioning, predictive adequacy, representation stability and scientific semantics remain separate gates."
            ),
        },
        "download_attempt_history": {
            "collectri": collectri_history,
            "dorothea": dorothea_history,
            "gse98812": gse_history,
        },
        "expression_values_opened": False,
        "tf_activity_scored": False,
        "tf_panel_selected": False,
        "state_dimension_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE_PREOUTCOME_REPRESENTATION_AUDIT_ONLY",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "GRI_CHI_BIO_B3_NETWORK_DEPENDENCE.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    result = run_probe(Path("development_outputs/chi_bio_regulon_source/b3_network_dependence_20260913"))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
