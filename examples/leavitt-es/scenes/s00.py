# Scene 0 · Gancho
MUSIC = {'bells': 1, 'pad': 0.4}
INTENSITY = 0.35

# ---- shared helpers for this film (later scenes use them) ----
import random
from pathlib import Path
FOTOS = Path(__file__).resolve().parent.parent / 'fotos'
WHITE = '#E7EBF1'


def P(id, name, cx, cy, s, at, color='blue', **k):
    """Line drawing from worldkit.PICS centred on (cx, cy)."""
    return W.pic(id, name, cx - s / 2, cy - s / 2, s, s, at, color=color, **k)


def D(id, paths, cx, cy, s, at, color='blue', **k):
    """Free line drawing: paths in a 100x100 box, centred on (cx, cy)."""
    return N(id, 'svg', cx - s / 2, cy - s / 2, s, s, at, color=color, paths=paths, **k)


def person(id, cx, cy, at, color='blue', s=40, **k):
    return N(id, 'person', cx - s * .45, cy - s * .8, s * .9, s * 1.6, at, color=color, **k)


def FOTO(id, x, y, w, h, file, name, at, **k):
    """Archive photo; until fotos/<file> exists, a dashed placeholder labelled `name`."""
    src = f'fotos/{file}' if (FOTOS / file).exists() else None
    return W.photo(id, x, y, w, h, name, at, src=src, **k)


def DATE(id, x, y, text, at, fs=20, color='teal', **k):
    """Typed date (month always written out)."""
    return N(id, 'txt', x, y, len(text) * fs * CW + 8, fs + 8, at, color=color, fs=fs, type=12, text=text, **k)


def star(id, cx, cy, at, s=10, color='amber', period=None, depth=.75, **k):
    """A star; with `period` (seconds on screen) it pulses like a variable star."""
    if period: k.update(blink=depth, bf=round(2 * math.pi / period, 3))
    return P(id, 'dot', cx, cy, s, at, color=color, **k)


def field(id, n, x, y, w, h, at, seed=1, color='muted', r=(0.5, 1.4), ellipse=False, **k):
    """A field of tiny stars drawn as one node (x, y, w, h must be square for a uniform scale)."""
    rnd = random.Random(seed); d = ''
    while n > 0:
        px, py = rnd.uniform(2, 98), rnd.uniform(2, 98)
        if ellipse and ((px - 50) / 48) ** 2 + ((py - 50) / (48 * ellipse)) ** 2 > 1: continue
        d += W._circ(round(px, 1), round(py, 1), round(rnd.uniform(*r), 2)); n -= 1
    return N(id, 'svg', x, y, w, h, at, color=color, paths=[dict(d=d, f=1, s=0)], **k)


def chipT(id, cx, cy, label, at, color='muted', **k): return ch(id, cx, cy, 0, label, at, color=color, **k)


SAW = 'M2 75L10 22L30 75L38 22L58 75L66 22L86 75L94 22'          # Cepheid light curve: fast rise, slow fall
AXES = [dict(d='M10 8V90H96', sw=1.8)]
HOUSE = [dict(d='M18 50L50 20L82 50V88H18Z', f='#171D26'), dict(d='M42 88V66H58V88', sw=1.8)]
CHURCH = [dict(d='M28 52L50 32L72 52V90H28Z', f='#171D26'), dict(d='M50 32V8M43 15H57', sw=2.2), dict(d='M44 90V72Q50 64 56 72V90', sw=1.6)]
DOME = [dict(d='M14 90V58H86V90Z', f='#171D26'), dict(d='M20 58Q20 22 50 22Q80 22 80 58', f='#171D26'), dict(d='M50 22L62 40', sw=3)]
LETTER = [dict(d='M12 26H88V76H12Z', f='#171D26'), dict(d='M12 26L50 54L88 26', sw=1.8)]
RING = [dict(d=W._circ(50, 50, 30), sw=4)]
SCOPE = [dict(d='M18 52L72 30L78 44L24 66Z', f='#171D26'), dict(d='M44 58L34 92M48 56L60 92', sw=2.2)]

# ---- 0a — title
cues = [dict(a='seal', at='S0', until='0b', ext=0, p=dict(text='La mujer que midió el universo', sub='Henrietta Swan Leavitt', at=0.5, type=14, scale=1.0, cy=215, ty=392), bg=True, fade=[0.8, 2.0])]

