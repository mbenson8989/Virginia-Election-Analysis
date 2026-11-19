"""Cross-source checks (different DOE publications of the same contests)."""
import csv, glob, json, collections
def key(s): return ' '.join(s.upper().replace('&', 'AND').split())
A = {r['key']: r for r in csv.DictReader(open('data/virginia_localities_passA.csv'))}
out = {}
# 1) 2022 US House: ENR locality JSON (used) vs historical elections database contest CSVs
h = collections.defaultdict(collections.Counter)
for f in glob.glob('raw/2022/historical_db/*.csv'):
    rows = list(csv.reader(open(f))); party = rows[1]; hdr = rows[0]
    di, ri, ti = party.index('Democratic'), party.index('Republican'), hdr.index('Total Votes Cast')
    for r in rows:
        if r[0] == 'Locality':
            k = key(r[1]); h[k]['D'] += int(r[di]); h[k]['R'] += int(r[ri]); h[k]['T'] += int(r[ti])
d = []
for k, r in A.items():
    for a, b in (('D22', 'D'), ('R22', 'R'), ('house_total22', 'T')):
        if int(r[a]) != h[k][b]: d.append((k, a, int(r[a]), h[k][b]))
out['house2022_enr_vs_historical'] = {'localities': len(h), 'figures': 3 * len(A), 'differences': len(d),
    'D_diff_total': sum(x[2] - x[3] for x in d if x[1] == 'D22'), 'R_diff_total': sum(x[2] - x[3] for x in d if x[1] == 'R22'),
    'T_diff_total': sum(x[2] - x[3] for x in d if x[1] == 'house_total22'), 'details': d}
# 2) 2025 governor: ENR 2025 results CSV (used) vs historical database export
g = collections.defaultdict(collections.Counter)
rows = list(csv.reader(open('raw/2025/gov2025_locality.csv'))); di = rows[1].index('Democratic'); ti = rows[0].index('Total Votes Cast')
for r in rows:
    if r[0] == 'Locality': g[key(r[1])]['D'] = int(r[di]); g[key(r[1])]['T'] = int(r[ti])
d2 = [(k, a, int(A[k][a]), g[k][b]) for k in A for a, b in (('govD25', 'D'), ('govTot25', 'T')) if int(A[k][a]) != g[k][b]]
out['gov2025_enr_vs_historical'] = {'figures': 2 * len(A), 'differences': len(d2), 'details': d2}
# 3) 2022 ENR locality JSON sums vs ENR statewide Congress.json district totals
cj = json.load(open('raw/2022/Congress.json')); dist = collections.Counter(); loc = collections.Counter()
for race in cj['Races']:
    for c in race['Candidates']: dist[(race['RaceName'][-3:-1], c['BallotName'])] += c['Votes']
for f in glob.glob('raw/2022/locality/*.json'):
    for race in json.load(open(f))['Races']:
        if race['RaceName'].startswith('Member House of Representatives'):
            for c in race['Candidates']: loc[(race['RaceName'][-3:-1], c['BallotName'])] += c['Votes']
d3 = [(k, dist[k], loc[k]) for k in set(dist) | set(loc) if dist[k] != loc[k]]
out['house2022_locality_sum_vs_district_totals'] = {'candidate_lines': len(set(dist) | set(loc)), 'differences': len(d3), 'details': d3}
# 4) 2021 governor export internal consistency: locality rows sum to state row; precinct rows sum to locality rows
rows = list(csv.reader(open('raw/2021/gov2021_locality.csv'))); ti = rows[0].index('Total Votes Cast')
state = int([r for r in rows if r[0] == 'State'][0][ti]); locs = {}; prec = collections.Counter(); cur = None
for r in rows:
    if r[0] == 'Locality': cur = r[1]; locs[cur] = int(r[ti])
    elif r[0] == 'Precinct': prec[cur] += int(r[ti])
bad = [(k, locs[k], prec[k]) for k in locs if locs[k] != prec[k]]
out['gov2021_internal'] = {'state_row': state, 'sum_of_localities': sum(locs.values()), 'localities': len(locs),
                           'localities_where_precincts_do_not_sum': len(bad), 'details': bad}
json.dump(out, open('out/crosscheck.json', 'w'), indent=1)
for k, v in out.items(): print(k, {a: b for a, b in v.items() if a != 'details'}, v['details'][:8])
