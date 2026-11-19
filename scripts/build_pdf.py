"""Build the 133-locality PDF (modeled on Nebraska_93_County_Democratic_Registration_and_Vote_Change.pdf)
from the double-verified data/virginia_localities_final.csv.
Virginia has NO party registration: the 'Dem Baseline' columns are a labeled substitute
(Democratic share of the prior odd-year governor vote; estimated count = share x total registered voters)."""
import csv, json
from fractions import Fraction
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = '/usr/share/fonts/truetype/sand-box/google/Carlito/'
pdfmetrics.registerFont(TTFont('Carlito', FD + 'Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Carlito-Bold', FD + 'Carlito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Carlito-Italic', FD + 'Carlito-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Carlito-BoldItalic', FD + 'Carlito-BoldItalic.ttf'))
from reportlab.lib.fonts import addMapping
addMapping('Carlito', 0, 0, 'Carlito'); addMapping('Carlito', 1, 0, 'Carlito-Bold')
addMapping('Carlito', 0, 1, 'Carlito-Italic'); addMapping('Carlito', 1, 1, 'Carlito-BoldItalic')

OUT = 'pdf/Virginia_133_Locality_Democratic_Baseline_and_Vote_Change.pdf'
rows = list(csv.DictReader(open('data/virginia_localities_final.csv')))
I = lambda r, c: int(float(r[c]))
meta = json.load(open('raw/2026/election_meta.json'))

def est(d, tot, reg):            # round-half-up of d/tot*reg, exact
    num, den = d * reg, tot
    return (2 * num + den) // (2 * den)
def cnt(n): return f'{n:,}'
def chg(n): return f'{n:+,}'
def pct(x): return f'{x:.1f}%'
def pchg(new, old): return f'{100 * (new - old) / old:+.1f}%'
def pts(x): return f'{x:+.2f}'

L = []
for r in rows:
    v = {c: I(r, c) for c in ['D22', 'D26', 'house_total22', 'house_total26', 'reg22', 'reg26',
                              'govD21', 'govTot21', 'govD25', 'govTot25', 'ballots22', 'ballots26']}
    v['name'] = r['locality']
    v['B22'] = 100 * v['govD21'] / v['govTot21']; v['B26'] = 100 * v['govD25'] / v['govTot25']
    v['E22'] = est(v['govD21'], v['govTot21'], v['reg22']); v['E26'] = est(v['govD25'], v['govTot25'], v['reg26'])
    L.append(v)
L.sort(key=lambda v: -v['B26'])
T = {c: sum(v[c] for v in L) for c in ['D22', 'D26', 'house_total22', 'house_total26', 'reg22', 'reg26',
                                        'govD21', 'govTot21', 'govD25', 'govTot25', 'ballots22', 'ballots26', 'E22', 'E26']}
T['name'] = 'Statewide total'
T['B22'] = 100 * T['govD21'] / T['govTot21']; T['B26'] = 100 * T['govD25'] / T['govTot25']

def row1(v):
    return [v['name'], pct(v['B26']), cnt(v['E22']), cnt(v['E26']), chg(v['E26'] - v['E22']), pchg(v['E26'], v['E22']),
            cnt(v['D22']), cnt(v['D26']), chg(v['D26'] - v['D22']), pchg(v['D26'], v['D22']),
            cnt(v['house_total22']), cnt(v['house_total26']), chg(v['house_total26'] - v['house_total22']),
            pchg(v['house_total26'], v['house_total22'])]
def row2(v):
    s22 = 100 * v['D22'] / v['house_total22']; s26 = 100 * v['D26'] / v['house_total26']
    return [v['name'], pct(s22), pct(s26), pts(s26 - s22), pct(v['B22']), cnt(v['reg22']), pct(v['B26']), cnt(v['reg26']),
            cnt(v['ballots22']), cnt(v['ballots26'])]

