from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional

import numpy as np
import pandas as pd

BLOCKS = ("R", "S", "E", "G", "P", "M", "T", "Q")
BLOCK_DESCRIPTIONS = {
    "R": "RNA/regulatory organization",
    "S": "methylation/substrate organization",
    "E": "embedding/context and measured composition",
    "G": "genomic context/constraints",
    "P": "protein/phosphoprotein coupling",
    "M": "modal/vector organization",
    "T": "temporal/operator behavior",
    "Q": "uncertainty/robustness/identifiability metadata",
}


@dataclass(frozen=True)
class BlockProfile:
    values: pd.DataFrame
    evidence_class: str = "UNSPECIFIED"
    source: str = "UNSPECIFIED"


def _standardize(frame: pd.DataFrame) -> pd.DataFrame:
    x = frame.astype(float).copy()
    mu = x.mean(axis=0)
    sd = x.std(axis=0, ddof=0).replace(0.0, np.nan)
    z = (x - mu) / sd
    return z.fillna(0.0)


def _row_geometry(frame: pd.DataFrame) -> np.ndarray:
    z = _standardize(frame).to_numpy(dtype=float)
    if z.shape[1] == 0:
        return np.full((z.shape[0], z.shape[0]), np.nan)
    norms = np.linalg.norm(z, axis=1)
    denom = np.outer(norms, norms)
    sim = z @ z.T
    out = np.zeros_like(sim, dtype=float)
    np.divide(sim, denom, out=out, where=denom > 0)
    return np.clip(out, -1.0, 1.0)


class ConglomerateChiV01:
    """Non-compressive carrier for capital-Chi biological architecture."""

    def __init__(self, sample_ids: Iterable[str], blocks: Mapping[str, Optional[BlockProfile]]):
        self.sample_ids = tuple(str(x) for x in sample_ids)
        unknown = set(blocks) - set(BLOCKS)
        if unknown:
            raise ValueError(f"unknown blocks: {sorted(unknown)}")
        self.blocks: Dict[str, Optional[BlockProfile]] = {b: blocks.get(b) for b in BLOCKS}
        self._validate()

    def _validate(self) -> None:
        if len(set(self.sample_ids)) != len(self.sample_ids):
            raise ValueError("sample_ids must be unique")
        for name, block in self.blocks.items():
            if block is None:
                continue
            frame = block.values
            if tuple(map(str, frame.index)) != self.sample_ids:
                raise ValueError(f"{name}: row identity/order does not match carrier sample_ids")
            if frame.columns.duplicated().any():
                raise ValueError(f"{name}: duplicate feature names")
            if frame.shape[1] == 0:
                raise ValueError(f"{name}: present block has zero features")

    def present_blocks(self):
        return tuple(b for b in BLOCKS if self.blocks[b] is not None)

    def missing_blocks(self):
        return tuple(b for b in BLOCKS if self.blocks[b] is None)

    def standardized_blocks(self) -> Dict[str, pd.DataFrame]:
        return {b: _standardize(self.blocks[b].values) for b in self.present_blocks()}

    def block_geometries(self) -> Dict[str, np.ndarray]:
        return {b: _row_geometry(self.blocks[b].values) for b in self.present_blocks()}

    def geometry_concordance(self) -> pd.DataFrame:
        names = self.present_blocks()
        out = pd.DataFrame(np.nan, index=names, columns=names, dtype=float)
        geoms = self.block_geometries()
        tri = np.triu_indices(len(self.sample_ids), k=1)
        for a in names:
            xa = geoms[a][tri]
            for b in names:
                xb = geoms[b][tri]
                if xa.size == 0 or np.std(xa) == 0 or np.std(xb) == 0:
                    val = np.nan
                else:
                    val = float(np.corrcoef(xa, xb)[0, 1])
                out.loc[a, b] = val
        return out

    def leave_one_block_out(self) -> Dict[str, dict]:
        present = self.present_blocks()
        return {
            removed: {
                "removed": removed,
                "remaining_blocks": [b for b in present if b != removed],
                "scalar_output_created": False,
            }
            for removed in present
        }

    def manifest(self) -> dict:
        return {
            "schema": "GRI_CHI_BIO_CONGLOMERATE_V01",
            "sample_count": len(self.sample_ids),
            "present_blocks": list(self.present_blocks()),
            "missing_blocks": list(self.missing_blocks()),
            "block_descriptions": BLOCK_DESCRIPTIONS,
            "universal_scalar_required": False,
            "damped_oscillator_assumed": False,
            "unity_boundary_assumed": False,
            "scalar_chi_bio_value": None,
        }


def synthetic_demo(outdir: Path) -> None:
    rng = np.random.default_rng(20260918)
    n = 96
    ids = [f"S{i:03d}" for i in range(n)]
    latent = rng.normal(size=(n, 3))
    blocks = {}
    for i, name in enumerate(("R", "S", "E", "G", "P", "M")):
        w = rng.normal(size=(3, 5 + (i % 3)))
        noise = rng.normal(scale=0.45 + 0.05 * i, size=(n, w.shape[1]))
        frame = pd.DataFrame(latent @ w + noise, index=ids,
                             columns=[f"{name}_{j}" for j in range(w.shape[1])])
        blocks[name] = BlockProfile(frame, evidence_class="SYNTHETIC_KNOWN_TRUTH", source="synthetic_demo")
    blocks["T"] = None
    blocks["Q"] = BlockProfile(
        pd.DataFrame({"uncertainty": rng.uniform(0, 1, size=n)}, index=ids),
        evidence_class="SYNTHETIC_KNOWN_TRUTH",
        source="synthetic_demo",
    )

    carrier = ConglomerateChiV01(ids, blocks)
    outdir.mkdir(parents=True, exist_ok=True)
    carrier.geometry_concordance().to_csv(outdir / "synthetic_geometry_concordance.csv")
    (outdir / "synthetic_manifest.json").write_text(json.dumps(carrier.manifest(), indent=2) + "\n")
    (outdir / "synthetic_leave_one_block_out.json").write_text(
        json.dumps(carrier.leave_one_block_out(), indent=2) + "\n"
    )


if __name__ == "__main__":
    synthetic_demo(Path("conglomerate_v01_outputs"))
