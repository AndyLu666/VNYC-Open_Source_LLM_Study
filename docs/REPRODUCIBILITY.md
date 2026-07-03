# Reproducibility Notes

This artifact supports reproducibility at the analysis-table and manuscript-figure level. It does not include raw API calls, downloaded PDFs, or private local logs.

## Environment

Recommended environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Core dependencies:

- Python 3.10+
- pandas
- numpy
- matplotlib

Optional for paper compilation:

- TeX Live or TinyTeX
- `latexmk`
- `pdflatex`
- `bibtex`

## Verify Artifact Integrity

```bash
python scripts/verify_artifact.py
```

This checks that expected data files, scripts, and paper assets are present and that no placeholder citation keys remain in the paper source.

## Regenerate Figures and Tables

```bash
python scripts/make_figures_tables.py
```

The script reads the CSVs under `data/derived/database/` and writes figures/tables into:

- `paper/figures/`
- `paper/tables/`

The final manuscript currently uses:

- `paper/figures/fig1_overview_gpt_image2_icon_polished_library_crop.png`
- `paper/figures/fig2_metadata_completeness.pdf`
- `paper/figures/fig3_provenance_alignment.pdf`
- `paper/figures/fig4_release_curatability.pdf`

## Compile the Paper

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

The paper is configured with the anonymous ACM format.

## Scope of Reproducibility

The public artifact is designed to reproduce:

- Main result tables.
- Manuscript figures.
- Integrated curatability thresholds.
- Audit interval summaries.
- Construct-validity and failure-mode support tables.

It does not reproduce from raw web/API collection because those stages require external services, platform snapshots, and intermediate files that are large or not appropriate for anonymous review release. The included tables are the analysis-ready outputs used by the manuscript.

