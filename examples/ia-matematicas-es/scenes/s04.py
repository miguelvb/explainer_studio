# Scene 4 · El número pi
MUSIC = {'data': 0.6, 'pad': 0.8, 'bells': 0.3}
INTENSITY = 0.55
cues = []

def dot(id, x, y, at, color=BLU, s=9, **k):
    return N(id, 'sandbox', x - s / 2, y - s / 2, s, s, at, color=color, label='', **k)

def seg(a, b, at, color=BLU, **k):
    return link(a, b, at, color=color, rel=True, **k)

def Yv(v): return 470 - (v - 2) * 52          # y of exponent value v on the meter
SX = 790                                         # x of the meter axis
PX, LY = 330, 250                                # pi on the number line

# ================================================================== 4a-4b (circle, number line, narrowing bands, exponent meter)
n = []; lk = []
# --- 4a: a circle (made of points) with its diameter, the symbol pi, and the number line with two fractions
for i in range(36):
    a = i / 36 * 2 * math.pi
    n.append(dot(f'cc{i}', 130 + 52 * math.cos(a), 135 + 52 * math.sin(a), f'4a#número+{0.04 * i:.2f}', color=TEAL, s=7))
n += [dot('d1', 78, 135, '4a#número+1.0', color=TEAL, s=7), dot('d2', 182, 135, '4a#número+1.0', color=TEAL, s=7),
      T('pi', 225, 108, 'π', '4a#pi', color='#E7EBF1', fs=60)]
lk.append(seg('d1', 'd2', '4a#número+1.2', TEAL))
n += [dot('n0', 80, LY, '4a#irracional', color=GRY, s=6), dot('n1', 640, LY, '4a#irracional', color=GRY, s=6)]
lk.append(seg('n0', 'n1', '4a#irracional', GRY))
n += [dot('np', PX, LY, '4a#irracional+0.4', color=AMB, s=13), T('pl', PX - 6, LY + 14, 'π', '4a#irracional+0.4', color=AMB, fs=18),
      dot('f1', PX + 15, LY, '4a#veintidós', color=VIO, s=8), dot('f2', PX + 140, LY, '4a#trescientos', color=TEAL, s=8),
      N('c2', 'chip', PX + 15 - 36, 176, 72, 26, '4a#veintidós', color=TEAL, label='355/113', fs=12),
      N('c1', 'chip', PX + 140 - 30, 196, 60, 26, '4a#trescientos', color=VIO, label='22/7', fs=12)]
# NB: 355/113 is the very close one (15 px from pi), 22/7 the farther one (140 px)
lk += [seg('c2', 'f1', '4a#trescientos+0.3', TEAL), seg('c1', 'f2', '4a#veintidós+0.3', VIO)]

# --- 4b: bands narrowing around pi while fractions with bigger denominators are tried; the exponent meter wobbles
BW = [(300, '4b#aproximaciones'), (170, '4b#aproximaciones+1.0'), (90, '4b#aproximaciones+2.0'), (44, '4b#aproximaciones+3.0')]
for j, (w, t) in enumerate(BW):
    tu = BW[j + 1][1] if j + 1 < len(BW) else None
    n.append(N(f'bd{j}', 'sandbox', PX - w / 2, LY - 36 - j * 0, w, 72, t, color=AMB, open=True, label='', **({'until': tu} if tu else {})))
# the meter (axis made of ticks) appears with the word "exponente"
for v in range(2, 10):
    n.append(dot(f'k{v}', SX, Yv(v), f'4b#exponente+{0.08 * (v - 2):.2f}', color=GRY, s=7))
    if v > 2: lk.append(seg(f'k{v - 1}', f'k{v}', f'4b#exponente+{0.08 * (v - 2):.2f}', GRY))
    if v % 2 == 0: n.append(T(f'kt{v}', SX + 18, Yv(v) - 8, str(v), f'4b#exponente+{0.08 * (v - 2):.2f}', color=GRY, fs=14))
n.append(T('ke', SX - 40, Yv(9) - 34, 'exponente', '4b#exponente', color=GRY, fs=12))
mv = [dict(at='4b#exponente+1.2', x=SX - 64, y=Yv(5) - 13, dur=1.0), dict(at='4b#Cuanto', x=SX - 64, y=Yv(3.2) - 13, dur=1.0),
      dict(at='4b#Cuanto+1.6', x=SX - 64, y=Yv(6.5) - 13, dur=1.2), dict(at='4b#fracciones', x=SX - 64, y=Yv(4) - 13, dur=1.0)]
