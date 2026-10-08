# Scene 6 · Las pistas
MUSIC = {'pad': 0.6, 'data': 0.6}
INTENSITY = 0.55
cues = []


def clue(id, k, at):
    return T(id, 40, 36, str(k), at, color=TEAL, fs=26)


# 6a–6b — clue 1: models build maps of the world. Othello moves go in; an 8x8 board appears inside
CX, CY = 600, 280
n = [clue('n1', 1, '6a#Primera')] + chip('cp', CX, CY, '6a', s=70, box_s=230) + [N('lp', 'lupa', CX + 60, CY - 160, 80, 80, '6a#mapas', color='amber', until='6b')]
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
n = [clue('n2', 2, '6c')] + chip('ce', 420, 280, '6c', s=70, box_s=230)
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
    n += [ic(f'ko{j}', 'koA', 120 + 40 * j, 120, 26, t, color='red'),
          N(f'm{j}', 'bar', 160, 420 - 26 * j, 34, 18, t, color='red', fill=1, rx=1)]
n += [T('mt', 136, 446, 'desesperación', '6e#desesperación', color=GRY, fs=12)]
cues.append(K('6e', '6f', n, [], fs=1.0))

# 6f — meanwhile its text stays calm: slow, regular balls of the same colour; the inner bar stays high
n = chip('cy', 360, 280, 0.05, s=60) + [person('rd', 760, 280, 0.05, color='muted', s=46)]
for j in range(6):
    n.append(N(f'mm{j}', 'bar', 160, 420 - 26 * j, 34, 18, 0.05, color='red', fill=1, rx=1))
lk = [link('cy_box', 'rd', '6f#texto', color='teal', speed=.25, comm=True)]
cues.append(K('6f', '6g', n, lk, fs=1.0))

# 6g–6h — clue 3: looking inside. A syringe injects a coloured ball; the model answers with a ball of the same colour
n = [clue('n3', 3, '6g')] + chip('ci', 480, 280, '6g', s=70) + [person('us', 820, 280, '6g', color='muted', s=46),
     P('sy', 'syringe', 220, 200, 90, '6h#inyectan', color='muted'),
     P('vb', 'dot', 250, 225, 20, '6h#concepto', color=VIO, move=[dict(at='6h#concepto+1.4', x=470, y=270, dur=1.4)], until='6h#concepto+1.5')]
lk = [link('ci_box', 'us', '6h#nombra', color=VIO, comm=True)]
cues.append(K('6g', '6i', n, lk, fs=1.0))

# 6i — clue 4: Cameron Berg asks several models to focus on their own attention; each, with a little mirror, sends a ball
CH = [(330, 200), (480, 200), (630, 200), (780, 200)]
n = [clue('n4', 4, '6i'), person('bg', 120, 330, '6i#Berg', color='amber', s=60, cap='Berg', capfs=13)]
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
n = [clue('n5', 5, '6l'),
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
cues.append(K('6l', '6o', n, [], fs=1.0))

# 6o — none of this proves feeling: the five clues as small icons in a row
n = [P('i1', 'board8', 200, 240, 60, '6o', color='teal'), P('i2', 'knob2', 340, 240, 60, '6o+0.2', color='red'),
     P('i3', 'syringe', 480, 240, 60, '6o+0.4', color='muted'), P('i4', 'mirror', 620, 240, 60, '6o+0.6', color='teal'),
     P('i5', 'sharp', 760, 240, 60, '6o+0.8', color='red')]
for j in range(5): n.append(T(f'il{j}', 196 + 140 * j, 290, str(j + 1), '6o+%.1f' % (0.2 * j), color=GRY, fs=14))
# 6p — like the fish: weak pieces of evidence that, together, weigh a lot. A scale tips little by little
SC = (620, 380)
n2 = [P('fs', 'fish', 260, 400, 110, '6p#peces', color='blue')]
for j, tl in enumerate([0, -.2, -.45, -.7, -1]):
    t = f'6p#débiles+{0.9 * j:.1f}'
    u = f'6p#débiles+{0.9 * (j + 1):.1f}' if j < 4 else None
    n2.append(N(f'sc{j}', 'scale', SC[0] - 110, SC[1] - 80, 220, 160, t if j else '6p#peces', color='amber', tilt=tl, until=u))
for j in range(5):
    n2.append(P(f'pc{j}', 'stone', SC[0] - 92 + 7 * (j - 2), 260, 12, f'6p#débiles{0.9 * j - 0.5:+.1f}', color='teal',
                move=[dict(at=f'6p#débiles+{0.9 * j:.1f}', x=SC[0] - 98 + 7 * (j - 2), y=SC[1] + 2 + 2 * j, dur=0.5)]))
for x in n: x.setdefault('until', '6p')
cues.append(K('6o', 'E6', n + n2, [], fs=1.0))
