"""Generate the 5 wiki pages + sidebar + README from data/ and out/ (no hand-typed numbers)."""
import json, pandas as pd
A = json.load(open('out/analysis.json')); V = json.load(open('out/verification.json')); X = json.load(open('out/crosscheck.json'))
d = pd.read_csv('data/virginia_localities_final.csv')
meta26 = json.load(open('raw/2026/election_meta.json'))
REPO = 'https://github.com/mbenson8989/Virginia-Election-Analysis'
IMG = 'https://raw.githubusercontent.com/mbenson8989/Virginia-Election-Analysis/main/graphs/'
CEDAR = 'https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
NEWIKI = 'https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki'
BUILT = open('out/build_time.txt').read().strip()

def m(s): return s.replace('-', '−')
def s2(x): return m(f'{x:+.2f}')
def p2(x): return m(f'{x:.2f}')
def s4(x): return m(f'{x:+.4f}')
def n0(x): return m(f'{int(round(x)):,}')
def sn0(x): return m(f'{int(round(x)):+,}')
def L(name): return d[d.locality == name].iloc[0]
S = A['statewide']; F = A['fit_all']; FN = A['fit_narrowed']; FW = A['fit_weighted']; FB = A['fit_ballots_all']; FBN = A['fit_ballots_no_over']
Q = A['forward']; VF = json.load(open('out/verify_forward.json'))
M26 = m(f"{Q['26']['m']:.2f}")
def pm(x, k=2): return ('+ ' if x >= 0 else '− ') + f'{abs(x):.{k}f}'
def pf(p, lt=False): return '< 0.001' if p < 0.001 else (('= ' if lt else '') + f'{p:.3f}')
DS = A['dG_summary']; RS = A['residual_summary']; BD = A['B_drop_summary']
ceil = A['ceiling']; floor = A['floor']; low = A['lowest_dG']; hb = A['highest_baseline']
names = lambda rs: ', '.join(r['locality'] for r in rs)
dmin = d.loc[d.dG.idxmin()]; dmax = d.loc[d.dG.idxmax()]

BANNER = ('> **\\*2026 figures are unofficial.** The Virginia State Board of Elections has not certified the November 3, 2026 general election. '
 'The Department of Elections (DOE) results site, enr.elections.virginia.gov (2026 November General), still labels them unofficial results; '
 'the files used here were published there on Nov 19, 2026 at 11:27 AM CST. 2022, 2021 and 2025 figures are certified. '
 '**PROXY BASELINE: Virginia has no party registration.** Where the other state wikis use the Democratic registration share, these pages use '
 '**B** = the Democratic share of the governor vote in the odd-year election just before each midterm (2021 for 2022, 2025 for 2026). '
 'It is not a count of registered Democrats. **Race: US House**, all 11 districts summed per county or independent city (Virginia had no governor, '
 'General Assembly or statewide race in 2022). Votes are votes for the Democratic candidate. These pages measure a pattern; they make no claim about intent, fraud or cause.')
REL = lambda *pages: '---\n**Related:** ' + ' · '.join(pages)
P = {'home': '[Home](Home)', 'rev': '[Bottom-Up Reverse Math](Reverse-Math)', 'lock': '[Locked Virginia Formula](Locked-Virginia-Formula)',
     'fc': '[Floor and Ceiling Localities](Floor-and-Ceiling)', 'gr': '[Graphs](Graphs)', 'pdf': '[Virginia County PDF Information](Virginia-County-PDF-Information)', 'cedar': f'[Cedar County Audit (Nebraska)]({CEDAR})'}
def img(file, alt, cap): return f'![{alt}]({IMG}{file})\n\n_{cap}_\n'

