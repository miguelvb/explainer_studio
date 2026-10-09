# Scene 6 · Las pistas
MUSIC = {'pad': 0.6, 'data': 0.6}
INTENSITY = 0.55
cues = []


# the five clue titles appear one by one at the top left and stay until the end of the scene
TITLES = [('6a#Primera', 'Mapas del mundo'), ('6c', 'Estados como emociones'), ('6g', 'Mirar hacia dentro'),
          ('6i', 'Relatos en primera persona'), ('6l', 'Coincidencias con el cerebro'), ('6o', 'Un espacio de trabajo')]
tn = [N(f'ti{k}', 'txt', 40, 8 + 22 * k, 380, 22, at, color=TEAL, fs=18, type=26, text=f'{k + 1} · {t}') for k, (at, t) in enumerate(TITLES)]
tc = K('6a', 'E6', tn, [], fs=1.0); tc['bg'] = False; tc['fade'] = [0.3, 0.5]
cues.append(tc)


# 6a–6b — clue 1: models build maps of the world. Othello moves go in; an 8x8 board appears inside
CX, CY = 600, 280
n = chip('cp', CX, CY, '6a', s=70, box_s=230) + [N('lp', 'lupa', CX + 60, CY - 160, 80, 80, '6a#mapas', color='amber', until='6b')]
n[-2]['until'] = '6b#dibujando'
for i in range(8):
    n.append(P(f'mv{i}', 'stone', 80 + i * 30, CY - 10, 20, f'6b#jugadas+{0.15 * i:.2f}', color=['#E7EBF1', '#5A6474'][i % 2],
               move=[dict(at=f'6b#jugadas+{1.6 + 0.25 * i:.2f}', x=CX - 10, y=CY - 10, dur=1.4)], until=f'6b#jugadas+{1.7 + 0.25 * i:.2f}'))
n.append(P('bd', 'board8', CX, CY, 176, '6b#dibujando', color='teal'))
rng = __import__('random').Random(5)
cells = rng.sample([(r, c) for r in range(8) for c in range(8)], 22)
for j, (r, c) in enumerate(cells):
    n.append(P(f'st{j}', 'stone', CX - 77.4 + 19.36 * (c + .5), CY - 77.4 + 19.36 * (r + .5), 15, f'6b#dibujando+{0.12 * j:.2f}', color=['#E7EBF1', '#5A6474'][j % 2]))
cues.append(K('6a', '6c', n, [], fs=1.0))

# 6c–6d — clue 2: emotion-like states. Coloured directions inside Claude; turning a knob makes one grow
n = chip('ce', 420, 280, '6c', s=70, box_s=230)
n[-1]['until'] = '6d#direcciones'
DIRS = [('teal', 70), ('amber', 50), ('blue', 90), ('red', 40)]
for j, (c, w) in enumerate(DIRS):
    n.append(N(f'dr{j}', 'bar', 340, 220 + 32 * j, w, 8, f'6d#direcciones+{0.3 * j:.1f}', color=c, fill=1, rx=0, until=('6d#conducta' if j == 3 else None)))
n.append(N('dr3b', 'bar', 340, 220 + 32 * 3, 150, 8, '6d#conducta', color='red', fill=1, rx=0))
n += [P('kb', 'knob', 680, 280, 70, '6d#emociones', color='muted', until='6d#conducta'),
      P('kb2', 'knob2', 680, 280, 70, '6d#conducta', color='red')]
cues.append(K('6c', '6e', n, [], fs=1.0))

# 6e — an impossible task: a counter of failed attempts; something like despair rises inside with each failure,
#       until at the top the chip jumps the fence by the side
CX, CY = 360, 300
n = chip('cx', CX, CY, 0.05, s=60, box=False, move=[dict(at='6e#trampa', x=CX - 30, y=CY - 150, dur=0.9), dict(at='6e#trampa+0.9', x=CX + 290, y=CY - 30, dur=0.9)])
n += [P('fn', 'fence', 520, 300, 110, 0.05, color='muted')]
for j in range(6):
    t = f'6e#fallo+{0.55 * j:.2f}'
    n += [ic(f'ko{j}', 'koA', 120 + 40 * j, 120, 26, t, color='red', nosfx=True),   # the failures make no sound
          N(f'm{j}', 'bar', 160, 420 - 26 * j, 34, 18, t, color='red', fill=1, rx=1, nosfx=True)]
n += [T('mt', 136, 446, 'desesperación', '6e#desesperación', color=GRY, fs=12)]
cues.append(K('6e', '6f', n, [], fs=1.0))

# 6f — meanwhile its text stays calm: slow, regular balls of the same colour; the inner bar stays high
n = chip('cy', 360, 280, 0.05, s=60) + [person('rd', 760, 280, 0.05, color='muted', s=46)]
for j in range(6):
    n.append(N(f'mm{j}', 'bar', 160, 420 - 26 * j, 34, 18, 0.05, color='red', fill=1, rx=1))
