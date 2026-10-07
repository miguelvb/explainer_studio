# Scene 5 · Lean
MUSIC = {'data': 0.7, 'pad': 0.7}
INTENSITY = 0.45
cues = []

def dot(id, x, y, at, color=BLU, s=9, **k):
    return N(id, 'sandbox', x - s / 2, y - s / 2, s, s, at, color=color, label='', **k)

def seg(a, b, at, color=BLU, **k):
    return link(a, b, at, color=color, rel=True, **k)

# ------------------------------------------------------------------ 5a · Lean and the verifier agent holding a flag
n = [AN('ver', 150, 170, 'VERIFICADOR', at=0.4, color=TEAL, lc=TEAL, blink=.2, bf=4),
     N('vf', 'flFly', 320, 190, 40, 56, '5a#palabra', color=GRN),
     N('ln', 'server', 540, 225, 170, 66, '5a#aceptarse', color=VIO, label='Lean', sub='', big=True, blink=.1, bf=4)]
lk = [link('ver', 'ln', '5a#Por+0.3', color=TEAL, curve=.3, bi=True)]
cues.append(K('S5', '5b', n, lk, fs=1.0))

# ------------------------------------------------------------------ 5b · a console writes the proof, a ribbon of steps gets ticked, "compila"
LEAN = """theorem pi_exponent :
  irrationalityExponent pi = 2 := by
  intro n hn
  have h1 := approx_bound n
  have h2 := denom_estimate h1
  apply lemma_gap h2
  rw [mul_comm, add_assoc]
  exact tight_bound hn
  simp at *
  linarith
done
""" * 3
n = [W.console('co', 50, 70, w=400, h=250, at='5b#programación', code=LEAN, k=4, a=2.5, cols=40, color=VIO)]
lk = []
XS = [110 + 90 * i for i in range(8)]
for i, x in enumerate(XS):
    t = f'5b#comprueba+{0.55 * i:.2f}'
    n.append(N(f'st{i}', 'sandbox', x - 22, 400 - 22, 44, 44, f'5b#estricto+{0.2 * i:.2f}', color=GRY, label=''))
    n.append(ic(f'ok{i}', 'check', x, 400, 28, t, color='teal'))
    if i: lk.append(seg(f'st{i - 1}', f'st{i}', f'5b#estricto+{0.2 * i:.2f}', GRY))
n += [ic('cp', 'okB', 840, 400, 64, '5b#compila', color='teal'), T('ct', 800, 442, 'compila', '5b#compila', color=TEAL, fs=18)]
lk.append(seg('st7', 'cp', '5b#compila', TEAL))
cues.append(K('5b', '5c', n, lk, fs=1.0))

# ------------------------------------------------------------------ 5c · many proofs through one small kernel, out with a green seal
n = [N('nu', 'server', 410, 232, 140, 76, '5c#núcleo', color=VIO, label='núcleo', sub='', blink=.12, bf=4)]
lk = []
COL = [TEAL, BLU, AMB, CORAL, GRN]
for j in range(5):
    y = 90 + j * 90
    t = f'5c#confianza+{0.45 * j:.2f}'
    n.append(N(f'dc{j}', 'doc', 120, y, 44, 56, t, color=COL[j]))
    lk.append(link(f'dc{j}', 'nu', f'5c#núcleo+{0.3 * j:.2f}', color=COL[j], curve=.3))
    n.append(ic(f'sl{j}', 'okB', 800, y + 28, 44, f'5c#revisa+{0.45 * j:.2f}', color='teal'))
    lk.append(link('nu', f'sl{j}', f'5c#revisa+{0.45 * j:.2f}', color='teal', curve=.3))
cues.append(K('5c', '5d', n, lk, fs=1.0))

