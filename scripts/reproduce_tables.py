"""Check released aggregate tables using the Python standard library."""
from pathlib import Path
from collections import defaultdict
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'


def read(name):
    with (DATA / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


matrix = defaultdict(dict)
for row in read('company_cluster_counts.csv'):
    matrix[row['company']][int(row['cluster_id'])] = int(row['patent_count'])

stages = defaultdict(dict)
for row in read('company_stage_counts.csv'):
    stages[row['company']][row['stage_as_saved']] = int(row['patent_count'])

stage_by_cluster = {
    int(row['cluster_id']): row['current_stage']
    for row in read('lifecycle_parameters.csv')
}

out_rows = []
for company, counts in sorted(matrix.items()):
    total = sum(counts.values())
    fractions = [count / total for count in counts.values() if count > 0]
    shannon = -sum(p * math.log(p) for p in fractions) if total else 0.0
    derived_stages = defaultdict(int)
    for cluster_id, count in counts.items():
        derived_stages[stage_by_cluster.get(cluster_id, 'Unassigned')] += count
    saved_stages = stages.get(company, {})
    out_rows.append({
        'company': company,
        'total_from_matrix': total,
        'entropy_natural_log': f'{shannon:.9f}',
        'stage_totals_equal_saved': str(dict(derived_stages) == saved_stages),
    })

if out_rows:
    destination = ROOT / 'reproduced_company_summary.csv'
    with destination.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        writer.writeheader()
        writer.writerows(out_rows)
    print(f'Wrote {destination.name} ({len(out_rows)} companies)')

cluster_total = sum(int(r['patent_count']) for r in read('cluster_counts.csv'))
print('Total labels in cluster counts:', cluster_total)
print('Saved K evaluations:', len(read('clustering_metrics.csv')))
print('Lifecycle series:', len(set(r['cluster_id'] for r in read('lifecycle_observed.csv'))))
