import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = pd.read_csv('data/virginia_localities_final.csv'); A = json.load(open('out/analysis.json'))
ceil = {r['locality'] for r in A['ceiling']}; floor = {r['locality'] for r in A['floor']}
narrow = {r['locality'] for r in A['narrowed_out']}
OR, BL, GR = '#E07B00', '#1f5fbf', '#9a9a9a'
col = ['#E07B00' if l in ceil else '#1f5fbf' if l in floor else GR for l in d.locality]
note = 'US House 2022 vs 2026* (all districts summed per locality). Baseline = Democratic share of the prior governor race (PROXY: VA has no party registration). *2026 unofficial.'
def foot(fig): fig.text(0.01, 0.005, note, fontsize=7, color='#444')
P = 'graphs/'
# 1 slope
fig, ax = plt.subplots(figsize=(8, 10))
for _, r in d.iterrows():
    c = OR if r.locality in ceil else BL if r.locality in floor else GR
    ax.plot([0, 1], [r.G22, r.G26], color=c, lw=2 if c != GR else .6, alpha=1 if c != GR else .5)
    if c != GR: ax.text(1.02, r.G26, f"{r.locality} ({r.dG:+.2f})", fontsize=7, color=c, va='center')
ax.set_xticks([0, 1]); ax.set_xticklabels(['G 2022', 'G 2026*']); ax.set_xlim(-.1, 1.6); ax.axhline(0, color='k', lw=.5)
ax.set_ylabel('G = S − B (points)'); ax.set_title('Virginia: G 2022 → G 2026*, all 133 localities\norange = ceiling (5 largest ΔG), blue = floor (5 lowest baseline)')
foot(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(P + 'VA_Slope_G2022_to_G2026.png', dpi=130); plt.close()
# 2 dG by population
fig, ax = plt.subplots(figsize=(18, 6.5))
ax.bar(range(len(d)), d.dG, color=col); ax.axhline(0, color='k', lw=.6); ax.axhline(A['dG_summary']['median'], color='red', ls='--', lw=.8, label=f"median {A['dG_summary']['median']:+.2f}")
ax.set_xticks(range(len(d))); ax.set_xticklabels(d.locality, rotation=90, fontsize=5.5); ax.set_xlim(-1, len(d))
ax.set_ylabel('ΔG* (points)'); ax.set_title('Virginia ΔG*, all 133 counties and independent cities, largest to smallest population (orange ceiling, blue floor)'); ax.legend()
foot(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(P + 'VA_DeltaG_by_Population.png', dpi=120); plt.close()
# 3 fitted scatter
f = A['fit_all']; fn = A['fit_narrowed']
fig, ax = plt.subplots(figsize=(9, 6.5))
m = d.locality.isin(narrow)
ax.scatter(d.B_drop[~m], d.dG[~m], s=np.sqrt(d.pop2025[~m]) / 8, color=BL, alpha=.6, label='locality (size = population)')
ax.scatter(d.B_drop[m], d.dG[m], s=np.sqrt(d.pop2025[m]) / 8, facecolor='none', edgecolor='red', lw=1.2, label='narrowed out (Cook\'s D > 4/n)')
for _, r in d[m].iterrows(): ax.annotate(r.locality, (r.B_drop, r.dG), fontsize=6.5, xytext=(3, 3), textcoords='offset points')
xs = np.linspace(d.B_drop.min() - .5, d.B_drop.max() + .5, 50)
ax.plot(xs, f['constant'] + f['multiplier'] * xs, color='k', label=f"all 133: ΔG = {f['constant']:+.2f} + {f['multiplier']:.2f} × drop (R² {f['r2']:.3f})")
ax.plot(xs, fn['constant'] + fn['multiplier'] * xs, color='red', ls='--', label=f"narrowed n={fn['n']}: ΔG = {fn['constant']:+.2f} + {fn['multiplier']:.2f} × drop (R² {fn['r2']:.3f})")
ax.axhline(0, color='k', lw=.4); ax.set_xlabel('Baseline-share drop = B2022 − B2026 (points; negative = baseline rose) [PROXY]'); ax.set_ylabel('ΔG* (points)')
ax.set_title('Virginia statewide fitted equation (OLS, VA data only)'); ax.legend(fontsize=7.5, loc='lower right')
foot(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(P + 'VA_Fitted_Equation_Scatter.png', dpi=130); plt.close()
# 4 paired bars
fig, ax = plt.subplots(figsize=(18, 6.5)); x = np.arange(len(d))
ax.bar(x - .2, d.S22, .4, color=BL, label='S 2022'); ax.bar(x + .2, d.S26, .4, color=OR, label='S 2026*')
ax.set_xticks(x); ax.set_xticklabels(d.locality, rotation=90, fontsize=5.5); ax.set_xlim(-1, len(d)); ax.set_ylabel('Democratic share of US House votes (%)')
ax.set_title('Democratic share of the US House vote, 2022 vs 2026*, largest to smallest population'); ax.legend()
foot(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(P + 'VA_Paired_Bars_Dem_Share_2022_2026.png', dpi=120); plt.close()
# 5 residual bars
fig, ax = plt.subplots(figsize=(18, 6.5)); med = A['residual_summary']['median']
ax.axhspan(med - 3, med + 3, color='#eee'); ax.bar(x, d.residual, color=col); ax.axhline(med, color='red', ls='--', lw=.8, label=f'median {med:+.2f}; band = median ± 3')
ax.set_xticks(x); ax.set_xticklabels(d.locality, rotation=90, fontsize=5.5); ax.set_xlim(-1, len(d)); ax.set_ylabel('Residual = ΔG − baseline drop = S2026 − S2022 (points)')
ax.set_title('Residual after the baseline step, all 133 localities, largest to smallest population'); ax.legend()
foot(fig); fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(P + 'VA_Residual_Bars_by_Population.png', dpi=120); plt.close()
# 6 regional constants
rc = A['regional_common_slope']['constants']; names = sorted(rc, key=lambda k: rc[k]['constant'])
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(names, [rc[k]['constant'] for k in names], xerr=[rc[k]['se'] for k in names], color=BL, alpha=.8)
for i, k in enumerate(names): ax.text(rc[k]['constant'] + rc[k]['se'] + .1, i, f"{rc[k]['constant']:+.2f} (n={rc[k]['n']})", va='center', fontsize=8)
ax.set_xlabel(f"Regional constant (common multiplier {A['regional_common_slope']['multiplier']:.2f}), ± 1 SE"); ax.set_title('Virginia regional constants (one common multiplier)'); ax.axvline(0, color='k', lw=.5)
foot(fig); fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(P + 'VA_Regional_Constants.png', dpi=130); plt.close()
# 7 over-ballot check
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, yr, dr, bal in ((axs[0], '2022', 'D22', 'ballots22'), (axs[1], '2026*', 'D26', 'ballots26')):
    dd = d[dr] + d['R' + dr[1:]]; ratio = dd / d[bal]
    ax.scatter(d.pop2025, ratio, s=12, color=np.where(ratio > 1, 'red', BL)); ax.axhline(1, color='red', lw=.8)
    ax.set_xscale('log'); ax.set_xlabel('Population (log)'); ax.set_ylabel('(D + R US House votes) ÷ DOE ballots cast')
    ax.set_title(f'{yr}: {(ratio > 1).sum()} of 133 localities above 1.0')
for _, r in d[(d.D22 + d.R22) / d.ballots22 > 1.1].iterrows(): axs[0].annotate(r.locality, (r.pop2025, (r.D22 + r.R22) / r.ballots22), fontsize=7)
fig.suptitle('Texas-style check: Democratic + Republican votes vs DOE ballots cast'); foot(fig)
fig.tight_layout(rect=(0, .03, 1, .95)); fig.savefig(P + 'VA_Over_Ballot_Check.png', dpi=130); plt.close()
# 8 forward surplus (share version) S = m*(D/100) + b
FW = A['forward']
fig, axs = plt.subplots(1, 2, figsize=(14, 7), sharey=True)
for ax, yr, lab in ((axs[0], '22', '2022'), (axs[1], '26', '2026*')):
    q = FW[yr]; X = d['B' + yr]; Y = d['G' + yr]
    ax.scatter(X, Y, s=np.sqrt(d.pop2025) / 8, color=BL if yr == '22' else OR, alpha=.75, zorder=3, label='locality (size = population)')
    xs = np.linspace(X.min() - 2, X.max() + 2, 50); ys = q['m'] * xs / 100 + q['b']
    ax.fill_between(xs, ys - q['resid_sd'], ys + q['resid_sd'], color='#e6e6e6', zorder=0, label=f"±1 residual SD ({q['resid_sd']:.2f})")
    ax.plot(xs, ys, color='k', zorder=2, label=f"S = {q['m']:.2f} × (D/100) {'+' if q['b'] >= 0 else '−'} {abs(q['b']):.2f}\nR² {q['r2']:.3f}, mean |residual| {q['mean_abs_resid']:.2f}")
    ax.axhline(0, color='k', lw=.4); ax.set_xlabel(f"D = Democratic baseline share for 20{yr} (%) [PROXY: {'2021' if yr == '22' else '2025'} governor vote]")
    ax.set_title(f'{lab}: n = {q["n"]}'); ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(.5, -.13), ncol=1, frameon=False)
axs[0].set_ylabel('S = surplus G = House share − baseline share (points)')
fig.suptitle('Virginia forward surplus fit, share version S = m × (D/100) + b (OLS, VA data only)'); foot(fig)
fig.tight_layout(rect=(0, .03, 1, .95)); fig.savefig(P + 'VA_Forward_Surplus_Fit_S_vs_D.png', dpi=130); plt.close()
print('ok')
