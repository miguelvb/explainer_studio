# Scene 2 · Qué se ha publicado
MUSIC = {'data': 0.8, 'pad': 0.5}
INTENSITY = 0.4
cues = []

# 2a — the repository: 722 manuscripts (tower) grouped into 372 packages
FX, FY = 130, 310
n = [N('gh', 'chip', 100, 270, 90, 26, '2a#repositorio', color='muted', label='GitHub', fs=12),
     N('fo', 'folder', FX, FY, 120, 90, '2a#repositorio', color='amber', cap='openai/math', capfs=13)]
n += mt_tower('d', 480, 470, t0='2a#setecientos', dt=0.025, src=(FX + 50, FY + 30))
x0 = 480 - 6 * 22 / 2
for r in range(14):
    for p in range(3):
        n.append(N(f'pk{r}_{p}', 'sandbox', x0 + p * 44 - 1, 470 - (r + 1) * 25 + 1, 42, 23, f'2a#trescientas+{0.05 * (r * 3 + p):.2f}', color='teal', label=''))
n += [W.counter('n722', 640, 230, 722, '2a#setecientos', cap='manuscritos', w=200, dur=2.0, fs=60, until='2a#trescientas-0.2'),
      W.counter('n372', 640, 230, 372, '2a#trescientas', cap='familias', w=200, dur=2.0, fs=60, **{'from': 722})]
cues.append(K('S2', '2b', n, [], fs=1.0))

# 2b — funnel: ~4,000 problems in, packages out; 3 h per result
SX = 330
n = [N('s1', 'sandbox', SX - 150, 40, 300, 110, '2b#modelo', color='blue', label=''),
     N('s2', 'sandbox', SX - 95, 175, 190, 80, '2b#modelo+0.5', color='blue', label=''),
     N('s3', 'sandbox', SX - 40, 280, 80, 56, '2b#modelo+1.0', color='blue', label=''),
     N('c1', 'crowd', SX - 140, 50, 280, 90, '2b#cuatro', color='blue', n=400, grow=[dict(at='2b#cuatro', n=400, dur=2.0), dict(at='2b#salieron-0.5', n=70, dur=2.5)]),
     N('c2', 'crowd', SX - 85, 185, 170, 60, '2b#salieron-0.8', color='blue', n=60, grow=[dict(at='2b#salieron-0.8', n=70, dur=1.0), dict(at='2b#salieron+1.5', n=18, dur=1.5)]),
     N('c3', 'crowd', SX - 30, 290, 60, 36, '2b#salieron+0.5', color='teal', n=20, grow=[dict(at='2b#salieron+0.5', n=20, dur=1.0)]),
     W.counter('n4k', 560, 60, 4000, '2b#cuatro', cap='problemas', w=200, dur=2.0, fs=56),
     W.counter('h3', 560, 280, 3, '2b#tres', cap='horas por resultado', w=200, dur=1.0, fs=56, suf=' h')]
for i in range(6):
    n.append(N(f'pq{i}', 'doc', SX - 11, 330, 22, 28, f'2b#salieron+{1.2 + 0.5 * i:.1f}', color='teal',
               move=[dict(at=f'2b#salieron+{2.2 + 0.5 * i:.1f}', x=SX - 140 + 50 * i, y=410, dur=0.9)]))
lk = [OR('s1', 's2', '2b#modelo+0.5', 'blue', 'v'), OR('s2', 's3', '2b#modelo+1.0', 'blue', 'v')]
cues.append(K('2b', '2c', n, lk, fs=1.0))

# 2c — packages spread into columns by area of mathematics
AREAS = [('números', 6, '2c#teoría'), ('geometría', 4, '2c#geometría'), ('análisis', 5, '2c#análisis'), ('informática', 9, '2c#informática'),
         ('física mat.', 3, '2c#física'), ('topología', 3, '2c#topología'), ('combinatoria', 8, '2c#topología', 0.9)]
n = []
for i, (nm, h, t, *o) in enumerate(AREAS):
    o0 = o[0] if o else 0
    cx = 110 + i * 123
    n.append(ch(f'a{i}', cx, 470, 100, nm, f'{t}+{o0}', color='teal' if nm in ('informática', 'combinatoria') else 'muted', fs=12))
    for k in range(h):
        n.append(N(f'b{i}_{k}', 'sandbox', cx - 36, 440 - 22 * (k + 1), 72, 17, f'{t}+{o0 + 0.12 * k + 0.2:.2f}', color='teal', label=''))
cues.append(K('2c', '2d', n, [], fs=1.0))

# 2d — famous titles: some flagged green with a Lean seal, others grey with a question mark
FVX, FVY, RH2 = 290, 80, 46
rc2 = lambda j: FVY + 48 + j * RH2
items = [dict(name='Región sin ceros de la función zeta', at='2d#región'), dict(name='Décimo problema de Hilbert (racionales)', at='2d#Hilbert'),
         dict(name='Fórmula de Birch y Swinnerton-Dyer', at='2d#Birch')]
n = [AN('oa', 50, 120, 'OpenAI', at='2d#afirmaciones', color='blue'),
     W.folder_view('tt', FVX, FVY, items, label='openai/math', w=420, h=48 + 3 * RH2 - 8, rh=RH2, fs=13, at='2d#nombres')]
for j in range(3):
    ok = j == 0
    n.append(N(f'fg{j}', 'flag', 735, rc2(j) - 15, 26, 30, '2d#afirmaciones+%.1f' % (0.4 * j + 0.3), color='teal' if ok else 'muted', dashed=not ok))
    if ok: n.append(ch('ln', 800, rc2(j), 54, 'Lean', '2d#afirmaciones+0.8', color='teal', fs=12))
    else: n.append(ic(f'q{j}', 'question', 812, rc2(j), 26, '2d#afirmaciones+%.1f' % (0.4 * j + 0.5), color='muted'))
lk = [link('oa', 'tt', '2d#afirmaciones', color='blue', bi=True)]
cues.append(K('2d', 'E2', n, lk, fs=1.0))
