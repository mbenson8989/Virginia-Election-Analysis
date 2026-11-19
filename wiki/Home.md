# Virginia 2022 vs 2026 US House: ΔG Method (proxy baseline)

**Version 1, built Nov 19, 2026, 12:54 PM CST.**

> **\*2026 figures are unofficial.** The Virginia State Board of Elections has not certified the November 3, 2026 general election. The Department of Elections (DOE) results site, enr.elections.virginia.gov (2026 November General), still labels them unofficial results; the files used here were published there on Nov 19, 2026 at 11:27 AM CST. 2022, 2021 and 2025 figures are certified. **PROXY BASELINE: Virginia has no party registration.** Where the other state wikis use the Democratic registration share, these pages use **B** = the Democratic share of the governor vote in the odd-year election just before each midterm (2021 for 2022, 2025 for 2026). It is not a count of registered Democrats. **Race: US House**, all 11 districts summed per county or independent city (Virginia had no governor, General Assembly or statewide race in 2022). Votes are votes for the Democratic candidate. These pages measure a pattern; they make no claim about intent, fraud or cause.

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP). It began with her [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) on the [Nebraska Election Analysis wiki](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki), the origin of the ΔG method and the reverse step used here. This wiki applies the same arithmetic to all 133 Virginia localities (95 counties and 38 independent cities), with one change forced by Virginia law: there is no party registration, so a vote-share baseline stands in for registration share. Data: Virginia Department of Elections results files for 2021, 2022, 2025 and 2026 and the DOE historical elections database; population from the Census Bureau Vintage 2025 county estimates. Compiled Nov 19, 2026. Data, scripts and both verification passes: [mbenson8989/Virginia-Election-Analysis](https://github.com/mbenson8989/Virginia-Election-Analysis).

## Contents

Start with the Cedar County audit in Nebraska. That is where the method began. The Virginia pages then build up from one locality (Chesterfield) to the six largest localities, to all 133, and to the formula.

1. [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) (Nebraska wiki): where the method started
2. [Bottom-Up Reverse Math](Reverse-Math): Chesterfield → the six largest localities → all 133, then solved backward for implied extra votes; full 133-locality table
3. [Locked Virginia Formula](Locked-Virginia-Formula): the **statewide fitted equation** (constant, multiplier, R², standard errors), regional constants, and the blank fill-in template
4. [Floor and Ceiling Localities](Floor-and-Ceiling): the localities at the top and bottom, localities narrowed out of the fit, and the Texas-style over-ballot check
5. [Graphs](Graphs): slope chart, ΔG by population, fitted-equation scatter, paired bars, residual bars, regional constants, over-ballot check
6. [Virginia County PDF Information](Virginia-County-PDF-Information): downloadable 133-locality PDF table (baseline, Democratic votes and ballots, 2022 vs 2026\*), every cell checked against the raw DOE files

## Why US House 2022 vs 2026

Virginia elects its governor and House of Delegates in odd years (2021, 2025) and its state Senate in 2019 and 2023. The DOE files confirm what was on the two midterm ballots:

- **Nov 8, 2022:** US House (all 11 districts) plus local offices and local questions. No statewide office, no General Assembly race.
- **Nov 3, 2026\*:** US Senate, US House (all 11 districts), three proposed constitutional amendments, one House of Delegates special (District 20) and local races.

The only race on every ballot in both years is US House, so it is the midterm-to-midterm comparison. It is clean: all 133 localities are present in both years; both major parties contested all 11 districts in both years; the district map is the same in both years (the April 21, 2026 redistricting referendum was voided by the Supreme Court of Virginia on May 8, 2026, and all 145 locality-district pieces match). 10 localities are split between districts; their district results are summed.

## Statewide at a glance

| Measure | 2022 | 2026\* | Change |
|---|---|---|---|
| Democratic US House votes | 1,572,296 | 2,156,783\* | +584,487\* |
| Total US House votes (all candidates) | 3,047,729 | 3,654,176\* | +606,447\* |
| DOE ballots cast (turnout report) | 3,021,956 | 3,686,609\* | +664,653\* |
| Registered voters, active + inactive | 6,106,090 | 6,514,124 | +408,034 |
| S = Democratic share of US House votes | 51.59% | 59.02%\* | +7.43 pts\* |
| B = Democratic share of prior governor vote **[PROXY]** | 48.64% (2021) | 57.58% (2025) | +8.94 pts |
| G = S − B | +2.95 | +1.44\* | ΔG −1.50\* |

## Locality results in brief

- **ΔG is close to zero and splits both ways.** Median ΔG is +0.11\*, range −6.56\* (Fredericksburg City) to +4.02\* (Buckingham County). 68 localities rose, 65 fell; 112 of 133 are within 3 points of the median. Statewide, the Democratic US House share rose nearly as much as the governor-vote baseline did.
- **Statewide fitted equation (VA only, n = 133):** ΔG = +3.09 + 0.48 × (baseline-share drop), R² = 0.267. Details on [Locked Virginia Formula](Locked-Virginia-Formula#statewide-fitted-equation).
- **The baseline rose everywhere.** B rose from 2021 to 2025 in all 133 localities (baseline-share drop from −12.03 to −2.60 points, median −6.83). Only Greensville County had fewer Democratic governor votes in 2025 than in 2021.
- **Residual after the baseline step** (= vote-share change S2026 − S2022): median +6.55\*, positive in 133 of 133.
- **Solved backward (hypothesis):** the locality figures add up to 258,001\* implied extra votes (271,626\* on pooled statewide numbers). See [Bottom-Up Reverse Math](Reverse-Math).
- **Ceiling and floor:** the five largest ΔG are Buckingham County, Smyth County, Galax City, Sussex County, Cumberland County. The floor (most Republican baseline, lowest 2021 governor share) is Lee County, Scott County, Tazewell County, Bland County, Russell County, all in Southwest Virginia. See [Floor and Ceiling Localities](Floor-and-Ceiling).
- **Texas-style check:** no locality has Democratic + Republican votes above ballots cast in 2026\* (0 of 133, US House and US Senate). In 2022, 61 localities show D + R above the DOE turnout figure, because the 2022 DOE turnout report is incomplete (for example, Albemarle's turnout leaves out its mailed absentee ballots). Details on [Floor and Ceiling Localities](Floor-and-Ceiling#texas-style-over-ballot-check).

## Verification

Two independent passes (separate scripts that re-parse every raw DOE and Census file from scratch) were run over all 133 localities and every figure: **5,320 figures checked (40 per locality), 0 discrepancies.** Cross-source checks against a second DOE publication found filing errors in the DOE historical database export (not in the files used); see the [README](https://github.com/mbenson8989/Virginia-Election-Analysis#verification).

## Read this before using the numbers

- **B is a proxy, not registration.** A governor-vote baseline moves with candidates and campaigns, not with list maintenance. A Virginia ΔG is not directly comparable to a ΔG computed from party registration in Nebraska, Iowa or South Dakota.
- **Different candidates.** 10 of the 11 districts had a different Democratic or Republican nominee in 2026 than in 2022; only District 2 (Luria vs. Kiggans) was a rematch. Candidate effects are inside every number here.
- **Denominator.** The other state wikis divide by total ballots cast. Virginia's 2022 DOE turnout report is incomplete (US House votes exceed it in 94 of 133 localities), so these pages divide by total votes cast in the US House race in both years, the denominator the Nebraska pages use. The ballots-denominator fit is shown for comparison on [Locked Virginia Formula](Locked-Virginia-Formula#sensitivity-checks).
- **A residual is not evidence of altered votes.** Candidate choice, crossover voting, turnout differences and the strong Democratic year in 2025 all move these numbers. The arithmetic cannot separate them.
- **2026 is unofficial.** Every 2026 figure is marked \* and will be re-run after the State Board of Elections certifies the election.

---
**Related:** [Bottom-Up Reverse Math](Reverse-Math) · [Locked Virginia Formula](Locked-Virginia-Formula) · [Floor and Ceiling Localities](Floor-and-Ceiling) · [Graphs](Graphs) · [Virginia County PDF Information](Virginia-County-PDF-Information) · [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)
