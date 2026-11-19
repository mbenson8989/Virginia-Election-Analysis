# Virginia Election Analysis: 2022 vs 2026 US House, ΔG method (proxy baseline)

Built Nov 19, 2026, 12:54 PM CST. **2026 figures are unofficial** (Virginia State Board of Elections has not certified the Nov 3, 2026 election; DOE results files published Nov 19, 2026 11:27 AM CST).

Wiki: [Home](https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/Home) · [Bottom-Up Reverse Math](https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/Reverse-Math) · [Locked Virginia Formula](https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/Locked-Virginia-Formula) · [Floor and Ceiling](https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/Floor-and-Ceiling) · [Graphs](https://github.com/mbenson8989/Virginia-Election-Analysis/wiki/Graphs). Method origin: [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit).

## What this is

Morissa Benson's ΔG / reverse-factoring method, run on all 133 Virginia localities (95 counties, 38 independent cities).

- **Race:** US House, all 11 districts summed per locality. Virginia's governor, House of Delegates and state Senate are elected in odd years; the Nov 8, 2022 ballot had only US House plus local races, and the Nov 3, 2026 ballot had US Senate, US House, three constitutional amendments, one House of Delegates special (HD-20) and local races. Both parties contested all 11 districts in both years and the map did not change (the Apr 21, 2026 redistricting referendum was voided on May 8, 2026).
- **Baseline (PROXY):** Virginia has no party registration. Instead of Democratic registration share, B = Democratic share of the governor vote in the prior odd year (2021 for 2022, 2025 for 2026). Baseline-share drop = B2022 − B2026.
- **Denominator:** total votes cast in the US House race. The 2022 DOE turnout report is incomplete (House votes exceed it in 94 of 133 localities), so ballots are used only in a sensitivity fit.

## Statewide fitted equation (OLS, n = 133, Virginia data only)

```
ΔG = +3.0917 (SE 0.5175) + 0.4827 (SE 0.0698) × baseline-share drop     R² = 0.2674
```

## Verification

Two independent passes over every raw file:
- `scripts/pass_a.py` (pandas; regex parse of the 2022 statistics pages; 2026 TotalVoteTurnout column; 2026 registration from the turnout CSV)
- `scripts/pass_b.py` (standard library only; html.parser row parse; 2026 ballots as the sum of the five vote-method columns; 2026 registration from the ENR `vr.json` API file)
- `scripts/verify.py` diffs them: **133 localities × 40 figures = 5,320 figures checked, 0 discrepancies**, same population order.

Cross-source checks (`scripts/crosscheck.py`, `out/crosscheck.json`):
- 2022 US House, DOE results-site locality files (used) vs DOE historical elections database exports: 47 of 399 figures differ. The historical export files Richmond City's votes under Richmond County and Franklin City's under Franklin County, and its Alexandria Democratic and Republican counts are 933 and 243 lower with almost the same total; the other differences are 1 to 5 votes in total-vote (write-in) counts. The results-site locality files sum exactly to the results-site district totals (0 differences on 35 candidate lines).
- 2025 governor, DOE results-site CSV (used) vs historical export: 4 figures differ. The historical export puts Westmoreland precinct 202 (666 votes) under Nottoway.
- 2021 governor (historical export, the only locality file DOE still publishes): locality rows sum to the state row (3,288,327) and precinct rows sum to every locality row.

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
- `wiki/*.md` – wiki page sources

These files measure a pattern; they make no claim about intent, fraud or cause.
