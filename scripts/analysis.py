"""Statewide fit, regional constants, narrowing, floor/ceiling, over-ballot check (reads pass A table)."""
import json
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
d = pd.read_csv('data/virginia_localities_passA.csv')
n = len(d); out = {'n': n}

def fit(df, y='dG', x='B_drop'):
    m = smf.ols(f'{y} ~ {x}', data=df).fit()
    return m, {'n': int(m.nobs), 'constant': m.params['Intercept'], 'constant_se': m.bse['Intercept'],
               'multiplier': m.params[x], 'multiplier_se': m.bse[x], 'r2': m.rsquared,
               'p_multiplier': m.pvalues[x], 'p_constant': m.pvalues['Intercept'], 'resid_se': np.sqrt(m.scale)}
m_all, out['fit_all'] = fit(d)
infl = m_all.get_influence()
d['cooks'] = infl.cooks_distance[0]; d['stud'] = infl.resid_studentized_external
d['fitted'] = m_all.fittedvalues; d['fit_resid'] = m_all.resid
flag = (d.cooks > 4 / n) | (d.stud.abs() > 3)
out['narrowed_out'] = d.loc[flag, ['locality', 'region', 'dG', 'B_drop', 'cooks', 'stud', 'house_total26']].sort_values('cooks', ascending=False).to_dict('records')
_, out['fit_narrowed'] = fit(d[~flag])
# weighted by 2026 House votes (sensitivity)
mw = smf.wls('dG ~ B_drop', data=d, weights=d.house_total26).fit()
out['fit_weighted'] = {'constant': mw.params['Intercept'], 'constant_se': mw.bse['Intercept'], 'multiplier': mw.params['B_drop'],
                       'multiplier_se': mw.bse['B_drop'], 'r2': mw.rsquared, 'n': n}
# ballots-denominator sensitivity
_, out['fit_ballots_all'] = fit(d, y='dG_b')
_, out['fit_ballots_no_over'] = fit(d[d.over22 <= 0], y='dG_b')
# regional constants: common multiplier, one constant per region
mr = smf.ols('dG ~ 0 + C(region) + B_drop', data=d).fit()
out['regional_common_slope'] = {'multiplier': mr.params['B_drop'], 'multiplier_se': mr.bse['B_drop'], 'r2_vs_mean':
    1 - mr.ssr / ((d.dG - d.dG.mean()) ** 2).sum(), 'constants': {}}
for k, v in mr.params.items():
    if k.startswith('C(region)'):
        r = k.split('[')[1].rstrip(']')
        out['regional_common_slope']['constants'][r] = {'constant': v, 'se': mr.bse[k], 'n': int((d.region == r).sum())}
mr2 = smf.ols('dG ~ C(region) + B_drop', data=d).fit()
ft = mr2.compare_f_test(m_all)
out['regional_F_test'] = {'F': ft[0], 'p': ft[1], 'df_diff': ft[2], 'adj_r2_regional': mr2.rsquared_adj, 'adj_r2_statewide': m_all.rsquared_adj}
out['regional_separate'] = {}
for r, g in d.groupby('region'):
    _, f = fit(g); f['median_dG'] = g.dG.median(); out['regional_separate'][r] = f
# statewide pooled
T = d[['D22', 'D26', 'house_total22', 'house_total26', 'govD21', 'govTot21', 'govD25', 'govTot25', 'ballots22', 'ballots26', 'R22', 'R26', 'reg22', 'reg26']].sum()
S22 = T.D22 / T.house_total22 * 100; S26 = T.D26 / T.house_total26 * 100; B22 = T.govD21 / T.govTot21 * 100; B26 = T.govD25 / T.govTot25 * 100
out['statewide'] = {**{k: int(v) for k, v in T.items()}, 'S22': S22, 'S26': S26, 'B22': B22, 'B26': B26, 'G22': S22 - B22, 'G26': S26 - B26,
    'dG': (S26 - B26) - (S22 - B22), 'B_drop': B22 - B26, 'implied_pooled': T.D26 - S22 / 100 * T.house_total26}
out['dG_summary'] = {'median': d.dG.median(), 'min': d.dG.min(), 'max': d.dG.max(), 'mean': d.dG.mean(), 'sd': d.dG.std(),
    'n_negative': int((d.dG < 0).sum()), 'n_positive': int((d.dG > 0).sum()), 'within3_of_median': int(((d.dG - d.dG.median()).abs() <= 3).sum())}
out['residual_summary'] = {'median': d.residual.median(), 'min': d.residual.min(), 'max': d.residual.max(), 'n_positive': int((d.residual > 0).sum()),
    'within3_of_median': int(((d.residual - d.residual.median()).abs() <= 3).sum()), 'sd': d.residual.std()}
