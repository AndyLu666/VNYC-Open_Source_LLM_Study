# Data Dictionary

This document explains the analysis-ready data files released with the artifact. Percentages in the paper are computed from these tables unless otherwise stated.

## Main Analysis Tables

Path: `data/main_analysis/`

### Repository-Level Metadata

- `jcdl_metadata_completeness_repo_level.csv`
  - Unit: Hugging Face repository record in the scoped May 2026 snapshot.
  - Important fields:
    - `repo_level_id`: stable anonymized repository-row identifier.
    - `hf_repo_id`: public model repository identifier.
    - `created_year`: repository creation year.
    - `model_repo_type`: project-inferred artifact role.
    - `variant_type`: project-inferred package or variant type.
    - `family_primary`: normalized model-family signal.
    - `has_family_label`, `has_upstream_model`, `has_typed_upstream_relation`, `has_arxiv_reference`, `has_task_descriptors`, `has_domain_descriptors`, `has_license_tag_signal`: binary metadata-signal indicators.

- `metadata_completeness_matrix.csv`
  - Unit: curation metadata field.
  - Used for Figure 2 panel (a).

- `jcdl_metadata_completeness_summary_by_role_year.csv`
  - Unit: repository role by year.
  - Used for robustness and descriptive checks.

### Paper-Level Curatability

- `jcdl_paper_curatability_paper_level.csv`
  - Unit: main-analysis paper record.
  - Important fields:
    - `paper_id`, `work_id`: stable anonymized paper/work identifiers.
    - `title`, `year`, `mechanism`: descriptive bibliographic and mechanism fields.
    - `provenance_points_0_to_3`: provenance-evidence score.
    - `release_package_points_0_to_4`: visible release-package evidence score.
    - `paper_repo_link_points_0_to_2`: direct linkage score.
    - `curatability_score_0_to_9`: integrated score.
    - `curatability_category`: integrated curation-readiness category.
    - `curatability_gap_flags`: missing or weak evidence fields.

- `jcdl_paper_curatability_summary.csv`
  - Unit: integrated curatability category.
  - Used to report the visibility-to-curatability funnel.

- `jcdl_curatability_threshold_sensitivity.csv`
  - Unit: threshold rule.
  - Used to show how stricter or broader integrated thresholds change counts.

### Provenance and Linkage

- `jcdl_provenance_sufficiency_paper_level.csv`
  - Unit: main-analysis paper record.
  - Used to evaluate upstream-evidence support.

- `jcdl_provenance_sufficiency_by_mechanism.csv`
  - Unit: mechanism by provenance tier.
  - Used for Figure 3 panel (a).

- `jcdl_paper_repo_alignment_edges.csv`
  - Unit: paper-to-repository alignment edge.
  - Used to inspect direct paper/model-hub evidence.

- `jcdl_paper_repo_alignment_decomposition.csv`
  - Unit: alignment signal type.
  - Used for Figure 3 panel (b).

### Release Evidence

- `jcdl_release_package_completeness_paper_level.csv`
  - Unit: main-analysis paper record.
  - Used to evaluate visible release assets.

- `release_package_completeness_distribution.csv`
  - Unit: release-package evidence tier.
  - Used for Figure 4 panel (a).

- `jcdl_release_package_completeness_by_mechanism.csv`
  - Unit: mechanism by release-evidence tier.

### Claim and Design Support

- `jcdl_claim_evidence_ledger.csv`
  - Maps manuscript claims to supporting output files.

- `jcdl_evidence_source_construct_validity.csv`
  - Maps each construct to evidence sources, checks, and safe claims.

- `jcdl_metadata_recommendation_crosswalk.csv`
  - Maps empirical findings to metadata/interface recommendations.

- `jcdl_curation_failure_examples.csv`
  - Curated examples explaining why typed links, relation fields, provenance tiers, and release-package fields are needed.

## Validity-Strengthening Tables

Path: `data/validity_checks/`

- `audit_wilson_ci.csv`
  - Wilson 95% confidence intervals for audit-derived proportions.

- `construct_validity_main_table.csv`
  - Concise construct-validity mapping used for main-text table design.

- `curatability_threshold_rationale.csv`
  - Maps numerical thresholds to curator tasks.

- `failure_modes_curated_for_jcdl.csv`
  - Curated failure modes used to support the metadata design agenda.

- `curator_schema_review_cases_10.csv`
  - Internal schema review cases over boundary examples. This is an expert review aid, not a blinded multi-curator reliability study.

- `curator_schema_review_summary.csv`
  - Summary of the schema review cases.

## Minimal Supporting Tables

- `data/sensitivity_checks/hf_query_bucket_leave_one_out.csv`
  - Query-bucket sensitivity table retained because the JCDL paper scopes the repository snapshot as query-based.

- `data/audit_support/hf_repo_artifact_typing_precision.csv`
  - Balanced artifact-role audit table used for Figure 2 panel (b).

## Denominators

- Repository-level percentages use `191,375` scoped Hugging Face repository records.
- Paper-level percentages use `2,214` main-analysis paper records unless otherwise stated.
- Audit-derived proportions use their own audit sample sizes and should not be interpreted as corpus prevalence estimates.