H1 = ['Locality', 'Dem Baseline\nShare 2026 %\n(2025 Gov)', 'Est. Dem\nBaseline 2022', 'Est. Dem\nBaseline 2026*',
      'Baseline\nChange #', 'Baseline\nChange %', 'Dem House\nVotes 2022', 'Dem House\nVotes 2026*', 'Vote Change\n#',
      'Vote Change %\n(on 2022 base)', 'Total\nBallots† 2022', 'Total\nBallots† 2026*', 'Ballot Change\n#', 'Ballot\nChange %']
H2 = ['Locality', 'Dem Share of\nHouse Votes\n2022 %', 'Dem Share of\nHouse Votes\n2026* %', 'Change (pts)',
      'Dem Baseline\nShare 2022 %\n(2021 Gov)', 'Total Registered\n2022', 'Dem Baseline\nShare 2026 %\n(2025 Gov)',
      'Total Registered\n2026*', 'DOE-Reported\nBallots 2022‡', 'DOE-Reported\nBallots 2026*']

reg_fell = [v['name'] for v in L if v['reg26'] < v['reg22']]
gov_fell = [v['name'] for v in L if v['govD25'] < v['govD21']]
over94 = sum(v['house_total22'] > v['ballots22'] for v in L)
top_share = L[0]['name']; top_raw = max(L, key=lambda v: v['E26'])['name']

with open('data/virginia_pdf_table.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['table'] + [h.replace('\n', ' ') for h in H1]); [w.writerow(['1'] + row1(v)) for v in L + [T]]
    w.writerow(['table'] + [h.replace('\n', ' ') for h in H2]); [w.writerow(['2'] + row2(v)) for v in L + [T]]

ss = ParagraphStyle('t', fontName='Carlito-Bold', fontSize=13, leading=16)
si = ParagraphStyle('s', fontName='Carlito-Italic', fontSize=7.6, leading=9.2)
sh = ParagraphStyle('h', fontName='Carlito-Bold', fontSize=7.2, leading=8.4, alignment=1, textColor=colors.white)
NAVY = colors.HexColor('#1F2A4D'); BLUE = colors.HexColor('#DCE8F5'); ORANGE = colors.HexColor('#FBE3D3')
SRC = ("*2026 figures are unofficial and not certified by the Virginia State Board of Elections (DOE Enhanced Voting results site "
       "and turnout file, as of Nov 19, 2026, 11:27 AM CST). 2022 US House votes, ballots and registration: DOE 2022 November General "
       "results (certified). 2021 governor: DOE historical elections database, contest 147466 (certified). 2025 governor: DOE results site, "
       "2025 November General (certified). Registered voters are total (active + inactive) registered voters reported with each November general. "
       "Votes are votes for the Democratic US House candidates, summed across all districts in a locality.")
SUB = ("<b>Substitute baseline, not party registration:</b> Virginia does not register voters by party, so there is no Democratic registration to report. "
       "Dem Baseline Share = Democratic governor votes ÷ total governor votes in the prior odd-year election (2021 for the 2022 column, 2025 for 2026). "
       "Est. Dem Baseline = that share × total registered voters, rounded. It is an estimate, not a count of registered Democrats.")
DEN = (f"†Total ballots = total US House votes cast (all candidates, including write-ins), the denominator used in the analysis. "
       f"DOE's 2022 turnout report leaves out many early, mailed and provisional ballots (US House votes exceed it in {over94} of 133 localities), "
       "so it is not used; DOE-reported ballots are shown in the second table for reference.")

def legend():
    t = Table([['Legend:', f"Total registered voters fell ({', '.join(reg_fell)})", '',
                f"Democratic governor votes fell 2021 to 2025 ({', '.join(gov_fell)})"]],
              colWidths=[50, 300, 20, 300])
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Carlito', 7.5), ('FONT', (0, 0), (0, 0), 'Carlito-Bold', 7.5),
                           ('BACKGROUND', (1, 0), (1, 0), BLUE), ('BACKGROUND', (3, 0), (3, 0), ORANGE)]))
    return t

