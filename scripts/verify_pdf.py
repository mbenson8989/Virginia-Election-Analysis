"""Independent PDF verifier (t5u). Reads ONLY raw DOE source files under raw/ and the PDF itself.
Does not read data/ or out/ files or import any project script. Recomputes every displayed cell with
exact rational arithmetic (fractions.Fraction, round half up) and compares it to the PDF text at the displayed precision."""
import csv, json, os, re, sys, subprocess
from fractions import Fraction as F
from collections import defaultdict
PDF = sys.argv[1] if len(sys.argv) > 1 else 'pdf/Virginia_133_Locality_Democratic_Baseline_and_Vote_Change.pdf'
R = 'raw'
def nk(s): return re.sub(r'\s+', ' ', s.upper().replace('&', ' AND ')).strip()
V = defaultdict(lambda: defaultdict(int))

# 2022 US House: per-locality JSON; reconciled against district totals in Congress.json
dist = defaultdict(lambda: defaultdict(int))
for fn in os.listdir(f'{R}/2022/locality'):
    j = json.load(open(f'{R}/2022/locality/{fn}')); k = nk(j['Locality']['LocalityName'])
    for race in j['Races']:
        m = re.match(r'Member House of Representatives \((\d+)\)$', race['RaceName'])
        if not m: continue
        for c in race['Candidates']:
            V[k]['T22'] += c['Votes']; dist[m.group(1)][c['BallotName']] += c['Votes']
            if c['PoliticalParty'] == 'Democratic': V[k]['D22'] += c['Votes']
for race in json.load(open(f'{R}/2022/Congress.json'))['Races']:
    d = re.search(r'\((\d+)\)', race['RaceName']).group(1)
    for c in race['Candidates']:
        assert dist[d][c['BallotName']] == c['Votes'], ('2022 district reconcile', d, c['BallotName'])
# 2022 registration and DOE ballots: per-<tr> regex on the raw HTML
def html_rows(path, n):
    out = {}
    for tr in re.findall(r'<tr.*?</tr>', open(path, encoding='utf-8', errors='replace').read(), re.S | re.I):
        cells = [re.sub(r'<[^>]+>|&nbsp;', '', c).strip() for c in re.findall(r'<td.*?</td>', tr, re.S | re.I)]
        cells = [c for c in cells if c]
        if cells and re.search(r'(COUNTY|CITY)$', cells[0]) and len(cells) >= n + 1:
            out[nk(cells[0])] = [int(c.replace(',', '')) for c in cells[1:n + 1]]
    return out
for k, v in html_rows(f'{R}/2022/registration.html', 3).items(): V[k]['reg22'] = v[2]; assert v[0] + v[1] == v[2]
for k, v in html_rows(f'{R}/2022/turnout.html', 5).items(): V[k]['bal22'] = v[4]
# 2026 US House (unofficial ENR precinct CSV)
with open(f'{R}/2026/election_results.csv', encoding='latin-1') as f:
    for r in csv.DictReader(f):
        if not (r['OfficeTitle'] or '').startswith('Member, House of Representatives'): continue
        n = int(r['TOTAL_VOTES']) if r['TOTAL_VOTES'] else int(r['WriteInVote'] or 0)
        k = nk(r['LocalityName']); V[k]['T26'] += n
        if r['Party'] == 'Democratic': V[k]['D26'] += n
# 2026 registration + ballots: turnout CSV precinct rows, registration cross-checked against vr.json
with open(f'{R}/2026/election_turnout.csv') as f:
    for r in csv.DictReader(f):
        k = nk(r['locality']); V[k]['reg26'] += int(r['TotalRegisteredVoters'] or 0); V[k]['bal26'] += int(r['TotalVoteTurnout'] or 0)
for r in json.load(open(f'{R}/2026/vr.json'))['data']:
    k = nk([x['text'] for x in r['localityName'] if x['languageId'] == 'en'][0]); assert V[k]['reg26'] == r['total'], ('reg26 vr.json', k)
# 2021 governor: summed from PRECINCT rows, checked against locality and state rows
rows = list(csv.reader(open(f'{R}/2021/gov2021_locality.csv')))
di, ti = rows[1].index('Democratic'), rows[0].index('Total Votes Cast')
cur, pre, loc = None, defaultdict(lambda: [0, 0]), {}
for r in rows[2:]:
    if r[0] == 'Locality': cur = nk(r[1]); loc[cur] = (int(r[di]), int(r[ti]))
    elif r[0] == 'Precinct': pre[cur][0] += int(r[di]); pre[cur][1] += int(r[ti])
    elif r[0] == 'State': state21 = (int(r[di]), int(r[ti]))
for k in loc: assert tuple(pre[k]) == loc[k], ('2021 precinct sum', k); V[k]['gD21'], V[k]['gT21'] = loc[k]
assert (sum(v[0] for v in loc.values()), sum(v[1] for v in loc.values())) == state21
# 2025 governor (certified ENR precinct CSV)
with open(f'{R}/2025/election_results.csv', encoding='latin-1') as f:
    for r in csv.DictReader(f):
        if r['OfficeTitle'] != 'Governor': continue
        n = int(r['TOTAL_VOTES']) if r['TOTAL_VOTES'] else int(r['WriteInVote'] or 0)
        k = nk(r['LocalityName']); V[k]['gT25'] += n
        if r['Party'] == 'Democratic': V[k]['gD25'] += n