lk = [link('cy_box', 'rd', '6f#texto', color='teal', speed=.25, comm=True)]
cues.append(K('6f', '6g', n, lk, fs=1.0))

# 6g–6h — clue 3: looking inside. A syringe injects a coloured ball; the model answers with a ball of the same colour
n = chip('ci', 480, 280, '6g', s=70) + [person('us', 820, 280, '6g', color='muted', s=46),
     P('sy', 'syringe', 220, 200, 90, '6h#inyectan', color='muted'),
     P('vb', 'dot', 250, 225, 20, '6h#concepto', color=VIO, move=[dict(at='6h#concepto+1.4', x=470, y=270, dur=1.4)], until='6h#concepto+1.5')]
lk = [link('ci_box', 'us', '6h#nombra', color=VIO, comm=True)]
cues.append(K('6g', '6i', n, lk, fs=1.0))

# 6i — clue 4: Cameron Berg asks several models to focus on their own attention; each, with a little mirror, sends a ball
CH = [(330, 200), (480, 200), (630, 200), (780, 200)]
n = [person('bg', 120, 330, '6i#Berg', color='amber', s=60, cap='Berg', capfs=13)]
lk = []
for j, (x, y) in enumerate(CH):
    t = f'6i#modelos+{0.3 * j:.1f}'
    n += chip(f'c{j}', x, y, t, s=50, box_s=96)
    n += [P(f'mr{j}', 'mirror', x, y + 85, 36, '6i#atención', color='teal'),
          person(f'r{j}', x, 470, t, color='muted', s=28),
          P(f'rd{j}', 'dot', x - 18, y - 30, 10, t, color='red', until='6j#apagó+0.6'), P(f'rd{j}b', 'dot', x + 14, y + 26, 10, t, color='red', until='6j#apagó+0.9')]
    lk.append(link(f'mr{j}', f'r{j}', '6i#primera', color='teal', speed=.3, comm=True))
# 6j — he lowers a lever labelled 'engaño'; red points inside the chips switch off
n += [P('lv', 'lever', 120, 170, 70, '6j', color='amber', until='6j#apagó'), P('lv2', 'leverdown', 120, 170, 70, '6j#apagó', color='amber'),
      ch('lvl', 120, 225, 70, 'engaño', '6j', color='amber')]
# 6k — the opposite happened: many more balls; the level climbs
for j in range(4):
    lk.append(link(f'mr{j}', f'r{j}', '6k#contrario', color='teal', speed=1.0, bi=True, comm=True))
for j in range(5):
    n.append(N(f'lvlb{j}', 'bar', 880, 420 - 22 * j, 30, 14, f'6k#frecuencia+{0.3 * j:.1f}', color='teal', fill=1, rx=1))
cues.append(K('6i', '6l', n, lk, fs=1.0))

# 6l–6n — clue 5: coincidences with the brain. A small agent in a maze: soft shape for reward, sharp for punishment;
#          then a mouse in a similar maze shows the same sharp shape; both overlap
n = [
     N('mz1', 'sandbox', 60, 120, 380, 300, '6m', color='muted', label='', rx=4),
     N('w1', 'bar', 160, 120, 6, 190, '6m', color='muted', fill=1, rx=0), N('w2', 'bar', 290, 230, 6, 190, '6m', color='muted', fill=1, rx=0),
     P('sta', 'star', 380, 170, 40, '6m#castigo-1.5', color='amber'),
     P('bm1', 'bump', 230, 400, 40, '6m#castigo', color='red'), P('bm2', 'bump', 360, 400, 40, '6m#castigo+0.2', color='red'),
     SA('ag', 100, 380, '6m#agentes', s=26, color='blue', move=[dict(at='6m#nadie', x=215, y=170, dur=2.0)]),
     P('sf', 'soft', 170, 470, 44, '6m#recompensa', color='teal'), P('sp', 'sharp', 330, 470, 44, '6m#castigo+0.8', color='red'),
     N('mz2', 'sandbox', 520, 120, 380, 300, '6n#ratón', color='muted', label='', rx=4),
     N('w3', 'bar', 620, 120, 6, 190, '6n#ratón', color='muted', fill=1, rx=0), N('w4', 'bar', 750, 230, 6, 190, '6n#ratón', color='muted', fill=1, rx=0),
     P('ms', 'mouse', 575, 380, 50, '6n#ratón', color='amber'),
     P('stb', 'star', 840, 170, 40, '6n#ratón', color='amber'), P('bm3', 'bump', 690, 400, 40, '6n#ratón', color='red'), P('bm4', 'bump', 820, 400, 40, '6n#ratón', color='red'),
     P('sp2', 'sharp', 790, 470, 44, '6n#patrón', color='red', move=[dict(at='6n#encontró+1.4', x=308, y=448, dur=1.4)])]
