# Scene 7 · La regla se estira
MUSIC = {'pad': 1, 'bells': 0.6}
INTENSITY = 0.7
cues = []

# 7a–7b — Shapley measures the Milky Way; the Sun is off-centre; the fuzzy patches
n = [DATE('d', 60, 40, '1918', '7a'),
     field('mw', 380, 180, 0, 520, 520, '7a', seed=7, color='blue', ellipse=.3, r=(.35, .9)),
     star('sun', 440, 260, '7a#Sol', s=14, color='amber', cap='Sol', capfs=11, move=[dict(at='7a#lado', x=553, y=253, dur=1.6)]),
     person('sh', 120, 420, '7a#Shapley', color='blue', s=34, cap='Shapley', capfs=12),
     P('g1', 'cloud', 90, 140, 60, '7b#manchas', color='muted', alpha=.6, tag='?'),
     P('g2', 'cloud', 880, 120, 54, '7b#manchas+0.4', color='muted', alpha=.6, tag='?'),
     P('g3', 'cloud', 860, 440, 66, '7b#manchas+0.8', color='muted', alpha=.6, tag='?')]
cm = [dict(at='7a', x=50, y=50, z=1), dict(at='7b', x=50, y=50, z=.92, dur=2)]
cues.append(K('7a', '7c', n, [], fs=1.0, cam=cm))

# 7c — Hubble's plate: VAR!
n = [DATE('d', 60, 40, 'octubre 1923', '7c'),
     FOTO('var', 80, 100, 420, 320, 'var.jpg', 'Placa H335H de Hubble', '7c#Andrómeda'),
     person('hb', 640, 300, '7c#Hubble', color='blue', s=46, cap='Hubble', capfs=13),
     star('v1', 760, 180, '7c#cefeida', s=22, color='amber', period=1.4),
     T('var', 600, 400, 'VAR!', '7c#VAR', color=RED, fs=34, font='pixel')]
cues.append(K('7c', '7d', n, [], fs=1.0))

# 7d–7e — the ruler stretches beyond the Milky Way; the frame breaks; galaxies drift apart
n = [field('mw', 30, 40, 150, 240, 240, '7d', seed=7, color='blue', ellipse=.3),
     N('frm', 'sandbox', 20, 180, 280, 180, '7d', color='red', label='', dashed=True, until='7d#otra'),
     P('and', 'cloud', 860, 270, 80, '7d', color='teal', cap='Andrómeda', capfs=12),
     N('rl', 'bar', 260, 268, 560, 6, '7d#distancia', color='teal', fill=1, cap='casi 1.000.000 años luz', capfs=13, until='7e')]
rnd = random.Random(31)
for j in range(14):
    x, y = rnd.uniform(60, 900), rnd.uniform(40, 500)
    dx, dy = (x - 480) * .25, (y - 270) * .25
    n.append(P(f'g{j}', 'cloud', x, y, rnd.uniform(26, 46), f'7d#otra+{0.15 * j:.2f}', color='muted', alpha=.7,
               move=[dict(at='7e#alejan', x=round(x + dx - 18), y=round(y + dy - 18), dur=6)]))
n.append(DATE('d', 60, 40, '1929', '7e#1929'))
cues.append(K('7d', 'E7', n, [], fs=1.0))