NEED = ['D22', 'T22', 'reg22', 'bal22', 'D26', 'T26', 'reg26', 'bal26', 'gD21', 'gT21', 'gD25', 'gT25']
V = {k: v for k, v in V.items()}
assert len(V) == 133, len(V)
for k, v in V.items():
    for n in NEED: assert v.get(n, 0) > 0, (k, n)

# exact formatting, round half up
def rh(x, places):                      # x Fraction -> rounded Fraction
    s = 10 ** places; q = abs(x) * s; r = (2 * q.numerator + q.denominator) // (2 * q.denominator)
    return (r if x >= 0 else -r), s
def fx(x, places, sign=False, suffix=''):
    r, s = rh(F(x), places); a = abs(r); txt = f'{a // s}' + (f'.{a % s:0{places}d}' if places else '')
    neg = r < 0
    return ('-' if neg else ('+' if sign else '')) + txt + suffix
def ci(n, sign=False): return ('+' if sign and n >= 0 else '') + f'{n:,}'
def sh(a, b): return F(100 * a, b)
def ec(d, t, reg): r, _ = rh(F(d * reg, t), 0); return r

for v in V.values():
    v['E22'] = ec(v['gD21'], v['gT21'], v['reg22']); v['E26'] = ec(v['gD25'], v['gT25'], v['reg26'])
S = {n: sum(v[n] for v in V.values()) for n in NEED + ['E22', 'E26']}
def exp1(v):
    return [fx(sh(v['gD25'], v['gT25']), 1, suffix='%'), ci(v['E22']), ci(v['E26']), ci(v['E26'] - v['E22'], True),
            fx(sh(v['E26'] - v['E22'], v['E22']), 1, True, '%'), ci(v['D22']), ci(v['D26']), ci(v['D26'] - v['D22'], True),
            fx(sh(v['D26'] - v['D22'], v['D22']), 1, True, '%'), ci(v['T22']), ci(v['T26']), ci(v['T26'] - v['T22'], True),
            fx(sh(v['T26'] - v['T22'], v['T22']), 1, True, '%')]
def exp2(v):
    return [fx(sh(v['D22'], v['T22']), 1, suffix='%'), fx(sh(v['D26'], v['T26']), 1, suffix='%'),
            fx(sh(v['D26'], v['T26']) - sh(v['D22'], v['T22']), 2, True), fx(sh(v['gD21'], v['gT21']), 1, suffix='%'),
            ci(v['reg22']), fx(sh(v['gD25'], v['gT25']), 1, suffix='%'), ci(v['reg26']), ci(v['bal22']), ci(v['bal26'])]
C1 = ['Dem Baseline Share 2026 %', 'Est. Dem Baseline 2022', 'Est. Dem Baseline 2026*', 'Baseline Change #', 'Baseline Change %',
      'Dem House Votes 2022', 'Dem House Votes 2026*', 'Vote Change #', 'Vote Change %', 'Total Ballots 2022', 'Total Ballots 2026*',
      'Ballot Change #', 'Ballot Change %']
C2 = ['Dem Share House 2022 %', 'Dem Share House 2026* %', 'Change (pts)', 'Dem Baseline Share 2022 %', 'Total Registered 2022',
      'Dem Baseline Share 2026 %', 'Total Registered 2026*', 'DOE Ballots 2022', 'DOE Ballots 2026*']
order = sorted(V, key=lambda k: -F(V[k]['gD25'], V[k]['gT25']))

# parse PDF text
txt = subprocess.run(['pdftotext', '-layout', PDF, '-'], capture_output=True, text=True, check=True).stdout
NUM = r'[+\-]?[\d,]+(?:\.\d+)?%?'
parsed = []
for line in txt.splitlines():
    m = re.match(rf'^\s*(Statewide total|[A-Za-z][A-Za-z .&\']*?(?:County|City))((?:\s+{NUM})+)\s*$', line)
    if m: parsed.append((m.group(1).strip(), m.group(2).split()))
t1 = [p for p in parsed if len(p[1]) == 13]; t2 = [p for p in parsed if len(p[1]) == 9]
bad = [p for p in parsed if len(p[1]) not in (9, 13)]
checked = matched = 0; mism = []
for tbl, cols, fn in ((t1, C1, exp1), (t2, C2, exp2)):
    assert len(tbl) == 134, ('row count', len(tbl))
    names = [nk(n) for n, _ in tbl[:-1]]
    if names != order: mism.append(('ORDER', 'sort by 2026 baseline share', names[:3], order[:3]))
    for name, cells in tbl:
        src = S if name == 'Statewide total' else V[nk(name)]
        ex = fn(src)
        for c, pv, sv in zip(cols, cells, ex):
            checked += 1
            if pv == sv: matched += 1
            else: mism.append((name, c, pv, sv))
    checked += 134; matched += 134          # locality-name cells (matched to raw keys above)
print(f'PDF cells checked: {checked}  matched: {matched}  mismatches: {len(mism)}  unparsed rows: {len(bad)}')
for m in mism[:200]: print('MISMATCH', m)
json.dump({'checked': checked, 'matched': matched, 'mismatches': mism, 'unparsed': bad}, open('out/verify_pdf.json', 'w'), indent=1, default=str)
sys.exit(1 if mism or bad else 0)