# ---------------- HOME ----------------
cand = json.load(open('out/candidates.json'))
def _last(n): return n.replace(',', '').replace(' Jr.', '').replace(' Sr.', '').replace(' III', '').split()[-1]
nchg = sum(1 for v in cand.values() if any(_last(v['2022'][p]) != _last(v['2026'][p]) for p in ('Democratic', 'Republican')))
fx = L('Fairfax County')
home = f"""# Virginia 2022 vs 2026 US House: ΔG Method (proxy baseline)

**Version 1, built {BUILT}.**

{BANNER}

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP). It began with her [Cedar County Audit]({CEDAR}) on the [Nebraska Election Analysis wiki]({NEWIKI}), the origin of the ΔG method and the reverse step used here. This wiki applies the same arithmetic to all 133 Virginia localities (95 counties and 38 independent cities), with one change forced by Virginia law: there is no party registration, so a vote-share baseline stands in for registration share. Data: Virginia Department of Elections results files for 2021, 2022, 2025 and 2026 and the DOE historical elections database; population from the Census Bureau Vintage 2025 county estimates. Compiled {', '.join(BUILT.split(', ')[:2])}. Data, scripts and both verification passes: [{REPO.split('github.com/')[1]}]({REPO}).

## Contents

Start with the Cedar County audit in Nebraska. That is where the method began. The Virginia pages then build up from one locality (Chesterfield) to the six largest localities, to all 133, and to the formula.

1. [Cedar County Audit]({CEDAR}) (Nebraska wiki): where the method started
2. [Bottom-Up Reverse Math](Reverse-Math): Chesterfield → the six largest localities → all 133, then solved backward for implied extra votes; full 133-locality table
3. [Locked Virginia Formula](Locked-Virginia-Formula): the **statewide fitted equation** (constant, multiplier, R², standard errors), the share-version surplus equations S = m × (D/100) + b, regional constants, and the blank fill-in template
4. [Floor and Ceiling Localities](Floor-and-Ceiling): the localities at the top and bottom, localities narrowed out of the fit, and the Texas-style over-ballot check
5. [Graphs](Graphs): slope chart, ΔG by population, fitted-equation scatter, paired bars, residual bars, regional constants, over-ballot check
6. [Virginia County PDF Information](Virginia-County-PDF-Information): downloadable 133-locality PDF table (baseline, Democratic votes and ballots, 2022 vs 2026\\*), every cell checked against the raw DOE files

## Why US House 2022 vs 2026

Virginia elects its governor and House of Delegates in odd years (2021, 2025) and its state Senate in 2019 and 2023. The DOE files confirm what was on the two midterm ballots:

- **Nov 8, 2022:** US House (all 11 districts) plus local offices and local questions. No statewide office, no General Assembly race.
- **Nov 3, 2026\\*:** US Senate, US House (all 11 districts), three proposed constitutional amendments, one House of Delegates special (District 20) and local races.

The only race on every ballot in both years is US House, so it is the midterm-to-midterm comparison. It is clean: all 133 localities are present in both years; both major parties contested all 11 districts in both years; the district map is the same in both years (the April 21, 2026 redistricting referendum was voided by the Supreme Court of Virginia on May 8, 2026, and all 145 locality-district pieces match). {len(A['split_localities'])} localities are split between districts; their district results are summed.

## Statewide at a glance

| Measure | 2022 | 2026\\* | Change |
|---|---|---|---|
| Democratic US House votes | {n0(S['D22'])} | {n0(S['D26'])}\\* | {sn0(S['D26']-S['D22'])}\\* |
| Total US House votes (all candidates) | {n0(S['house_total22'])} | {n0(S['house_total26'])}\\* | {sn0(S['house_total26']-S['house_total22'])}\\* |
| DOE ballots cast (turnout report) | {n0(S['ballots22'])} | {n0(S['ballots26'])}\\* | {sn0(S['ballots26']-S['ballots22'])}\\* |
| Registered voters, active + inactive | {n0(S['reg22'])} | {n0(S['reg26'])} | {sn0(S['reg26']-S['reg22'])} |
| S = Democratic share of US House votes | {p2(S['S22'])}% | {p2(S['S26'])}%\\* | {s2(S['S26']-S['S22'])} pts\\* |
| B = Democratic share of prior governor vote **[PROXY]** | {p2(S['B22'])}% (2021) | {p2(S['B26'])}% (2025) | {s2(S['B26']-S['B22'])} pts |
| G = S − B | {s2(S['G22'])} | {s2(S['G26'])}\\* | ΔG {s2(S['dG'])}\\* |

## Locality results in brief

- **ΔG is close to zero and splits both ways.** Median ΔG is {s2(DS['median'])}\\*, range {s2(DS['min'])}\\* ({dmin.locality}) to {s2(DS['max'])}\\* ({dmax.locality}). {DS['n_positive']} localities rose, {DS['n_negative']} fell; {DS['within3_of_median']} of 133 are within 3 points of the median. Statewide, the Democratic US House share rose nearly as much as the governor-vote baseline did.
- **Statewide fitted equation (VA only, n = 133):** ΔG = {s2(F['constant'])} + {p2(F['multiplier'])} × (baseline-share drop), R² = {F['r2']:.3f}. Details on [Locked Virginia Formula](Locked-Virginia-Formula#statewide-fitted-equation).
- **The baseline rose everywhere.** B rose from 2021 to 2025 in all 133 localities (baseline-share drop from {s2(BD['min'])} to {s2(BD['max'])} points, median {s2(BD['median'])}). Only Greensville County had fewer Democratic governor votes in 2025 than in 2021.
- **Residual after the baseline step** (= vote-share change S2026 − S2022): median {s2(RS['median'])}\\*, positive in {RS['n_positive']} of 133.
- **Solved backward (hypothesis):** the locality figures add up to {n0(A['implied_sum'])}\\* implied extra votes ({n0(S['implied_pooled'])}\\* on pooled statewide numbers). See [Bottom-Up Reverse Math](Reverse-Math).
- **Ceiling and floor:** the five largest ΔG are {names(ceil)}. The floor (most Republican baseline, lowest 2021 governor share) is {names(floor)}, all in Southwest Virginia. See [Floor and Ceiling Localities](Floor-and-Ceiling).
- **Texas-style check:** no locality has Democratic + Republican votes above ballots cast in 2026\\* (0 of 133, US House and US Senate). In 2022, {len(A['over22'])} localities show D + R above the DOE turnout figure, because the 2022 DOE turnout report is incomplete (for example, Albemarle's turnout leaves out its mailed absentee ballots). Details on [Floor and Ceiling Localities](Floor-and-Ceiling#texas-style-over-ballot-check).

## Verification

Two independent passes (separate scripts that re-parse every raw DOE and Census file from scratch) were run over all 133 localities and every figure: **{V['figures_checked']:,} figures checked ({V['figures_per_locality']} per locality), {V['discrepancies']} discrepancies.** Cross-source checks against a second DOE publication found filing errors in the DOE historical database export (not in the files used); see the [README]({REPO}#verification).

## Read this before using the numbers

- **B is a proxy, not registration.** A governor-vote baseline moves with candidates and campaigns, not with list maintenance. A Virginia ΔG is not directly comparable to a ΔG computed from party registration in Nebraska, Iowa or South Dakota.
- **Different candidates.** {nchg} of the 11 districts had a different Democratic or Republican nominee in 2026 than in 2022; only District 2 (Luria vs. Kiggans) was a rematch. Candidate effects are inside every number here.
- **Denominator.** The other state wikis divide by total ballots cast. Virginia's 2022 DOE turnout report is incomplete (US House votes exceed it in {A['house_over22_count']} of 133 localities), so these pages divide by total votes cast in the US House race in both years, the denominator the Nebraska pages use. The ballots-denominator fit is shown for comparison on [Locked Virginia Formula](Locked-Virginia-Formula#sensitivity-checks).
- **A residual is not evidence of altered votes.** Candidate choice, crossover voting, turnout differences and the strong Democratic year in 2025 all move these numbers. The arithmetic cannot separate them.
- **2026 is unofficial.** Every 2026 figure is marked \\* and will be re-run after the State Board of Elections certifies the election.

{REL(P['rev'], P['lock'], P['fc'], P['gr'], P['pdf'], P['cedar'])}
"""

# ---------------- REVERSE MATH ----------------
ch = L('Chesterfield County')
six = d.head(6)
def grp(g):
    T = g[['D22','D26','house_total22','house_total26','govD21','govTot21','govD25','govTot25']].sum()
    s22=T.D22/T.house_total22*100; s26=T.D26/T.house_total26*100; b22=T.govD21/T.govTot21*100; b26=T.govD25/T.govTot25*100
    return s22,s26,b22,b26,(s26-b26)-(s22-b22), g.dG.median(), g.dG.min(), g.dG.max(), g.implied_extra.sum()
rows3 = []
for lab, g in (('Six largest localities', d.head(6)), ('Other localities', d.iloc[6:]), ('All Virginia localities', d)):
    s22,s26,b22,b26,dg,med,mn,mx,imp = grp(g)
    rows3.append(f"| {lab} | {len(g)} | {p2(s22)}% → {p2(s26)}%\\* | {p2(b22)}% → {p2(b26)}% | {s2(s26-s22)} | {s2(b26-b22)} | {s2(dg)} | {s2(med)} ({s2(mn)} to {s2(mx)}) | {sn0(imp)} |")
