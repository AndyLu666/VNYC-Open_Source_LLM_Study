#!/usr/bin/env python3
"""Sanity checks for the anonymized review artifact."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "docs/DATA_DICTIONARY.md",
    "docs/REPRODUCIBILITY.md",
    "docs/ANONYMIZED_REVIEW.md",
    "docs/DATA_STATEMENT.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/acmart.cls",
    "paper/ACM-Reference-Format.bst",
    "paper/sections/01_introduction.tex",
    "paper/sections/02_problem.tex",
    "paper/sections/03_related_work.tex",
    "paper/sections/04_data_methods.tex",
    "paper/sections/05_results.tex",
    "paper/sections/06_discussion.tex",
    "paper/sections/07_limitations_conclusion.tex",
    "paper/figures/fig1_overview_gpt_image2_icon_polished_library_crop.png",
    "paper/figures/fig2_metadata_completeness.pdf",
    "paper/figures/fig3_provenance_alignment.pdf",
    "paper/figures/fig4_release_curatability.pdf",
    "scripts/make_figures_tables.py",
    "data/derived/database/19_jcdl_revision/jcdl_metadata_completeness_repo_level.csv",
    "data/derived/database/19_jcdl_revision/jcdl_paper_curatability_paper_level.csv",
    "data/derived/database/19_jcdl_revision/jcdl_provenance_sufficiency_paper_level.csv",
    "data/derived/database/19_jcdl_revision/jcdl_release_package_completeness_paper_level.csv",
    "data/derived/database/19_jcdl_revision/jcdl_paper_repo_alignment_edges.csv",
    "data/derived/database/20_jcdl_validity_strengthening/audit_wilson_ci.csv",
    "data/derived/database/20_jcdl_validity_strengthening/construct_validity_main_table.csv",
    "data/derived/database/20_jcdl_validity_strengthening/failure_modes_curated_for_jcdl.csv",
]

EXPECTED_ROWS = {
    "data/derived/database/19_jcdl_revision/jcdl_metadata_completeness_repo_level.csv": 191_375,
    "data/derived/database/19_jcdl_revision/jcdl_paper_curatability_paper_level.csv": 2_214,
    "data/derived/database/19_jcdl_revision/jcdl_provenance_sufficiency_paper_level.csv": 2_214,
    "data/derived/database/19_jcdl_revision/jcdl_release_package_completeness_paper_level.csv": 2_214,
}

FORBIDDEN_NAMES = {".env", ".DS_Store"}
FORBIDDEN_TEXT = [
    "/Users/yiyilu",
    "OPENAI_API_KEY",
    "api_key",
    "SECRET",
    "PRIVATE KEY",
    "cite: 1",
]
TEXT_SUFFIXES = {
    ".bib",
    ".cls",
    ".csv",
    ".md",
    ".py",
    ".tex",
    ".txt",
}


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing required file: {rel}")

    for rel, expected in EXPECTED_ROWS.items():
        path = ROOT / rel
        if path.exists():
            observed = count_csv_rows(path)
            if observed != expected:
                errors.append(f"row-count mismatch for {rel}: expected {expected}, observed {observed}")

    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in FORBIDDEN_NAMES for part in path.parts):
            errors.append(f"forbidden file name present: {rel}")
        if path.is_file() and is_text_file(path):
            if path == Path(__file__).resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError as exc:
                errors.append(f"could not read {rel}: {exc}")
                continue
            for needle in FORBIDDEN_TEXT:
                if needle in text:
                    errors.append(f"forbidden text marker {needle!r} found in {rel}")

    if errors:
        print("Artifact verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Artifact verification passed.")
    print("Checked required files, key row counts, and common anonymization markers.")
    for rel, expected in EXPECTED_ROWS.items():
        print(f"- {rel}: {expected:,} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
