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
