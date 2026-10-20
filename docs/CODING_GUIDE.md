# Coding Guide

This guide summarizes how public traces are converted into the record-level evidence fields reported in the paper. Repository-level and paper-level denominators remain separate throughout the analysis.

## Evidence Sources

- Structured repository metadata, tags, upstream fields, and scholarly references are parsed directly.
- Paper-side Hugging Face and code-hosting links are retained as typed linkage signals.
- For unstructured paper text, model-assisted extraction locates candidate evidence and supporting excerpts. Final labels are assigned by deterministic normalization, inventory matching, link resolution, and the rules below.

## Evidence Codes

### Provenance (`P`)

- `P=0`: no usable upstream signal.
- `P=1`: weak or contextual family clue.
- `P=2`: inventory-backed family evidence, usable for collection-level grouping.
- `P=3`: explicit or canonical upstream evidence, required for an explicit upstream claim.

### Release package (`R`)

- `R=0`: no release signal.
- `R=1`: stated or incomplete release.
- `R=2`: code, scripts, or recipe.
- `R=3`: checkpoint, adapter, data, or evaluation asset.
- `R=4`: multi-asset package or full recipe.

### Scholarly relation (`L`)

`L` is a relation gate rather than an evidence-strength ladder.

- `L=0`: no direct paper-repository or paper-asset relation signal.
- `L=1`: one direct relation signal.
- `L=2`: multiple direct signals corroborate the relation.

Fuzzy family or size matches do not satisfy `L>=1`. Release evidence answers which assets are visible; linkage answers how those assets or repositories relate to the focal paper.

## Integrated Status

- Discovery-ready: at least one nonzero `P`, `R`, or `L` signal.
- Operational P+R: `P>=2` and `R>=2`.
- Operational+link sensitivity: `P>=2`, `R>=2`, and `L>=1`.
- High curatability: `P>=2`, `R>=3`, and `L>=1`.
- Preservation-review candidate: `P>=2`, `R>=4`, and `L>=1`.

These labels describe public-record evidence; they are not model-quality or execution-reproducibility scores.

## Expert Audit Protocol

A study-team expert reviewed each sampled audit row against retained public evidence. The reviewer recorded a decision, supporting excerpt, and audit note. This single-expert adjudication protocol calibrates rule-derived boundaries; its outcomes are summarized as support rates with Wilson 95% confidence intervals.

The supporting files are:

- `data/validity_checks/audit_wilson_ci.csv`
- `data/validity_checks/curatability_threshold_rationale.csv`
- `data/validity_checks/failure_modes_curated_for_jcdl.csv`

Separately, `data/validity_checks/curator_schema_review_cases_10.csv` provides ten illustrative schema walkthroughs prepared for author/coauthor spot-check. Their follow-up status is recorded in `needs_user_recheck`.
