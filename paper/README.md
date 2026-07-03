# Paper Source

This directory contains the anonymous ACM/JCDL manuscript source.

## Compile

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

## Contents

- `main.tex`: manuscript entry point.
- `sections/`: section-level source files.
- `figures/`: final manuscript figures in PDF/PNG form.
- `tables/`: tables used directly by the manuscript.
- `tables/supplementary/`: generated supporting table files retained for inspection.
- `references.bib`: manuscript bibliography.

The main data and reproducibility instructions are in `../data/` and `../docs/`.
