# Scene 3 · El problema de las distancias unitarias
MUSIC = {'data': 0.8, 'pad': 0.6}
INTENSITY = 0.5
cues = []

def dot(id, x, y, at, color=BLU, s=9, **k):
    """A point of the plane: a tiny circle."""
    return N(id, 'sandbox', x - s / 2, y - s / 2, s, s, at, color=color, label='', **k)

def seg(a, b, at, color=BLU, **k):
    """A unit segment between two points: straight, continuous, no balls."""
    return link(a, b, at, color=color, rel=True, **k)

# ------------------------------------------------------------------ 3a · the plane, a pair at distance one
PTS = [(300, 150), (410, 120), (520, 175), (640, 130), (730, 200), (350, 260), (470, 230), (620, 240),
       (700, 345), (400, 395), (540, 420), (650, 410), (270, 355), (760, 120)]
n = [N('pl', 'sandbox', 240, 80, 560, 380, '3a#planteó', color=TEAL, label='', open=True, bg='#0A0F17'),
     N('er', 'person', 80, 150, 60, 80, '3a#Erdős', color=AMB, cap='Erdős', capc='amber', capfs=12),
     T('y46', 66, 300, '1946', '3a#1946', color=AMB, fs=24, type=8, until='3b')]
for i, (x, y) in enumerate(PTS):
    n.append(dot(f'p{i}', x, y, f'3a#puntos+{0.12 * i:.2f}', color='#7C97FF'))
n.append(T('nn', 250, 468, 'n puntos', '3a#puntos', color=GRY, fs=12, until='3b'))
# the chosen pair (470,300)-(600,270) is moved to distance 1: drawn as the highlighted pair
n += [dot('q1', 470, 330, '3a#distancia', color=AMB, s=14, until='3b'), dot('q2', 600, 330, '3a#distancia', color=AMB, s=14, until='3b'),
      N('u1', 'chip', 520, 296, 30, 22, '3a#uno', color=AMB, label='1', fs=14, until='3b')]
lk = [seg('q1', 'q2', '3a#distancia+0.3', AMB, until='3b')]
cues.append(K('S3', '3b', n, lk, fs=1.0))

# ------------------------------------------------------------------ 3b · a line gives n-1, a grid gives many more
n = []; lk = []
LX0, LY, LS = 250, 135, 62
for i in range(8):
    n.append(dot(f'l{i}', LX0 + i * LS, LY, f'3b#línea+{0.2 * i:.2f}', color=TEAL, s=11))
    if i: lk.append(seg(f'l{i - 1}', f'l{i}', f'3b#línea+{0.2 * i + .15:.2f}', TEAL))
n.append(T('cl', LX0 + 8 * LS - 30, LY - 11, 'n−1', '3b#menos', color=TEAL, fs=26))
GX0, GY0, GS, GC, GR = 250, 250, 62, 8, 4
for r in range(GR):
    for c in range(GC):
        t = f'3b#cuadrícula+{0.06 * (r * GC + c):.2f}'
        n.append(dot(f'g{r}_{c}', GX0 + c * GS, GY0 + r * GS, t, color=AMB, s=11))
        if c: lk.append(seg(f'g{r}_{c - 1}', f'g{r}_{c}', t, AMB))
        if r: lk.append(seg(f'g{r - 1}_{c}', f'g{r}_{c}', t, AMB))
n.append(T('cg', GX0 + GC * GS - 30, GY0 + 85, '≈ 2n', '3b#bastantes', color=AMB, fs=26))
cues.append(K('3b', '3c', n, lk, fs=1.0))

# ------------------------------------------------------------------ 3c · the scaled grid and the almost flat curve
n = []; lk = []
for r in range(5):
    for c in range(5):
        n.append(dot(f'e{r}_{c}', 95 + c * 20, 255 + r * 20, '3c#cuadrícula', color=AMB, s=8, until='3c#escalada'))
        n.append(dot(f'f{r}_{c}', 80 + c * 36, 240 + r * 36, '3c#escalada', color=AMB, s=9))
for r in range(5):
    for c in range(5):
        if c: lk.append(seg(f'e{r}_{c - 1}', f'e{r}_{c}', '3c#cuadrícula+0.3', AMB, until='3c#escalada')); lk.append(seg(f'f{r}_{c - 1}', f'f{r}_{c}', '3c#escalada+0.2', AMB))
        if r: lk.append(seg(f'e{r - 1}_{c}', f'e{r}_{c}', '3c#cuadrícula+0.3', AMB, until='3c#escalada')); lk.append(seg(f'f{r - 1}_{c}', f'f{r}_{c}', '3c#escalada+0.2', AMB))
# axes and curve
AX, AY, AW, AH = 430, 440, 450, 330
n += [dot('a0', AX, AY, '3c#consigue', color=GRY, s=6), dot('a1', AX + AW, AY, '3c#consigue', color=GRY, s=6), dot('a2', AX, AY - AH, '3c#consigue', color=GRY, s=6),
      T('ax', AX + AW - 40, AY + 12, 'n', '3c#consigue', color=GRY, fs=14), T('ay', AX - 70, AY - AH - 4, 'parejas', '3c#consigue', color=GRY, fs=12)]
lk += [seg('a0', 'a1', '3c#consigue', GRY), seg('a0', 'a2', '3c#consigue', GRY)]
M = 30
for i in range(M):
    f = i / (M - 1); x = AX + 14 + f * (AW - 40); y = AY - 12 - f * (AH - 70) * (1 + .06 * f * f)
    n.append(dot(f'c{i}', x, y, f'3c#algo+{0.16 * i:.2f}', color=TEAL, s=7))
