# Patent analytics: reproducibility tables

This repository contains compact CSV exports derived from saved analysis checkpoints.
The exported tables record clustering diagnostics, cluster counts, ranked keywords,
logistic lifecycle observations and fitted curves, and company-level patent counts.

## Contents

- `data/clustering_metrics.csv`: saved clustering diagnostics for the evaluated K values.
- `data/cluster_counts.csv`: saved patent counts by cluster.
- `data/cluster_names_as_saved.csv`: labels exactly as stored in the checkpoint.
- `data/cluster_keywords.csv`: top ranked terms as saved.
- `data/lifecycle_parameters.csv`: saved parameter estimates and stage assignments.
- `data/lifecycle_observed.csv`: observed cumulative normalized patent series.
- `data/lifecycle_fitted.csv`: saved fitted curve coordinates.
- `data/company_cluster_counts.csv`: company-by-cluster aggregate counts.
- `data/company_stage_counts.csv`: company-by-lifecycle-stage aggregate counts.
- `data/checkpoint_sha256.csv`: SHA-256 digests of source checkpoints.
- `environment.json`: software versions recorded in the export environment.
- `scripts/reproduce_tables.py`: checks aggregate totals and computes portfolio entropy.

## Re-run the published aggregate checks

```bash
python scripts/reproduce_tables.py
```

The script uses only Python's standard library and writes results to
`reproduced_company_summary.csv` in the repository directory.

## Reproducibility scope

This release supports reconstruction and checking of selected reported aggregate
results from saved checkpoints. It does **not** contain the original patent
texts, the full retrieved patent corpus, transformer embedding matrices, or
model checkpoints. The upstream retrieval, preprocessing, embedding, and
clustering computations therefore cannot be independently rerun from these CSVs.
The saved CSV values are presented as checkpoint outputs, without introducing
additional experiments or uncertainty estimates.

## Data use and provenance

Patent source: Lens patent records, as described in the associated manuscript.
Original records and third-party patent text have not been redistributed.
The `checkpoint_sha256.csv` hashes allow comparison against the author's
original checkpoint files.
