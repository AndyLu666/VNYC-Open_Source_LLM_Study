# JCDL Revision Output Summary

This directory contains lightweight analyses for reframing the paper as a JCDL submission about curatable AI artifact infrastructure.

## Key Preliminary Findings

### Metadata completeness
- Stable repository id: 100.0% (broadly available in the snapshot).
- Publisher or owner: 100.0% (broadly available in the snapshot).
- Creation timestamp: 100.0% (broadly available in the snapshot).
- Artifact role: 100.0% (broadly available in the snapshot).
- Variant type: 100.0% (broadly available in the snapshot).
- Model family label: 62.0% (available for many records but incomplete).
- Explicit upstream model: 53.5% (available for many records but incomplete).
- Typed upstream relation: 53.5% (available for many records but incomplete).
- Scholarly reference: 33.3% (sparse; useful where present but not collection-wide).
- Task descriptors: 65.2% (available for many records but incomplete).
- Domain descriptors: 14.4% (rare; weak basis for collection-wide curation).
- General tag record: 100.0% (broadly available in the snapshot).
- License tag signal: 46.8% (sparse; useful where present but not collection-wide).

### Release package completeness
- Score 0 / no_explicit_release_signal: 32.8% of main-analysis papers.
- Score 1 / stated_or_incomplete_release_signal: 31.3% of main-analysis papers.
- Score 2 / code_or_scripts_or_recipe: 24.3% of main-analysis papers.
- Score 3 / data_or_evaluation_assets: 0.1% of main-analysis papers.
- Score 3 / model_checkpoint_or_adapter: 6.8% of main-analysis papers.
- Score 4 / multiple_assets_or_complete_recipe: 4.5% of main-analysis papers.

### Paper-repository alignment
- has_code_or_scripts_signal: 30.7% (code/scripts release evidence).
- has_data_or_evaluation_asset_signal: 0.3% (data or evaluation asset release evidence).
- has_model_checkpoint_or_adapter_signal: 11.3% (model weights/checkpoint/adapter release evidence).
- has_multiple_asset_or_complete_recipe_signal: 4.5% (strict multi-asset or full-recipe evidence).
- has_recipe_or_pipeline_signal: 36.6% (recipe, pipeline, or procedural reuse evidence).
- has_stated_release_or_partial_signal: 67.2% (any stated release or open-asset signal).
- mentions_github_link: 30.6% (code-hosting or project link in paper text).
- mentions_huggingface_link: 10.5% (direct model-hub link in paper text).

### Provenance sufficiency audit
- audited_rows: 200 (Expert-reviewed lineage/provenance audit rows.)
- strict_unique_primary_support: 56 (28.0% of audited rows.)
- usable_family_signal_support: 158 (79.0% of audited rows.)

### Integrated curatability
- 1_high_curatability: 6.1% (records support provenance, concrete release assets, and at least one paper-repository link signal).
- 2_operational_curatability: 12.0% (records support usable provenance and concrete code/recipe or stronger release evidence).
- 3_partial_curatability: 72.6% (records expose at least one useful signal but lack a complete curation package).
- 4_low_curatability: 9.3% (records lack usable provenance, explicit release evidence, and direct paper-repository link signals).

### Curation functions
- Artifact identity: project-inferred artifact role available for 100.0%; project-inferred variant type available for 100.0%; strict audited role agreement 85.3%
- Bibliographic control: stable id/owner/date 100.0%/100.0%/100.0%; repository scholarly reference 33.3%; paper HF link 10.5%; paper GitHub link 30.6%
- Provenance sufficiency: paper exact HF edge 5.6%; inventory-backed family signal 45.6%; expert strict support 28.0% of audited rows.; expert usable support 79.0% of audited rows.
- Reuse and preservation readiness: any release/open-asset signal 67.2%; concrete code/asset signal 35.8%; strict full package 4.5%
- Integrated curatability: high curatability 6.1% jointly satisfies provenance, concrete release, and link criteria; high or operational curatability 18.1% under the operational rubric

## Writing Implication

The JCDL manuscript should foreground metadata completeness, provenance sufficiency, and release-package completeness. The old WWW artifact ecology results should become supporting evidence, not the main storyline. Use curatability as the organizing concept: public records make open LLM artifacts visible, but only partly support identity, bibliographic control, provenance, reuse, and preservation.
