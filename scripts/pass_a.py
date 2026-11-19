"""PASS A: build the Virginia locality table from raw DOE + Census files (pandas).
Comparison: US House 2022 vs US House 2026 (all districts summed per locality).
Baseline proxy (VA has no party registration): Democratic share of the governor vote in the
odd-year election just before each midterm (2021 for 2022, 2025 for 2026)."""
import json, glob, re, html, sys
import pandas as pd
R = 'raw'

def key(s):
    s = str(s).upper().replace('&', 'AND')
    return re.sub(r'\s+', ' ', s).strip()

# ---- Census Vintage 2025 ----
c = pd.read_csv(f'{R}/census/co-est2025-alldata.csv', encoding='latin-1', dtype=str)
c = c[(c.STATE == '51') & (c.SUMLEV == '050')].copy()
df = pd.DataFrame({'key': c.CTYNAME.map(key), 'fips': '51' + c.COUNTY,
                   'locality': c.CTYNAME.str.replace(' city', ' City'),
                   'pop2025': c.POPESTIMATE2025.astype(int)})

# ---- 2022 US House (ENR locality JSON) ----
rows = []
for f in glob.glob(f'{R}/2022/locality/*.json'):
    d = json.load(open(f))
    k = key(d['Locality']['LocalityName'])
    for r in d['Races']:
        if r['RaceName'].startswith('Member House of Representatives'):
            dist = int(r['RaceName'][-3:-1])
            for cand in r['Candidates']:
                rows.append((k, dist, cand['PoliticalParty'], cand['Votes']))
h22 = pd.DataFrame(rows, columns=['key', 'dist', 'party', 'votes'])
agg22 = h22.groupby('key').apply(lambda g: pd.Series({
    'D22': g.loc[g.party == 'Democratic', 'votes'].sum(),
    'R22': g.loc[g.party == 'Republican', 'votes'].sum(),
    'house_total22': g.votes.sum(),
    'districts22': ';'.join(str(x) for x in sorted(g.dist.unique()))}), include_groups=False).reset_index()
contested22 = h22.groupby('dist').party.apply(lambda p: {'Democratic', 'Republican'} <= set(p))

# ---- 2022 ballots + registration (ENR statistics pages) ----
def enr_table(path, ncols):
    t = open(path, encoding='utf-8', errors='replace').read()
    cells = [x.strip() for x in html.unescape(re.sub(r'<[^>]+>', '|', t)).split('|') if x.strip()]
    out = {}
    for i, x in enumerate(cells):
        if re.fullmatch(r"[A-Z][A-Z .&']+ (COUNTY|CITY)", x):
            v = cells[i + 1:i + 1 + ncols]
            if len(v) == ncols and all(re.fullmatch(r'[\d,]+', y) for y in v):
                out[key(x)] = [int(y.replace(',', '')) for y in v]
    return out
t22 = enr_table(f'{R}/2022/turnout.html', 5)
g22 = enr_table(f'{R}/2022/registration.html', 3)
b22 = pd.DataFrame([(k, v[4]) for k, v in t22.items()], columns=['key', 'ballots22'])
r22 = pd.DataFrame([(k, v[2]) for k, v in g22.items()], columns=['key', 'reg22'])

# ---- 2026 US House + Senate (ENR results CSV, precinct rows) ----
e = pd.read_csv(f'{R}/2026/election_results.csv', dtype=str, encoding='latin-1')
e['votes'] = e.TOTAL_VOTES.fillna(e.WriteInVote).astype(int);  # write-in rows carry votes in WriteInVote
e["key"] = e.LocalityName.map(key)
hh = e[e.OfficeTitle.str.startswith('Member, House of Representatives', na=False)]
agg26 = hh.groupby('key').apply(lambda g: pd.Series({
    'D26': g.loc[g.Party == 'Democratic', 'votes'].sum(),
    'R26': g.loc[g.Party == 'Republican', 'votes'].sum(),
    'house_total26': g.votes.sum(),
    'districts26': ';'.join(str(int(x)) for x in sorted(g.DistrictName.astype(int).unique()))}), include_groups=False).reset_index()
contested26 = hh.groupby('DistrictName').Party.apply(lambda p: {'Democratic', 'Republican'} <= set(p.dropna()))
ss = e[e.OfficeTitle == 'Member, United States Senate']
sen26 = ss.groupby('key').apply(lambda g: pd.Series({
    'senD26': g.loc[g.Party == 'Democratic', 'votes'].sum(),
    'senR26': g.loc[g.Party == 'Republican', 'votes'].sum()}), include_groups=False).reset_index()
