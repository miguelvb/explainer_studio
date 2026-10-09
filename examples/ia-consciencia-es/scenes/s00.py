# Scene 0 · Intro
MUSIC = {'bells': 1, 'pad': 0.3}
INTENSITY = 0.35

# ---- shared helpers for this film (later scenes use them) ----
PIX = 24                      # Press Start 2P size of the typed letters (rendered at .6 of it)
GW = PIX * .6                 # width of one pixel-font glyph


def chip(id, cx, cy, at, s=70, color='blue', box=True, box_s=None, until=None, **k):
    """The model: a chip drawing, optionally inside its own small container."""
    out = []
    if box:
        bs = box_s or s * 1.7
        out.append(N(id + '_box', 'sandbox', cx - bs / 2, cy - bs / 2, bs, bs, at, color='teal', label='', until=until))
    out.append(W.pic(id, 'chip', cx - s / 2, cy - s / 2, s, s, at, color=color, until=until, **k))
    return out


def glow(id, cx, cy, at, s=40, color='amber', until=None, **k):
    """The inner glow: 'there is something it is like to be this'."""
    return W.pic(id, 'glow', cx - s / 2, cy - s / 2, s, s, at, color=color, until=until, **k)


def P(id, name, cx, cy, s, at, color='blue', **k):
    """Line drawing centred on (cx, cy)."""
    return W.pic(id, name, cx - s / 2, cy - s / 2, s, s, at, color=color, **k)


def person(id, cx, cy, at, color='blue', s=40, **k):
    return N(id, 'person', cx - s * .45, cy - s * .8, s * .9, s * 1.6, at, color=color, **k)


def puz(id, cx, cy, size, icon, at, color='blue', kind='puzzle', until=None, move=None, **k):
    """Puzzle piece (or its dark `hole`) of `size` px with its drawing inside the body of the piece, clear of the notch and the knobs.
    move = [dict(at, cx, cy, dur)] moves both parts together. Returns [piece, content] (ids `id` and `id`+'i')."""
    isz = size * .40
    out = []
    for nid, nm, x, y, w in ((id, kind, cx - size / 2, cy - size / 2, size), (id + 'i', icon, cx + .07 * size - isz / 2, cy + .11 * size - isz / 2, isz)):
        d = W.pic(nid, nm, x, y, w, w, at, color=color, until=until, **k)
        if move:
            off = (0, 0) if nid == id else (cx + .07 * size - isz / 2 - (cx - size / 2), cy + .11 * size - isz / 2 - (cy - size / 2))
            d['move'] = [dict(at=m['at'], x=round(m['cx'] - size / 2 + off[0]), y=round(m['cy'] - size / 2 + off[1]), dur=m.get('dur', 1.2)) for m in move]
        out.append(d)
    return out


def arrow(id, x1, y1, x2, y2, at, color='blue', sw=2.6, head=11, until=None, **k):
    """Straight line from (x1, y1) to (x2, y2) with an arrow head at the end (a free line drawing)."""
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2; S = max(abs(x2 - x1), abs(y2 - y1)) + 40; kk = S / 100
    L = lambda x, y: (round((x - cx) / kk + 50, 2), round((y - cy) / kk + 50, 2))
    a = math.atan2(y2 - y1, x2 - x1); (p1, p2) = L(x1, y1), L(x2, y2)
    h1 = L(x2 - head * math.cos(a - .45), y2 - head * math.sin(a - .45)); h2 = L(x2 - head * math.cos(a + .45), y2 - head * math.sin(a + .45))
    d = f'M{p1[0]} {p1[1]}L{p2[0]} {p2[1]}M{h1[0]} {h1[1]}L{p2[0]} {p2[1]}L{h2[0]} {h2[1]}'
    return N(id, 'svg', cx - S / 2, cy - S / 2, S, S, at, color=color, paths=[dict(d=d, sw=sw)], until=until, **k)


def noexp(prefix, cx, y, at, until=None, color=GRY):
    """The caption «sin experiencia / interna» in two lines, centred on cx."""
    out = []
    for j, t in enumerate(('sin experiencia', 'interna')):
        fs = 11; w = len(t) * fs * CW
        out.append(N(f'{prefix}{j}', 'txt', cx - w / 2, y + 14 * j, w + 4, fs + 4, at, color=color, fs=fs, text=t, until=until))
    return out


def wrap(text, cols):
    lines, cur = [], ''
    for w in text.split(' '):
        if cur and len(cur) + 1 + len(w) > cols: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w) if cur else w
    return lines + [cur]


def phrase_anchor(bid, text, i):
    """Anchor at character i of beat `bid` (a line start): the shortest run of words from i that is found first at i."""
    words = text[i:].split(' ')
    for k_ in range(1, len(words) + 1):
        ph = ' '.join(words[:k_]).rstrip('.,;:?!»')
        m = re.search(r'(^|[^A-Za-z0-9])' + re.escape(ph) + r'(?![A-Za-z0-9])', text, re.I)
        if m and m.start() + len(m.group(1)) == i: return f'{bid}#' + ph.replace(' ', '_')
    return bid


def typed_doc(prefix, beats, x, top, bottom, cols=46, cps=15, lh=27, pgap=14, until=None, color='#E7EBF1'):
    """Text typed letter by letter in Press Start 2P while the voice reads it; one paragraph per beat.
    beats = [(beat_id, text)]. Each paragraph pushes the earlier ones up when the page is full.
    Returns (nodes, end anchor of the last line)."""
    lay = []; y = 0
    for bid, text in beats:
        ls = wrap(text, cols); pos = 0; par = []
        for ln in ls:
            i = text.index(ln, pos); pos = i + len(ln)
            par.append((ln, y, bid if i == 0 else phrase_anchor(bid, text, i)))
            y += lh
        lay.append((bid, par, y)); y += pgap
    vis = bottom - top
    offs = [max(0, yb - vis) for _, _, yb in lay]           # scroll offset while paragraph j is written
    nodes = []; n_ = 0
    for j, (bid, par, _) in enumerate(lay):
        for ln, yy, anc in par:
            nd = N(f'{prefix}{n_}', 'txt', x, top + yy - offs[j], len(ln) * GW + 10, lh, anc, color=color, fs=PIX, type=cps, text=ln, font='pixel')
            mv = []; last = offs[j]; gone = None
            for jj in range(j + 1, len(lay)):
                if offs[jj] != last:
                    ny = top + yy - offs[jj]
                    if ny < top - 4: gone = lay[jj][0]; break
                    mv.append(dict(at=lay[jj][0] + '+0.6', x=x, y=ny, dur=0.6)); last = offs[jj]
            if mv: nd['move'] = mv
            u = gone or until
            if u: nd['until'] = u
            nodes.append(nd); n_ += 1
    return nodes


# 0a — title seal: the title is typed, the voice reads it
cues = [dict(a='seal', at='S0', until='E0', ext=0, p=dict(text='¿Hay alguien ahí dentro?', sub='Arkinos @ oct 2026', at=0.5, type=14, scale=1.0, cy=215, ty=392), bg=True, fade=[0.8, 2.0])]