out['B_drop_summary'] = {'median': d.B_drop.median(), 'min': d.B_drop.min(), 'max': d.B_drop.max(), 'n_positive': int((d.B_drop > 0).sum())}
out['implied_sum'] = d.implied_extra.sum(); out['baseline_scaled_sum'] = d.baseline_scaled_gap.sum()
out['n_implied_negative'] = int((d.implied_extra < 0).sum())
# ---- forward surplus (share version): S = m * (D/100) + b, S = G (points), D = B baseline share [PROXY] ----
out['fit_all']['mean_abs_resid'] = float(m_all.resid.abs().mean())
fw = {}
for yr in ('22', '26'):
    dd = pd.DataFrame({'S': d['G' + yr], 'Dfrac': d['B' + yr] / 100})
    mf = smf.ols('S ~ Dfrac', data=dd).fit()
    d['fS' + yr] = mf.fittedvalues; d['fres' + yr] = mf.resid
    fw[yr] = {'n': int(mf.nobs), 'm': mf.params['Dfrac'], 'm_se': mf.bse['Dfrac'], 'b': mf.params['Intercept'], 'b_se': mf.bse['Intercept'],
              'r2': mf.rsquared, 'resid_sd': float(np.sqrt(mf.scale)), 'mean_abs_resid': float(mf.resid.abs().mean()),
              'p_m': mf.pvalues['Dfrac'], 'p_b': mf.pvalues['Intercept'], 'D_min': d['B' + yr].min(), 'D_max': d['B' + yr].max()}
pool = pd.concat([pd.DataFrame({'S': d.G22, 'Dfrac': d.B22 / 100, 'y26': 0}), pd.DataFrame({'S': d.G26, 'Dfrac': d.B26 / 100, 'y26': 1})], ignore_index=True)
mp = smf.ols('S ~ Dfrac', data=pool).fit()
fw['pooled'] = {'n': int(mp.nobs), 'm': mp.params['Dfrac'], 'm_se': mp.bse['Dfrac'], 'b': mp.params['Intercept'], 'b_se': mp.bse['Intercept'],
                'r2': mp.rsquared, 'resid_sd': float(np.sqrt(mp.scale)), 'mean_abs_resid': float(mp.resid.abs().mean())}
mi = smf.ols('S ~ Dfrac * y26', data=pool).fit()
fw['year_test'] = {'dm': mi.params['Dfrac:y26'], 'p_dm': mi.pvalues['Dfrac:y26'], 'db': mi.params['y26'], 'p_db': mi.pvalues['y26']}
out['forward'] = fw
cols = ['locality', 'region', 'pop2025', 'B22', 'B26', 'S22', 'S26', 'G22', 'G26', 'dG', 'B_drop', 'residual', 'implied_extra', 'D22', 'D26', 'govD21', 'govD25', 'house_total22', 'house_total26']
out['ceiling'] = d.nlargest(5, 'dG')[cols].to_dict('records')
out['lowest_dG'] = d.nsmallest(5, 'dG')[cols].to_dict('records')
out['floor'] = d.nsmallest(5, 'B22')[cols].to_dict('records')
out['highest_baseline'] = d.nlargest(5, 'B22')[cols].to_dict('records')
out['baseline_loss'] = d.loc[d.baseline_votes_fell, cols].to_dict('records')
out['over22'] = d.loc[d.over22 > 0, ['locality', 'D22', 'R22', 'ballots22', 'over22', 'house_total22', 'house_over22']].sort_values('over22', ascending=False).to_dict('records')
out['house_over22_count'] = int((d.house_over22 > 0).sum())
out['over26_count'] = int((d.over26 > 0).sum()); out['sen_over26_count'] = int((d.sen_over26 > 0).sum()); out['house_over26_count'] = int((d.house_over26 > 0).sum())
out['dS_negative'] = d.loc[d.dS < 0, 'locality'].tolist()
out['split_localities'] = d.loc[d.districts22.astype(str).str.contains(';'), ['locality', 'districts22']].to_dict('records')
out['log_pop_r2'] = smf.ols('dG ~ np.log(pop2025)', data=d).fit().rsquared
d.to_csv('data/virginia_localities_final.csv', index=False)
json.dump(out, open('out/analysis.json', 'w'), indent=1, default=float)
for k in ['fit_all', 'fit_narrowed', 'fit_weighted', 'fit_ballots_all', 'fit_ballots_no_over', 'regional_F_test', 'statewide', 'dG_summary', 'residual_summary', 'B_drop_summary']:
    print(k, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in out[k].items()})
print('forward', {k: {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()} for k, v in out['forward'].items()})
print('narrowed', [(r['locality'], round(r['cooks'], 3), round(r['stud'], 2)) for r in out['narrowed_out']])
print('regional', {k: (round(v['constant'], 2), round(v['se'], 2), v['n']) for k, v in out['regional_common_slope']['constants'].items()}, round(out['regional_common_slope']['multiplier'], 3))
for k in ['ceiling', 'lowest_dG', 'floor', 'highest_baseline', 'baseline_loss']:
    print(k, [(r['locality'], round(r['dG'], 2), round(r['B22'], 2)) for r in out[k]])
print('over22', len(out['over22']), 'house_over22', out['house_over22_count'], 'over26', out['over26_count'], out['sen_over26_count'], out['house_over26_count'])
print('implied', out['implied_sum'], out['n_implied_negative'], 'dS<0', out['dS_negative'], 'logpop r2', out['log_pop_r2'])
