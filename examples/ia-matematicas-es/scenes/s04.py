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

# ================================================================== 4a-4f (one persistent diagram)
n = []; lk = []
# --- 4a: a circle (made of points) with its diameter, the symbol pi, and the number line with two fractions
for i in range(36):
    a = i / 36 * 2 * math.pi
    n.append(dot(f'cc{i}', 130 + 52 * math.cos(a), 135 + 52 * math.sin(a), f'4a#número+{0.04 * i:.2f}', color=TEAL, s=7, until='4b#La'))
n += [dot('d1', 78, 135, '4a#número+1.0', color=TEAL, s=7, until='4b#La'), dot('d2', 182, 135, '4a#número+1.0', color=TEAL, s=7, until='4b#La'),
      T('pi', 225, 108, 'π', '4a#pi', color='#E7EBF1', fs=60, until='4c#Para')]
lk.append(seg('d1', 'd2', '4a#número+1.2', TEAL, until='4b#La'))
n += [dot('n0', 80, LY, '4a#irracional', color=GRY, s=6, until='4c#Para'), dot('n1', 640, LY, '4a#irracional', color=GRY, s=6, until='4c#Para')]
lk.append(seg('n0', 'n1', '4a#irracional', GRY, until='4c#Para'))
n += [dot('np', PX, LY, '4a#irracional+0.4', color=AMB, s=13, until='4c#Para'), T('pl', PX - 6, LY + 14, 'π', '4a#irracional+0.4', color=AMB, fs=18, until='4c#Para'),
      dot('f1', PX + 15, LY, '4a#veintidós', color=VIO, s=8, until='4c#Para'), dot('f2', PX + 140, LY, '4a#trescientos', color=TEAL, s=8, until='4c#Para'),
      N('c2', 'chip', PX + 15 - 36, 176, 72, 26, '4a#veintidós', color=TEAL, label='355/113', fs=12, until='4c#Para'),
      N('c1', 'chip', PX + 140 - 30, 196, 60, 26, '4a#trescientos', color=VIO, label='22/7', fs=12, until='4c#Para')]
# NB: 355/113 is the very close one (15 px from pi), 22/7 the farther one (140 px)
lk += [seg('c2', 'f1', '4a#trescientos+0.3', TEAL, until='4c#Para'), seg('c1', 'f2', '4a#veintidós+0.3', VIO, until='4c#Para')]

# --- 4b: bands narrowing around pi while fractions with bigger denominators are tried; the exponent meter wobbles
BW = [(300, '4b#aproximaciones'), (170, '4b#aproximaciones+1.0'), (90, '4b#aproximaciones+2.0'), (44, '4b#aproximaciones+3.0')]
for j, (w, t) in enumerate(BW):
    tu = BW[j + 1][1] if j + 1 < len(BW) else '4c#Para'
    n.append(N(f'bd{j}', 'sandbox', PX - w / 2, LY - 36 - j * 0, w, 72, t, color=AMB, open=True, label='', until=tu))
# the meter (axis made of ticks) appears with the word "exponente"
for v in range(2, 10):
    n.append(dot(f'k{v}', SX, Yv(v), f'4b#exponente+{0.08 * (v - 2):.2f}', color=GRY, s=7))
    if v > 2: lk.append(seg(f'k{v - 1}', f'k{v}', f'4b#exponente+{0.08 * (v - 2):.2f}', GRY))
    if v % 2 == 0: n.append(T(f'kt{v}', SX + 18, Yv(v) - 8, str(v), f'4b#exponente+{0.08 * (v - 2):.2f}', color=GRY, fs=14))
n.append(T('ke', SX - 40, Yv(9) - 34, 'exponente', '4b#exponente', color=GRY, fs=12))
mv = [dict(at='4b#exponente+1.2', x=SX - 64, y=Yv(5) - 13, dur=1.0), dict(at='4b#Cuanto', x=SX - 64, y=Yv(3.2) - 13, dur=1.0),
      dict(at='4b#Cuanto+1.6', x=SX - 64, y=Yv(6.5) - 13, dur=1.2), dict(at='4b#fracciones', x=SX - 64, y=Yv(4) - 13, dur=1.0)]
