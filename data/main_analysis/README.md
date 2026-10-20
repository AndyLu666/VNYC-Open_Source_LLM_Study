# Main Analysis Tables

[Data index](../README.md) · [Data dictionary](../../docs/DATA_DICTIONARY.md) · [Evidence codes](../../docs/CODING_GUIDE.md)

## Record-Level Data

| Table | Unit | Use |
| :--- | :--- | :--- |
| [Repository metadata](jcdl_metadata_completeness_repo_level.csv) | 191,375 repository records | Coverage indicators, inferred role, package form, and family |
| [Paper curatability](jcdl_paper_curatability_paper_level.csv) | 2,214 paper records | `P/R/L` scores, readiness categories, and evidence gaps |
| [Provenance evidence](jcdl_provenance_sufficiency_paper_level.csv) | 2,214 paper records | Strongest observable upstream-evidence tier |
| [Release evidence](jcdl_release_package_completeness_paper_level.csv) | 2,214 paper records | Visible assets and release-package tier |
| [Alignment edges](jcdl_paper_repo_alignment_edges.csv) | Paper-repository edge | Direct alignment evidence |

## Summaries and Comparisons

| Question | Tables |
| :--- | :--- |
| Which metadata fields are visible? | [Coverage matrix](metadata_completeness_matrix.csv) · [Role/year breakdown](jcdl_metadata_completeness_summary_by_role_year.csv) |
| How do readiness rules change coverage? | [Threshold sensitivity](jcdl_curatability_threshold_sensitivity.csv) · [Exclusive readiness categories](jcdl_paper_curatability_summary.csv) |
| How does evidence vary across records? | [Curatability by mechanism](jcdl_paper_curatability_by_mechanism.csv) · [By year](jcdl_paper_curatability_by_year.csv) |
| What upstream evidence is visible? | [Provenance summary](jcdl_provenance_sufficiency_summary.csv) · [By mechanism](jcdl_provenance_sufficiency_by_mechanism.csv) |
| What is publicly released? | [Package distribution](release_package_completeness_distribution.csv) · [By mechanism](jcdl_release_package_completeness_by_mechanism.csv) |
| Which signals connect papers and repositories? | [Signal decomposition](jcdl_paper_repo_alignment_decomposition.csv) · [Alignment summary](jcdl_paper_repo_alignment_summary.csv) |

Threshold coverage is cumulative: operational P+R includes records that also meet high curatability. The exclusive category table instead assigns each record to one group. Use the [coding guide](../../docs/CODING_GUIDE.md) for exact definitions.

## From Evidence to Metadata Design

- [Claim-evidence ledger](jcdl_claim_evidence_ledger.csv): maps measurements to their supporting analyses.
- [Construct-validity mapping](jcdl_evidence_source_construct_validity.csv): connects constructs, sources, and interpretation.
- [Metadata recommendation crosswalk](jcdl_metadata_recommendation_crosswalk.csv): connects observed patterns to proposed fields.
- [Curated failure examples](jcdl_curation_failure_examples.csv): illustrates ambiguity in public records.
- [Curation-function coverage](jcdl_record_function_coverage_summary.csv): organizes evidence by digital-library task.

Existing filenames are retained so analysis scripts and published links remain stable. Field definitions, denominator conventions, and supporting-table descriptions are in the [data dictionary](../../docs/DATA_DICTIONARY.md).
