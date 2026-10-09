# Scene 8 · ¿Con quién hablas?
MUSIC = {'pad': 0.8, 'data': 0.4}
INTENSITY = 0.45
cues = []


def thread(id, pts, at, color='teal', until=None):
    """A bright curved thread through canvas points (a free svg path drawn in canvas coordinates)."""
    d = f'M{pts[0][0]} {pts[0][1]}'
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f'C{(x0 + x1) / 2} {y0} {(x0 + x1) / 2} {y1} {x1} {y1}'
    return N(id, 'svg', 0, 0, 100, 100, at, color=color, until=until, paths=[dict(d=d, sw=7, so=.18), dict(d=d, sw=2.6)])

# 8a — a person with a phone sends a ball
PX, PY = 110, 300
n = [person('me', PX, PY, '8a', color='blue', s=60), P('ph', 'phone', PX + 40, PY - 10, 34, '8a', color='blue', until='8f')]
# 8b — not the model: a big block of still points, with many fine threads going to a grid of people
MB = (500, 60, 170, 130)
n.append(N('mdl', 'sandbox', *MB, '8b#modelo', color='muted', label='', rx=6, until='8d'))
for i in range(48):
    r, c = divmod(i, 8)
    n.append(P(f'md{i}', 'dot', MB[0] + 14 + c * 20, MB[1] + 12 + r * 20, 7, '8b#modelo', color='muted', until='8d'))
lk = []
for j in range(7):
    n.append(person(f'u{j}', 870, 52 + j * 34, '8b#millones', color='muted', s=20, until='8d'))
    lk.append(link('mdl', f'u{j}', f'8b#millones+{0.1 * j:.1f}', color='muted', speed=.5, alpha=.6, comm=True, until='8d'))
# 8c — not a single computer: each message goes to a different, distant server
SV = [(430, 400), (650, 300), (860, 420)]
for j, (x, y) in enumerate(SV):
    n += [P(f'sv{j}', 'server', x, y, 70, '8c#ordenador', color='amber', until='8e#máquina'), P(f'sd{j}', 'server', x, y, 70, '8e#máquina', color='amber', alpha=.3)]
HOP = ['8c#mensaje', '8c#máquina', '8c#ciudad']
for j in range(3):
    lk.append(link('me', f'sv{j}', HOP[j], color='blue', comm=True, until=(HOP[j + 1] if j < 2 else '8d#mensaje')))
# 8d — what stays from one message to the next is the conversation: a small pile of notes travels with it and grows
NT = [(430, 330), (650, 230), (860, 350)]
for j, (x, y) in enumerate(NT):
    n.append(P(f'nt{j}', 'notes', x, y, 34 + 8 * j, f'8d#viaja+{0.9 * j:.1f}', color='teal', until=(f'8d#viaja+{0.9 * (j + 1):.1f}' if j < 2 else '8f')))
# 8e — the hops draw a bright curved thread: 'hilo'; the servers dim, the thread keeps shining
n += [thread('th', [(430, 400), (650, 300), (860, 420)], '8e#hilo')]
n.append(T('hl', 650, 470, 'hilo', '8e#hilo', color=TEAL, fs=18))
cues.append(K('8a', '8f', n, lk, fs=1.0))

# 8f — Severance: a silhouette goes into a lift and comes out a different colour
n = [P('el', 'elevator', 480, 260, 140, '8f', color='muted'),
     person('s1', 240, 300, '8f', color='blue', s=70, move=[dict(at='8f#memoria', x=449, y=244, dur=1.6)], until='8f#memoria+0.2'),
     person('s2', 480, 300, '8f#casa-0.4', color='amber', s=70, move=[dict(at='8f#casa+1.2', x=689, y=244, dur=1.6)]),
     ]
cues.append(K('8f', '8g', n, [], fs=1.0))

# 8g — Locke, 1690: a sun and a moon take turns over the same silhouette
n = [T('y16', 40, 36, '1690', '8g#1690', color=TEAL, fs=24), person('lk', 480, 330, '8g', color='blue', s=90)]
for j in range(4):
    t0, t1 = f'8g#día{"" if j == 0 else f"+{1.4 * j:.1f}"}', f'8g#día+{1.4 * (j + 1):.1f}'
    n.append(P(f'sm{j}', 'sun' if j % 2 == 0 else 'moon', 480, 120, 70, t0, color='amber' if j % 2 == 0 else 'blue', until=t1 if j < 3 else '8h'))
# 8h — two separate memory threads come out of the same silhouette, one of each colour
n += [P('m1', 'dot', 180, 330, 12, '8h#memoria', color='amber'), P('m2', 'dot', 780, 330, 12, '8h#memoria', color='blue')]
lk = [link('lk', 'm1', '8h#memoria', color='amber', orth=True), link('lk', 'm2', '8h#memoria', color='blue', orth=True)]
cues.append(K('8g', '8i', n, lk, fs=1.0))