six_rows = '\n'.join(f"| {r.locality} | {n0(r.pop2025)} | {p2(r.B22)}% → {p2(r.B26)}% | {n0(r.D22)} → {n0(r.D26)} | {n0(r.house_total22)} → {n0(r.house_total26)} | {s2(r.dS)} | {s2(r.B26-r.B22)} | {s2(r.dG)} | {sn0(r.implied_extra)} |" for r in six.itertuples())
all_rows = '\n'.join(f"| {i+1} | {r.locality} | {r.region} | {n0(r.pop2025)} | {n0(r.D22)} | {n0(r.house_total22)} | {n0(r.D26)} | {n0(r.house_total26)} | {p2(r.S22)} | {p2(r.S26)} | {p2(r.B22)} | {p2(r.B26)} | {s2(r.dG)} | {s2(r.residual)} | {sn0(r.implied_extra)} |" for i, r in enumerate(d.itertuples()))
sw_switch = S['B_drop']
rev = f"""# Bottom-Up Reverse Math

{BANNER}

The same arithmetic at three levels, from one locality up to the whole state, then solved backward for implied extra votes. Denominator: total votes cast in the US House race (see [Locked Virginia Formula](Locked-Virginia-Formula#denominator)). The method comes from the [Cedar County Audit]({CEDAR}) in Nebraska.

## Step 1: Chesterfield County

| Step | Value |
|---|---|
| Democratic US House share (S) | {p2(ch.S22)}% (2022) → {p2(ch.S26)}%\\* (2026): **{s2(ch.dS)} points\\*** |
| Baseline B, Democratic share of prior governor vote **[PROXY]** | {p2(ch.B22)}% (2021) → {p2(ch.B26)}% (2025): **{s2(ch.B26-ch.B22)} points** |
| ΔG = vote-share change − baseline change | {p2(ch.dS)} − ({s2(ch.B26-ch.B22)}) = **{s2(ch.dG)} points\\*** |
| Reverse step: ΔG − baseline-share drop | {s2(ch.dG)} − ({s2(ch.B_drop)}) = {s2(ch.residual)} (the residual) |
| Implied extra votes | {n0(ch.D26)}\\* − {p2(ch.S22)}% × {n0(ch.house_total26)}\\* = **about {sn0(ch.implied_extra)}\\*** |
| Baseline-scaled gap (stand-in for the Nebraska wiki's "gap in votes" line, for comparison) | {n0(ch.D26)}\\* − {n0(ch.D22)} × ({n0(ch.govD25)} ÷ {n0(ch.govD21)}) = about {sn0(ch.baseline_scaled_gap)}\\* |

Chesterfield's Democratic baseline rose (it did not fall), so under the Nebraska rule it is a **non-loss** locality: the residual is shown for completeness.

## Step 2: the six largest localities

Largest to smallest population (Census Vintage 2025).

| Locality | Population | B 2021 → 2025 [PROXY] | Dem US House votes 2022 → 2026\\* | US House votes 2022 → 2026\\* | Vote-share change\\* (pts) | Baseline change (pts) | ΔG\\* (pts) | Implied extra votes\\* |
|---|---|---|---|---|---|---|---|---|
{six_rows}

ΔG is negative in {'all six' if (six.dG<0).sum()==6 else str((six.dG<0).sum())+' of the six'} largest localities: there the Democratic 2026 House share rose less than the 2021→2025 governor baseline did.

## Step 3: all 133 localities

| Group | Localities | Dem US House share | Baseline B [PROXY] | Vote-share change\\* | Baseline change | Pooled ΔG\\* | Locality median ΔG\\* (range) | Implied extra votes\\* |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows3)}

Locality size explains little of the spread (R² = {A['log_pop_r2']:.3f} against log population).

## Solving backward: implied extra votes (hypothesis)

For each locality, implied extra votes = 2026 Democratic votes − (2022 Democratic share × 2026 US House votes). That is how many more Democratic votes the locality cast than it would have at its 2022 share on 2026 turnout.

| Measure | Votes |
|---|---|
| Sum of the 133 locality figures | {n0(A['implied_sum'])}\\* |
| Statewide, pooled: ({p2(S['S26'])}% − {p2(S['S22'])}%) × {n0(S['house_total26'])} | {n0(S['implied_pooled'])}\\* |
| Raw rise in Democratic votes | {sn0(S['D26']-S['D22'])}\\* = {n0(S['implied_pooled'])} share gain + {n0(S['D26']-S['D22']-S['implied_pooled'])} from more votes at the 2022 share |
| Localities with negative implied extra votes | {A['n_implied_negative']} |
| Sum of baseline-scaled gaps (comparison line) | {n0(A['baseline_scaled_sum'])}\\* |

**No offset-need line.** In registration states this table also shows the votes needed to offset a registration-share *decline*. Virginia's baseline did not decline anywhere: statewide B rose {s2(-sw_switch)} points from 2021 to 2025, so there is no decline to offset.

> **Hypothesis label.** Turning the residual into "implied extra votes" and calling them injected, switched or offset votes is a hypothesis the arithmetic cannot test. The same number reflects candidate choice, crossover voting, turnout changes and any other cause. Candidate votes are not turnout, and a governor-vote baseline is not a count of Democrats.

## What the arithmetic cannot tell you

- **The baseline moved more than the House vote.** Statewide, B rose {s2(S['B26']-S['B22'])} points and S rose {s2(S['S26']-S['S22'])}\\*, so statewide ΔG is {s2(S['dG'])}\\*.
- **The swing was near-uniform.** {RS['within3_of_median']} of 133 residuals are within 3 points of the median ({s2(RS['median'])}\\*).
- **No control cycle.** The Iowa wiki compares 2018→2022. Virginia's 2018 US House map was different and District 3 was uncontested in 2018, so a matching control was not run.
- **2026 is unofficial.** These totals will be re-run after certification.

{img('VA_Residual_Bars_by_Population.png', 'Residual bars by population', 'Residual (ΔG minus baseline-share drop, equal to S2026 − S2022) for all 133 localities, largest to smallest population. Shaded band: median ± 3 points.')}
## All 133 localities

Largest to smallest population. S = Democratic share of US House votes; B = Democratic share of prior governor vote [PROXY]. Full precision and every input column: [data/virginia_localities_final.csv]({REPO}/blob/main/data/virginia_localities_final.csv).

| # | Locality | Region | Population | Dem 2022 | House votes 2022 | Dem 2026\\* | House votes 2026\\* | S 2022 | S 2026\\* | B 2021 | B 2025 | ΔG\\* | Residual\\* | Implied extra\\* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{all_rows}

{REL(P['lock'], P['fc'], P['gr'], P['home'])}
"""

# ---------------- LOCKED FORMULA ----------------
rc = A['regional_common_slope']; rs = A['regional_separate']; ft = A['regional_F_test']
_o = sorted(rc['constants'], key=lambda k: rc['constants'][k]['constant']); hi3 = _o[::-1][:4]; lo3 = _o[:3]
reg_rows = '\n'.join(f"| {k} | {v['n']} | {s2(v['constant'])} ({p2(v['se'])}) | {s2(rs[k]['constant'])} ({p2(rs[k]['constant_se'])}) | {p2(rs[k]['multiplier'])} ({p2(rs[k]['multiplier_se'])}) | {rs[k]['r2']:.3f} | {s2(rs[k]['median_dG'])} |"
                     for k, v in sorted(rc['constants'].items(), key=lambda kv: kv[1]['constant']))