n.append(N('mp1', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4b#exponente+0.8', color=AMB, label='π', fs=14, move=mv, until='4c#Para'))

# --- 4c: the minimum, 2: a cloud ("almost all") stays there, and sqrt(2) too
rs = [0.31, 0.77, 0.12, 0.58, 0.93, 0.44, 0.26, 0.69, 0.05, 0.84, 0.37, 0.62, 0.19, 0.51, 0.88, 0.03, 0.72, 0.46, 0.95, 0.24, 0.66, 0.15, 0.81, 0.40, 0.55, 0.09, 0.74, 0.33, 0.97, 0.60]
n.append(N('cl', 'sandbox', 110, 330, 250, 130, '4c#casi', color=TEAL, open=True, label='', until='4d#Pero'))
for i in range(30):
    n.append(dot(f'q{i}', 125 + rs[i] * 220, 345 + rs[(i * 7 + 3) % 30] * 100, f'4c#casi+{0.05 * i:.2f}', color='#7C97FF', s=7, until='4d#Pero'))
n += [N('ct', 'chip', 140, 468, 130, 26, '4c#casi', color=TEAL, label='casi todos', fs=12, until='4d#Pero'),
      N('cm', 'chip', 400, 330 + 52, 66, 26, '4c#algebraicos', color=VIO, label='√2', fs=14, until='4d#Pero'),
      N('c2m', 'chip', 520, 330 + 52, 38, 26, '4c#raíz', color=GRY, label='2', fs=14, until='4d#Pero'),
      N('mc', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4c#casi', color=TEAL, label='2', fs=14, until='4d#Pero')]
lk += [seg('cm', 'c2m', '4c#raíz+0.4', VIO, until='4d#Pero'), link('cl', 'mc', '4c#cualquier', color=TEAL, curve=.3, until='4d#Pero')]
n.append(N('mn', 'sandbox', SX - 13, Yv(2) - 13, 26, 26, '4c#mínimo', color=RED, label='', open=True, until='4d#Pero'))

# --- 4d: pi's exponent climbs above 7 and stays an open question
n += [N('mp2', 'chip', SX - 64, Yv(2) - 13, 44, 26, '4d#Pero', color=AMB, label='π', fs=14,
        move=[dict(at='4d#nadie', x=SX - 64, y=Yv(7.6) - 13, dur=1.6), dict(at='4e#exactamente', x=SX - 64, y=Yv(2) - 13, dur=0.5)]),
      N('qm', 'question', SX - 130, Yv(7.6) - 16, 32, 32, '4d#nadie+1.6', color=GRY, until='4e#modelo'),
      N('bt', 'chip', 470, Yv(7.0) - 13, 208, 26, '4d#cota', color=RED, label='mejor cota conocida > 7', fs=12, until='4e#modelo')]
# --- 4e: it drops to 2 and a green flag lights up next to pi
n += [N('fl', 'flFly', 640, Yv(2) - 55, 34, 46, '4e#exactamente+0.5', color=GRN), T('pm', 440, 330, 'π = 2', '4e#corriente', color=AMB, fs=40)]
cues.append(K('S4', '4f', n, lk, fs=1.0))

# ================================================================== 4f · Flint Hills: terms are added, the counter settles
def term(i): return 1 / (i ** 3 * math.sin(i) ** 2)
n = []; lk = []
BASE, X0, DX, NT = 400, 100, 17, 40
n += [dot('bs0', X0 - 10, BASE, '4f#suma', color=GRY, s=6), dot('bs1', X0 + NT * DX, BASE, '4f#suma', color=GRY, s=6)]
lk.append(seg('bs0', 'bs1', '4f#suma', GRY))
for i in range(1, NT + 1):
    h = max(6, min(210, term(i) * 130))
    n.append(N(f'tm{i}', 'sandbox', X0 + (i - 1) * DX, BASE - h, 11, h, f'4f#suma+{0.14 * i:.2f}', color=AMB if i % 2 else VIO, label='', fill=1))
n += [N('fh', 'txt', 100, 78, 360, 30, '4f#Flint', color=AMB, fs=26, text='Flint Hills', type=12),
      W.counter('sm', 640, 110, 30, at='4f#suma', cap='suma', w=200, h=60, fs=60, dur=6.5)]
cues.append(K('4f', '4g', n, lk, fs=1.0))

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
n = [W.console('co', 60, 110, w=310, h=300, at='4g#resumen', code=CODE4, k=3, a=2.2, cols=34),
     N('ex', 'exam', EXx, EXy, EXw, EXh, '4g#probando', color='blue',
       maze=dict(cell=CELL, cols=COLS, rows=ROWS, entry=3, seed=17, end=[fx, fy]), solve=dict(at='4g#descartándolas', dur=5.5)),
     N('fg', 'flFly', fx - 10, fy - 26, 28, 38, '4g#probando', color=AMB, blink=.6, bf=8, bat='4g#descartándolas+5.0')]
for j in range(6):
    t = f'4g#probando+{1.0 * j:.2f}'
    n.append(ic(f'x{j}', 'cross', 440, 130 + j * 48, 30, t, color='red'))
n.append(ic('xo', 'check', 440, 130 + 6 * 48, 34, '4g#callejones', color='teal'))
lk = []
cues.append(K('4g', 'E4', n, lk, fs=1.0))
