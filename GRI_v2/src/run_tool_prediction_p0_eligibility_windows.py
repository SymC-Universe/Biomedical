from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from src.run_tool_prediction_p0_eligibility import run


def choose_file(title: str, filetypes: list[tuple[str, str]]) -> Path | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    value = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return Path(value) if value else None


def show_error(text: str) -> None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror("P0 eligibility failed", text)
    root.destroy()


def main() -> None:
    base = Path.cwd()
    config = base / "config" / "tool_prediction_p0_eligibility_gate_20260830.json"
    out = base / "tool_prediction_p0_eligibility_outputs"

    source = choose_file(
        "Select the same C0-audited 5.02 GB methylation TSV",
        [("TSV", "*.tsv"), ("All files", "*.*")],
    )
    if source is None:
        print("CANCELLED: no methylation source selected", flush=True)
        return

    manifest = choose_file(
        "Select p0_preeligibility_split_manifest.csv from the completed P0 split run",
        [("CSV", "*.csv"), ("All files", "*.*")],
    )
    if manifest is None:
        print("CANCELLED: no P0 split manifest selected", flush=True)
        return

    try:
        result = run(config, manifest, source, out)
    except Exception as exc:
        text = f"P0 ELIGIBILITY FAILED\n\n{type(exc).__name__}: {exc}"
        print(text, flush=True)
        show_error(text)
        raise

    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(
        "P0 eligibility complete",
        "P0 SAMPLE ELIGIBILITY COMPLETE\n\n"
        "This step used methylation values only to count finite probes per participant.\n"
        "No RNA Hallmark target values or predictive outcomes were read.\n\n"
        "Return the three compact files in tool_prediction_p0_eligibility_outputs.",
    )
    root.destroy()


if __name__ == "__main__":
    main()
