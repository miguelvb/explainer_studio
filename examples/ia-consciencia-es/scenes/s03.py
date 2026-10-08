# Scene 3 · Por qué no hay un test
MUSIC = {'pad': 1, 'data': 0.3}
INTENSITY = 0.35
cues = []

# 3a — two people, a transparent wall between them
A1, A2, PY = 260, 700, 330
n = [person('h1', A1, PY, '3a', color='blue', s=90), person('h2', A2, PY, '3a', color='blue', s=90),
     N('wall', 'bar', 476, 150, 8, 300, '3a#cabeza', color='muted', fill=0, rx=0, alpha=.5),
     # 3b — the same brain in both; then the same gesture at the same time
     P('b1', 'brain', A1, PY - 175, 80, '3b#hecha', color='amber'), P('b2', 'brain', A2, PY - 175, 80, '3b#hecha', color='amber')]
for k_, x in (('h1', A1), ('h2', A2)):
    n[[i for i, d in enumerate(n) if d['id'] == k_][0]]['shake'] = dict(at='3b#comporta', dur=1.4, amp=6, f=14)
cues.append(K('3a', '3c', n, [], fs=1.0))

# 3c — a dog: its brain looks half like ours; the chip: nothing looks alike
n = [person('h3', 160, 330, 0.05, color='blue', s=80), P('b3', 'brain', 160, 175, 70, 0.05, color='amber'),
     P('dg', 'dog', 470, 320, 120, '3c#perro', color='blue'), P('b4', 'brain', 470, 205, 60, '3c#perro+0.6', color='amber', alpha=.45),
     ch('hm', 470, 410, 70, 'a medias', '3c#medias', color='muted')]
n += chip('cz', 780, 300, '3c#inteligencia', s=64)
n[-1]['until'] = '3d#números'
n += [N('qz', 'question', 765, 175, 30, 30, '3c#lados', color='amber')]
# 3d — zoom into the chip: a grid of points switching on and off
for i in range(36):
    r, c = divmod(i, 6)
    n.append(P(f'z{i}', 'dot', 755 + c * 10, 275 + r * 10, 7, '3d#números', color=['teal', 'blue', 'amber'][(i * 7) % 3], blink=1, bf=2 + (i * 13) % 7))
cm = [dict(at='3c', x=50, y=50, z=1), dict(at='3d#números', to='cz', z=3.4, dur=2.0), dict(at='>3d', to='cz', z=3.4)]
cues.append(K('3c', '3e', n, [], fs=1.0, cam=cm))

# 3e — an avalanche of books and pages goes into the chip; among them a little sci-fi robot whose eyes light up
CX, CY = 640, 290
n = chip('ce', CX, CY, 0.05, s=70)
for i in range(14):
    nm = ['book', 'page', 'page', 'book'][i % 4]
    y0 = 90 + (i * 53) % 360; t = f'3e#entrenamos+{0.35 * i:.2f}'
    n.append(P(f'bk{i}', nm, 80, y0, 44, t, color='muted', move=[dict(at=f'3e#entrenamos+{0.35 * i + 1.6:.2f}', x=CX - 22, y=CY - 22, dur=1.6)],
               until=f'3e#entrenamos+{0.35 * i + 1.7:.2f}'))
n += [P('rb', 'robot', 300, 400, 70, '3e#robots', color='teal', litAt='3e#despiertan'),
      # 3f — a big hand (the company) puts a lid on the chip's container
      P('hd', 'hand', CX, 40, 90, '3f', color='muted', move=[dict(at='3f#entrenarlas', x=CX - 45, y=110, dur=1.4)], until='3g'),
      N('ld', 'svg', CX - 70, 150, 140, 40, '3f', color='muted', paths=W.PICS['lid'], move=[dict(at='3f#entrenarlas', x=CX - 70, y=CY - 80 - 20, dur=1.4)])]
# 3g — a green ball and a red ball leave the chip; both fade before arriving
n += [P('yes', 'dot', CX + 80, CY - 20, 24, '3g#sí', color='teal', move=[dict(at='3g#sí+2.0', x=CX + 220, y=CY - 50, dur=2.0)], until='3g#sí+1.6'),
      P('no', 'dot', CX + 80, CY + 20, 24, '3g#no', color='red', move=[dict(at='3g#no+2.0', x=CX + 220, y=CY + 50, dur=2.0)], until='3g#no+1.6'),
      person('obs', 900, CY, '3g', color='muted', s=40),
      # 3h — a magnifier over the chip
      N('lp', 'lupa', CX - 10, CY - 120, 90, 90, '3h#investigar', color='amber')]
# 3i — the camera pulls away into an empty dark space
cm = [dict(at='3e', x=50, y=50, z=1), dict(at='3i#idea', x=50, y=50, z=1), dict(at='>3i+0.8', to='ce', z=.35, dur=3.0)]
cues.append(K('3e', 'E3', n, [], fs=1.0, cam=cm))
