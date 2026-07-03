# Reproducibility

This repository supports reproduction at the analysis-table, figure, and manuscript-source level. The raw web/API collection stage is not rerun from this artifact; instead, the repository provides the derived public-record tables used by the paper and the scripts that regenerate the reported figures and LaTeX tables.

## Environment

Use Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The Python workflow uses `pandas`, `numpy`, and `matplotlib`.

## Artifact Check

Run:

```bash
python scripts/verify_artifact.py
```

The check verifies that expected data, manuscript, figure, and script files are present; that key tables have the expected number of rows; that released-file checksums match `MANIFEST.csv`; and that common placeholder or local-path markers are absent.

Expected key counts:

- `jcdl_metadata_completeness_repo_level.csv`: 191,375 repository records
- `jcdl_paper_curatability_paper_level.csv`: 2,214 paper records
- `jcdl_provenance_sufficiency_paper_level.csv`: 2,214 paper records
- `jcdl_release_package_completeness_paper_level.csv`: 2,214 paper records

## Regenerating Figures and Tables

Run:

```bash
python scripts/make_figures_tables.py
```

The script reads the released tables under `data/` and writes:

- manuscript figures to `paper/figures/`;
- main manuscript tables to `paper/tables/`;
- supporting generated tables to `paper/tables/supplementary/`.

The manuscript uses the following figure files:

- `paper/figures/fig1_overview_gpt_image2_icon_polished_library_crop.png`
- `paper/figures/fig2_metadata_completeness.pdf`
- `paper/figures/fig3_provenance_alignment.pdf`
- `paper/figures/fig4_release_curatability.pdf`

## Compiling the Manuscript

The manuscript source is in `paper/`.

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

The source uses the anonymous ACM format and a local copy of the ACM reference style.

## Manifest

`MANIFEST.csv` records each released file, its artifact role, byte size, and SHA-256 checksum. It can be used to verify that an anonymous mirror preserves the same file set.
