from __future__ import annotations

import json
import tkinter as tk
import zipfile
from pathlib import Path
from tkinter import filedialog, messagebox

from src.run_tool_prediction_p0_d1_discovery_source import run


def choose_file(title: str, filetypes: list[tuple[str, str]]) -> Path | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return Path(path) if path else None


def show(kind: str, title: str, text: str) -> None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    getattr(messagebox, kind)(title, text)
    root.destroy()


def main() -> None:
    base = Path.cwd()
    source = choose_file(
        "Select the same C0-audited 5.02 GB methylation TSV",
        [("TSV", "*.tsv"), ("All files", "*.*")],
    )
    if source is None:
        print("CANCELLED: no methylation source selected", flush=True)
        return
    hallmarks = choose_file(
        "Select the exact Hallmark membership snapshot (.gmt) used in Stage A",
        [("GMT", "*.gmt"), ("All files", "*.*")],
    )
    if hallmarks is None:
        print("CANCELLED: no Hallmark membership snapshot selected", flush=True)
        return
    out = base / "tool_prediction_p0_d1_outputs"
    try:
        result = run(
            base / "config" / "tool_prediction_p0_d1_discovery_source_freeze_20260830.json",
            base / "inputs" / "P0_ELIGIBILITY_SUMMARY.json",
            base / "inputs" / "p0_sample_eligibility.csv",
            base / "inputs" / "p0_partition_eligibility_counts.csv",
            source,
            base / "inputs" / "stage_c1a_annotation_export.tsv.gz",
            base / "inputs" / "stage_c1a_chen_crossreactive_probe_ids.txt",
            hallmarks,
            out,
        )
    except Exception as exc:
        text = f"P0 D1 DISCOVERY SOURCE PREPROCESS FAILED\n\n{type(exc).__name__}: {exc}"
        print(text, flush=True)
        show("showerror", "P0 D1 failed", text)
        raise
    zip_path = base / "P0_D1_DISCOVERY_SOURCE_PREPROCESS_RESULTS.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in sorted(out.iterdir()):
            if p.is_file():
                zf.write(p, p.name)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print(f"RESULT ZIP: {zip_path}", flush=True)
    show(
        "showinfo",
        "P0 D1 complete",
        "P0 D1 DISCOVERY SOURCE PREPROCESS COMPLETE\n\n"
        "Only eligible DISCOVERY methylation values were analyzed.\n"
        "No RNA expression, replication methylation, final-holdout methylation, or predictive target values were read.\n\n"
        "Return P0_D1_DISCOVERY_SOURCE_PREPROCESS_RESULTS.zip to ChatGPT.",
    )


if __name__ == "__main__":
    main()
