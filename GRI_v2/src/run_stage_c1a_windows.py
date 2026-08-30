#!/usr/bin/env python3
"""Windows picker wrapper for the Stage C1A local probe inventory."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def pick(title: str, patterns: list[tuple[str, str]]) -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=patterns)
    root.destroy()
    if not path:
        raise SystemExit(f"CANCELLED: {title}")
    return path


def main() -> None:
    here = Path(__file__).resolve().parents[1]
    methylation = pick(
        "Select the already-audited 5.02 GB PanCanAtlas methylation TSV",
        [("TSV files", "*.tsv"), ("All files", "*.*")],
    )
    annotation = pick(
        "Select stage_c1a_annotation_export.tsv.gz from the C1A source artifact",
        [("Gzip TSV", "*.gz"), ("All files", "*.*")],
    )
    chen = pick(
        "Select stage_c1a_chen_crossreactive_probe_ids.txt",
        [("Text files", "*.txt"), ("All files", "*.*")],
    )
    summary = pick(
        "Select STAGE_C1A_ANNOTATION_SOURCE_SUMMARY.json",
        [("JSON files", "*.json"), ("All files", "*.*")],
    )
    outdir = here / "stage_c1a_probe_inventory_outputs"
    cmd = [
        sys.executable,
        "-m",
        "src.run_stage_c1a_probe_inventory",
        "--methylation-tsv",
        methylation,
        "--annotation-export",
        annotation,
        "--chen-ids",
        chen,
        "--source-summary",
        summary,
        "--outdir",
        str(outdir),
    ]
    print("Running frozen Stage C1A exact-probe inventory.")
    print("The 5.02 GB TSV is streamed for SHA-256 and probe IDs only; beta values are not parsed.")
    proc = subprocess.run(cmd, cwd=here)
    if proc.returncode != 0:
        messagebox.showerror("Stage C1A", "Stage C1A stopped or failed. Keep all files and send the console output to ChatGPT.")
        raise SystemExit(proc.returncode)
    messagebox.showinfo(
        "Stage C1A complete",
        "Stage C1A probe inventory passed. Return the summary JSON and regulatory-stratum counts CSV to ChatGPT.",
    )


if __name__ == "__main__":
    main()
