# Scene 10 · Por qué importa ahora
MUSIC = {'cinema': 0.7, 'pad': 0.5}
MOOD = 'tense'
INTENSITY = 0.6
cues = []

# 10a — the umbrella closes; the camera pulls away
n = [person('us', 480, 330, 0.05, color='teal', s=70, until='10b'), P('uo', 'umbrella', 480, 220, 120, 0.05, color='teal', until='10a#importa'),
     P('uc', 'umbrellac', 520, 280, 70, '10a#importa', color='teal', until='10b')]
cm = [dict(at='10a', x=50, y=50, z=1), dict(at='>10a+0.6', x=50, y=50, z=.6, dur=1.8), dict(at='10b+0.3', x=50, y=50, z=1, dur=0.3)]
# 10b — the grid of points spreads to fill the screen; many of them have a cold glow
for i in range(24 * 13):
    r, c = divmod(i, 24)
    x, y = 30 + c * 39, 30 + r * 40
    d = ((x - 480) ** 2 + (y - 270) ** 2) ** .5
    t = f'10b#sufrimiento+{d / 300:.2f}'
    n.append(P(f'g{i}', 'dot', x - 3, y - 3, 7, t, color='muted', until='10c'))
    if (i * 37) % 5 == 0: n.append(glow(f'cg{i}', x, y, f'10b#copias+{d / 400:.2f}', s=26, color='blue', alpha=.8, until='10c'))
cues.append(K('10a', '10c', n, [], fs=1.0, cam=cm))

# 10c — a hand carries a shield to an empty chip, while a dog and a person are left outside
n = chip('ec', 640, 280, '10c', s=60, box_s=110)
n += [N('ng', 'svg', 615, 255, 50, 50, '10c#vacías', color='muted', paths=[dict(d='M50 20a30 30 0 1 0 .1 0Z', sw=2)], alpha=.5),
      P('sd', 'shield', 330, 200, 120, '10c#cuidado', color='teal', move=[dict(at='10c#máquinas+0.4', x=580, y=220, dur=1.8)]),
      P('hd', 'hand', 280, 300, 70, '10c#cuidado', color='muted', move=[dict(at='10c#máquinas+0.4', x=545, y=300, dur=1.8)], until='10d'),
      P('dg', 'dog', 200, 440, 80, '10c#quien', color='blue'), person('pp', 300, 460, '10c#quien', color='blue', s=50),
      glow('dgg', 214, 432, '10c#sufre', s=22, color='blue'), glow('ppg', 300, 412, '10c#sufre', s=22, color='blue')]
cues.append(K('10c', '10d', n, [], fs=1.0))

# 10d — an industrial farm with rows of hens; gears fit around it and lock
n = [P('fc', 'factory', 480, 250, 260, '10d#granjas', color='muted')]
for j in range(8):
    n.append(P(f'hn{j}', 'hen', 380 + 28 * (j % 4) + (14 if j >= 4 else 0), 300 + 26 * (j // 4), 26, f'10d#granjas+{0.15 * j:.2f}', color='amber'))
for j, (x, y) in enumerate([(250, 160), (710, 160), (250, 380), (710, 380)]):
    n.append(P(f'gr{j}', 'gear', x + (-80 if x < 480 else 80), y, 90, f'10d#economía+{0.3 * j:.1f}', color='red',
               move=[dict(at=f'10d#construye+{0.3 * j:.1f}', x=round(x - 45), y=round(y - 45), dur=1.2)], shake=dict(at='10d#deshacerlo', dur=1.0, amp=3, f=30)))
n.append(ic('lk', 'sigLock', 480, 120, 34, '10d#imposible', color='red'))
cues.append(K('10d', '10e', n, [], fs=1.0))

# 10e — a big chip in front of a small silhouette; between them a curved link with a calm ball going back and forth
n = chip('bc', 640, 250, '10e', s=130, box=False) + [person('sp', 260, 330, '10e', color='blue', s=56)]
lk = [link('sp', 'bc', '10e#amenaza-1.5', color='teal', bi=True, speed=.25, comm=True)]
cues.append(K('10e', 'E10', n, lk, fs=1.0))
