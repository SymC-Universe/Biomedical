from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from src.build_tool_prediction_p0_split_manifest import run


def choose_file(title: str, filetypes: list[tuple[str, str]]) -> Path | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return Path(path) if path else None


def _show_error(text: str) -> None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror("P0 split manifest failed", text)
    root.destroy()


def main() -> None:
    base = Path.cwd()
    config = base / "config" / "tool_prediction_p0_holdout_freeze_20260830.json"
    identity_plan = base / "config" / "stage_c0_1_sample_identity_plan.json"
    out = base / "tool_prediction_p0_split_outputs"

    cache = choose_file(
        "Select the completed Stage A hallmark_profile_cache.npz",
        [("NumPy cache", "*.npz"), ("All files", "*.*")],
    )
    if cache is None:
        print("CANCELLED: no Stage A cache selected", flush=True)
        return

    source = choose_file(
        "Select the C0-audited 5.02 GB methylation TSV",
        [("TSV", "*.tsv"), ("All files", "*.*")],
    )
    if source is None:
        print("CANCELLED: no methylation source selected", flush=True)
        return

    c0_summary = choose_file(
        "Select STAGE_C0_METHYLATION_SOURCE_SUMMARY.json returned by the completed C0 run",
        [("JSON", "*.json"), ("All files", "*.*")],
    )
    if c0_summary is None:
        print("CANCELLED: no C0 summary selected", flush=True)
        return

    try:
        result = run(config, identity_plan, cache, source, c0_summary, out)
    except Exception as exc:
        text = f"P0 SPLIT MANIFEST FAILED\n\n{type(exc).__name__}: {exc}"
        print(text, flush=True)
        _show_error(text)
        raise

    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(
        "P0 split manifest complete",
        "P0 PRE-ELIGIBILITY SPLIT MANIFEST COMPLETE\n\n"
        "No methylation beta-value rows or predictive target values were read.\n\n"
        "Return the three compact files in tool_prediction_p0_split_outputs.",
    )
    root.destroy()


if __name__ == "__main__":
    main()
