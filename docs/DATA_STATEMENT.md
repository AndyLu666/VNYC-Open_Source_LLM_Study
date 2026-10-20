# Data Statement

[Repository home](../README.md) · [Data dictionary](DATA_DICTIONARY.md) · [Coding guide](CODING_GUIDE.md)

## Collection and Units

The study characterizes compact and derived open LLM artifacts through a fixed **May 2026** public-record snapshot. Its analysis-ready tables connect model-hub metadata, scholarly metadata, and public paper/repository traces.

| Analysis layer | Scope | Unit |
| :--- | :--- | :--- |
| Repository metadata | 191,375 Hugging Face repositories selected through scoped queries | Repository record |
| Paper evidence | 2,214 main-analysis records | Scholarly paper record |
| Role audit | 300 repositories, balanced across five inferred roles | Audited repository |
| Upstream audit | 200 sampled provenance rows | Audited paper-level evidence |
| Release audit | 50 reviewed URL/asset rows | Audited release evidence |

Repository and paper identifiers provide traceability between analysis tables. Counts and percentages should be interpreted with the denominator of their own layer. Audit support rates calibrate coding decisions within the corresponding audit samples.

## Data Products

- **Record-level tables:** metadata coverage, evidence scores, provenance tiers, and visible release packages.
- **Alignment tables:** paper-repository edges, link signals, and summary counts.
- **Aggregate measurements:** mechanism and year breakdowns, curation thresholds, and query-scope sensitivity.
- **Audit and design evidence:** Wilson confidence intervals, threshold rationales, curated cases, and metadata recommendations.

The [data index](../data/README.md) provides entry points; the [coding guide](CODING_GUIDE.md) defines the interpretation of `P`, `R`, and `L`. These scores describe observable public-record evidence for curation.

## Reuse and Attribution

Original analysis annotations and aggregations are released under the [MIT License](../LICENSE), alongside the project code and documentation. Public-source metadata and referenced artifacts retain their original terms, as described in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

Please cite the [associated paper](https://doi.org/10.1145/3805696.3846021) when using the study's data or framework, and retain source identifiers when extending the analysis.
