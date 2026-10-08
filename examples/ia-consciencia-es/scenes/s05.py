# Scene 5 · La objeción
MUSIC = {'pad': 0.8, 'cinema': 0.5}
INTENSITY = 0.5
cues = []

# 5a — the brain alone; the camera moves to its back, the visual area
n = [P('br', 'brain', 480, 270, 260, '5a', color='amber'),
     P('vz', 'dot', 590, 290, 30, '5a#cerebro', color='red', alpha=.7, blink=.6, bf=4)]
cm = [dict(at='5a', x=50, y=50, z=1), dict(at='>5a', x=61, y=53, z=2.2, dur=2.4)]
cues.append(K('5a', '5b', n, [], fs=1.0, cam=cm))

# 5b — a person whose eyes are 'off'; a ball appears on their left and the arm points at it precisely
HX, HY = 560, 330
n = [person('bp', HX, HY, '5b', color='blue', s=100),
     N('ey', 'bar', HX - 24, HY - 62, 48, 8, '5b#dañada', color='muted', fill=1, rx=2),
     P('ob', 'stone', 230, 300, 34, '5b#objeto', color='amber'),
     N('arm', 'bar', 260, HY - 4, HX - 300, 6, '5b#señalar', color='blue', fill=1, rx=3),
     # 5c — blindsight: the signal climbs the layers, but the inner glow does not come on
     T('vc', 40, 36, 'visión ciega', '5c#ciega', color=TEAL, fs=20)]
tw, TY = tower('v', 820, 470, '5c#procesó', floors=4, w=150, fh=34, gap=14, dots=False)
n += tw + [P('sg', 'dot', 811, TY[0] - 9, 18, '5c#procesó+0.8', color='amber', move=[dict(at=f'5c#procesó+{1.6 + 0.8 * k_:.1f}', x=811, y=round(TY[k_] - 9), dur=0.8) for k_ in range(1, 4)]),
           N('off', 'svg', 790, 60, 60, 60, '5c#experiencia', color='muted', paths=[dict(d='M50 20a30 30 0 1 0 .1 0Z', sw=2)], dashed=True, cap='sin experiencia', capfs=11)]
cues.append(K('5b', '5d', n, [], fs=1.0))

# 5d — so abstraction alone is not enough: a puzzle-shaped hole in the building
TX, TB = 300, 480
tw, TY = tower('t', TX, TB, 0.05)
HOLE = (TX + 95, TY[4] - 28)
n = list(tw) + [P('hole', 'hole', HOLE[0], HOLE[1], 52, '5d#falta', color='muted')]
# 5e — three candidate ingredients parade: broadcast to everything, loops, self-representation
PZ = [(600, 180), (720, 180), (840, 180)]
for j, (nm, (x, y)) in enumerate(zip(['arrows', 'loop', 'mirror'], PZ)):
    t = ['5e#comparta', '5e#bucles', '5e#represente'][j]
    u = None if j == 2 else '5f#última'
    n += [P(f'pz{j}', 'puzzle', x, y, 100, t, color=['blue', 'teal', 'amber'][j], until=u),
          P(f'pi{j}', nm, x, y + 4, 44, t, color=['blue', 'teal', 'amber'][j], until=u)]
# 5f — the mirror piece stays (moves to the centre of the right side)
for k_ in ('pz2', 'pi2'):
    d = [x for x in n if x['id'] == k_][0]; d['move'] = [dict(at='5f#clave', x=d['x'] - 120, y=d['y'] + 100, dur=1.2)]
# 5g — Hofstadter: the ball climbs to the top, turns and comes back down, a loop; a tiny drawing of the building on top
n += [person('hf', 820, 470, '5g#Hofstadter', color='muted', s=40, cap='Hofstadter', capfs=12),
      P('lb', 'dot', TX - 9, TY[0] - 9, 18, '5g#capas', color='amber',
        move=[dict(at=f'5g#capas+{0.6 * k_:.1f}', x=TX - 9, y=round(TY[k_] - 9), dur=0.6) for k_ in range(1, 5)] +
             [dict(at=f'5g#capas+{3.0 + 0.6 * k_:.1f}', x=TX - 9, y=round(TY[4 - k_] - 9), dur=0.6) for k_ in range(1, 5)]),
      P('lp', 'loop', TX - 120, TY[4] - 70, 64, '5g#sí_mismas', color='amber'),
      P('mini', 'server', TX, TY[4] - 64, 38, '5g#mapa', color='blue', paths=[dict(d='M20 20h60v12h-60ZM20 44h60v12h-60ZM20 68h60v12h-60Z', sw=3)])]
# 5h — the mirror piece fits in the hole; for the first time, the glow lights inside the building
for k_ in ('pz2', 'pi2'):
    d = [x for x in n if x['id'] == k_][0]
    d['move'].append(dict(at='5h#mira', x=HOLE[0] - (50 if k_ == 'pz2' else 22), y=HOLE[1] - (50 if k_ == 'pz2' else 18), dur=1.6))
n += [glow('ig', TX, TY[2], '5h#experiencia', s=130, color='amber')]
for x in n:
    if x['id'] in ('pz2', 'pi2'):
        x['until'] = '5i'
cues.append(K('5d', '5i', n, [], fs=1.0))

# 5i — transition: the building turns back into the chip
tw, TY = tower('u', TX, TB, 0.05, until='5i#Veamos')
n = tw + chip('cp', 480, 270, '5i#Veamos', s=80)
cues.append(K('5i', 'E5', n, [], fs=1.0))