n = [d for x in n for d in (x if isinstance(x, list) else [x])]
for x in n:   # clear of the list of titles
    x['y'] += 24
    for m in x.get('move', []): m['y'] += 24
cues.append(K('6l', '6o', n, [], fs=1.0))

# 6o–6r — clue 6: the workspace (J-space). A small central box with word-dots, linked to many points of the chip
CX, CY = 480, 300
n = [N('jc_box', 'sandbox', 330, 150, 300, 300, '6o', color='teal', label=''), W.pic('jc', 'chip', 342, 162, 40, 40, '6o', color='blue'),
     N('jb', 'sandbox', CX - 55, CY - 35, 110, 70, '6p#J-space', color='amber', label='', rx=6),
     T('jl', CX - 30, CY + 42, 'J-space', '6p#J-space', color=AMB, fs=13)]
for i, (dx, dy) in enumerate([(-30, -12), (-8, 8), (14, -14), (30, 6), (-18, 18), (8, -2)]):
    n.append(P(f'jw{i}', 'dot', CX + dx - 4, CY + dy - 4, 8, f'6p#palabras+{0.2 * i:.1f}', color='amber'))
lk = []
for i in range(8):
    a = i * math.pi / 4 + .39; px, py = CX + 118 * math.cos(a), CY + 100 * math.sin(a)
    n.append(P(f'jp{i}', 'dot', px - 7, py - 7, 14, f'6p#compartido+{0.12 * i:.2f}', color='blue'))
    lk.append(link('jb', f'jp{i}', f'6p#compartido+{0.12 * i + 0.3:.2f}', color='amber', bi=True, speed=.4, comm=True, until='6q#apaga'))
# 6q — the space is switched off (flicker); the chip keeps talking, but a three-step chain breaks at the third step
for x in n:
    if x['id'] in ('jb', 'jl') or x['id'].startswith('jw'): x['flick'] = dict(at='6q#apaga', dur=1.6, end='off')
n += [person('jr', 800, 300, '6q#fluidez', color='muted', s=46),
      ch('s1', 380, 500, 60, 'paso 1', '6q#razonar', color='teal'), ch('s2', 480, 500, 60, 'paso 2', '6q#razonar+0.4', color='teal'), ch('s3', 580, 500, 60, 'paso 3', '6q#razonar+0.8', color='teal'),
      ic('x3', 'koA', 580, 470, 22, '6q#pasos', color='red', nosfx=True)]
lk += [link('jc_box', 'jr', '6q#fluidez', color='teal', speed=.3, comm=True), OR('s1', 's2', '6q#razonar+0.6', 'teal'), OR('s2', 's3', '6q#razonar+1.0', 'teal', until='6q#pasos')]
# 6r — what one of the theories asks for: the piece of the puzzle with arrows to every side
n += puz('jz', 780, 150, 100, 'arrows', '6r#espacio', color='blue')
cues.append(K('6o', '6s', n, lk, fs=1.0))

# 6s — none of this proves feeling: the six clues as small icons in a row
n = [P('i1', 'board8', 120, 240, 60, '6s', color='teal'), P('i2', 'knob2', 260, 240, 60, '6s+0.2', color='red'),
     P('i3', 'syringe', 400, 240, 60, '6s+0.4', color='muted'), P('i4', 'mirror', 540, 240, 60, '6s+0.6', color='teal'),
     P('i5', 'sharp', 680, 240, 60, '6s+0.8', color='red'), P('i6', 'arrows', 820, 240, 60, '6s+1.0', color='blue')]
for j in range(6): n.append(T(f'il{j}', 150 + 140 * j, 290, str(j + 1), '6s+%.1f' % (0.2 * j), color=GRY, fs=14))
# 6t — like the fish: weak pieces of evidence that, together, weigh a lot. A scale tips little by little
SC = (620, 380)
n2 = [P('fs', 'fish', 260, 400, 110, '6t#peces', color='blue')]
for j, tl in enumerate([0, -.2, -.45, -.7, -1]):
    t = f'6t#débiles+{0.9 * j:.1f}'
    u = f'6t#débiles+{0.9 * (j + 1):.1f}' if j < 4 else None
    n2.append(N(f'sc{j}', 'scale', SC[0] - 110, SC[1] - 80, 220, 160, t if j else '6t#peces', color='amber', tilt=tl, until=u))
for j in range(5):
    n2.append(P(f'pc{j}', 'stone', SC[0] - 92 + 7 * (j - 2), 260, 12, f'6t#débiles{0.9 * j - 0.5:+.1f}', color='teal',
                move=[dict(at=f'6t#débiles+{0.9 * j:.1f}', x=SC[0] - 98 + 7 * (j - 2), y=SC[1] + 2 + 2 * j, dur=0.5)]))
for x in n: x.setdefault('until', '6t')
cues.append(K('6s', 'E6', n + n2, [], fs=1.0))