n.append(W.sheet('ca', 500, 95, 190, 80, ['Erdős:', 'casi n'], at='3c#conjeturó', fs=21, color='amber'))
cues.append(K('3c', '3d', n, lk, fs=1.0))

# ------------------------------------------------------------------ 3d / 3e · the gap between n and n^(4/3); it gets filled
BX, YA, YB, YC = 420, 405, 90, 345          # band centre x; casi n, n^(4/3), n^(1,014)
n = [N('fr', 'sandbox', BX - 46, YB, 92, YA - YB, '3d#Durante+0.4', color=RED, open=True, label=''),
     N('m1', 'chip', BX + 66, YA - 13, 96, 26, '3d#casi', color=TEAL, label='casi n', fs=14),
     N('m2', 'chip', BX + 66, YB - 13, 120, 26, '3d#cuatro', color=RED, label='n^(4/3)', fs=14),
     T('t0', 650, 200, '1946', '3d#Durante', color=GRY, fs=52, until='3d#ochenta+1.2'),
     T('t1', 650, 200, '2026', '3d#ochenta+1.2', color='#E7EBF1', fs=52, type=6, until='3e#refutó'),
     N('why', 'question', BX - 18, 232, 36, 36, '3d#nadie', color=GRY, until='3e#refutó')]
lk = []
# 3e: the new mark appears and the strip below it is filled
n += [N('fl2', 'sandbox', BX - 46, YC, 92, YA - YC, '3e#configuraciones', color=GRN, label='', fill=1, rx=0),
      N('m3', 'chip', BX + 66, YC - 13, 150, 26, '3e#delta', color=GRN, label='n^(1,014)', fs=14),
      N('fg', 'flFly', BX + 230, YC - 46, 30, 42, '3e#delta+0.6', color=GRN),
      N('sw', 'person', 700, 170, 46, 62, '3e#Sawin', color=BLU, cap='Sawin', capc='muted', capfs=12),
      N('ai', 'agent', 140, 300, 40, 40, '3e#modelo', color=BLU, label='OpenAI')]
lk += [link('ai', 'fl2', '3e#Encontró', color=BLU, curve=.3), link('sw', 'm3', '3e#catorce', color=BLU, curve=.3)]
cues.append(K('3d', '3f', n, lk, fs=1.0))

# ------------------------------------------------------------------ 3f · from the square grid to a dense mesh, fed by number theory
n = []; lk = []
for r in range(4):
    for c in range(5):
        n.append(dot(f'z{r}_{c}', 380 + c * 40, 150 + r * 40, '3f#cuadrícula', color=AMB, s=9, until='3f#sustituyó'))
for r in range(4):
    for c in range(5):
        if c: lk.append(seg(f'z{r}_{c - 1}', f'z{r}_{c}', '3f#cuadrícula+0.3', AMB, until='3f#sustituyó'))
        if r: lk.append(seg(f'z{r - 1}_{c}', f'z{r}_{c}', '3f#cuadrícula+0.3', AMB, until='3f#sustituyó'))
n.append(T('zg', 380, 300, 'enteros gaussianos', '3f#enteros', color=AMB, fs=14, until='3f#sustituyó'))
MC, MR, MP = 17, 8, 28; MX0, MY0 = 240, 80
for r in range(MR):
    for c in range(MC):
        n.append(dot(f'h{r}_{c}', MX0 + c * MP, MY0 + r * MP, f'3f#sustituyó+{0.025 * (r * MC + c):.2f}', color=TEAL, s=8))
for r in range(MR):
    for c in range(MC):
        t = f'3f#sustituyó+{0.025 * (r * MC + c) + .15:.2f}'
        if c: lk.append(seg(f'h{r}_{c - 1}', f'h{r}_{c}', t, TEAL))
        if r: lk.append(seg(f'h{r - 1}_{c}', f'h{r}_{c}', t, TEAL))
n.append(N('ant', 'server', 299, 400, 330, 66, '3f#teoría', color=VIO, label='teoría algebraica de números', sub='', fs=14))
lk.append(OR('ant', 'h7_8', '3f#teoría+0.6', VIO, 'v'))
cues.append(K('3f', '3g', n, lk, fs=1.0))

# ------------------------------------------------------------------ 3g · two quotes
def qw(lines): return max(len(l) for l in lines) * 15 * .62 + 40
L1 = ['«Lo habría aceptado', 'en Annals»']; L2 = ['«Lo intenté', 'y fracasé»']
x1, x2 = 90, 600
n = [N('gw', 'person', x1 + qw(L1) / 2 - 35, 300, 70, 100, '3g#Gowers', color=TEAL, cap='Gowers', capc='teal', capfs=12),
     N('ts', 'person', x2 + qw(L2) / 2 - 35, 300, 70, 100, '3g#Tsimerman', color=AMB, cap='Tsimerman', capc='amber', capfs=12),
     Q('q1', x1, 140, 0, L1, '3g#habría', color=TEAL),
     Q('q2', x2, 140, 0, L2, '3g#intentado', color=AMB)]
lk = [OR('gw', 'q1', '3g#habría+0.2', TEAL, 'v'), OR('ts', 'q2', '3g#intentado+0.2', AMB, 'v')]
cues.append(K('3g', 'E3', n, lk, fs=1.0))
