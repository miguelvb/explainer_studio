# Scene 5 · La ley
MUSIC = {'pad': 1, 'bells': 0.6}
INTENSITY = 0.55
cues = []

# 5a — 25 Cepheids in the Small Cloud, each with its own rhythm
rnd = random.Random(12)
CEPH = [(rnd.uniform(300, 660), rnd.uniform(140, 400), rnd.uniform(.8, 3.6)) for _ in range(25)]
n = [DATE('d', 60, 40, '1912', '5a'), field('cl', 320, 280, 70, 400, 400, '5a', seed=21, color='muted', ellipse=.7)]
for j, (x, y, per) in enumerate(CEPH):
    n.append(star(f'c{j}', x, y, f'5a#veinticinco+{0.08 * j:.2f}', s=6 + 3 * per, color='amber', period=per))
n.append(T('n25', 690, 120, '25 cefeidas', '5a#cefeidas', color=AMB, fs=16))
cues.append(K('5a', '5b', n, [], fs=1.0))

# 5b — how a Cepheid beats: fast rise, slow fall
n = [star('dc', 480, 180, '5b', s=60, color='amber', period=2.4, depth=.8, cap='δ Cephei · 1784', capfs=13),
     D('saw', [dict(d=SAW, sw=2.4)], 480, 390, 300, '5b#brillo', color='amber')]
cues.append(K('5b', '5c', n, [], fs=1.0))

# 5c–5d — all at the same distance, so brighter means truly brighter
n = [star('ea', 130, 270, '5c', s=18, color='blue', cap='Tierra', capfs=12),
     field('cl', 260, 620, 110, 320, 320, '5c', seed=21, color='muted', ellipse=.7),
     N('ru', 'bar', 150, 268, 600, 4, '5c#misma', color='teal', fill=1, cap='la misma distancia', capfs=12),
     star('a', 740, 230, '5d', s=34, color='amber', tag='brilla más de verdad', tagfs=12),
     star('b', 840, 320, '5d', s=12, color='amber')]
cues.append(K('5c', '5e', n, [], fs=1.0))

# 5e–5f — the plot: brightness against period, the points fall on a straight line
GX, GY, GS = 120, 60, 420
n = [D('ax', AXES, GX + GS / 2, GY + GS / 2, GS, '5e', color='muted'),
     T('xl', GX + 250, GY + GS - 8, 'periodo', '5e', fs=13), T('yl', GX - 10, GY - 6, 'brillo', '5e', fs=13)]
for j in range(25):
    u = j / 24; px = GX + GS * (.14 + .78 * u); py = GY + GS * (.82 - .64 * u) + rnd.uniform(-10, 10)
    n.append(star(f'p{j}', px, py, f'5e#gráfico+{0.12 * j:.2f}', s=8, color='amber'))
n += [D('fit', [dict(d='M14 82L92 18', sw=2)], GX + GS / 2, GY + GS / 2, GS, '5e#recta', color='teal'),
      FOTO('c173', 590, 60, 330, 250, 'circular173.jpg', 'Circular 173 · 1912', '5f'),
      Q('q', 580, 340, 360, ['«Se puede trazar fácilmente', 'una línea recta…»'], '5f#Se', color='teal', fs=14)]
cues.append(K('5e', '5g', n, [], fs=1.0))

# 5g–5h — period gives the true brightness, which gives the distance; the 100 W bulb
n = [star('cp', 160, 200, '5g', s=30, color='amber', period=1.6, cap='periodo', capfs=12),
     D('mini', AXES + [dict(d='M14 82L92 18', sw=2.4)], 480, 200, 90, '5g#brilla', color='teal', cap='brillo real', capfs=12),
     N('rl', 'bar', 640, 196, 260, 8, '5g#distancia', color='teal', fill=1, cap='distancia', capfs=12),
     W.bulb('b1', 220, 420, '5h', s=60), T('w1', 190, 470, '100 W', '5h', color=AMB, fs=13),
     W.bulb('b2', 820, 420, '5h#lejos', s=26, alpha=.45), T('w2', 800, 450, '100 W', '5h#lejos', color=GRY, fs=11),
     N('rb', 'bar', 270, 420, 520, 3, '5h#débil', color='muted', fill=1)]
lk = [OR('cp', 'mini', '5g#brilla', 'amber'), OR('mini', 'rl', '5g#distancia', 'teal')]
cues.append(K('5g', '5i', n, lk, fs=1.0))

# 5i — signed by Pickering, «prepared by Miss Leavitt»
n = [N('sh', 'sheet', 260, 60, 440, 400, '5i', color='muted', lines=['Harvard College Observatory', 'Circular 173 · 1912', '', '', '', '']),
     T('pr', 300, 160, 'prepared by Miss Leavitt', '5i#preparado', color=AMB, fs=13),
     T('sg', 400, 400, 'E. C. Pickering', '5i#Pickering', color=WHITE, fs=24)]
cues.append(K('5i', 'E5', n, [], fs=1.0))
