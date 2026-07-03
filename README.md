# Open Source LLM Study

This repository provides the research artifact for the paper:

**From Visibility to Curatability: Metadata, Provenance, and Release Evidence for Compact and Derived Open LLM Artifacts**

The project studies compact and derived open LLM artifacts as distributed scholarly objects. Instead of treating a model repository as a complete record by itself, the analysis links model-hub metadata, scholarly paper records, paper-side repository links, upstream model evidence, release statements, and model-card traces. The central question is whether these public records provide enough structured evidence for digital-library curation: artifact identity, scholarly linkage, provenance evidence, release-package evidence, and integrated curation readiness.

## Repository Structure

```text
.
├── data/
│   ├── main_analysis/          # Main repository-level and paper-level analysis tables
│   ├── validity_checks/        # Audit intervals, construct checks, and curated failure modes
│   ├── sensitivity_checks/     # Snapshot-scope sensitivity support
│   └── audit_support/          # Balanced repository-role audit support
├── docs/
│   ├── DATA_DICTIONARY.md
│   ├── DATA_STATEMENT.md
│   ├── REPRODUCIBILITY.md
│   └── ANONYMIZED_REVIEW.md
├── paper/
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── tables/
├── scripts/
│   ├── make_figures_tables.py
│   └── verify_artifact.py
├── MANIFEST.csv
├── requirements.txt
└── LICENSE
```

## Main Entry Points

For most readers, the following files are the best starting points:

- `docs/DATA_DICTIONARY.md`: describes the released tables, units of analysis, and denominators.
- `docs/REPRODUCIBILITY.md`: gives the commands for checking the artifact and regenerating manuscript figures/tables.
- `data/main_analysis/`: contains the main repository-level and paper-level analysis tables.
- `data/validity_checks/`: contains audit intervals, construct-validity mappings, threshold rationales, and curated failure-mode cases.
- `data/sensitivity_checks/`: contains the query-bucket sensitivity table used to document snapshot scope.
- `data/audit_support/`: contains balanced repository-role audit support used by the manuscript figures.
- `scripts/make_figures_tables.py`: regenerates the paper figures and LaTeX tables from the released CSVs.
- `scripts/verify_artifact.py`: checks required files, key row counts, manifest checksums, and common anonymization issues.
- `MANIFEST.csv`: records file paths, roles, byte sizes, and SHA-256 checksums.

The paper source is included under `paper/`. The main manuscript tables are in `paper/tables/`; supporting generated tables are in `paper/tables/supplementary/`.

## Quick Reproduction Check

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/verify_artifact.py
python scripts/make_figures_tables.py
```

To compile the manuscript source:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

## Data Scope

The released files are analysis-ready tables derived from a fixed May 2026 public-record snapshot. Repository-level percentages use 191,375 scoped Hugging Face repository records. Paper-level percentages use 2,214 main-analysis paper records unless otherwise stated. Audit-derived statistics use their own audit sample sizes and are reported as calibration checks rather than corpus prevalence estimates.

The repository is designed to support inspection of the paper's reported measurements and to regenerate the main figures and tables. It does not attempt to distribute raw model files, downloaded PDFs, private local logs, or raw API transcripts. See `docs/DATA_STATEMENT.md` for details.

## Review and Anonymity

The manuscript source is configured for anonymous ACM/JCDL review. When sharing this repository during a double-blind review process, use an anonymous mirror such as `anonymous.4open.science` rather than a personally identifying GitHub URL. See `docs/ANONYMIZED_REVIEW.md` for the release notes used for review.
