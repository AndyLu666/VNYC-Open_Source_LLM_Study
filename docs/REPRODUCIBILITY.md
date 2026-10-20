# Analysis Workflow

[Repository home](../README.md) · [Data index](../data/README.md) · [Coding guide](CODING_GUIDE.md)

The workflow starts with the released May 2026 analysis tables. Use it to check file integrity, inspect record-level measurements, and generate analysis figures and LaTeX table exports.

## Setup

Use Python 3.10 or newer. Run the commands from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Check the Data Release

```bash
python scripts/verify_artifact.py
```

This standard-library check verifies required files, key record counts, file sizes and checksums in `MANIFEST.csv`, and local-path or placeholder markers. Local environments, caches, and generated `paper/` outputs are excluded from the release inventory.

| Table | Unit | Expected rows |
| :--- | :--- | ---: |
| `jcdl_metadata_completeness_repo_level.csv` | Scoped repository record | 191,375 |
| `jcdl_paper_curatability_paper_level.csv` | Main-analysis paper record | 2,214 |
| `jcdl_provenance_sufficiency_paper_level.csv` | Main-analysis paper record | 2,214 |
| `jcdl_release_package_completeness_paper_level.csv` | Main-analysis paper record | 2,214 |

## Recompute the Headline Counts

```python
import pandas as pd

records = pd.read_csv("data/main_analysis/jcdl_paper_curatability_paper_level.csv")
p = records["provenance_points_0_to_3"]
r = records["release_package_points_0_to_4"]
l = records["paper_repo_link_points_0_to_2"]

thresholds = {
    "Discovery-ready": (p > 0) | (r > 0) | (l > 0),
    "Operational P+R": (p >= 2) & (r >= 2),
    "Operational+link": (p >= 2) & (r >= 2) & (l >= 1),
    "High curatability": (p >= 2) & (r >= 3) & (l >= 1),
}
for label, selected in thresholds.items():
    print(f"{label}: {selected.sum():,} / {len(records):,} ({selected.mean():.1%})")
```

Expected counts are **2,008**, **401**, **400**, and **136**, respectively. These thresholds overlap. The mutually exclusive categories in `curatability_category` answer a different question: assignment to a single readiness group.

## Generate Figures and Tables

```bash
python scripts/make_figures_tables.py
```

For a headless environment, use `MPLBACKEND=Agg python scripts/make_figures_tables.py`.

| Output | Content |
| :--- | :--- |
| `paper/figures/fig2_metadata_completeness.{pdf,png}` | Metadata-field coverage and role-label audit |
| `paper/figures/fig3_provenance_alignment.{pdf,png}` | Provenance tiers by mechanism and alignment signals |
| `paper/figures/fig4_release_curatability.{pdf,png}` | Release evidence and provenance-release co-occurrence |
| `paper/tables/` | Study-design and headline-results LaTeX exports |
| `paper/tables/supplementary/` | Additional descriptive, audit, sensitivity, and design table exports |

The script combines data-driven plots and table exports with fixed study-design and reporting templates. These are standalone analysis outputs; the [published paper](https://doi.org/10.1145/3805696.3846021) provides the final manuscript layout. The filenames retain their original numbering for stable references.

Generated outputs are ignored by Git and may be regenerated in place. The two figures displayed on the repository homepage are maintained separately in [assets/readme/](../assets/readme/).

## Development Checks

```bash
python -m unittest discover -s tests -v
python scripts/verify_artifact.py
```

`MANIFEST.csv` inventories released files with their roles, byte sizes, and SHA-256 checksums. It is updated when a release changes; analysis CSVs remain the inputs to the workflow.
