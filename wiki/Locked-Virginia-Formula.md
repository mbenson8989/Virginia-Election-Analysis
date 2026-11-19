# Locked Virginia Formula

> **\*2026 figures are unofficial.** The Virginia State Board of Elections has not certified the November 3, 2026 general election. The Department of Elections (DOE) results site, enr.elections.virginia.gov (2026 November General), still labels them unofficial results; the files used here were published there on Nov 19, 2026 at 11:27 AM CST. 2022, 2021 and 2025 figures are certified. **PROXY BASELINE: Virginia has no party registration.** Where the other state wikis use the Democratic registration share, these pages use **B** = the Democratic share of the governor vote in the odd-year election just before each midterm (2021 for 2022, 2025 for 2026). It is not a count of registered Democrats. **Race: US House**, all 11 districts summed per county or independent city (Virginia had no governor, General Assembly or statewide race in 2022). Votes are votes for the Democratic candidate. These pages measure a pattern; they make no claim about intent, fraud or cause.

> **Why a substitute baseline.** Virginia voters do not register by party; the DOE publishes only active and inactive registered voters per locality. There is no Democratic registration count, so the registration share R used in every other state wiki does not exist here, and none is invented. In its place these pages use **B = Democratic governor votes ÷ total governor votes** in the odd-year election just before each midterm (**2021** for 2022, **2025** for 2026), from the same locality. "Registration-share drop" becomes **baseline-share drop = B2022 − B2026**. Every B figure is labeled **[PROXY]**.

## Statewide Fitted Equation

Ordinary least squares across **all 133 Virginia counties and independent cities**, each weighted equally, Virginia data only. No other state's constant is reused.

```
Virginia equation:  ΔG = +3.09 + 0.48 × (baseline-share drop, points)   [PROXY baseline]
Four decimals:      ΔG = +3.0917 + 0.4827 × (baseline-share drop, points)
```

| Item | Rounded | 4 decimals | Standard error |
|---|---|---|---|
| Constant (intercept) | +3.09 | +3.0917 | 0.5175 |
| Multiplier (slope) | 0.48 | 0.4827 | 0.0698 |
| R² | 0.27 | 0.2674 | |
| n (localities) | 133 | 133 | |
| Residual standard error (points) | 1.94 | 1.9353 | |

_2022 vs 2026\* US House, all districts summed per locality; denominator = total US House votes; baseline-share drop = B2022 − B2026 in points (negative = the baseline rose). 2026 unofficial (DOE results files published Nov 19, 2026 11:27 AM CST)._ Both coefficients are significant (p < 0.001).

**What it means:** across Virginia's localities, each 1-point *rise* in the governor-vote baseline (a drop of −1) goes with about 0.48 points *lower* ΔG, starting from about +3.09 where the baseline does not move. Because every Virginia locality's baseline rose (drop from −12.03 to −2.60), the constant is an extrapolation outside the data. Put the other way (1 − 0.48 = 0.52): each extra point of 2021→2025 baseline rise goes with about 0.52 points more 2022→2026 House vote-share gain, so the House vote picked up about half of each locality's extra governor swing. The fit explains about 27% of the locality-to-locality differences in ΔG. This line describes the pattern; it does not prove anything.

**Worked example: Fairfax County.** B *rose* from 64.89 to 73.78, a baseline-share drop of −8.8936 points. Predicted ΔG = +3.0917 + 0.4827 × (−8.8936) = −1.20. Actual ΔG = −1.26\*. Difference from the fitted line (actual − predicted) = −0.06\*. This difference is not the line-11 residual in the template below, which is ΔG minus the baseline-share drop.

### Sensitivity checks

