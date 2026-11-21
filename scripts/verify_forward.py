"""Second, independent pass for the fitted equations (t6u). Standard library only.
Reads data/virginia_localities_passB.csv (pass B, rebuilt from raw DOE files with separate parsing),
refits every line with closed-form least squares, and compares with out/analysis.json (pass A, statsmodels)
and the per-locality fitted values/residuals in data/virginia_localities_final.csv."""
import csv, json, math, sys
B = {r['key']: r for r in csv.DictReader(open('data/virginia_localities_passB.csv'))}
FIN = {r['key']: r for r in csv.DictReader(open('data/virginia_localities_final.csv'))}
A = json.load(open('out/analysis.json'))
assert len(B) == 133 and set(B) == set(FIN)
def ols(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    m = sxy / sxx; b = my - m * mx
    res = [y - (m * x + b) for x, y in zip(xs, ys)]
    sse = sum(e * e for e in res); sst = sum((y - my) ** 2 for y in ys); s2 = sse / (n - 2)
    return {'n': n, 'm': m, 'b': b, 'm_se': math.sqrt(s2 / sxx), 'b_se': math.sqrt(s2 * (1 / n + mx * mx / sxx)),
            'r2': 1 - sse / sst, 'resid_sd': math.sqrt(s2), 'mean_abs_resid': sum(abs(e) for e in res) / n}, res
f = lambda r, c: float(r[c])
K = sorted(B)
checks = bad = 0
def cmp(label, a, b, tol=1e-9):
    global checks, bad
    checks += 1
    if abs(a - b) > tol * max(1, abs(a)): bad += 1; print('MISMATCH', label, a, b)
# locked dG fit
r, res = ols([f(B[k], 'B_drop') for k in K], [f(B[k], 'dG') for k in K])
for a, b in (('m', 'multiplier'), ('b', 'constant'), ('m_se', 'multiplier_se'), ('b_se', 'constant_se'), ('r2', 'r2'), ('resid_sd', 'resid_se'), ('mean_abs_resid', 'mean_abs_resid')):
    cmp(f'locked {a}', r[a], A['fit_all'][b])
for k, e in zip(K, res): cmp(f'locked resid {k}', e, f(FIN[k], 'fit_resid'))
# forward share fits
for yr in ('22', '26'):
    r, res = ols([f(B[k], 'B' + yr) / 100 for k in K], [f(B[k], 'G' + yr) for k in K])
    for a in ('n', 'm', 'b', 'm_se', 'b_se', 'r2', 'resid_sd', 'mean_abs_resid'): cmp(f'forward{yr} {a}', r[a], A['forward'][yr][a])
    for k, e in zip(K, res):
        cmp(f'forward{yr} resid {k}', e, f(FIN[k], 'fres' + yr))
        # plug the 4-decimal published equation in: fitted = m*(D/100)+b
        cmp(f'forward{yr} plug {k}', A['forward'][yr]['m'] * f(B[k], 'B' + yr) / 100 + A['forward'][yr]['b'], f(FIN[k], 'fS' + yr))
r, _ = ols([f(B[k], 'B22') / 100 for k in K] + [f(B[k], 'B26') / 100 for k in K], [f(B[k], 'G22') for k in K] + [f(B[k], 'G26') for k in K])
for a in ('n', 'm', 'b', 'm_se', 'b_se', 'r2', 'resid_sd', 'mean_abs_resid'): cmp(f'pooled {a}', r[a], A['forward']['pooled'][a])
json.dump({'checks': checks, 'mismatches': bad}, open('out/verify_forward.json', 'w'))
print(f'fit verification (pass B, stdlib) checks: {checks}  mismatches: {bad}')
sys.exit(1 if bad else 0)
