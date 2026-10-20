# Study Data

[Repository home](../README.md) · [Data dictionary](../docs/DATA_DICTIONARY.md) · [Coding guide](../docs/CODING_GUIDE.md)

The tables are organized by analysis purpose. Start with record-level data to inspect individual observations, summary tables for collection-level measurements, and audit tables to understand calibration.

| Directory | Contents | Starting point |
| :--- | :--- | :--- |
| [main_analysis/](main_analysis/) | Repository and paper records, evidence summaries, alignment edges, design crosswalks | [Table index](main_analysis/README.md) |
| [validity_checks/](validity_checks/) | Confidence intervals, threshold rationales, and curated cases | [Audit and validity index](validity_checks/README.md) |
| [sensitivity_checks/](sensitivity_checks/) | Snapshot scope under query-bucket exclusions | [Leave-one-bucket-out results](sensitivity_checks/hf_query_bucket_leave_one_out.csv) |
| [audit_support/](audit_support/) | Balanced repository-role audit summaries | [Role support](audit_support/hf_repo_artifact_typing_precision.csv) |

Repository percentages use **191,375 scoped repository records**. Paper-level percentages use **2,214 main-analysis paper records**, unless the table specifies another denominator. Audit tables report their own sample sizes.

See the [data statement](../docs/DATA_STATEMENT.md) for source scope and reuse terms, and the [analysis workflow](../docs/REPRODUCIBILITY.md) for executable examples.
