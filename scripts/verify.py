"""Diff pass A vs pass B: every locality, every figure. Integers must match exactly;
derived percentages/votes must match to 1e-9."""
import csv, json, sys
A = {r['key']: r for r in csv.DictReader(open('data/virginia_localities_passA.csv'))}
B = {r['key']: r for r in csv.DictReader(open('data/virginia_localities_passB.csv'))}
cols = [c for c in next(iter(B.values())).keys() if c != 'key']
checked = 0; disc = []
assert set(A) == set(B) and len(A) == 133, (len(A), len(B), set(A) ^ set(B))
for k in A:
    for c in cols:
        a, b = A[k][c], B[k][c]; checked += 1
        if a in ('True', 'False') or b in ('True', 'False'):
            ok = a == b
        else:
            fa, fb = float(a), float(b)
            ok = (fa == fb) if (fa.is_integer() and fb.is_integer() and c not in ('implied_extra', 'baseline_scaled_gap')) else abs(fa - fb) < 1e-9
        if not ok: disc.append((k, c, a, b))
# order check: both sorted by population largest->smallest
orderA = list(A); orderB = list(B)
res = {'localities': len(A), 'figures_per_locality': len(cols), 'figures_checked': checked,
       'discrepancies': len(disc), 'details': disc[:50], 'same_population_order': orderA == orderB}
json.dump(res, open('out/verification.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'details'}), disc[:10])
sys.exit(1 if disc or orderA != orderB else 0)