| Fit | n | Constant (SE) | Multiplier (SE) | R² |
|---|---|---|---|---|
| **All localities (locked)** | 133 | +3.09 (0.52) | 0.48 (0.07) | 0.267 |
| Narrowed (9 high-influence localities out, see [Floor and Ceiling](Floor-and-Ceiling#localities-narrowed-out-of-the-fit)) | 124 | +3.22 (0.49) | 0.49 (0.07) | 0.297 |
| Weighted by 2026 US House votes | 133 | +2.90 (0.69) | 0.52 (0.08) | 0.251 |
| Ballots denominator (DOE turnout), all localities | 133 | +3.05 (0.82) | 0.59 (0.11) | 0.178 |
| Ballots denominator, localities without a 2022 over-ballot flag | 72 | +2.45 (0.67) | 0.38 (0.10) | 0.174 |

**The locked Virginia constants are the all-locality fit: constant +3.09, multiplier 0.48.** Narrowing barely moves them.

### Regional constants

Same multiplier for every region (0.27, SE 0.06), one constant per region; and, for comparison, a separate line fitted inside each region. Regions are groups of localities defined for this wiki (list in [data/regions.csv](https://github.com/mbenson8989/Virginia-Election-Analysis/blob/main/data/regions.csv)).

| Region | n | Regional constant, common multiplier (SE) | Separate fit: constant (SE) | Separate fit: multiplier (SE) | Separate fit R² | Median ΔG\* |
|---|---|---|---|---|---|---|
| Central Piedmont | 10 | −1.35 (0.67) | +2.01 (2.72) | 0.71 (0.35) | 0.340 | −3.98 |
| Hampton Roads | 16 | −0.06 (0.63) | +0.79 (1.91) | 0.37 (0.23) | 0.158 | −1.93 |
| Northern Virginia | 13 | +0.22 (0.74) | −0.71 (2.99) | 0.17 (0.31) | 0.028 | −2.14 |
| Eastern Shore and Northern Neck | 11 | +1.46 (0.60) | +3.95 (2.10) | 0.68 (0.33) | 0.318 | −0.34 |
| Richmond Metro | 17 | +1.55 (0.59) | +1.78 (1.11) | 0.30 (0.14) | 0.237 | −0.61 |
| Shenandoah Valley | 16 | +2.31 (0.61) | +1.79 (0.76) | 0.20 (0.09) | 0.246 | +0.36 |
| Southwest | 22 | +2.75 (0.48) | +2.54 (0.76) | 0.23 (0.13) | 0.144 | +1.27 |
| Roanoke-Lynchburg | 12 | +2.75 (0.59) | −0.37 (1.16) | −0.22 (0.18) | 0.139 | +1.33 |
| Southside | 16 | +3.21 (0.52) | +2.48 (1.23) | 0.14 (0.21) | 0.031 | +1.78 |

**Regions matter.** Adding regional constants raises adjusted R² from 0.262 to 0.559 (F = 12.02, p < 0.001). The highest regional constants are Southside, Roanoke-Lynchburg, Southwest, Shenandoah Valley; the lowest are Central Piedmont, Hampton Roads, Northern Virginia. With the regional constants in the model, the common multiplier falls to 0.27: much of the statewide slope reflects the difference between regions. Separate within-region fits rest on 10 to 22 localities each and have wide standard errors.

## The equation

- **S** (Democratic vote share) = Democratic US House votes ÷ total US House votes × 100, all districts in the locality summed
- **B** (baseline, **[PROXY]** for Democratic registration share) = Democratic governor votes ÷ total governor votes × 100, from the prior odd-year election (2021 for 2022; 2025 for 2026)
- **G** = S − B
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (B2026 − B2022)
- **Reverse step (baseline-drop subtraction):** residual = ΔG − (B2022 − B2026) = S2026 − S2022
- **Solved backward, implied extra votes:** D2026 − (S2022 ÷ 100) × total US House votes 2026
- **Baseline-scaled gap** (stand-in for the Nebraska wiki's "gap in votes" line, comparison only): D2026 − D2022 × (governor D 2025 ÷ governor D 2021)

### Denominator

The other state wikis divide by total ballots cast. Virginia's 2022 DOE turnout report (results site, Turnout Statistics, generated Dec 6, 2022) is incomplete: total US House votes exceed it in 94 of 133 localities, and in Albemarle the turnout figure leaves out mailed absentee ballots and part of early voting (38,050 ballots against 50,206 House votes). The 2026 DOE turnout report has no such gap. Because one year's ballots figure cannot be trusted, both years use total votes cast in the US House race, the denominator the current Nebraska pages use. The ballots version is in the sensitivity table above.

### Why the governor race for the baseline

The baseline needs to measure each locality's partisan lean independently of the US House race being tested, one year before each midterm, from DOE data. The governor race is on every Virginia ballot in 2021 and 2025, is statewide and is contested by both parties. Virginia's party primaries are open (any registered voter may choose either party's primary), so primary turnout is not a clean partisan count either.

## Blank template

| Line | Item | 2022 | 2026\* |
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
| 14 | Fitted ΔG = +3.0917 + 0.4827 × (−line 9) | | ______ |
| 15 | Distance from the Virginia line = line 8 − line 14 | | ______ |

## Rules for using this formula

1. **If a locality lost Democratic baseline votes, run the residual step** (line 11) and the implied-votes line (line 12). In Virginia only **Greensville County** lost Democratic governor votes (1,915 in 2021 → 1,902 in 2025). Every other locality is a **non-loss locality**: report its raw numbers. Its line 11 is shown for completeness and equals its vote-share change.
2. **The starting point is different in every state. Don't assume Nebraska's numbers carry over.** Virginia's statewide ΔG was −1.50\* and its locality median +0.11\*. Compare Virginia localities with Virginia's own range, and remember B is a proxy.
3. **Always pull out the ceiling and floor localities.** In Virginia the ceiling locality is Buckingham County (+4.02\*) and the lowest ΔG is Fredericksburg City (−6.56\*). See [Floor and Ceiling Localities](Floor-and-Ceiling).

**Terms used in this wiki** (full definitions on [Floor and Ceiling Localities](Floor-and-Ceiling#terminology)):
- **Ceiling localities**: the five largest ΔG (Buckingham County, Smyth County, Galax City, Sussex County, Cumberland County).
- **Floor localities**: the most Republican baseline, the five lowest 2021 governor shares (Lee County, Scott County, Tazewell County, Bland County, Russell County).
- **Non-loss localities**: no loss of Democratic baseline votes (all but Greensville).

## Worked example: Chesterfield County

| Line | Item | 2022 | 2026\* |
|---|---|---|---|
| 1 | Democratic US House votes | 70,534 | 107,196\* |
| 2 | Total US House votes | 140,257 | 177,464\* |
| 3 | S | 50.29 | 60.40\* |
| 4 | Democratic governor votes [PROXY] | 74,085 (2021) | 100,595 (2025) |
| 5 | Total governor votes [PROXY] | 156,277 | 170,910 |
| 6 | B [PROXY] | 47.41 | 58.86 |
| 7 | G | +2.88 | +1.55\* |
| 8 | ΔG | | −1.34\* |
| 9 | Baseline change | | +11.45 |
| 10 | Baseline votes fell? | | No (non-loss) |
| 11 | Residual | | +10.12\* |
| 12 | Implied extra votes | | +17,951\* |
| 13 | Baseline-scaled gap | | +11,423\* |
| 14 | Fitted ΔG | | −2.44 |
| 15 | Distance from the Virginia line | | +1.10\* |

---
**Related:** [Bottom-Up Reverse Math](Reverse-Math) · [Floor and Ceiling Localities](Floor-and-Ceiling) · [Graphs](Graphs) · [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit) · [Home](Home)
