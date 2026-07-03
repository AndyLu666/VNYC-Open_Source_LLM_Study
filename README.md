# Open Source LLM Study

This repository contains the anonymized code and analysis-ready data for the paper:

**From Visibility to Curatability: Metadata, Provenance, and Release Evidence for Compact and Derived Open LLM Artifacts**

The study treats compact and derived open LLM artifacts as distributed scholarly objects. It asks whether public records across model hubs, scholarly papers, model cards, code links, release statements, and provenance signals provide enough evidence for digital-library curation.

## Repository Layout

```text
.
├── data/
│   └── derived/database/
│       ├── 19_jcdl_revision/              # Main analysis tables used by the paper
│       ├── 20_jcdl_validity_strengthening/ # Audit intervals, failure modes, threshold rationale
│       ├── 16_www_revision/               # Minimal query-sensitivity support table
│       └── 18_www_reviewer_requested_validations/
│           └── hf_repo_artifact_typing_precision.csv
├── docs/
│   ├── DATA_DICTIONARY.md
│   ├── REPRODUCIBILITY.md
│   ├── ANONYMIZED_REVIEW.md
│   └── DATA_STATEMENT.md
├── paper/
│   ├── main.tex
│   ├── sections/
│   ├── tables/
│   └── figures/
├── scripts/
│   ├── make_figures_tables.py
│   └── verify_artifact.py
├── requirements.txt
└── MANIFEST.csv
```

## What Is Included

- Analysis-ready repository-level and paper-level CSV tables.
- Audit and validity-strengthening tables used to support the measurement design.
- Figure and table generation code for the manuscript's core visual results.
- An anonymized LaTeX manuscript source snapshot with final tables and figures.
- A file manifest with SHA-256 hashes for integrity checking.

## What Is Not Included

- API keys, `.env` files, local logs, or private credentials.
- Raw LLM API prompts/outputs.
- Downloaded PDFs and OCR/GROBID intermediates.
- Internal drafting notes, review conversations, and venue-planning notes.
- Full raw Hugging Face/source snapshots that are large or close to GitHub file-size limits.

The released CSVs are the analysis-ready public-record tables needed to inspect the paper's reported claims and regenerate the main paper tables/figures.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/verify_artifact.py
python scripts/make_figures_tables.py
```

To compile the paper source, use a TeX distribution with `pdflatex`, `bibtex`, and `latexmk`:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

## Main Data Products

The paper's primary empirical claims are supported by:

- `data/derived/database/19_jcdl_revision/jcdl_metadata_completeness_repo_level.csv`
- `data/derived/database/19_jcdl_revision/jcdl_paper_curatability_paper_level.csv`
- `data/derived/database/19_jcdl_revision/jcdl_provenance_sufficiency_paper_level.csv`
- `data/derived/database/19_jcdl_revision/jcdl_release_package_completeness_paper_level.csv`
- `data/derived/database/19_jcdl_revision/jcdl_paper_repo_alignment_edges.csv`
- `data/derived/database/20_jcdl_validity_strengthening/audit_wilson_ci.csv`
- `data/derived/database/20_jcdl_validity_strengthening/construct_validity_main_table.csv`
- `data/derived/database/20_jcdl_validity_strengthening/failure_modes_curated_for_jcdl.csv`

See [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for details.


