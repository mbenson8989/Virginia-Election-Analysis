import json
A = json.load(open('out/analysis.json')); V = json.load(open('out/verification.json')); X = json.load(open('out/crosscheck.json'))
F = A['fit_all']; BUILT = open('out/build_time.txt').read().strip()
def m(s): return s.replace('-', '−')
W = 'https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/'
h = X['house2022_enr_vs_historical']; g = X['gov2025_enr_vs_historical']
txt = f"""# Virginia Election Analysis: 2022 vs 2026 US House, ΔG method (proxy baseline)

Built {BUILT}. **2026 figures are unofficial** (Virginia State Board of Elections has not certified the Nov 3, 2026 election; DOE results files published Nov 19, 2026 11:27 AM CST).

Wiki: [Home]({W}Home) · [Bottom-Up Reverse Math]({W}Reverse-Math) · [Locked Virginia Formula]({W}Locked-Virginia-Formula) · [Floor and Ceiling]({W}Floor-and-Ceiling) · [Graphs]({W}Graphs) · [Virginia County PDF Information]({W}Virginia-County-PDF-Information). Method origin: [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit).

## What this is

Morissa Benson's ΔG / reverse-factoring method, run on all 133 Virginia localities (95 counties, 38 independent cities).

- **Race:** US House, all 11 districts summed per locality. Virginia's governor, House of Delegates and state Senate are elected in odd years; the Nov 8, 2022 ballot had only US House plus local races, and the Nov 3, 2026 ballot had US Senate, US House, three constitutional amendments, one House of Delegates special (HD-20) and local races. Both parties contested all 11 districts in both years and the map did not change (the Apr 21, 2026 redistricting referendum was voided on May 8, 2026).
- **Baseline (PROXY):** Virginia has no party registration. Instead of Democratic registration share, B = Democratic share of the governor vote in the prior odd year (2021 for 2022, 2025 for 2026). Baseline-share drop = B2022 − B2026.
- **Denominator:** total votes cast in the US House race. The 2022 DOE turnout report is incomplete (House votes exceed it in {A['house_over22_count']} of 133 localities), so ballots are used only in a sensitivity fit.

## Statewide fitted equation (OLS, n = 133, Virginia data only)

```
ΔG = {m(f"{F['constant']:+.4f}")} (SE {F['constant_se']:.4f}) + {F['multiplier']:.4f} (SE {F['multiplier_se']:.4f}) × baseline-share drop     R² = {F['r2']:.4f}
```

## Verification

Two independent passes over every raw file:
- `scripts/pass_a.py` (pandas; regex parse of the 2022 statistics pages; 2026 TotalVoteTurnout column; 2026 registration from the turnout CSV)
- `scripts/pass_b.py` (standard library only; html.parser row parse; 2026 ballots as the sum of the five vote-method columns; 2026 registration from the ENR `vr.json` API file)
- `scripts/verify.py` diffs them: **{V['localities']} localities × {V['figures_per_locality']} figures = {V['figures_checked']:,} figures checked, {V['discrepancies']} discrepancies**, same population order.

Cross-source checks (`scripts/crosscheck.py`, `out/crosscheck.json`):
- 2022 US House, DOE results-site locality files (used) vs DOE historical elections database exports: {h['differences']} of {h['figures']} figures differ. The historical export files Richmond City's votes under Richmond County and Franklin City's under Franklin County, and its Alexandria Democratic and Republican counts are 933 and 243 lower with almost the same total; the other differences are 1 to 5 votes in total-vote (write-in) counts. The results-site locality files sum exactly to the results-site district totals ({X['house2022_locality_sum_vs_district_totals']['differences']} differences on {X['house2022_locality_sum_vs_district_totals']['candidate_lines']} candidate lines).
- 2025 governor, DOE results-site CSV (used) vs historical export: {g['differences']} figures differ. The historical export puts Westmoreland precinct 202 (666 votes) under Nottoway.
- 2021 governor (historical export, the only locality file DOE still publishes): locality rows sum to the state row ({X['gov2021_internal']['state_row']:,}) and precinct rows sum to every locality row.

Run everything: `scripts/run_all.sh` (prints ALL CLEAN only if both passes match).

## Sources (raw copies in `raw/`)

| File | Source |
|---|---|
| `raw/2022/locality/*.json`, `Congress.json`, `turnout.html`, `registration.html` | DOE results site, 2022 November General (results.elections.virginia.gov/vaelections/2022 November General/), certified |
| `raw/2022/turnout_2022_november_general.csv` | DOE turnout CSV (apps.elections.virginia.gov/SBE_CSV/ELECTIONS/ELECTIONTURNOUT/) – checked, not used |
| `raw/2022/historical_db/*.csv` | DOE historical elections database (historical.elections.virginia.gov), 2022 US House contests – cross-check only |
| `raw/2026/election_results.csv`, `election_turnout.csv`, `vr.json`, `election_meta.json` | DOE results site, 2026 November General (enr.elections.virginia.gov), **unofficial** |
| `raw/2021/gov2021_locality.csv` | DOE historical elections database, contest 147466 (2021 Governor) |
| `raw/2025/election_results.csv`, `election_turnout.csv` | DOE results site, 2025 November General (official) |
| `raw/2025/gov2025_locality.csv` | DOE historical elections database, contest 164996 – cross-check only |
| `raw/census/co-est2025-alldata.csv` | US Census Bureau, Vintage 2025 county population estimates (July 1, 2025) – sort order |

## Files

- `data/virginia_localities_final.csv` – every input and computed column, 133 rows, largest to smallest population
- `data/virginia_localities_passA.csv`, `data/virginia_localities_passB.csv` – the two verification passes
- `data/regions.csv` – region assignment used for regional constants
- `out/analysis.json` – fits, regional constants, narrowed-out localities, floor/ceiling, over-ballot flags
- `graphs/*.png` – charts used on the wiki
- `scripts/verify_forward.py` – second pass (standard library) for every fitted line, including the share-version surplus equations S = m × (D/100) + b (result in `out/verify_forward.json`)
- `pdf/Virginia_133_Locality_Democratic_Baseline_and_Vote_Change.pdf` – 133-locality PDF table (substitute Democratic baseline, Democratic US House votes and total ballots, 2022 vs 2026, 2026 unofficial); built by `scripts/build_pdf.py`, every cell re-checked from the raw DOE files by `scripts/verify_pdf.py` (result in `out/verify_pdf.json`)
- `wiki/*.md` – wiki page sources

These files measure a pattern; they make no claim about intent, fraud or cause.
"""
open('README.md', 'w').write(txt)
print('readme ok')