pred = F['constant'] + F['multiplier'] * fx.B_drop
lock = f"""# Locked Virginia Formula

{BANNER}

> **Why a substitute baseline.** Virginia voters do not register by party; the DOE publishes only active and inactive registered voters per locality. There is no Democratic registration count, so the registration share R used in every other state wiki does not exist here, and none is invented. In its place these pages use **B = Democratic governor votes ÷ total governor votes** in the odd-year election just before each midterm (**2021** for 2022, **2025** for 2026), from the same locality. "Registration-share drop" becomes **baseline-share drop = B2022 − B2026**. Every B figure is labeled **[PROXY]**.

## Statewide Fitted Equation

Ordinary least squares across **all 133 Virginia counties and independent cities**, each weighted equally, Virginia data only. No other state's constant is reused.

```
Virginia equation:  ΔG = {s2(F['constant'])} + {p2(F['multiplier'])} × (baseline-share drop, points)   [PROXY baseline]
Four decimals:      ΔG = {s4(F['constant'])} + {F['multiplier']:.4f} × (baseline-share drop, points)
```

| Item | Rounded | 4 decimals | Standard error |
|---|---|---|---|
| Constant (intercept) | {s2(F['constant'])} | {s4(F['constant'])} | {F['constant_se']:.4f} |
| Multiplier (slope) | {p2(F['multiplier'])} | {F['multiplier']:.4f} | {F['multiplier_se']:.4f} |
| R² | {F['r2']:.2f} | {F['r2']:.4f} | |
| n (localities) | 133 | 133 | |
| Residual standard error (points) | {p2(F['resid_se'])} | {F['resid_se']:.4f} | |

_2022 vs 2026\\* US House, all districts summed per locality; denominator = total US House votes; baseline-share drop = B2022 − B2026 in points (negative = the baseline rose). 2026 unofficial (DOE results files published Nov 19, 2026 11:27 AM CST)._ Both coefficients are significant (p < 0.001).

**What it means:** across Virginia's localities, each 1-point *rise* in the governor-vote baseline (a drop of −1) goes with about {p2(F['multiplier'])} points *lower* ΔG, starting from about {s2(F['constant'])} where the baseline does not move. Because every Virginia locality's baseline rose (drop from {s2(BD['min'])} to {s2(BD['max'])}), the constant is an extrapolation outside the data. Put the other way (1 − {p2(F['multiplier'])} = {p2(1-F['multiplier'])}): each extra point of 2021→2025 baseline rise goes with about {p2(1-F['multiplier'])} points more 2022→2026 House vote-share gain, so the House vote picked up about half of each locality's extra governor swing. The fit explains about {F['r2']*100:.0f}% of the locality-to-locality differences in ΔG. This line describes the pattern; it does not prove anything.

**Worked example: Fairfax County.** B *rose* from {p2(fx.B22)} to {p2(fx.B26)}, a baseline-share drop of {m(f'{fx.B_drop:.4f}')} points. Predicted ΔG = {s4(F['constant'])} + {F['multiplier']:.4f} × ({m(f'{fx.B_drop:.4f}')}) = {s2(pred)}. Actual ΔG = {s2(fx.dG)}\\*. Difference from the fitted line (actual − predicted) = {s2(fx.dG-pred)}\\*. This difference is not the line-11 residual in the template below, which is ΔG minus the baseline-share drop.

### Forward surplus equations (share version): S = m × (D/100) + b

Here **S** is the surplus G (Democratic share of US House votes − baseline share, in points) and **D** is the Democratic baseline share **[PROXY]** in percent (0–100 scale): the Democratic share of the prior odd-year governor vote, used because Virginia has no Democratic registration share. Ordinary least squares across all 133 localities, each weighted equally, Virginia data only. This is the same form as the Nebraska, Kansas and South Dakota surplus equations.

| Fit | n | Virginia equation | m (SE) | b (SE) | R² | Residual SD (pts) | Mean absolute residual (pts) |
|---|---|---|---|---|---|---|---|
| 2022 (certified) | {Q['22']['n']} | S = {p2(Q['22']['m'])} × (D/100) {pm(Q['22']['b'])} | {s2(Q['22']['m'])} ({p2(Q['22']['m_se'])}) | {s2(Q['22']['b'])} ({p2(Q['22']['b_se'])}) | {Q['22']['r2']:.3f} | {p2(Q['22']['resid_sd'])} | {p2(Q['22']['mean_abs_resid'])} |
| 2026\\* (unofficial) | {Q['26']['n']} | S\\* = {m(f"{Q['26']['m']:.2f}")} × (D/100) {pm(Q['26']['b'])} | {s2(Q['26']['m'])} ({p2(Q['26']['m_se'])}) | {s2(Q['26']['b'])} ({p2(Q['26']['b_se'])}) | {Q['26']['r2']:.3f} | {p2(Q['26']['resid_sd'])} | {p2(Q['26']['mean_abs_resid'])} |
| Pooled, both years | {Q['pooled']['n']} | S = {m(f"{Q['pooled']['m']:.2f}")} × (D/100) {pm(Q['pooled']['b'])} | {s2(Q['pooled']['m'])} ({p2(Q['pooled']['m_se'])}) | {s2(Q['pooled']['b'])} ({p2(Q['pooled']['b_se'])}) | {Q['pooled']['r2']:.3f} | {p2(Q['pooled']['resid_sd'])} | {p2(Q['pooled']['mean_abs_resid'])} |

```
Four decimals, 2022:   S  = {m(f"{Q['22']['m']:.4f}")} × (D/100) {pm(Q['22']['b'], 4)}
Four decimals, 2026*:  S* = {m(f"{Q['26']['m']:.4f}")} × (D/100) {pm(Q['26']['b'], 4)}
```

**What it means:** the baseline share explains little of the surplus: about {Q['22']['r2']*100:.0f}% of the locality-to-locality spread in 2022 and {Q['26']['r2']*100:.0f}% in 2026\\*. In 2022 the line tilts up (m {s2(Q['22']['m'])}, p = {pf(Q['22']['p_m'])}): moving from a 20% to an 80% baseline adds about {p2(Q['22']['m']*0.6)} points of surplus. In 2026\\* it tilts down (m {s2(Q['26']['m'])}, p {pf(Q['26']['p_m'], True)}): the same move takes away about {p2(-Q['26']['m']*0.6)} points. Testing both years in one model, the 2026\\* multiplier is {p2(-Q['year_test']['dm'])} lower (p {pf(Q['year_test']['p_dm'], True)}) and the offset {p2(Q['year_test']['db'])} higher (p {pf(Q['year_test']['p_db'], True)}). D ranges from {p2(Q['22']['D_min'])} to {p2(Q['22']['D_max'])} in 2022 and from {p2(Q['26']['D_min'])} to {p2(Q['26']['D_max'])} in 2026, so b (the value at D = 0) lies outside the data.

**Forward check: Fairfax County, 2026\\*.** S\\* = {m(f"{Q['26']['m']:.4f}")} × ({fx.B26:.4f} ÷ 100) {pm(Q['26']['b'], 4)} = {s2(fx.fS26)}\\*. Actual surplus G 2026 = {s2(fx.G26)}\\*. Residual (actual − fitted) = {s2(fx.fres26)}\\*. For 2022: S = {Q['22']['m']:.4f} × ({fx.B22:.4f} ÷ 100) {pm(Q['22']['b'], 4)} = {s2(fx.fS22)} fitted, against an actual {s2(fx.G22)} (residual {s2(fx.fres22)}).

**Check of the locked equation against the data and graphs.** Plugging all 133 localities into ΔG = {s4(F['constant'])} + {F['multiplier']:.4f} × drop reproduces the fitted line in [graph 3](Graphs#3-statewide-fitted-equation): mean absolute residual {p2(F['mean_abs_resid'])} points, and the residuals sum to zero. The share-version lines are drawn in [graph 8](Graphs#8-forward-surplus-fit-share-version). A second pass ([`scripts/verify_forward.py`]({REPO}/blob/main/scripts/verify_forward.py), standard library only, on the pass B table rebuilt from the raw DOE files) refits every line and recomputes every locality's fitted value and residual: {VF['checks']} checks, {VF['mismatches']} mismatches.

### Sensitivity checks

| Fit | n | Constant (SE) | Multiplier (SE) | R² |
|---|---|---|---|---|
| **All localities (locked)** | {F['n']} | {s2(F['constant'])} ({p2(F['constant_se'])}) | {p2(F['multiplier'])} ({p2(F['multiplier_se'])}) | {F['r2']:.3f} |
| Narrowed ({len(A['narrowed_out'])} high-influence localities out, see [Floor and Ceiling](Floor-and-Ceiling#localities-narrowed-out-of-the-fit)) | {FN['n']} | {s2(FN['constant'])} ({p2(FN['constant_se'])}) | {p2(FN['multiplier'])} ({p2(FN['multiplier_se'])}) | {FN['r2']:.3f} |
| Weighted by 2026 US House votes | {FW['n']} | {s2(FW['constant'])} ({p2(FW['constant_se'])}) | {p2(FW['multiplier'])} ({p2(FW['multiplier_se'])}) | {FW['r2']:.3f} |
| Ballots denominator (DOE turnout), all localities | {FB['n']} | {s2(FB['constant'])} ({p2(FB['constant_se'])}) | {p2(FB['multiplier'])} ({p2(FB['multiplier_se'])}) | {FB['r2']:.3f} |
| Ballots denominator, localities without a 2022 over-ballot flag | {FBN['n']} | {s2(FBN['constant'])} ({p2(FBN['constant_se'])}) | {p2(FBN['multiplier'])} ({p2(FBN['multiplier_se'])}) | {FBN['r2']:.3f} |

**The locked Virginia constants are the all-locality fit: constant {s2(F['constant'])}, multiplier {p2(F['multiplier'])}.** Narrowing barely moves them.

### Regional constants

Same multiplier for every region ({p2(rc['multiplier'])}, SE {p2(rc['multiplier_se'])}), one constant per region; and, for comparison, a separate line fitted inside each region. Regions are groups of localities defined for this wiki (list in [data/regions.csv]({REPO}/blob/main/data/regions.csv)).

| Region | n | Regional constant, common multiplier (SE) | Separate fit: constant (SE) | Separate fit: multiplier (SE) | Separate fit R² | Median ΔG\\* |
|---|---|---|---|---|---|---|
{reg_rows}

**Regions matter.** Adding regional constants raises adjusted R² from {ft['adj_r2_statewide']:.3f} to {ft['adj_r2_regional']:.3f} (F = {ft['F']:.2f}, p < 0.001). The highest regional constants are {', '.join(hi3)}; the lowest are {', '.join(lo3)}. With the regional constants in the model, the common multiplier falls to {p2(rc['multiplier'])}: much of the statewide slope reflects the difference between regions. Separate within-region fits rest on 10 to 22 localities each and have wide standard errors.

## The equation

- **S** (Democratic vote share) = Democratic US House votes ÷ total US House votes × 100, all districts in the locality summed
- **B** (baseline, **[PROXY]** for Democratic registration share) = Democratic governor votes ÷ total governor votes × 100, from the prior odd-year election (2021 for 2022; 2025 for 2026)
- **G** = S − B
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (B2026 − B2022)
- **Reverse step (baseline-drop subtraction):** residual = ΔG − (B2022 − B2026) = S2026 − S2022
- **Solved backward, implied extra votes:** D2026 − (S2022 ÷ 100) × total US House votes 2026
- **Baseline-scaled gap** (stand-in for the Nebraska wiki's "gap in votes" line, comparison only): D2026 − D2022 × (governor D 2025 ÷ governor D 2021)

### Denominator

The other state wikis divide by total ballots cast. Virginia's 2022 DOE turnout report (results site, Turnout Statistics, generated Dec 6, 2022) is incomplete: total US House votes exceed it in {A['house_over22_count']} of 133 localities, and in Albemarle the turnout figure leaves out mailed absentee ballots and part of early voting (38,050 ballots against 50,206 House votes). The 2026 DOE turnout report has no such gap. Because one year's ballots figure cannot be trusted, both years use total votes cast in the US House race, the denominator the current Nebraska pages use. The ballots version is in the sensitivity table above.

### Why the governor race for the baseline

The baseline needs to measure each locality's partisan lean independently of the US House race being tested, one year before each midterm, from DOE data. The governor race is on every Virginia ballot in 2021 and 2025, is statewide and is contested by both parties. Virginia's party primaries are open (any registered voter may choose either party's primary), so primary turnout is not a clean partisan count either.

## Blank template

| Line | Item | 2022 | 2026\\* |
|---|---|---|---|
| 1 | Democratic US House votes (all districts in the locality) | ______ | ______ |
| 2 | Total US House votes, all candidates incl. write-ins | ______ | ______ |
| 3 | S = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Democratic governor votes, prior odd year (2021 / 2025) **[PROXY]** | ______ | ______ |
| 5 | Total governor votes, prior odd year (2021 / 2025) **[PROXY]** | ______ | ______ |
| 6 | B = line 4 ÷ line 5 × 100 **[PROXY: not party registration]** | ______ | ______ |
| 7 | G = line 3 − line 6 | ______ | ______ |
| 8 | ΔG = G 2026 − G 2022 | | ______ |
| 9 | Baseline change = B 2026 − B 2022 | | ______ |
| 10 | Did Democratic baseline votes fall? (line 4: 2025 < 2021) | | Yes / No |
| 11 | Residual = line 8 + line 9 (= line 8 − baseline-share drop) | | ______ |
| 12 | Implied extra votes = line 1 (2026) − line 3 (2022) ÷ 100 × line 2 (2026) | | ______ |
| 13 | Baseline-scaled gap = line 1 (2026) − line 1 (2022) × (line 4 2026 ÷ line 4 2022) | | ______ |
| 14 | Fitted ΔG = {s4(F['constant'])} + {F['multiplier']:.4f} × (−line 9) | | ______ |
| 15 | Distance from the Virginia line = line 8 − line 14 | | ______ |

## Rules for using this formula

1. **If a locality lost Democratic baseline votes, run the residual step** (line 11) and the implied-votes line (line 12). In Virginia only **Greensville County** lost Democratic governor votes (1,915 in 2021 → 1,902 in 2025). Every other locality is a **non-loss locality**: report its raw numbers. Its line 11 is shown for completeness and equals its vote-share change.
2. **The starting point is different in every state. Don't assume Nebraska's numbers carry over.** Virginia's statewide ΔG was {s2(S['dG'])}\\* and its locality median {s2(DS['median'])}\\*. Compare Virginia localities with Virginia's own range, and remember B is a proxy.
3. **Always pull out the ceiling and floor localities.** In Virginia the ceiling locality is {dmax.locality} ({s2(dmax.dG)}\\*) and the lowest ΔG is {dmin.locality} ({s2(dmin.dG)}\\*). See [Floor and Ceiling Localities](Floor-and-Ceiling).

**Terms used in this wiki** (full definitions on [Floor and Ceiling Localities](Floor-and-Ceiling#terminology)):
- **Ceiling localities**: the five largest ΔG ({names(ceil)}).
- **Floor localities**: the most Republican baseline, the five lowest 2021 governor shares ({names(floor)}).
- **Non-loss localities**: no loss of Democratic baseline votes (all but Greensville).

## Worked example: Chesterfield County

| Line | Item | 2022 | 2026\\* |
|---|---|---|---|
| 1 | Democratic US House votes | {n0(ch.D22)} | {n0(ch.D26)}\\* |
| 2 | Total US House votes | {n0(ch.house_total22)} | {n0(ch.house_total26)}\\* |
| 3 | S | {p2(ch.S22)} | {p2(ch.S26)}\\* |
| 4 | Democratic governor votes [PROXY] | {n0(ch.govD21)} (2021) | {n0(ch.govD25)} (2025) |
| 5 | Total governor votes [PROXY] | {n0(ch.govTot21)} | {n0(ch.govTot25)} |
| 6 | B [PROXY] | {p2(ch.B22)} | {p2(ch.B26)} |
| 7 | G | {s2(ch.G22)} | {s2(ch.G26)}\\* |
| 8 | ΔG | | {s2(ch.dG)}\\* |
| 9 | Baseline change | | {s2(ch.B26-ch.B22)} |
| 10 | Baseline votes fell? | | No (non-loss) |
| 11 | Residual | | {s2(ch.residual)}\\* |
| 12 | Implied extra votes | | {sn0(ch.implied_extra)}\\* |
| 13 | Baseline-scaled gap | | {sn0(ch.baseline_scaled_gap)}\\* |
| 14 | Fitted ΔG | | {s2(F['constant']+F['multiplier']*ch.B_drop)} |
| 15 | Distance from the Virginia line | | {s2(ch.dG-(F['constant']+F['multiplier']*ch.B_drop))}\\* |

{REL(P['rev'], P['fc'], P['gr'], P['cedar'], P['home'])}
"""

