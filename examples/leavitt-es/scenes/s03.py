# Scene 3 · Estrellas que parpadean
MUSIC = {'pad': 1, 'bells': 0.6}
INTENSITY = 0.45
cues = []

# 3a — a variable star and its light curve
n = [star('v', 480, 200, '3a', s=40, color='amber', period=2.4, depth=.8),
     D('lc', [dict(d='M2 50Q14 10 26 50T50 50T74 50T98 50', sw=2.4)], 480, 390, 260, '3a#brillo', color='amber')]
cues.append(K('3a', '3b', n, [], fs=1.0))

# 3b — negative over positive: what has not changed cancels, what changed jumps out
def plate(id, cx, cy, s, at, neg, odd, **k):
    rnd = random.Random(5); d = ''
    for _ in range(26): d += W._circ(round(rnd.uniform(8, 92), 1), round(rnd.uniform(8, 92), 1), 1.8)
    d += W._circ(62, 38, 1.8 if odd else 3.6)
    bg = dict(d='M2 2H98V98H2Z', f='#D8DEE6' if neg else '#0B0E13', s=0)
    return N(id, 'svg', cx - s / 2, cy - s / 2, s, s, at, color='muted', paths=[bg, dict(d=d, f='#10151C' if neg else '#E7EBF1', s=0)], **k)

n = [plate('neg', 300, 270, 220, '3b#negativo', True, False, cap='negativo', capfs=13, until='3b#anulaban'),
     plate('pos', 660, 270, 220, '3b#positivo', False, True, cap='otro día', capfs=13, until='3b#anulaban',
           move=[dict(at='3b#sobre+0.2', x=190, y=160, dur=1.4)]),
     N('blank', 'sandbox', 190, 160, 220, 220, '3b#anulaban', color='muted', label=''),
     P('hit', 'target', 326, 244, 34, '3b#cambiado', color='red', blink=.4, bf=6)]
cues.append(K('3b', '3c', n, [], fs=1.0))

# 3c–3d — the Magellanic Clouds, hundreds of variables, 1777
n = [FOTO('smc', 60, 60, 420, 420, 'nube.jpg', 'Pequeña Nube de Magallanes', '3c', until='3e')]
rnd = random.Random(9)
for j in range(16):
    n.append(P(f'm{j}', 'target', rnd.uniform(110, 430), rnd.uniform(110, 430), 18, f'3c#cientos+{0.25 * j:.2f}', color='red', until='3e'))
n += [W.counter('cnt', 560, 200, 1777, '3d#mil', cap='estrellas variables', w=260, fs=56, dur=3.5, until='3e'),
      DATE('d', 600, 330, '1908', '3d', until='3e'),
      T('ann', 540, 370, 'Annals of Harvard College Observatory', '3d#1908+0.4', fs=12, until='3e')]
cues.append(K('3c', '3e', n, [], fs=1.0))

# 3e — the hidden line
n = [N('sh', 'sheet', 200, 90, 560, 330, '3e', color='muted', lines=['1777 Variables', 'in the Magellanic Clouds', '', '', '']),
     Q('q', 230, 300, 500, ['«las variables más brillantes', 'tienen los periodos más largos»'], '3e#Merece', color='amber', fs=15),
     N('lp', 'lupa', 610, 250, 120, 120, '3e#escondida', color='teal')]
cues.append(K('3e', '3f', n, [], fs=1.0))

# 3f — the brighter, the slower
n = [star('b', 330, 230, '3f', s=70, color='amber', period=3.6, cap='30 días', capfs=14),
     star('s', 640, 250, '3f', s=26, color='amber', period=1.0, cap='3 días', capfs=14)]
cues.append(K('3f', 'E3', n, [], fs=1.0))
