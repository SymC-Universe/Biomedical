from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.run_tool_prediction_p0_d1_discovery_source import run


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for b in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def make_fixture(tmp: Path, holdout_token: str):
    discovery = [f"TCGA-AA-{i:04d}" for i in range(1, 21)]
    repl = "TCGA-AA-9001"
    final = "TCGA-AA-9002"
    labels = [f"{p}-01A" for p in discovery + [repl, final]]
    source = tmp / f"methylation_{holdout_token}.tsv"
    with source.open("w", encoding="utf-8", newline="") as fh:
        fh.write("probe\t" + "\t".join(labels) + "\n")
        for j in range(1, 21):
            vals = [str(float(i + j)) for i in range(20)]
            if j == 1:
                vals[0] = "NA"
            vals += [holdout_token, holdout_token]
            fh.write(f"cg{j:08d}\t" + "\t".join(vals) + "\n")

    sample = tmp / "p0_sample_eligibility.csv"
    with sample.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "cancer_type",
                "participant_root",
                "methylation_sample_root",
                "partition",
                "finite_primary_probe_count",
                "primary_probe_count",
                "finite_fraction",
                "eligible_primary_95pct",
            ],
        )
        w.writeheader()
        for p in discovery:
            w.writerow(
                {
                    "cancer_type": "TEST",
                    "participant_root": p,
                    "methylation_sample_root": f"{p}-01A",
                    "partition": "DISCOVERY",
                    "finite_primary_probe_count": 20,
                    "primary_probe_count": 20,
                    "finite_fraction": 1,
                    "eligible_primary_95pct": "true",
                }
            )
        for p, part in [(repl, "REPLICATION"), (final, "FINAL_HOLDOUT")]:
            w.writerow(
                {
                    "cancer_type": "TEST",
                    "participant_root": p,
                    "methylation_sample_root": f"{p}-01A",
                    "partition": part,
                    "finite_primary_probe_count": 20,
                    "primary_probe_count": 20,
                    "finite_fraction": 1,
                    "eligible_primary_95pct": "true",
                }
            )

    counts = tmp / "p0_partition_eligibility_counts.csv"
    pd.DataFrame(
        [
            {
                "cancer_type": "TEST",
                "pre_discovery_n": 20,
                "pre_replication_n": 1,
                "pre_final_holdout_n": 1,
                "eligible_discovery_n": 20,
                "eligible_replication_n": 1,
                "eligible_final_holdout_n": 1,
                "fully_evaluable_p0": "true",
            }
        ]
    ).to_csv(counts, index=False)
    summary = tmp / "P0_ELIGIBILITY_SUMMARY.json"
    summary.write_text(
        json.dumps(
            {
                "status": "P0_SAMPLE_ELIGIBILITY_COMPLETE",
                "eligible_records": 22,
                "fully_evaluable_cancer_types": ["TEST"],
                "pan_cancer_promotion_possible_under_p0": False,
            }
        )
        + "\n"
    )

    ann = tmp / "ann.tsv.gz"
    fields = [
        "probe_id",
        "UCSC_RefGene_Name",
        "UCSC_RefGene_Accession",
        "UCSC_RefGene_Group",
        "CpG_rs",
        "SBE_rs",
    ]
    with gzip.open(ann, "wt", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for j in range(1, 21):
            w.writerow(
                {
                    "probe_id": f"cg{j:08d}",
                    "UCSC_RefGene_Name": f"G{j}",
                    "UCSC_RefGene_Accession": f"NM{j}",
                    "UCSC_RefGene_Group": "TSS200" if j <= 12 else "Body",
                    "CpG_rs": "rs1" if j == 12 else "",
                    "SBE_rs": "",
                }
            )
    chen = tmp / "chen.txt"
    chen.write_text("cg00000011\n", encoding="utf-8")
    gmt = tmp / "hallmarks.gmt"
    gmt.write_text(
        "HALLMARK_TEST\ttest\t" + "\t".join(f"G{i}" for i in range(1, 11)) + "\n",
        encoding="utf-8",
    )

    config = tmp / f"config_{holdout_token}.json"
    cfg = {
        "methylation_source": {
            "sha256": sha(source),
            "size_bytes": source.stat().st_size,
            "header_columns": 23,
            "probe_rows": 20,
        },
        "p0_eligibility": {
            "summary_sha256": sha(summary),
            "sample_eligibility_sha256": sha(sample),
            "partition_counts_sha256": sha(counts),
            "eligible_records": 22,
            "records": 22,
            "fully_evaluable_cancers": ["TEST"],
            "eligible_discovery_counts": {"TEST": 20},
            "eligible_discovery_total": 20,
        },
        "c1a_assets": {
            "annotation_export_sha256": sha(ann),
            "chen_ids_sha256": sha(chen),
            "source_annotation_overlap": 20,
            "source_tss200_probe_count": 12,
            "source_chen_overlap": 1,
            "source_common_snp_overlap": 1,
            "source_technical_mask_union": 2,
            "source_masked_remaining": 18,
        },
        "hallmark_membership": {"sha256": sha(gmt), "modules": 1},
        "discovery_probe_rule": {"finite_fraction_min": 0.95},
        "source_representation": {
            "minimum_mapped_genes_per_hallmark": 10,
            "minimum_contributing_probes_per_hallmark": 10,
            "minimum_common_hallmarks_for_later_full_semantic_branch": 1,
        },
        "technical_tracks": ["PRIMARY_PUBLICATION", "MASKED_TECHNICAL"],
        "value_access": {
            "methylation_partitions_allowed": ["DISCOVERY"],
            "replication_methylation_values_allowed": False,
            "final_holdout_methylation_values_allowed": False,
            "rna_expression_values_allowed": False,
            "predictive_target_values_allowed": False,
            "biological_association_allowed": False,
            "biological_chi_allowed": False,
        },
        "claim_ceiling": "synthetic test",
    }
    config.write_text(json.dumps(cfg) + "\n")
    return config, summary, sample, counts, source, ann, chen, gmt


def run_fixture(root: Path, token: str):
    root.mkdir()
    paths = make_fixture(root, token)
    out = root / "out"
    run(*paths, out, chunksize=5)
    return out


def read_gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return fh.read()


def test_end_to_end_discovery_only_and_holdout_invariance(tmp_path: Path):
    a = run_fixture(tmp_path / "a", "HOLDOUT_A")
    b = run_fixture(tmp_path / "b", "HOLDOUT_B")

    assert (a / "p0_d1_hallmark_eligibility.csv").read_text() == (
        b / "p0_d1_hallmark_eligibility.csv"
    ).read_text()
    assert read_gzip_text(a / "p0_d1_probe_eligibility.csv.gz") == read_gzip_text(
        b / "p0_d1_probe_eligibility.csv.gz"
    )
    assert read_gzip_text(a / "p0_d1_methylation_pc1_transforms.csv.gz") == read_gzip_text(
        b / "p0_d1_methylation_pc1_transforms.csv.gz"
    )
    assert read_gzip_text(a / "p0_d1_methylation_discovery_scores.csv.gz") == read_gzip_text(
        b / "p0_d1_methylation_discovery_scores.csv.gz"
    )

    probe = pd.read_csv(a / "p0_d1_probe_eligibility.csv.gz")
    row = probe[(probe.cancer_type == "TEST") & (probe.probe_id == "cg00000001")].iloc[0]
    assert bool(row.retained_primary_95pct)
    assert int(row.finite_n) == 19
    assert abs(float(row.discovery_imputation_median) - 11.0) < 1e-12
    hall = pd.read_csv(a / "p0_d1_hallmark_eligibility.csv")
    assert set(hall.pc1_status) == {"PC1_EVALUABLE"}