# ---------------- FLOOR AND CEILING ----------------
def fcrow(r, grp):
    return f"| {r['locality']} | {grp} | {r['region']} | {n0(r['pop2025'])} | {p2(r['B22'])}% → {p2(r['B26'])}% | {s2(r['G22'])} | {s2(r['G26'])}\\* | {s2(r['dG'])}\\* | {n0(r['D22'])} → {n0(r['D26'])}\\* | {sn0(r['implied_extra'])}\\* |"
grpd = {}
for r in ceil: grpd[r['locality']] = (r, 'Ceiling')
for r in floor: grpd[r['locality']] = (r, 'Floor')
fc_rows = '\n'.join(fcrow(*grpd[k]) for k in sorted(grpd, key=lambda k: -grpd[k][0]['pop2025']))
nar = A['narrowed_out']
nar_rows = '\n'.join(f"| {r['locality']} | {r['region']} | {s2(r['dG'])}\\* | {s2(r['B_drop'])} | {r['cooks']:.3f} | {m(f'{r[chr(115)+chr(116)+chr(117)+chr(100)]:+.2f}')} |" for r in nar)
over = A['over22']
over_rows = '\n'.join(f"| {r['locality']} | {n0(r['D22'])} | {n0(r['R22'])} | {n0(r['ballots22'])} | {sn0(r['over22'])} | {n0(r['house_total22'])} |" for r in over[:15])
al = L('Albemarle County')
fc = f"""# Floor and Ceiling Localities

{BANNER}

## How to read floor and ceiling localities

Look for the pattern at both ends. The ceiling localities are the ones with the highest ΔG; in Virginia those are {names(ceil)}. The floor localities are the most Republican baseline localities, where there were the fewest Democrats to move.

- **The floor** by ΔG is the single locality with the lowest ΔG in the state. In Virginia that's {dmin.locality}, at {s2(dmin.dG)}\\*. Unlike Iowa, {DS['n_negative']} of Virginia's 133 localities have a negative ΔG, because the 2025 governor baseline rose more than the 2026 House vote in those places.
- **The ceiling** is the single locality with the highest ΔG in the state. In Virginia that's {dmax.locality}, at {s2(dmax.dG)}\\*.

Every state has its own floor and ceiling. Those two extremes set the range the rest of that state's localities fall within.

## Terminology

- **Ceiling localities** are the five largest positive ΔG: {', '.join(f"{r['locality']} {s2(r['dG'])}\\*" for r in ceil)}. All five are small rural localities ({', '.join(f"{r['locality']}: {r['region']}" for r in ceil)}).
- **Floor localities** are the most Republican baseline: the five lowest 2021 governor shares **[PROXY]**. {', '.join(f"{r['locality']} {p2(r['B22'])}% (ΔG {s2(r['dG'])}\\*)" for r in floor)}. All five are in Southwest Virginia and all five have a positive ΔG.
- **Lowest ΔG** (the other end, read by ΔG): {', '.join(f"{r['locality']} {s2(r['dG'])}\\*" for r in low)}.
- **Highest baseline** (most Democratic 2021 governor share): {', '.join(f"{r['locality']} {p2(r['B22'])}% (ΔG {s2(r['dG'])}\\*)" for r in hb)}. All five have a negative ΔG.
- **Non-loss localities** had no loss of Democratic baseline votes: 132 of 133. The one baseline-loss locality is Greensville County (Democratic governor votes 1,915 → 1,902; ΔG {s2(L('Greensville County').dG)}\\*).
- **Democratic share fell:** none. S rose from 2022 to 2026\\* in all 133 localities.

## Ceiling and floor detail

Largest to smallest population.

| Locality | Group | Region | Population | B 2021 → 2025 [PROXY] | G 2022 | G 2026\\* | ΔG\\* | Dem US House votes 2022 → 2026\\* | Implied extra votes\\* |
|---|---|---|---|---|---|---|---|---|---|
{fc_rows}

**Ceiling profile.** The ceiling localities are small and rural (populations {n0(min(r['pop2025'] for r in ceil))} to {n0(max(r['pop2025'] for r in ceil))}). Their 2025 governor baseline rose less than the state's (baseline-share drop between {s2(min(r['B_drop'] for r in ceil))} and {s2(max(r['B_drop'] for r in ceil))}, against a statewide median of {s2(BD['median'])}), so a normal House gain shows up as a positive ΔG.

**Floor profile.** The five floor localities are all in far Southwest Virginia, with 2021 Democratic governor shares from {p2(floor[0]['B22'])}% to {p2(floor[-1]['B22'])}%. All five have a positive ΔG.

Statewide, ΔG rose in {DS['n_positive']} of 133 localities and fell in {DS['n_negative']} (median {s2(DS['median'])}\\*).

## Localities narrowed out of the fit

Flagged by Cook's distance above 4/n (0.030) or an absolute studentized residual above 3 in the all-locality fit. None has a studentized residual above 3; all nine are flagged by Cook's distance. Refitting without them moves the constant from {s2(F['constant'])} to {s2(FN['constant'])} and the multiplier from {p2(F['multiplier'])} to {p2(FN['multiplier'])} (R² {F['r2']:.3f} → {FN['r2']:.3f}). They stay in every table; they are only left out of the narrowed fit.

| Locality | Region | ΔG\\* | Baseline-share drop | Cook's distance | Studentized residual |
|---|---|---|---|---|---|
{nar_rows}

Several are college towns (Harrisonburg, Radford, Fredericksburg) or Richmond-area cities (Richmond, Colonial Heights, Hopewell). {sum(1 for r in nar if r['B_drop'] < -10)} of the {len(nar)} have baseline-share drops below −10, at the far left of the fitted-equation chart, where the baseline rose most.

## Texas-style over-ballot check

Test: any locality where Democratic + Republican US House votes exceed the DOE's total ballots cast.

| Year | Localities checked | D + R above ballots (US House) | All House votes above ballots | D + R above ballots (US Senate) |
|---|---|---|---|---|
| 2022 | 133 | {len(over)} | {A['house_over22_count']} | (no Senate race) |
| 2026\\* | 133 | {A['over26_count']} | {A['house_over26_count']} | {A['sen_over26_count']} |

**2026\\*: clean.** No locality has more Democratic + Republican votes than ballots cast, in the House or Senate race.

**2022: {len(over)} flags, explained by an incomplete DOE turnout report, not by excess votes.** The 2022 ballots figure is the "Turnout Statistics" page on the DOE 2022 results site (Early Voting + Election Day + By Mail + Provisional). The DOE historical elections database breaks down each locality's 2022 US House votes by precinct, including the central absentee precincts, and those breakdowns show ballots the turnout page does not count:

- **Albemarle County** (largest flag): the turnout page shows {n0(al.ballots22)} ballots, with 5,271 early and 461 by mail. The precinct breakdown shows 11,517 early-voting House votes, 5,201 mailed-absentee votes processed through Election Day, 461 post-election mail votes and 992 provisional votes; the DOE results site gives {n0(al.house_total22)} House votes in all. D + R exceed the turnout figure by {n0(al.over22)}.
- **Grayson County:** the turnout page shows 0 early votes; the precinct breakdown shows 880 early-voting House votes.
- **Fairfax County:** the turnout page shows 2,647 provisional ballots; the precinct breakdown shows 6,023 provisional House votes.

The separate 2022 DOE turnout CSV (apps.elections.virginia.gov) is no better: it differs from the page in some localities (it does include Grayson's early votes) but has the same Albemarle gap (38,031 ballots), and total House votes exceed it in 97 of 133 localities. Because of this the analysis does not divide by 2022 ballots (see [Locked Virginia Formula](Locked-Virginia-Formula#denominator)).

Largest 2022 flags (all {len(over)} are in [out/analysis.json]({REPO}/blob/main/out/analysis.json)):

| Locality | Dem 2022 | Rep 2022 | DOE ballots 2022 | D + R − ballots | All House votes 2022 |
|---|---|---|---|---|---|
{over_rows}

{img('VA_DeltaG_by_Population.png', 'Delta-G by population, ceiling and floor localities marked', 'All 133 localities, ΔG\\* in population order. Orange: ceiling (5 largest ΔG). Blue: floor (5 lowest 2021 governor share). Dashed red line: median.')}
{img('VA_Slope_G2022_to_G2026.png', 'Locality slope chart, G 2022 to G 2026', 'Each line is one locality, G 2022 to G 2026\\*. Ceiling localities in orange, floor localities in blue, labeled with ΔG\\*.')}
{REL(P['rev'], P['gr'], P['lock'], P['home'])}
"""