def table(H, body, widths):
    data = [[Paragraph(h.replace('\n', '<br/>'), sh) for h in H]] + body
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('FONT', (0, 1), (-1, -1), 'Carlito', 7.6), ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
          ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
          ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#9AA3B5')),
          ('TOPPADDING', (0, 1), (-1, -1), 0.6), ('BOTTOMPADDING', (0, 1), (-1, -1), 0.9),
          ('FONT', (0, len(data) - 1), (-1, len(data) - 1), 'Carlito-Bold', 7.8),
          ('BACKGROUND', (0, len(data) - 1), (-1, len(data) - 1), colors.HexColor('#E8E8E8'))]
    for i, r in enumerate(body, 1):
        if r[0] in reg_fell: st.append(('BACKGROUND', (0, i), (-1, i), BLUE))
        if r[0] in gov_fell: st.append(('BACKGROUND', (0, i), (-1, i), ORANGE))
    t.setStyle(TableStyle(st)); return t

story = [Paragraph('Virginia 133 Localities — Democratic Baseline (substitute for party registration), Democratic US House Votes and Total Ballots, 2022 vs 2026*', ss),
         Paragraph(f'Sorted by 2026 Democratic baseline share (Democratic share of the Nov 2025 governor vote; Virginia has no party registration), highest first. '
                   f'{top_share} leads by share; {top_raw} leads by estimated baseline count. 133 counties and independent cities plus statewide total.', si),
         Spacer(1, 4), Paragraph(SRC, si), Spacer(1, 2), Paragraph(SUB, si), Spacer(1, 2), Paragraph(DEN, si), Spacer(1, 4), legend(), Spacer(1, 4),
         table(H1, [row1(v) for v in L + [T]], [96] + [49] * 3 + [45, 43] + [49] * 3 + [56] + [50, 50, 49, 41]),
         PageBreak(),
         Paragraph('Democratic US House Votes as a Share of Total House Votes, Democratic Baseline Share and Registered Voters, 2022 vs 2026*', ss),
         Paragraph('Sorted by 2026 Democratic baseline share, highest first (same order as the first table).', si), Spacer(1, 3),
         Paragraph(SRC, si), Spacer(1, 2), Paragraph(SUB, si), Spacer(1, 2),
         Paragraph('Share of House votes = Democratic US House votes ÷ total US House votes. Change (pts) = 2026 share minus 2022 share, in percentage points. '
                   '‡DOE-reported ballots: DOE turnout statistics (2022 report incomplete, see note †). Total registered = active + inactive.', si),
         Spacer(1, 4), table(H2, [row2(v) for v in L + [T]], [110, 68, 68, 58, 72, 78, 72, 78, 72, 72])]

def foot(c, d):
    c.saveState(); c.setFont('Carlito-Italic', 7.5)
    c.drawString(30, 18, '*2026 figures unofficial, not SBE-certified. Dem Baseline = governor-vote substitute; Virginia has no party registration.')
    c.drawRightString(762, 18, f'Page {d.page} of {{NP}}'); c.restoreState()

class Doc(SimpleDocTemplate):
    pass
from reportlab.pdfgen import canvas
class NumCanvas(canvas.Canvas):
    def __init__(s, *a, **k): super().__init__(*a, **k); s._pages = []
    def showPage(s): s._pages.append(dict(s.__dict__)); s._startPage()
    def save(s):
        n = len(s._pages)
        for p in s._pages:
            s.__dict__.update(p); s.setFont('Carlito-Italic', 7.5)
            s.drawString(30, 18, '*2026 figures unofficial, not SBE-certified. Dem Baseline = governor-vote substitute; Virginia has no party registration.')
            s.drawRightString(762, 18, f'Page {s._pageNumber} of {n}'); super().showPage()
        super().save()
doc = SimpleDocTemplate(OUT, pagesize=landscape(letter), leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=30,
                        title='Virginia 133 Localities: Democratic Baseline (substitute), US House Votes and Ballots, 2022 vs 2026 (unofficial)',
                        author='mbenson8989')
doc.build(story, canvasmaker=NumCanvas)
print('pdf written', OUT)
