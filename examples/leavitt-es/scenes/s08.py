# Scene 8 · Lo que quedó
MUSIC = {'pad': 1, 'bells': 0.5}
INTENSITY = 0.35
cues = []

# 8a — head of stellar photometry; 12 December 1921
n = [chipT('jf', 480, 120, 'jefa de fotometría estelar', '8a#jefa', color='teal'),
     person('w', 480, 300, '8a', color='amber', s=46, flick=dict(at='8a#murió', dur=1.6, end='off')),
     N('dk', 'bar', 420, 340, 120, 8, '8a', color='muted', fill=1),
     P('pl', 'page', 520, 320, 30, '8a', color='muted'),
     DATE('d', 60, 40, '12 diciembre 1921', '8a#doce')]
cues.append(K('8a', '8b', n, [], fs=1.0))

# 8b — the family grave in Cambridge Cemetery
MON = [dict(d='M40 92V40H60V92Z', f='#171D26'), dict(d='M30 92H70', sw=2.4), dict(d=W._circ(50, 28, 11), f='#171D26'), dict(d='M44 40H56', sw=1.6)]
n = [D('hill', [dict(d='M2 90Q50 66 98 90', sw=1.6, so=.6)], 480, 330, 600, '8b', color='muted'),
     D('mon', MON, 480, 260, 200, '8b#cementerio', color='muted'),
     T('pq', 380, 420, 'Henrietta · Mira · Roswell', '8b#Mira', color=WHITE, fs=15)]
cues.append(K('8b', '8c', n, [], fs=1.0))

# 8c — the letter from Stockholm reaches an empty desk
n = [DATE('d', 60, 40, '1925', '8c'),
     chipT('sk', 200, 270, 'Estocolmo', '8c#sueco', color='blue'),
     person('ml', 200, 190, '8c#Mittag-Leffler', color='blue', s=34),
     N('dk', 'bar', 700, 300, 120, 8, '8c', color='muted', fill=1),
     D('lt', LETTER, 760, 260, 50, '8c#escribió+0.8', color='amber'),
     chipT('nb', 760, 160, 'Nobel', '8c#Nobel', color='amber', until='8c#póstumo')]
lk = [link('sk', 'lt', '8c#escribió+0.2', color='amber', comm=True)]
cues.append(K('8c', '8d', n, lk, fs=1.0))

# 8d — the first rung of the cosmic distance ladder
LAD = [dict(d='M30 96V4M70 96V4', sw=2)] + [dict(d=f'M30 {90 - 18 * j}H70', sw=2) for j in range(5)]
n = [D('lad', LAD, 380, 280, 400, '8d', color='muted'),
     N('r1', 'bar', 318, 432, 124, 6, '8d#peldaño', color='amber', fill=1, cap='cefeidas · Leavitt', capfs=13),
     P('gx', 'cloud', 380, 60, 50, '8d#universo', color='teal'),
     D('jw', SCOPE, 760, 160, 90, '8d#Webb', color='blue', cap='James Webb', capfs=12),
     star('cw', 820, 360, '8d#Webb', s=20, color='amber', period=1.6)]
cues.append(K('8d', '8e', n, [], fs=1.0))

# 8e — the crater, the asteroid, the play, the book
n = [P('mn', 'moon', 260, 250, 200, '8e', color='muted'),
     P('cr', 'target', 240, 280, 26, '8e#cráter', color='amber', tag='Leavitt', tagfs=12),
     star('as', 520, 100, '8e#asteroide', s=10, color='amber', cap='5383 Leavitt', capfs=11, move=[dict(at='8e#asteroide+0.2', x=640, y=80, dur=4)]),
     T('sordas', 120, 410, 'dedicado a las personas sordas en la ciencia', '8e#sordas', color=GRY, fs=12),
     P('bk', 'book', 760, 330, 90, '8e#libros', color='amber', cap='«El universo de cristal» · Dava Sobel', capfs=11),
     chipT('sky', 760, 210, '«Silent Sky»', '8e#teatro', color='blue')]
cues.append(K('8e', '8f', n, [], fs=1.0))

# 8f — every distance to a galaxy uses her ruler
n = [P('gx', 'cloud', 860, 250, 80, '8f', color='teal'),
     star('ea', 100, 260, '8f', s=16, color='blue'),
     N('rl', 'bar', 120, 258, 690, 6, '8f#distancia', color='teal', fill=1),
     T('nm', 300, 290, 'Henrietta Swan Leavitt', '8f#regla', color=AMB, fs=18)]
cues.append(K('8f', '8g', n, [], fs=1.0))

# 8g — closing seal
cues.append(dict(a='seal', at='8g', until='E8', ext=0, p=dict(text='La mujer que midió el universo', sub='Arkinos @ oct 2026', at=0.3, type=14, scale=1.0, cy=215, ty=392), bg=True, fade=[0.8, 2.0]))