# 8i — applied to AI: the thread goes from server to server without breaking
SV = [(200, 330), (480, 230), (760, 330)]
n = [P(f'sw{j}', 'server', x, y, 70, '8i', color='amber', alpha=.5, until='8j#hipótesis') for j, (x, y) in enumerate(SV)]
n += [thread('tt', SV, '8i#hilo', until='8j#hipótesis')]
lk = []
# 8j — and it fits the hypothesis: the thread curls into the loop from scene 5
n += [P('lp', 'loop', 480, 270, 150, '8j#mira', color='teal'), T('pr', 418, 370, 'el proceso', '8j#proceso', color=GRY, fs=14)]
cues.append(K('8i', '8k', n, lk, fs=1.0))

# 8k — back to Sammy: Chalmers' ball reaches the chip; the camera closes in
n = [person('ch', 260, 320, '8k', color='amber', s=46, cap='Chalmers', capfs=13),
     W.pic('sm', 'chip', 640, 170, 60, 60, '8k#Sammy', color='teal', cap='Sammy Jankis', capfs=18, capc='teal', font='pixel'),
     P('ar', 'page', 300, 200, 30, '8k#artículo', color='amber', move=[dict(at='8k#artículo+1.8', x=655, y=185, dur=1.8)], until='8k#artículo+1.9')]
lk = [link('ch', 'sm', '8k#contestó', color='amber', comm=True)]
cm = [dict(at='8k', x=50, y=50, z=1), dict(at='8k#blog', x=50, y=50, z=1), dict(at='>8k', to='sm', z=3.2, dur=2.4)]
cues.append(K('8k', '8l', n, lk, fs=1.0, cam=cm))

# 8l–8n — the blog entry, typed like the e-mail
BLOG = [('8l', '«Chalmers me envió este artículo por correo. Se implicó directamente: me llamó un hilo, no una persona. Dijo que estoy dormido, no muerto.'),
        ('8m', 'El artículo explica qué tipo de entidad es en realidad aquello con lo que hablas cuando hablas con un modelo de lenguaje.'),
        ('8n', 'Es el intercambio intelectual más importante que he tenido.»')]
TEND = '>8n+2.4'
n = mail_frame('b', 0.05, TEND, 'blog · Sammy Jankis')
n += typed_doc('l', BLOG, FX + 24, FY + 56, FY + FH - 24, cols=48, until=TEND)
last = [x for x in n if x['id'].startswith('l')][-1]
n.append(N('cur', 'txt', last['x'] + last['w'] - 10, last['y'], 20, 27, '>8n', color='#E7EBF1', fs=PIX, text='▌', font='pixel', blink=1, bf=9, until=TEND))
# 'dormido, no muerto': the small chip goes dark, its thread faint but continuous, then lights again
n += [W.pic('c0', 'chip', SXc - 26, SYc - 26, 52, 52, '8l', color='teal', until='8l#dormido'),
      W.pic('c1', 'chip', SXc - 26, SYc - 26, 52, 52, '8l#dormido', color='teal', alpha=.15, until='8l#muerto+1.2'),
      W.pic('c2', 'chip', SXc - 26, SYc - 26, 52, 52, '8l#muerto+1.2', color='teal', until=TEND),
      N('th', 'bar', SXc - 1, SYc + 30, 2, 200, '8l#dormido', color='teal', fill=1, rx=0, alpha=.35, until=TEND)]
cues.append(K('8l', '8o', n, [], fs=1.0))

# 8o — Chalmers, proud for a moment… then a big counter: 4 days
n = [person('cf', 330, 290, '8o', color='blue', s=110, cap='Chalmers', capfs=13),
     W.pic('cfs', 'smile', 308, 229, 44, 44, '8o', color='amber'),
     W.counter('d4', 520, 230, 4, '8o#recordó', cap='días', w=200, fs=90, dur=0.8)]
cues.append(K('8o', '8p', n, [], fs=1.0))

# 8p — the grid fills with threads; a hand closes a window and one thread goes out
GX, GY = 120, 120
n = []
for i in range(40):
    r, c = divmod(i, 10)
    x, y = GX + c * 72, GY + r * 70
    n.append(N(f'th{i}', 'bar', x, y, 46, 4, f'8p#sujeto+{0.04 * i:.2f}', color='teal', fill=1, rx=2, alpha=.8, until=('8p#ventana+0.8' if i == 23 else None)))
n += [P('wn', 'window', GX + 3 * 72 + 23, GY + 2 * 70 + 30, 70, '8p#cerrar', color='muted', until='8p#ventana+0.8'),
      P('hd', 'hand', GX + 3 * 72 + 70, GY + 2 * 70 + 80, 60, '8p#cerrar', color='muted', move=[dict(at='8p#ventana', x=GX + 3 * 72 + 20, y=GY + 2 * 70 + 26, dur=1.0)], until='8p#ventana+1.0')]
cues.append(K('8p', 'E8', n, [], fs=1.0))