tu = pd.read_csv(f'{R}/2026/election_turnout.csv', dtype=str).fillna('0')
tu['key'] = tu.locality.map(key)
for col in ['TotalVoteTurnout', 'TotalRegisteredVoters']: tu[col] = tu[col].astype(int)
b26 = tu.groupby('key').agg(ballots26=('TotalVoteTurnout', 'sum'), reg26=('TotalRegisteredVoters', 'sum')).reset_index()

# ---- Governor baselines (DOE historical elections database contest CSVs) ----
def gov(path, dcol, tag):
    g = pd.read_csv(path, header=None, dtype=str)
    names, parties = list(g.iloc[0]), list(g.iloc[1])
    di = parties.index('Democratic'); ri = parties.index('Republican'); ti = names.index('Total Votes Cast')
    L = g[g[0] == 'Locality']
    return pd.DataFrame({'key': L[1].map(key), f'govD{tag}': L[di].astype(int),
                         f'govR{tag}': L[ri].astype(int), f'govTot{tag}': L[ti].astype(int)})
g21 = gov(f'{R}/2021/gov2021_locality.csv', 'Democratic', '21')
# 2025: official ENR results CSV (precinct rows). The historical-database export misfiles one
# Westmoreland precinct (202, 666 votes) under Nottoway, so it is used only as a cross-check.
e25 = pd.read_csv(f'{R}/2025/election_results.csv', dtype=str, encoding='latin-1')
e25 = e25[e25.OfficeTitle == 'Governor'].copy()
e25['votes'] = e25.TOTAL_VOTES.fillna(e25.WriteInVote).astype(int); e25['key'] = e25.LocalityName.map(key)
g25 = e25.groupby('key').apply(lambda g: pd.Series({
    'govD25': g.loc[g.Party == 'Democratic', 'votes'].sum(), 'govR25': g.loc[g.Party == 'Republican', 'votes'].sum(),
    'govTot25': g.votes.sum()}), include_groups=False).reset_index()

for part in [agg22, b22, r22, agg26, sen26, b26, g21, g25]:
    df = df.merge(part, on='key', how='left')
assert len(df) == 133, len(df)
missing = df[df.isna().any(axis=1)]
assert missing.empty, missing

df = df.sort_values('pop2025', ascending=False).reset_index(drop=True)
regions = pd.read_csv('data/regions.csv'); df = df.merge(regions, on='key', how='left')

# ---- equation ----
# Denominator: total votes cast in the US House race (all candidates incl. write-ins) in BOTH years.
# The 2022 DOE turnout statistic is incomplete (House votes exceed it in 94 of 133 localities),
# so the ballots-denominator version is kept only as a sensitivity column (suffix _b).
df['S22'] = df.D22 / df.house_total22 * 100
df['S26'] = df.D26 / df.house_total26 * 100
df['S22_b'] = df.D22 / df.ballots22 * 100
df['S26_b'] = df.D26 / df.ballots26 * 100
df['B22'] = df.govD21 / df.govTot21 * 100          # PROXY baseline for 2022 (2021 governor)
df['B26'] = df.govD25 / df.govTot25 * 100          # PROXY baseline for 2026 (2025 governor)
df['G22'] = df.S22 - df.B22
df['G26'] = df.S26 - df.B26
df['dG'] = df.G26 - df.G22
df['dS'] = df.S26 - df.S22
df['B_drop'] = df.B22 - df.B26                      # baseline-share drop (positive = fell)
df['residual'] = df.dG - df.B_drop                  # = S26 - S22
df['baseline_votes_fell'] = df.govD25 < df.govD21
df['implied_extra'] = df.D26 - df.S22 / 100 * df.house_total26
df['baseline_scaled_gap'] = df.D26 - df.D22 * (df.govD25 / df.govD21)
df['dG_b'] = (df.S26_b - df.B26) - (df.S22_b - df.B22)
df['over22'] = df.D22 + df.R22 - df.ballots22
df['over26'] = df.D26 + df.R26 - df.ballots26
df['sen_over26'] = df.senD26 + df.senR26 - df.ballots26
df['house_over22'] = df.house_total22 - df.ballots22
df['house_over26'] = df.house_total26 - df.ballots26
df.to_csv('data/virginia_localities_passA.csv', index=False)
json.dump({'contested22': contested22.to_dict(), 'contested26': {int(k): v for k, v in contested26.to_dict().items()}},
          open('out/contested.json', 'w'), indent=1)
print('pass A rows', len(df))
