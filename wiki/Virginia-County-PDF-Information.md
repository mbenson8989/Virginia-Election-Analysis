# Virginia County PDF Information

**[Download the PDF: Virginia 133 Localities, Democratic Baseline, Democratic US House Votes and Total Ballots, 2022 vs 2026\*](https://raw.githubusercontent.com/mbenson8989/Virginia-Election-Analysis/main/pdf/Virginia_133_Locality_Democratic_Baseline_and_Vote_Change.pdf)** (7 pages, landscape)

The PDF follows the layout of the [Nebraska 93-county PDF](https://github.com/mbenson8989/Nebraska-Election-Analysis-/blob/main/Nebraska_93_County_Democratic_Registration_and_Vote_Change.pdf): one row for each of Virginia's 133 counties and independent cities, plus a statewide total row. Rows are sorted by the 2026 Democratic baseline share, highest first (Charlottesville City first, Lee County last). Rows where total registered voters fell are shaded blue, and the one locality where Democratic governor votes fell from 2021 to 2025 is shaded orange.

> **Substitute baseline, not party registration.** Virginia does not register voters by party, so there is no Democratic registration to report. Where the Nebraska PDF shows Democratic registration, this PDF shows the **Dem Baseline**: the Democratic share of the governor vote in the odd-year election before each midterm (2021 for 2022, 2025 for 2026). The **Est. Dem Baseline** count is that share × total registered voters, rounded. It is an estimate, not a count of registered Democrats.

\*2026 figures are unofficial and not certified by the State Board of Elections (DOE results site as of Nov 19, 2026, 11:27 AM CST). The PDF should be rebuilt after certification.

## Statewide totals

| Measure | 2022 | 2026\* | Change # | Change % |
|---|---:|---:|---:|---:|
| Est. Dem Baseline (share × registered voters) | 3,008,590 | 3,768,608 | +760,018 | +25.3% |
| Democratic US House votes | 1,572,296 | 2,156,783 | +584,487 | +37.2% |
| Total ballots (total US House votes) | 3,047,729 | 3,654,176 | +606,447 | +19.9% |
| Dem Baseline share | 48.6% | 57.6% | | |
| Democratic share of US House votes | 51.6% | 59.0% | +7.43 pts | |
| Total registered voters | 6,106,090 | 6,514,124 | | |
| DOE-reported ballots (reference only) | 3,021,956 | 3,686,609 | | |

## Columns

**Table 1 (pages 1 to 4)**

| Column | What it shows |
|---|---|
| Dem Baseline Share 2026 % | Democratic governor votes ÷ total governor votes, Nov 2025. The sort key. |
| Est. Dem Baseline 2022 / 2026\* | Baseline share (2021 or 2025 governor) × total registered voters at the 2022 or 2026 general, rounded. Substitute for Democratic registration. |
| Baseline Change # / % | 2026 minus 2022, and that change as a percent of 2022. |
| Dem House Votes 2022 / 2026\* | Votes for the Democratic US House candidates, summed across all districts in the locality. |
| Vote Change # / % | 2026 minus 2022, and percent change on the 2022 base. |
| Total Ballots 2022 / 2026\* | Total US House votes cast (all candidates, including write-ins), the denominator used throughout this wiki. |
| Ballot Change # / % | 2026 minus 2022, and percent change on the 2022 base. |

**Table 2 (pages 5 to 7)**

| Column | What it shows |
|---|---|
| Dem Share of House Votes 2022 % / 2026\* % | Democratic US House votes ÷ total US House votes. |
| Change (pts) | 2026 share minus 2022 share, in percentage points. |
| Dem Baseline Share 2022 % / 2026 % | Democratic share of the 2021 and 2025 governor votes. |
| Total Registered 2022 / 2026\* | Active plus inactive registered voters reported with each November general. |
| DOE-Reported Ballots 2022 / 2026\* | Ballots cast from the DOE turnout statistics, for reference only. The 2022 report leaves out many early, mailed and provisional ballots, so the analysis does not use it (see [Floor and Ceiling Localities](Floor-and-Ceiling#texas-style-over-ballot-check)). |

## Verification

Every cell was rebuilt from the raw Department of Elections files by a separate script, [`scripts/verify_pdf.py`](https://github.com/mbenson8989/Virginia-Election-Analysis/blob/main/scripts/verify_pdf.py). That script does not read the analysis outputs. It reads the 2022 locality JSON files, the 2022 registration and turnout pages, the 2026 and 2025 precinct results CSVs, the 2026 turnout CSV, and the 2021 governor precinct rows. It then compares each value with the PDF text at the precision shown. Result: **3,216 cells checked, 3,216 matched, 0 mismatches.** The script also confirms the 2022 locality sums equal the district totals, the 2021 precinct rows add up to each locality and to the state, and the 2026 registration matches the DOE registration file. The same table is in [`data/virginia_pdf_table.csv`](https://github.com/mbenson8989/Virginia-Election-Analysis/blob/main/data/virginia_pdf_table.csv).

---
**Related:** [Home](Home) · [Graphs](Graphs) · [Locked Virginia Formula](Locked-Virginia-Formula) · [Floor and Ceiling Localities](Floor-and-Ceiling) · [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)