# ---- 0b–0c — a faint star: far and big, or near and small? then: is the Milky Way everything?
n = [field('sky', 140, 120, -60, 720, 720, '0b', seed=3, until='0c'),
     star('f', 480, 270, '0b', s=7, color='amber', until='0c'),
     P('big', 'star', 300, 300, 90, '0b#lejos', color='amber', alpha=.35, tag='lejos y enorme', tagfs=13, until='0c'),
     P('small', 'star', 660, 300, 26, '0b#pequeña', color='amber', tag='cerca y pequeña', tagfs=13, until='0c'),
     N('qm', 'txt', 466, 290, 40, 50, '0b#cerca', color=WHITE, fs=44, text='?', until='0c'),
     field('mw', 260, 330, 120, 300, 300, '0c', seed=7, color='blue', ellipse=.32, r=(.4, 1.0)),
     N('frm', 'sandbox', 300, 200, 360, 140, '0c#universo', color='red', label='', dashed=True, tag='¿todo el universo?', tagfs=13),
     P('n1', 'cloud', 130, 120, 70, '0c#mucho', color='muted', alpha=.6, tag='?'),
     P('n2', 'cloud', 820, 160, 60, '0c#mucho+0.4', color='muted', alpha=.6, tag='?'),
     P('n3', 'cloud', 780, 430, 64, '0c#mucho+0.8', color='muted', alpha=.6, tag='?')]
cm = [dict(at='0b', x=50, y=50, z=2.6), dict(at='0b#lejos', x=50, y=50, z=1, dur=1.6)]
cues.append(K('0b', '0d', n, [], fs=1.0, cam=cm))

# ---- 0d — parallax with a finger
HX, HY = 480, 230
jump = lambda t0, dx, n_=3, step=1.1, off=0: [dict(at=f'{t0}+{off + step * j:.1f}', x=HX - 40 + (dx if j % 2 == 0 else -dx), y=HY - 40, dur=.25) for j in range(n_)]
n = [field('bg', 90, 200, 0, 560, 560, '0d', seed=11, until='0e'),
     P('hand', 'hand', HX, HY, 80, '0d#dedo', color='amber', until='0e',
       move=jump('0d#ojo', 70) + [dict(at='0d#lejos', x=HX - 40, y=HY - 120, dur=1)] + jump('0d#lejos', 18, 3, .8, 1.2)),
     P('eL', 'eye', 440, 450, 44, '0d#ojo', color='blue', until='0e', blink=.8, bf=3),
     P('eR', 'eye', 520, 450, 44, '0d#otro', color='blue', until='0e')]
cues.append(K('0d', '0e', n, [], fs=1.0))

# ---- 0e — parallax with the Earth's orbit
n = [P('sun', 'sun', 480, 380, 60, '0e'),
     D('orb', [dict(d=W._circ(50, 50, 46), sw=1, dash='3 4', so=.6)], 480, 380, 240, '0e', color='muted'),
     star('ea', 370, 380, '0e', s=14, color='blue', cap='enero', move=[dict(at='0e#medio', x=583, y=373, dur=1.6)]),
     star('nr', 450, 120, '0e#estrellas', s=12, color='amber', tag='cercana', move=[dict(at='0e#medio+0.2', x=514, y=114, dur=1.6)]),
     star('far', 760, 70, '0e#lejanas', s=8, color='amber', alpha=.7, tag='demasiado lejos', tagfs=12),
     DATE('d1900', 40, 30, '1900', '0e#1900')]
cues.append(K('0e', '0f', n, [], fs=1.0))

# ---- 0f — the woman who found the answer
n = [FOTO('por', 330, 50, 300, 380, 'retrato.jpg', 'Henrietta Leavitt, hacia 1910', '0f'),
     T('pay', 680, 210, '0,30 $ / hora', '0f#treinta', color=AMB, fs=22),
     P('pl', 'page', 720, 300, 60, '0f#placas', color='muted'),
     T('name', 330, 462, 'Henrietta Swan Leavitt', '0f#Henrietta', color=WHITE, fs=22)]
cues.append(K('0f', 'E0', n, [], fs=1.0))
