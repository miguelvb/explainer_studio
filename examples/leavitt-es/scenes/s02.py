# Scene 2 · Las computadoras de Harvard
MUSIC = {'pad': 1, 'bells': 0.4}
INTENSITY = 0.4
cues = []

# 2a–2b — Pickering photographs the whole sky; plates arrive from Arequipa
n = [DATE('d', 60, 40, '1895', '2a'),
     FOTO('obs', 60, 110, 260, 190, 'observatorio.jpg', 'Observatorio de Harvard', '2a#observatorio', until='2b'),
     person('pk', 470, 200, '2a#Pickering', color='blue', s=46, cap='Pickering', capfs=13),
     D('sc', SCOPE, 600, 190, 90, '2a#fotografiar', color='blue')]
for j in range(6):
    n.append(N(f'pl{j}', 'sandbox', 720, 330 - 22 * j, 110, 16, f'2a#cielo+{0.4 * j:.1f}', color='muted', label=''))
n += [chipT('aq', 300, 470, 'Arequipa · Perú', '2b#Arequipa', color='teal'),
      chipT('hv', 300, 360, 'Harvard', '2b#Arequipa+0.3', color='red')]
for j in range(4):
    n.append(N(f'pq{j}', 'sandbox', 700 + 18 * j, 240 - 22 * j - 110, 110, 16, f'2b#miles+{0.4 * j:.1f}', color='muted', label=''))
lk = [link('aq', 'hv', '2b#Arequipa+0.8', color='teal', comm=True)]
cues.append(K('2a', '2c', n, lk, fs=1.0))

# 2c–2e — the women «computers», their pay, the fence in front of the telescope
n = [FOTO('cmp', 40, 40, 300, 210, 'computadoras.jpg', 'Las computadoras, 13 mayo 1913', '2c')]
for j in range(5):
    x = 420 + 100 * j
    n += [person(f'c{j}', x, 300, f'2c#mujeres+{0.3 * j:.1f}', color='amber' if j == 2 else 'blue', s=36),
          N(f'dk{j}', 'bar', x - 40, 336, 80, 8, f'2c#mujeres+{0.3 * j:.1f}', color='muted', fill=1)]
n += [T('lbl', 560, 360, '«computadoras»', '2c#computadoras', color=GRY, fs=15),
      T('pay', 120, 300, '0,25–0,50 $ / hora', '2d#veinticinco', color=AMB, fs=18),
      P('fn', 'fence', 190, 440, 80, '2d#telescopios', color='muted'),
      D('ts', SCOPE, 80, 430, 80, '2d#telescopios', color='blue'),
      person('man', 120, 470, '2d#telescopios+0.3', color='blue', s=28),
      T('har', 560, 140, '«el harén de Pickering»', '2e#harén', color=RED, fs=15, until='2e#Pero')]
for j in range(5):
    n.append(star(f'st{j}', 420 + 100 * j, 220, f'2e#descubrimientos+{0.35 * j:.1f}', s=12, color='amber', blink=.3, bf=2 + j * .4))
cues.append(K('2c', 'E2', n, [], fs=1.0))
