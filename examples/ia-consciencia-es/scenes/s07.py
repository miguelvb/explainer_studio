# Scene 7 · El otro lado
MUSIC = {'pad': 0.8, 'cinema': 0.4}
MOOD = 'tense'
INTENSITY = 0.5
cues = []

# 7a — the scale turns: the other plate, empty
n = [N('sc0', 'scale', 370, 200, 220, 160, 0.05, color='amber', tilt=-1, until='7a#otro'),
     N('sc1', 'scale', 370, 200, 220, 160, '7a#otro', color='amber', tilt=0, until='7b'),
     # 7b — Anil Seth: consciousness tied to being alive. A beating cell, a heart, a breathing body
     person('se', 140, 330, '7b#Seth', color='amber', s=60, cap='Anil Seth', capfs=13),
     P('cl', 'cell', 360, 230, 90, '7b#células', color='teal', blink=.4, bf=6),
     P('hr', 'heart', 500, 230, 80, '7b#cuerpo', color='red', blink=.5, bf=6),
     P('lg', 'lungs', 640, 230, 90, '7b#mantiene', color='blue', blink=.3, bf=2)]
# 7c — the chip copies the beat with points that light up, but inside there is no glow
for x in n[3:6]: x['until'] = '7d'
n.append(P('ng', 'ghost', 640, 430, 44, '7c#nada', color='muted', cap='sin experiencia', capfs=11))
n += chip('cc', 500, 430, '7c#chip', s=56, box_s=96)
for j in range(4):
    n.append(P(f'cd{j}', 'dot', 470 + 20 * j, 470, 8, '7c#imitar', color='red', blink=.5, bf=6))
# 7d — the container shuts with a padlock
n.append(ic('lk', 'sigLock', 452, 384, 30, '7d#silicio', color='amber'))
# 7e — a parrot next to the chip, repeating balls
n += [P('pr', 'parrot', 760, 430, 80, '7e#imitación', color='teal')]
lk = [link('cc_box', 'pr', '7e#leído', color='teal', bi=True, speed=.6, comm=True)]
cues.append(K('S7', '7f', n, lk, fs=1.0))

# 7f — 2023: Chalmers' list. Five empty puzzle pieces around the chip: eye, mirror, loop, central board, target
CX, CY = 480, 280
n = [T('y23', 40, 36, '2023', '7f#2023', color=TEAL, fs=24)] + chip('ck', CX, CY, '7f', s=60, box_s=100)
SL = [('eye', 'sentidos', CX - 250, CY - 120), ('mirror', 'sí mismas', CX, CY - 175), ('loop', 'bucles', CX + 250, CY - 120),
      ('plank', 'espacio común', CX + 250, CY + 120), ('target', 'metas', CX - 250, CY + 120)]
WORDS = ['sentidos', 'sí_mismas', 'bucles', 'espacio', 'metas']
for j, (nm, cap, x, y) in enumerate(SL):
    t = f'7f#{WORDS[j]}'
    n += [P(f'h{j}', 'hole', x, y, 96, t, color='muted', alpha=.8),
          P(f'i{j}', nm, x, y + 3, 40, t, color='muted'),
          # 7h — the other pieces are being built: they fill in one by one
          P(f'f{j}', 'puzzle', x, y, 96, f'7h#demás+{0.5 * j:.1f}', color='teal'),
          P(f'g{j}', nm, x, y + 3, 40, f'7h#demás+{0.5 * j:.1f}', color='teal')]
# 7g — a sixth piece, a cell, with a padlock
n += [P('h5', 'hole', CX, CY + 175, 96, '7g#biología', color='muted', alpha=.8), P('i5', 'cell', CX, CY + 178, 40, '7g#biología', color='amber'),
      ic('l5', 'sigLock', CX + 40, CY + 145, 26, '7g#permanente', color='amber')]
cues.append(K('7f', 'E7', n, [], fs=1.0))
