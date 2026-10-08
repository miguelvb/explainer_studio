# Scene 4 · La hipótesis: el significado tiene forma
MUSIC = {'pad': 0.8, 'cinema': 0.4}
INTENSITY = 0.45
cues = []
import random as _r


def tower(prefix, cx, base, at, floors=5, w=300, fh=46, gap=18, step=0.25, color='blue', until=None, dots=True):
    """The layered 'building': stacked flat planes; lower floors have many small points, upper floors fewer, bigger ones.
    Returns (nodes, [y centre of each floor])."""
    out, ys = [], []
    rng = _r.Random(7)
    for f in range(floors):
        y = base - (f + 1) * fh - f * gap; ys.append(y + fh / 2)
        t = at if isinstance(at, (int, float)) else f'{at}+{step * f:.2f}'
        out.append(N(f'{prefix}f{f}', 'sandbox', cx - w / 2, y, w, fh, t, color=color, label='', rx=6, bg='rgba(124,151,255,.06)', until=until))
        if dots:
            k = [14, 9, 6, 4, 3][min(f, 4)]; s = [6, 8, 10, 12, 14][min(f, 4)]
            for j in range(k):
                x = cx - w / 2 + 18 + (w - 36) * (j + .5) / k + rng.uniform(-6, 6)
                out.append(P(f'{prefix}d{f}_{j}', 'dot', x, y + fh / 2 + rng.uniform(-8, 8), s, t, color=['teal', 'blue', 'amber'][(j + f) % 3], alpha=.85, until=until))
    return out, ys


# 4a — a working hypothesis: Arkinos' small seal in the corner; the idea star (house icon for an idea) with a question mark
cues.append(dict(a='seal', at='4a', until='4b', p=dict(text='', small=True, at=0.2), bg=False))
n = [ic('id', 'ideaSpark', 470, 270, 110, '4a#hipótesis', color=AMB, blink=.65, bf=7, bat='4a#hipótesis+0.4'),
     N('qh', 'question', 535, 170, 46, 46, '4a#hipótesis+0.6', color='amber')]
cues.append(K('4a', '4b', n, [], fs=1.0))

# 4b — every word becomes a point in a space of thousands of dimensions: a slowly drifting constellation
rng = _r.Random(3)
PTS = []
while len(PTS) < 70:
    x, y = rng.uniform(60, 900), rng.uniform(50, 490)
    if all((x - a) ** 2 + (y - b) ** 2 > 38 ** 2 for a, b in PTS): PTS.append((x, y))
n = []
for i, (x, y) in enumerate(PTS):
    dx, dy = rng.uniform(-14, 14), rng.uniform(-10, 10)
    n.append(P(f'c{i}', 'dot', x, y, 9, f'4b#punto+{0.03 * i:.2f}', color=['blue', 'teal'][i % 2], alpha=.8,
               move=[dict(at='4b#dimensiones+6', x=round(x - 4.5 + dx), y=round(y - 4.5 + dy), dur=7), dict(at='4d', x=round(x - 4.5), y=round(y - 4.5), dur=7)]))
# 4c — similar words sit close: a cluster of animals, another of fruits
for j, (nm, x, y) in enumerate([('dog', 170, 150), ('cat', 235, 115), ('horse', 245, 190)]):
    n.append(P(f'an{j}', nm, x, y, 50, f'4c#parecidas+{0.3 * j:.1f}', color='teal', until='4d'))
for j, (nm, x, y) in enumerate([('apple', 700, 380), ('pear', 765, 345), ('grape', 770, 420)]):
    n.append(P(f'fr{j}', nm, x, y, 46, f'4c#cerca+{0.3 * j:.1f}', color='amber', until='4d'))
n += [N('ca', 'sandbox', 125, 75, 165, 160, '4c#parecidas', color='teal', label='', open=True, until='4d'),
      N('cf', 'sandbox', 655, 305, 160, 160, '4c#cerca', color='amber', label='', open=True, until='4d')]
cues.append(K('4b', '4d', n, [], fs=1.0))

# 4d — relations become directions: man → woman is the same arrow as king → queen
n = [person('mn', 300, 380, '4d#hombre', color='blue', s=46, cap='hombre', capfs=12),
     person('wm', 620, 380, '4d#mujer', color='teal', s=46, cap='mujer', capfs=12),
     person('kg', 300, 200, '4d#rey', color='blue', s=46, cap='rey', capfs=12),
     person('qn', 620, 200, '4d#reina', color='teal', s=46, cap='reina', capfs=12),
     P('k1', 'crown', 300, 140, 34, '4d#rey', color='amber'), P('k2', 'crown', 620, 140, 34, '4d#reina', color='amber')]
lk = [link('mn', 'wm', '4d#reina+0.4', color='amber', speed=.35, comm=True), link('kg', 'qn', '4d#reina+0.4', color='amber', speed=.35, comm=True)]
cues.append(K('4d', '4e', n, lk, fs=1.0))

# 4e — "embedding": the whole constellation lights up for a moment
n = [P(f'e{i}', 'dot', x, y, 9, 0.05, color=['blue', 'teal'][i % 2], alpha=.8) for i, (x, y) in enumerate(PTS)]
n += [P(f'el{i}', 'dot', x - 3, y - 3, 13, '4e#geometría', color=['teal', 'blue', 'amber'][i % 3], until='4e#geometría+1.8') for i, (x, y) in enumerate(PTS)]
n += [T('emb', 40, 36, 'embedding', '4e#embedding', color=TEAL, fs=22)]
cues.append(K('4e', '4f', n, [], fs=1.0))

# 4f — not one layer but many, stacked like the floors of a building
TX, TB = 330, 500
tw, TY = tower('t', TX, TB, '4f#capa', step=0.5)
n = list(tw)
# 4g — a ball climbs floor by floor
n.append(P('ball', 'dot', TX - 9, TY[0] - 9, 18, '4g', color='amber',
           move=[dict(at=f'4g#{w_}', x=TX - 9, y=round(TY[k_] - 9), dur=0.8) for k_, w_ in ((1, 'siguientes'), (2, 'categorías'), (3, 'profundas'), (4, 'causas'))], until='4h'))
# 4h — the building shines from bottom to top
for f in range(5):
    n.append(N(f'hl{f}', 'sandbox', TX - 150, TY[f] - 23, 300, 46, f'4h#comprender-{2.2 - 0.45 * f:.2f}', color='amber', label='', rx=6, bg='rgba(246,185,76,.10)'))
# 4i — next to it, a brain whose layers light up in the same pattern
n.append(P('br', 'brain', 720, 300, 220, '4i#cerebro', color='amber'))
for f, pts in enumerate([[(672, 360), (700, 372), (742, 372), (770, 360)], [(660, 320), (700, 330), (740, 330), (780, 320)], [(675, 280), (765, 280)], [(720, 250)]]):
    for j, (x, y) in enumerate(pts):
        n.append(P(f'bl{f}_{j}', 'dot', x, y, 8 + 3 * f, f'4i#parecido+{0.4 * f:.1f}', color='amber'))
cues.append(K('4f', 'E4', n, [], fs=1.0))
