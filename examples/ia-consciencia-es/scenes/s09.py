# Scene 9 · Los números
MUSIC = {'pad': 0.7, 'data': 0.5}
INTENSITY = 0.45
cues = []

# 9a — the small counter in the corner comes back to the centre, still on '?'
n = [N('qs', 'txt', 872, 20, 30, 40, 0.05, color='#E7EBF1', fs=34, text='?', blink=.45, bf=3,
       move=[dict(at='9a#probabilidad', x=462, y=230, dur=1.6)], until='9b')]
# 9b — Chalmers, 2023: two big counters "< 10 %" and "> 25 %", with 2023 and ≈ 2033
n += [W.counter('c10', 160, 210, 10, '9b#menos', pre='< ', suf=' %', w=260, fs=64, dur=1.2, cap='modelos de 2023', until='9c'),
      W.counter('c25', 540, 210, 25, '9b#más', pre='> ', suf=' %', w=260, fs=64, dur=1.2, cap='≈ 2033', until='9c'),
      T('y23', 40, 36, '2023', '9b#2023', color=TEAL, fs=24, until='9c'), person('chm', 480, 420, '9b#Chalmers', color='amber', s=40, cap='Chalmers', capfs=12, until='9c')]
# 9c — Berg: an empty horizontal ruler
RX, RW, RY = 100, 760, 330
X = lambda v: RX + RW * v / 100
n += [N('rl', 'bar', RX, RY, RW, 4, '9c#midió', color='muted', fill=1, rx=0)]
for v in range(0, 101, 10):
    n += [N(f'tk{v}', 'bar', X(v) - 1, RY - 8, 2, 20, '9c#midió', color='muted', fill=1, rx=0)]
    if v % 50 == 0: n.append(T(f'tl{v}', X(v) - 12, RY + 20, f'{v} %', '9c#midió', color=GRY, fs=12))
# 9d — on the ruler, in order: the chip (20–40), a bee (≈ 50), an octopus and a crow (60–80), a person (≈ 90)
n += [N('rg1', 'bar', X(20), RY - 3, X(40) - X(20), 10, '9d#modelos', color='blue', fill=1, rx=0),
      W.pic('ci', 'chip', X(30) - 26, RY - 90, 52, 52, '9d#modelos', color='blue', cap='20–40 %', capfs=12),
      P('be', 'bee', X(50) - 28, RY - 64, 56, '9d#abejas', color='amber', cap='abejas', capfs=11), T('bel', X(50) - 18, RY + 40, '≈ 50', '9d#abejas', color=AMB, fs=12),
      N('rg2', 'bar', X(60), RY - 3, X(80) - X(60), 10, '9d#humanos-1.2', color='teal', fill=1, rx=0),
      P('oc', 'octopus', X(66) - 26, RY - 64, 52, '9d#humanos-1.2', color='teal', cap='pulpos', capfs=11), P('cr', 'crow', X(76) - 26, RY - 64, 52, '9d#humanos-0.9', color='teal', cap='cuervos', capfs=11),
      T('rgl', X(70) - 22, RY + 40, '60–80 %', '9d#humanos-0.9', color=TEAL, fs=12),
      person('hm', X(90), RY - 40, '9d#humanos', color='blue', s=44), T('hml', X(90) - 18, RY + 40, '≈ 90', '9d#humanos', color=BLU, fs=12)]
for x in n:
    if x['id'] in ('rl',) or x['id'].startswith(('tk', 'tl', 'rg', 'ci', 'be', 'oc', 'cr', 'hm')): x['until'] = '9e'
cues.append(K('S9', '9e', n, [], fs=1.0))

# 9e — Noa Weiss: a big counter "> 50 %"
n = [person('nw', 260, 300, '9e', color='teal', s=60, cap='Noa Weiss', capfs=13, until='9f'),
     W.counter('c50', 400, 230, 50, '9e#probable', pre='> ', suf=' %', w=280, fs=72, dur=1.2, until='9f'),
     # 9f — a cloud with "30 %"; a silhouette opens its umbrella
     P('cl', 'cloud', 330, 170, 150, '9f#lluvia', color='blue'), T('c30', 302, 168, '30 %', '9f#lluvia', color=BLU, fs=22),
     person('us', 560, 340, '9f#gente', color='teal', s=70),
     P('uc', 'umbrellac', 600, 290, 70, '9f#gente', color='teal', until='9f#paraguas'),
     P('uo', 'umbrella', 560, 230, 120, '9f#paraguas', color='teal')]
cues.append(K('9e', 'E9', n, [], fs=1.0))
