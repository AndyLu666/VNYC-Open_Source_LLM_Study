# Data Statement

This artifact releases the analysis-ready tables used for the paper's public-record measurements. The tables are derived from public model-hub records, public scholarly metadata, and public paper/repository traces. The study scope is compact and derived open LLM artifacts, not a complete census of all Hugging Face repositories or all LLM papers.

## Released Data Products

The release includes:

- repository-level metadata and artifact-role indicators;
- paper-level curatability indicators;
- paper-repository alignment edges and alignment summaries;
- provenance-evidence tiers;
- release-package evidence tiers;
- audit summaries with Wilson intervals;
- construct-validity and threshold-rationale tables;
- curated failure-mode examples used to motivate the metadata design agenda.

## Data Not Distributed in This Artifact

The repository does not distribute raw platform snapshots, raw model files, downloaded PDFs, OCR/GROBID intermediates, local execution logs, API credentials, or raw LLM API transcripts. These materials are either unnecessary for checking the reported analysis tables, unsuitable for a compact review artifact, or tied to external services and time-specific platform states.

## Use and Citation

The released code is covered by the repository license. The tabular data are derived from public records and are intended for scholarly inspection, reproducibility checks, and follow-on research. Users should cite the associated paper and respect the terms of the original public sources.