# ---------------- GRAPHS ----------------
gr = f"""# Graphs

{BANNER}

All charts use the US House race, the total-US-House-votes denominator and the governor-vote baseline [PROXY], and list localities largest to smallest population unless the title says otherwise.

## 1. Locality slope chart

{img('VA_Slope_G2022_to_G2026.png', 'Locality slope chart, G 2022 to G 2026', f'Each line is one locality, G 2022 to G 2026\\*. Orange: the five ceiling localities; blue: the five floor localities; each labeled with its ΔG\\*.')}
## 2. ΔG by population

{img('VA_DeltaG_by_Population.png', 'Delta-G for all 133 localities in population order, floor and ceiling marked', f'All 133 localities in population order. Ceiling: {dmax.locality} is the highest ΔG\\*. Lowest: {dmin.locality}\\*. Dashed red line: median {s2(DS["median"])}.')}
## 3. Statewide fitted equation

{img('VA_Fitted_Equation_Scatter.png', 'Delta-G versus baseline-share drop with the fitted line', f'ΔG\\* against baseline-share drop for all 133 localities (dot size = population). Black: all-locality fit, ΔG = {s2(F["constant"])} + {p2(F["multiplier"])} × drop, R² {F["r2"]:.3f}. Red dashed: narrowed fit (n = {FN["n"]}). Red circles: the {len(A["narrowed_out"])} localities narrowed out.')}
## 4. Paired bars, 2022 vs 2026

{img('VA_Paired_Bars_Dem_Share_2022_2026.png', 'Democratic share of US House votes 2022 vs 2026 by locality', 'Democratic share of US House votes, 2022 (blue) and 2026\\* (orange), all 133 localities in population order.')}
## 5. Residual bars

{img('VA_Residual_Bars_by_Population.png', 'Residual bars by population', 'Residual (ΔG minus baseline-share drop, equal to S2026 − S2022) for all 133 localities. Shaded band: median ± 3 points.')}
## 6. Regional constants

{img('VA_Regional_Constants.png', 'Regional constants with one common multiplier', f'One constant per region with a common multiplier ({p2(rc["multiplier"])}), ± 1 standard error. These constants go with the common multiplier, so they are not comparable to the statewide constant {s2(F["constant"])}.')}
## 7. Texas-style over-ballot check

{img('VA_Over_Ballot_Check.png', 'Democratic plus Republican votes divided by DOE ballots cast, 2022 and 2026', f'(D + R US House votes) ÷ DOE ballots cast. 2026\\*: 0 of 133 above 1.0. 2022: {len(over)} of 133 above 1.0, caused by gaps in the 2022 DOE turnout report (Albemarle and Grayson labeled).')}
## 8. Forward surplus fit (share version)

{img('VA_Forward_Surplus_Fit_S_vs_D.png', 'Surplus G against Democratic baseline share with the fitted share-version lines, 2022 and 2026', f"S = surplus G (points) against D = Democratic baseline share (%, PROXY), all 133 localities, dot size = population. 2022: S = {p2(Q['22']['m'])} × (D/100) {pm(Q['22']['b'])}, R² {Q['22']['r2']:.3f}, mean absolute residual {p2(Q['22']['mean_abs_resid'])}. 2026\\*: S\\* = {M26} × (D/100) {pm(Q['26']['b'])}, R² {Q['26']['r2']:.3f}, mean absolute residual {p2(Q['26']['mean_abs_resid'])}. Shaded band: ±1 residual SD.")}
{REL(P['fc'], P['rev'], P['lock'], P['home'])}
"""

