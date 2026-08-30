from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from src.run_stage_c0_1_sample_identity import run


def choose_file(title: str, filetypes: list[tuple[str, str]]) -> Path | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return Path(path) if path else None


def main() -> None:
    base = Path.cwd()
    plan = base / "config" / "stage_c0_1_sample_identity_plan.json"
    out = base / "stage_c0_1_sample_identity_outputs"

    cache = choose_file("Select the completed Stage A hallmark_profile_cache.npz", [("NumPy cache", "*.npz"), ("All files", "*.*")])
    if cache is None:
        print("CANCELLED: no Stage A cache selected", flush=True)
        return

    source = choose_file("Select the C0-audited 5.02 GB methylation TSV", [("TSV", "*.tsv"), ("All files", "*.*")])
    if source is None:
        print("CANCELLED: no methylation source selected", flush=True)
        return

    c0_summary = choose_file("Select STAGE_C0_METHYLATION_SOURCE_SUMMARY.json returned by the completed C0 run", [("JSON", "*.json"), ("All files", "*.*")])
    if c0_summary is None:
        print("CANCELLED: no C0 summary selected", flush=True)
        return

    try:
        result = run(plan, cache, source, c0_summary, out)
    except Exception as exc:
        text = f"STAGE C0.1 FAILED\n\n{type(exc).__name__}: {exc}"
        print(text, flush=True)
        root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
        messagebox.showerror("Stage C0.1 failed", text)
        root.destroy()
        raise

    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
    messagebox.showinfo(
        "Stage C0.1 complete",
        "STAGE C0.1 SAMPLE IDENTITY GATE COMPLETE\n\nReturn the three compact files in stage_c0_1_sample_identity_outputs.",
    )
    root.destroy()


if __name__ == "__main__":
    main()