n.append(N('mp1', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4b#exponente+0.8', color=AMB, label='π', fs=14, move=mv))

cues.append(K('S4', '4c', n, lk, fs=1.0))

# ================================================================== 4h-4n · aside "para curiosos": what the exponent is
n = []; lk = []
# 4h: the symbol mu with a question mark
n += [N('cur', 'chip', 700, 40, 190, 28, '4c#curiosidad', color=VIO, label='para curiosos', fs=14),
      T('mu', 380, 170, 'μ', '4c#exponente', color=AMB, fs=140, until='4d#Una'),
      N('muq', 'question', 520, 190, 56, 56, '4c#exponente+0.8', color=GRY, until='4d#Una')]
# 4i: fraction p/q, then a ruler 3.0-3.3 with marks every 1/7; pi falls beside 22/7
RX0, RW, RY = 80, 800, 330
def RXv(v): return RX0 + (v - 3.0) / 0.3 * RW
n += [T('fp', 70, 60, 'p', '4d#numerador', color=TEAL, fs=44, until='4f#Para'), T('fq', 70, 120, 'q', '4d#denominador', color=VIO, fs=44, until='4f#Para'),
      dot('fb0', 60, 112, '4d#numerador', color='#E7EBF1', s=5, until='4f#Para'), dot('fb1', 120, 112, '4d#numerador', color='#E7EBF1', s=5, until='4f#Para'),
      T('fpl', 140, 74, 'numerador', '4d#numerador', color=GRY, fs=14, until='4f#Para'), T('fql', 140, 134, 'denominador', '4d#denominador', color=GRY, fs=14, until='4f#Para')]
lk.append(seg('fb0', 'fb1', '4d#numerador', GRY, until='4f#Para'))
n += [dot('r0', RX0, RY, '4d#siete', color=GRY, s=6, until='4f#Para'), dot('r1', RX0 + RW, RY, '4d#siete', color=GRY, s=6, until='4f#Para'),
      T('rq', RX0, RY - 70, 'q = 7', '4d#siete', color=VIO, fs=18, until='4f#Para')]
lk.append(seg('r0', 'r1', '4d#siete', GRY, until='4f#Para'))
for j in range(3):
    n.append(N(f'm7_{j}', 'bar', RXv(3 + j / 7) - 2, RY - 16, 4, 32, f'4d#siete+{0.2 + 0.2 * j:.2f}', color='violet', fill=1, until='4f#Para'))
    n.append(T(f'l7_{j}', RXv(3 + j / 7) - 14, RY + 24, f'{21 + j}/7', f'4d#siete+{0.2 + 0.2 * j:.2f}', color=VIO, fs=14, until='4f#Para'))
n += [dot('pi_', RXv(math.pi), RY - 34, '4d#Pi', color=AMB, s=13, until='4f#Para'), T('pil', RXv(math.pi) - 28, RY - 66, 'π', '4d#Pi', color=AMB, fs=24, until='4f#Para'),
      N('er1', 'chip', RXv(22 / 7) + 20, RY + 60, 210, 26, '4d#milésimo', color=RED, label='error ≈ 0,0013', fs=13, until='4f#Para')]
# 4j: finer ruler, q = 113 (34 marks)
RY2 = 450
n += [dot('s0', RX0, RY2, '4e#fina', color=GRY, s=6, until='4f#Para'), dot('s1', RX0 + RW, RY2, '4e#fina', color=GRY, s=6, until='4f#Para'),
      T('rq2', RX0, RY2 - 54, 'q = 113', '4e#fina', color=VIO, fs=18, until='4f#Para')]
lk.append(seg('s0', 's1', '4e#fina', GRY, until='4f#Para'))
for j in range(35):
    n.append(N(f'm113_{j}', 'bar', RXv(339 / 113 + j / 113) - 1, RY2 - 9, 2, 18, f'4e#ciento+{0.04 * j:.2f}', color='violet', fill=1, until='4f#Para'))
n += [dot('pi2', RXv(math.pi), RY2 - 24, '4e#juntas', color=AMB, s=11, until='4f#Para'),
      N('er2', 'chip', RXv(355 / 113) + 30, RY2 - 62, 260, 26, '4e#millonésima', color=RED, label='error < 0,000001', fs=13, until='4f#Para'),
      T('c355', RXv(355 / 113) - 30, RY2 + 14, '355/113', '4e#trescientos', color=VIO, fs=14, until='4f#Para')]
# 4k-4n: log-log chart of precision vs denominator; lines 2, 3, 4
CX0, CY0 = 110, 450
def CX(x): return CX0 + x * 92
def CY(y): return CY0 - y * 22.5
CONV = [(7, 2.898), (106, 4.08), (113, 6.574), (33102, 9.238), (33215, 9.479), (66317, 9.912), (99532, 10.535), (265381, 11.06), (364913, 11.793), (1360120, 12.394)]
n += [dot('cx0', CX0, CY0, '4f#Para', color=GRY, s=6), dot('cx1', CX(7.5), CY0, '4f#Para', color=GRY, s=6), dot('cy1', CX0, CY(16), '4f#Para', color=GRY, s=6),
      T('cxl', CX(4.3), CY0 + 14, 'tamaño del denominador q  (escala logarítmica) →', '4f#Para', color=GRY, fs=12),
      T('cyl', CX0 + 8, CY(16) - 18, '↑ precisión de la aproximación', '4f#Para', color=GRY, fs=12)]
lk += [seg('cx0', 'cx1', '4f#Para', GRY), seg('cx0', 'cy1', '4f#Para', GRY)]
prv = None
for j, (q_, y_) in enumerate(CONV):
    nid = f'cp{j}'; t = f'4f#Siempre+{0.18 * j:.2f}'
    n.append(dot(nid, CX(math.log10(q_)), CY(y_), t, color=AMB, s=10))
n += [T('c227', CX(0.845) + 10, CY(2.898) - 6, '22/7', '4f#Siempre', color=VIO, fs=13), T('c355b', CX(2.053) + 10, CY(6.574) - 22, '355/113', '4f#Siempre+0.4', color=VIO, fs=13)]
def line(id_, mu, at, color, lab):
    xe = min(7.5, 16 / mu); nd_ = []
    for j in range(1, 33):
        u = j / 32; nd_.append(dot(f'{id_}{j}', CX(xe * u), CY(mu * xe * u), f'{at}+{0.02 * j:.2f}', color=color, s=4))
    nd_.append(N(id_ + 'c', 'chip', CX(xe) + 8, CY(mu * xe) - 14, 34, 26, f'{at}+0.7', color=color, label=lab, fs=14))
    return nd_, []
for id_, mu, at, color, lab in [('L2', 2, '4f#línea', TEAL, '2'), ('L3', 3, '4g#cubo', VIO, '3'), ('L4', 4, '4g#cuarta', RED, '4')]:
    a_, b_ = line(id_, mu, at, color, lab); n += a_; lk += b_
n += [N('ring', 'sandbox', CX(2.053) - 14, CY(6.574) - 14, 28, 28, '4g#sola', color=RED, open=True, label='', rx=14, until='4h#Para'),
      N('one', 'chip', CX(2.053) + 24, CY(6.574) + 18, 190, 26, '4g#sola', color=RED, label='una sola: no cuenta', fs=12, until='4h#Para')]
for j in range(8):
    xx = 2.4 + 0.33 * j
    n.append(dot(f'inf{j}', CX(xx), CY(3.1 * xx + 0.3), f'4g#tienen+{0.12 * j:.2f}', color=VIO, s=8))
n.append(T('infs', CX(4.95), CY(15.6) - 6, '∞', '4g#infinitas', color=VIO, fs=36))
n += [N('halo', 'sandbox', CX(4.4), CY(13.5), 330, 78, '4h#pegadas', color=AMB, open=True, label='', rx=40),
      N('qq', 'question', CX(1.2), CY(14), 36, 36, '4h#difícil', color=GRY), T('qql', CX(1.2) + 46, CY(14) + 8, '¿infinitas?', '4h#arriba', color=GRY, fs=16),
      N('nt', 'chip', CX(5.0), CY(5.5), 250, 28, '4i#trucos', color=TEAL, label='2 = sin trucos', fs=15)]
cues.append(K('4c', '4j', n, lk, fs=1.0))

# ================================================================== 4c-4e (meter returns)
n = []; lk = []
for v in range(2, 10):
    n.append(dot(f'k{v}', SX, Yv(v), f'4j#Para+{0.06 * (v - 2):.2f}', color=GRY, s=7))
    if v > 2: lk.append(seg(f'k{v - 1}', f'k{v}', f'4j#Para+{0.06 * (v - 2):.2f}', GRY))
    if v % 2 == 0: n.append(T(f'kt{v}', SX + 18, Yv(v) - 8, str(v), f'4j#Para+{0.06 * (v - 2):.2f}', color=GRY, fs=14))
n.append(T('ke', SX - 40, Yv(9) - 34, 'exponente', '4j#Para', color=GRY, fs=12))
n.append(T('pi', 225, 108, 'π', '4j#Para', color='#E7EBF1', fs=60, until='4k#Pero'))
# --- 4c: the minimum, 2: a cloud ("almost all") stays there, and sqrt(2) too
rs = [0.31, 0.77, 0.12, 0.58, 0.93, 0.44, 0.26, 0.69, 0.05, 0.84, 0.37, 0.62, 0.19, 0.51, 0.88, 0.03, 0.72, 0.46, 0.95, 0.24, 0.66, 0.15, 0.81, 0.40, 0.55, 0.09, 0.74, 0.33, 0.97, 0.60]
n.append(N('cl', 'sandbox', 110, 330, 250, 130, '4j#casi', color=TEAL, open=True, label='', until='4k#Pero'))
for i in range(30):
    n.append(dot(f'q{i}', 125 + rs[i] * 220, 345 + rs[(i * 7 + 3) % 30] * 100, f'4j#casi+{0.05 * i:.2f}', color='#7C97FF', s=7, until='4k#Pero'))
n += [N('ct', 'chip', 140, 468, 130, 26, '4j#casi', color=TEAL, label='casi todos', fs=12, until='4k#Pero'),
      N('cm', 'chip', 400, 330 + 52, 66, 26, '4j#algebraicos', color=VIO, label='√2', fs=14, until='4k#Pero'),
      N('c2m', 'chip', 520, 330 + 52, 38, 26, '4j#raíz', color=GRY, label='2', fs=14, until='4k#Pero'),
      N('mc', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4j#casi', color=TEAL, label='2', fs=14, until='4k#Pero')]
lk += [seg('cm', 'c2m', '4j#raíz+0.4', VIO, until='4k#Pero'), link('cl', 'mc', '4j#cualquier', color=TEAL, curve=.3, until='4k#Pero')]
n.append(N('mn', 'sandbox', SX - 13, Yv(2) - 13, 26, 26, '4j#mínimo', color=RED, label='', open=True, until='4k#Pero'))

# --- 4d: all that was known: the exponent of pi is at most ~7.1, so it could be anything between 2 and 7.1
n += [N('mp2', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4k#Pero', color=AMB, label='π', fs=14,
        move=[dict(at='4k#mayor', x=SX - 64, y=Yv(7.1) - 13, dur=1.2), dict(at='4k#cualquier', x=SX - 64, y=Yv(4.6) - 13, dur=1.4), dict(at='4l#exactamente', x=SX - 64, y=Yv(2) - 13, dur=0.5)]),
      N('qm', 'question', SX - 130, Yv(4.6) - 16, 32, 32, '4k#cualquier+1.0', color=GRY, until='4l#modelo'),
      N('bt', 'chip', 440, Yv(7.1) - 13, 238, 26, '4k#mayor', color=RED, label='se sabía: ≤ 7,1', fs=12, until='4l#modelo')]
# --- 4e: it drops to 2 and a green flag lights up next to pi
n += [N('fl', 'flFly', 640, Yv(2) - 55, 34, 46, '4l#exactamente+0.5', color=GRN), T('pm', 440, 330, 'π = 2', '4l#corriente', color=AMB, fs=40)]
cues.append(K('4j', '4m', n, lk, fs=1.0))

# ================================================================== 4f · Flint Hills: the formula is written, the partial sums creep up, jump at n=355, and settle (converge)
def PS(N_):
    return sum(1 / (i ** 3 * math.sin(i) ** 2) for i in range(1, N_ + 1))
PXo, PYo = 100, 470
def gx(n_): return PXo + math.log10(n_) * 170
def gy(S_): return PYo - S_ * 10
n = []; lk = []
n += [T('f1', 50, 40, 'Σ', '4m#Flint', color=AMB, fs=54), T('f2', 105, 52, '1 /', '4m#uno', color='#E7EBF1', fs=34),
      T('f3', 175, 52, 'n³', '4m#cubo', color='#E7EBF1', fs=34), T('f4', 235, 52, '· sin²(n)', '4m#seno', color='#E7EBF1', fs=34),
      T('f5', 520, 92, 'n = 1, 2, 3 …', '4m#igual', color=GRY, fs=20),
      N('fh', 'chip', 640, 40, 150, 26, '4m#Flint', color=AMB, label='Flint Hills', fs=13)]
# axes
n += [dot('ax0', PXo, PYo, '4m#igual', color=GRY, s=6), dot('ax1', PXo + 640, PYo, '4m#igual', color=GRY, s=6), dot('ay1', PXo, gy(33), '4m#igual', color=GRY, s=6),
      T('xl', PXo + 470, PYo + 14, 'n  (escala logarítmica)', '4m#igual', color=GRY, fs=12), T('yl', PXo + 8, gy(33) - 18, 'suma acumulada', '4m#igual', color=GRY, fs=12)]
lk += [seg('ax0', 'ax1', '4m#igual', GRY), seg('ax0', 'ay1', '4m#igual', GRY)]
NS1 = [1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 200, 300, 354]
NS2 = [355, 400, 500, 700, 1000, 1500, 2000, 3000]
prev = None
for i, k_ in enumerate(NS1):
    t = f'4m#igual+{0.3 + 0.28 * i:.2f}'
    n.append(dot(f'pp{k_}', gx(k_), gy(PS(k_)), t, color=AMB, s=8))
    if prev: lk.append(seg(prev, f'pp{k_}', t, AMB))
    prev = f'pp{k_}'
n.append(T('v1', gx(354) - 10, gy(PS(354)) - 30, '4,8', '4m#igual+4.0', color=AMB, fs=18, until='4m#parar+0.6'))
tj = '4m#parar+0.6'
for j, k_ in enumerate(NS2):
    t = tj if j == 0 else f'4m#converja+{0.5 * (j - 1):.2f}'
    n.append(dot(f'pp{k_}', gx(k_), gy(PS(k_)), t, color=AMB if j else RED, s=8 if j else 12))
    lk.append(seg(prev, f'pp{k_}', t, AMB if j else RED)); prev = f'pp{k_}'
n += [N('j1', 'chip', gx(355) - 190, gy(18) - 13, 120, 26, tj, color=RED, label='n = 355', fs=13), T('j2', gx(355) - 190, gy(18) + 18, 'sin(355) ≈ 0 → término enorme', '4m#parar+0.9', color=GRY, fs=12),
      T('v2', gx(355) + 12, gy(PS(355)) - 30, '29,4', tj, color=AMB, fs=18, until='4m#converja'),
      dot('lm0', PXo, gy(30.31), '4m#fijo', color=TEAL, s=5), dot('lm1', PXo + 640, gy(30.31), '4m#fijo', color=TEAL, s=5),
      T('v3', PXo + 560, gy(30.31) - 30, '≈ 30,3', '4m#fijo', color=TEAL, fs=22)]
lk.append(seg('lm0', 'lm1', '4m#fijo', TEAL))
cues.append(K('4m', '4n', n, lk, fs=1.0))

# ================================================================== 4g · a long search: attempts crossed out, the way through the maze
CODE4 = """$ prove pi_exponent
try: lemma_a ... dead end
try: bound_7 ... gap too large
try: sieve_3 ... fails
try: fraction_chain ... loops
try: new_estimate ... dead end
try: alt_route ... fails
try: lemma_b ... partial
try: combine(a, b) ... fails
try: refine(bound) ... dead end
try: shrink(7 -> 2) ... ok
""" * 3
EXx, EXy, CELL, COLS, ROWS = 590, 90, 24, 9, 12
EXw, EXh = COLS * CELL + 80, ROWS * CELL + 76
fx = EXx + (EXw - COLS * CELL) / 2 + (COLS - 1) * CELL + CELL / 2; fy = EXy + (EXh - ROWS * CELL) / 2 + (ROWS - 1) * CELL + CELL / 2
n = [W.console('co', 60, 110, w=310, h=300, at='4n#resumen', code=CODE4, k=3, a=2.2, cols=34),
     N('ex', 'exam', EXx, EXy, EXw, EXh, '4n#probando', color='blue',
       maze=dict(cell=CELL, cols=COLS, rows=ROWS, entry=3, seed=17, end=[fx, fy]), solve=dict(at='4n#descartándolas', dur=5.5)),
     N('fg', 'flFly', fx - 10, fy - 26, 28, 38, '4n#probando', color=AMB, blink=.6, bf=8, bat='4n#descartándolas+5.0')]
for j in range(6):
    t = f'4n#probando+{1.0 * j:.2f}'
    n.append(ic(f'x{j}', 'cross', 440, 130 + j * 48, 30, t, color='red'))
n.append(ic('xo', 'check', 440, 130 + 6 * 48, 34, '4n#callejones', color='teal'))
lk = []
cues.append(K('4n', 'E4', n, lk, fs=1.0))