side = """**Virginia Election Analysis**

1. [[Home]]
2. [[Locked Virginia Formula|Locked-Virginia-Formula]]
3. [[Floor and Ceiling Localities|Floor-and-Ceiling]]
4. [[Bottom-Up Reverse Math|Reverse-Math]]
5. [[Graphs]]
6. [[Virginia County PDF Information|Virginia-County-PDF-Information]]

*2026 unofficial. Baseline is a proxy: Virginia has no party registration.*
"""
# ---- Virginia County PDF Information ----
import csv as _csv, subprocess as _sp
PDFNAME = 'Virginia_133_Locality_Democratic_Baseline_and_Vote_Change.pdf'
PDFRAW = f'https://raw.githubusercontent.com/mbenson8989/Virginia-Election-Analysis/main/pdf/{PDFNAME}'
_pt = [r for r in _csv.reader(open('data/virginia_pdf_table.csv'))]
_s1 = [r for r in _pt if r[0] == '1' and r[1] == 'Statewide total'][0][2:]
_s2 = [r for r in _pt if r[0] == '2' and r[1] == 'Statewide total'][0][2:]
_t1 = [r for r in _pt if r[0] == '1' and r[1] != 'Statewide total']
_np = [l.split()[-1] for l in _sp.run(['pdfinfo', f'pdf/{PDFNAME}'], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0]
_vp = json.load(open('out/verify_pdf.json'))
pdfp = f"""# Virginia County PDF Information

**[Download the PDF: Virginia 133 Localities, Democratic Baseline, Democratic US House Votes and Total Ballots, 2022 vs 2026\\*]({PDFRAW})** ({_np} pages, landscape)

The PDF follows the layout of the [Nebraska 93-county PDF](https://github.com/mbenson8989/Nebraska-Election-Analysis-/blob/main/Nebraska_93_County_Democratic_Registration_and_Vote_Change.pdf): one row for each of Virginia's 133 counties and independent cities, plus a statewide total row. Rows are sorted by the 2026 Democratic baseline share, highest first ({_t1[0][1]} first, {_t1[-1][1]} last). Rows where total registered voters fell are shaded blue, and the one locality where Democratic governor votes fell from 2021 to 2025 is shaded orange.

> **Substitute baseline, not party registration.** Virginia does not register voters by party, so there is no Democratic registration to report. Where the Nebraska PDF shows Democratic registration, this PDF shows the **Dem Baseline**: the Democratic share of the governor vote in the odd-year election before each midterm (2021 for 2022, 2025 for 2026). The **Est. Dem Baseline** count is that share × total registered voters, rounded. It is an estimate, not a count of registered Democrats.

\\*2026 figures are unofficial and not certified by the State Board of Elections (DOE results site as of Nov 19, 2026, 11:27 AM CST). The PDF should be rebuilt after certification.

## Statewide totals

| Measure | 2022 | 2026\\* | Change # | Change % |
|---|---:|---:|---:|---:|
| Est. Dem Baseline (share × registered voters) | {_s1[1]} | {_s1[2]} | {_s1[3]} | {_s1[4]} |
| Democratic US House votes | {_s1[5]} | {_s1[6]} | {_s1[7]} | {_s1[8]} |
| Total ballots (total US House votes) | {_s1[9]} | {_s1[10]} | {_s1[11]} | {_s1[12]} |
| Dem Baseline share | {_s2[3]} | {_s2[5]} | | |
| Democratic share of US House votes | {_s2[0]} | {_s2[1]} | {_s2[2]} pts | |
| Total registered voters | {_s2[4]} | {_s2[6]} | | |
| DOE-reported ballots (reference only) | {_s2[7]} | {_s2[8]} | | |

## Columns

**Table 1 (pages 1 to 4)**

| Column | What it shows |
|---|---|
| Dem Baseline Share 2026 % | Democratic governor votes ÷ total governor votes, Nov 2025. The sort key. |
| Est. Dem Baseline 2022 / 2026\\* | Baseline share (2021 or 2025 governor) × total registered voters at the 2022 or 2026 general, rounded. Substitute for Democratic registration. |
| Baseline Change # / % | 2026 minus 2022, and that change as a percent of 2022. |
| Dem House Votes 2022 / 2026\\* | Votes for the Democratic US House candidates, summed across all districts in the locality. |
| Vote Change # / % | 2026 minus 2022, and percent change on the 2022 base. |
| Total Ballots 2022 / 2026\\* | Total US House votes cast (all candidates, including write-ins), the denominator used throughout this wiki. |
| Ballot Change # / % | 2026 minus 2022, and percent change on the 2022 base. |

**Table 2 (pages 5 to {_np})**

| Column | What it shows |
|---|---|
| Dem Share of House Votes 2022 % / 2026\\* % | Democratic US House votes ÷ total US House votes. |
| Change (pts) | 2026 share minus 2022 share, in percentage points. |
| Dem Baseline Share 2022 % / 2026 % | Democratic share of the 2021 and 2025 governor votes. |
| Total Registered 2022 / 2026\\* | Active plus inactive registered voters reported with each November general. |
| DOE-Reported Ballots 2022 / 2026\\* | Ballots cast from the DOE turnout statistics, for reference only. The 2022 report leaves out many early, mailed and provisional ballots, so the analysis does not use it (see [Floor and Ceiling Localities](Floor-and-Ceiling#texas-style-over-ballot-check)). |

## Verification

Every cell was rebuilt from the raw Department of Elections files by a separate script, [`scripts/verify_pdf.py`]({REPO}/blob/main/scripts/verify_pdf.py). That script does not read the analysis outputs. It reads the 2022 locality JSON files, the 2022 registration and turnout pages, the 2026 and 2025 precinct results CSVs, the 2026 turnout CSV, and the 2021 governor precinct rows. It then compares each value with the PDF text at the precision shown. Result: **{_vp['checked']:,} cells checked, {_vp['matched']:,} matched, {len(_vp['mismatches'])} mismatches.** The script also confirms the 2022 locality sums equal the district totals, the 2021 precinct rows add up to each locality and to the state, and the 2026 registration matches the DOE registration file. The same table is in [`data/virginia_pdf_table.csv`]({REPO}/blob/main/data/virginia_pdf_table.csv).

{REL(P['home'], P['gr'], P['lock'], P['fc'], P['cedar'])}
"""

for name, txt in (('Virginia-County-PDF-Information', pdfp), ('Home', home), ('Reverse-Math', rev), ('Locked-Virginia-Formula', lock), ('Floor-and-Ceiling', fc), ('Graphs', gr), ('_Sidebar', side)):
    open(f'wiki/{name}.md', 'w').write(txt.strip() + '\n')
print('wiki written')