# ------------------------------------------------------------------ 5d · 235 / 372 and a bar with two thirds in green
BX, BY, BW = 220, 330, 520; W1 = round(BW * 235 / 372); W2 = BW - W1
n = [W.counter('c1', 230, 140, 235, at='5d#doscientas', cap='con Lean', w=200, h=70, fs=64, dur=3.5),
     T('sl', 440, 160, '/', '5d#trescientas', color=GRY, fs=60),
     W.counter('c2', 500, 140, 372, at='5d#trescientas', cap='familias', w=200, h=70, fs=64, dur=3.0),
     N('b1', 'bar', BX, BY, W1, 24, '5d#casi', color=GRN, fill=1), N('b2', 'bar', BX + W1, BY, W2, 24, '5d#casi+0.8', color=GRY, fill=1),
     T('tl', BX + W1 / 2 - 40, BY + 36, 'comprobadas', '5d#casi+1.2', color=GRN, fs=13), T('tg', BX + W1 + W2 / 2 - 40, BY + 36, 'sin Lean', '5d#casi+1.6', color=GRY, fs=13)]
cues.append(K('5d', '5e', n, [], fs=1.0))

# ------------------------------------------------------------------ 5e · same statement? words sheet vs Lean sheet, a magnifier compares them
n = [W.sheet('sl', 600, 150, 270, 140, ['exp(π)', '= 2', ''], at='5e#garantiza', fs=22, color='teal', mono=True),
     ic('ok', 'check', 835, 170, 30, '5e#correcta', color='teal'),
     T('ll', 640, 308, 'enunciado en Lean', '5e#garantiza', color=TEAL, fs=14),
     W.sheet('sw', 90, 150, 270, 140, ['el exponente de π', 'vale dos'], at='5e#problema', fs=19, color='amber'),
     T('lw', 120, 308, 'enunciado en palabras', '5e#problema', color=AMB, fs=14),
     N('lp', 'lupa', 440, 90, 64, 64, '5e#humanos', color='#E7EBF1', move=[dict(at='5e#leer', x=440, y=90, dur=.1), dict(at='5e#comprobar', x=400, y=110, dur=1.0)]),
     N('qq', 'question', 464, 340, 44, 44, '5e#querías', color=AMB)]
lk = [link('sw', 'sl', '5e#querías+0.4', color=AMB, curve=.3, bi=True)]
cues.append(K('5e', '5f', n, lk, fs=1.0))

# ------------------------------------------------------------------ 5f · the pi sheet: exponent inside the green frame, Flint Hills outside (grey)
n = [N('pg', 'sheet', 250, 60, 460, 250, '5f#formalización', color='muted', lines=[], fs=18),
     N('gf', 'sandbox', 290, 90, 380, 70, '5f#exponente', color=GRN, label=''),
     N('e1', 'chip', 330, 112, 220, 26, '5f#exponente', color=GRN, label='exponente de π = 2', fs=14),
     ic('e2', 'check', 620, 125, 34, '5f#exponente+0.6', color='teal'),
     N('f1', 'chip', 330, 220, 140, 26, '5f#consecuencia', color=GRY, label='Flint Hills', fs=14, dashed=True),
     N('f2', 'koA', 500, 217, 32, 32, '5f#Flint', color='red')]
for j in range(4):
    t = f'5f#Cada+{0.35 * j:.2f}'
    x = 160 + j * 200
    n.append(N(f'd{j}', 'doc', x, 370, 58, 74, t, color=[TEAL, BLU, AMB, CORAL][j]))
    n.append(N(f'g{j}', 'sandbox', x - 8, 370 + 4, 74, 26 + (j % 3) * 14, f'5f#Cada+{0.35 * j + .2:.2f}', color=GRN, label='', open=True))
n.append(N('lp2', 'lupa', 120, 400, 52, 52, '5f#mirar', color='#E7EBF1', move=[dict(at='5f#mirar+0.4', x=300, y=410, dur=1.0), dict(at='5f#documento', x=500, y=410, dur=1.0), dict(at='5f#uno', x=700, y=410, dur=1.0)]))
cues.append(K('5f', 'E5', n, [], fs=1.0))
