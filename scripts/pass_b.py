"""PASS B: independent re-build from the raw files using only the Python standard library
(csv / json / html.parser), with different parsing logic from pass A.
- 2022 ballots and registration: parsed row-by-row with html.parser (pass A uses regex on flattened text)
- 2026 ballots: sum of the five vote-method columns (pass A uses the TotalVoteTurnout column)
- 2026 registration: vr.json from the ENR API (pass A sums the turnout CSV)"""
import csv, json, glob, os, re
from html.parser import HTMLParser
R = 'raw'

def key(s):
    return ' '.join(s.upper().replace('&', 'AND').split())

class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows = []; self.row = None; self.cell = None
    def handle_starttag(self, tag, a):
        if tag == 'tr': self.row = []
        elif tag in ('td', 'th') and self.row is not None: self.cell = ''
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None and self.row is not None:
            self.row.append(self.cell.strip()); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None
    def handle_data(self, d):
        if self.cell is not None: self.cell += d

def stat_table(path):
    p = Rows(); p.feed(open(path, encoding='utf-8', errors='replace').read())
    out = {}
    for r in p.rows:
        r = [x for x in r if x != '']
        if r and (r[0].endswith(' COUNTY') or r[0].endswith(' CITY')):
            out[key(r[0])] = [int(x.replace(',', '')) for x in r[1:] if re.fullmatch(r'[\d,]+', x)]
    return out

L = {}
with open(f'{R}/census/co-est2025-alldata.csv', encoding='latin-1') as f:
    for r in csv.DictReader(f):
        if r['STATE'] == '51' and r['SUMLEV'] == '050':
            L[key(r['CTYNAME'])] = {'pop2025': int(r['POPESTIMATE2025'])}

def add(k, field, v):
    L[k][field] = L[k].get(field, 0) + v

for fn in sorted(os.listdir(f'{R}/2022/locality')):
    d = json.load(open(f'{R}/2022/locality/{fn}'))
    k = key(d['Locality']['LocalityName'])
    for race in d['Races']:
        if 'House of Representatives' not in race['RaceName']: continue
        for c in race['Candidates']:
            add(k, 'house_total22', c['Votes'])
            if c['PoliticalParty'] == 'Democratic': add(k, 'D22', c['Votes'])
            if c['PoliticalParty'] == 'Republican': add(k, 'R22', c['Votes'])

for k, v in stat_table(f'{R}/2022/turnout.html').items():
    L[k]['ballots22'] = v[4]
    assert sum(v[0:4]) == v[4], (k, v)          # internal check: methods add to total
for k, v in stat_table(f'{R}/2022/registration.html').items():
    L[k]['reg22'] = v[2]; assert v[0] + v[1] == v[2]

with open(f'{R}/2026/election_results.csv', encoding='latin-1') as f:
    for r in csv.DictReader(f):
        t = r['OfficeTitle'] or ''
        votes = int(r['TOTAL_VOTES'] or r['WriteInVote'] or 0)
        k = key(r['LocalityName'])
        if t.startswith('Member, House of Representatives'):
            add(k, 'house_total26', votes)
            if r['Party'] == 'Democratic': add(k, 'D26', votes)
            if r['Party'] == 'Republican': add(k, 'R26', votes)
        elif t == 'Member, United States Senate':
            if r['Party'] == 'Democratic': add(k, 'senD26', votes)
            if r['Party'] == 'Republican': add(k, 'senR26', votes)
with open(f'{R}/2026/election_turnout.csv') as f:
    for r in csv.DictReader(f):
        add(key(r['locality']), 'ballots26', sum(int(r[c] or 0) for c in
            ['Early Voting', 'Election Day', 'Mailed Absentee', 'Provisional', 'Post-Election']))
for r in json.load(open(f'{R}/2026/vr.json'))['data']:
    nm = [x['text'] for x in r['localityName'] if x['languageId'] == 'en'][0]
    L[key(nm)]['reg26'] = r['total']; assert r['activeVoters'] + r['inactiveVoters'] == r['total']

def gov(path, tag):
    rows = list(csv.reader(open(path)))
    hdr, party = rows[0], rows[1]
    di, ti = party.index('Democratic'), hdr.index('Total Votes Cast')
    ri = party.index('Republican')
    for r in rows:
        if r[0] == 'Locality':
            k = key(r[1]); L[k]['govD' + tag] = int(r[di]); L[k]['govR' + tag] = int(r[ri]); L[k]['govTot' + tag] = int(r[ti])
gov(f'{R}/2021/gov2021_locality.csv', '21')
with open(f'{R}/2025/election_results.csv', encoding='latin-1') as f:
    for r in csv.DictReader(f):
        if r['OfficeTitle'] != 'Governor': continue
        votes = int(r['TOTAL_VOTES'] or r['WriteInVote'] or 0); k = key(r['LocalityName'])
        add(k, 'govTot25', votes)
        if r['Party'] == 'Democratic': add(k, 'govD25', votes)
        if r['Party'] == 'Republican': add(k, 'govR25', votes)

need = ['pop2025','D22','R22','house_total22','ballots22','reg22','D26','R26','house_total26','senD26','senR26',
        'ballots26','reg26','govD21','govR21','govTot21','govD25','govR25','govTot25']
assert len(L) == 133
for k, v in L.items():
    for n in need: assert n in v, (k, n)
    S22 = 100 * v['D22'] / v['house_total22']; S26 = 100 * v['D26'] / v['house_total26']
    B22 = 100 * v['govD21'] / v['govTot21']; B26 = 100 * v['govD25'] / v['govTot25']
    v.update(S22=S22, S26=S26, B22=B22, B26=B26, G22=S22 - B22, G26=S26 - B26)
    v['S22_b'] = 100 * v['D22'] / v['ballots22']; v['S26_b'] = 100 * v['D26'] / v['ballots26']
    v['dG'] = v['G26'] - v['G22']; v['dS'] = S26 - S22; v['B_drop'] = B22 - B26
    v['residual'] = v['dG'] - v['B_drop']
    v['baseline_votes_fell'] = v['govD25'] < v['govD21']
    v['implied_extra'] = v['D26'] - S22 / 100 * v['house_total26']
    v['baseline_scaled_gap'] = v['D26'] - v['D22'] * v['govD25'] / v['govD21']
    v['dG_b'] = (v['S26_b'] - B26) - (v['S22_b'] - B22)
    v['over22'] = v['D22'] + v['R22'] - v['ballots22']; v['over26'] = v['D26'] + v['R26'] - v['ballots26']
    v['sen_over26'] = v['senD26'] + v['senR26'] - v['ballots26']
    v['house_over22'] = v['house_total22'] - v['ballots22']; v['house_over26'] = v['house_total26'] - v['ballots26']

cols = list(next(iter(L.values())).keys())
with open('data/virginia_localities_passB.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['key'] + cols)
    for k in sorted(L, key=lambda k: -L[k]['pop2025']):
        w.writerow([k] + [L[k][c] for c in cols])
print('pass B rows', len(L))
