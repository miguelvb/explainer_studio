"""Reusable presets for the `world` asset (graphic-novel scenes). Each function returns plain node / link dicts
that go into a world cue's p.nodes / p.links. Canvas is 960x540. Times are numbers or anchors ("0c#atacando+1.2").

  agent_named  - OpenAI-icon agent in a portrait card, real name under the icon
  agent        - small agent (icon in a circle) inside its own rounded box
  agent_group  - a wide container, open at the top, filled with rows of small agents that fade out upward ("very many")
  hugging_face - the Hugging Face structure (rack tower with logo header) + holes where attacks land
  counter      - big white number that counts up, small caption below
  clock        - typewriter UTC date/time that can run forward ("08-07-2026 -- 23:00 UTC")
"""

def _n(id, kind, x, y, w, h, at=0.05, **k):
    d = dict(id=id, kind=kind, x=round(x), y=round(y), w=round(w), h=round(h), at=at)
    d.update({a: b for a, b in k.items() if b is not None}); return d

def agent_named(id, x, y, name, at=0.05, w=170, h=240, color='blue', fs=14, blink=0.28, bf=4, **k):
    return _n(id, 'acard', x, y, w, h, at, color=color, label=name, fs=fs, blink=blink, bf=bf, **k)

def agent(id, cx, cy, at=0.05, s=46, color='blue', box=True, box_s=None, box_color='teal', **k):
    out = []
    if box: bs = box_s or s * 2; out.append(_n(f'{id}_box', 'sandbox', cx - bs / 2, cy - bs / 2, bs, bs, at, color=box_color, label='', **k))
    out.append(_n(id, 'agent', cx - s / 2, cy - s / 2, s, s, at, color=color, **k)); return out

def agent_group(prefix, x=40, w=460, cols=12, rows=15, pitch=36, y_bottom=452, at=0.05, until=None, box_s=32, icon_s=16,
                fade_from=-10, fade_len=170, blink=0.45, gap=None, gap_at=None, color='blue', box_color='teal', container_color='red', top=-120, bottom=490, appear=None):
    """container open at the top; rows grow upward and fade. gap=[y1,y2] opens a hole in the right wall at gap_at (swaps the container)."""
    n = []; H = bottom - top
    if gap and gap_at is not None:
        n += [_n(f'{prefix}_wall', 'sandbox', x, top, w, H, at, color=container_color, open=True, label='', notop=True, until=gap_at),
              _n(f'{prefix}_wallgap', 'sandbox', x, top, w, H, gap_at, color=container_color, open=True, label='', notop=True, gap=gap, until=until)]
    else:
        n.append(_n(f'{prefix}_wall', 'sandbox', x, top, w, H, at, color=container_color, open=True, label='', notop=True, gap=gap, until=until))
    x0 = x + 30
    for i in range(cols * rows):
        cx = x0 + pitch * (i % cols); cy = y_bottom - pitch * (i // cols)
        a = max(0.0, min(1.0, (cy + fade_from) / fade_len)); t = appear(i) if appear else at
        n.append(_n(f'{prefix}_b{i}', 'sandbox', cx - box_s / 2, cy - box_s / 2, box_s, box_s, t, color=box_color, label='', alpha=a, blink=blink, bf=3 + (i % 5) * .6, until=until))
        n.append(_n(f'{prefix}_a{i}', 'agent', cx - icon_s / 2, cy - icon_s / 2, icon_s, icon_s, t, color=color, alpha=a, blink=blink, bf=3 + (i % 5) * .6, until=until))
    return n

def hugging_face(id='hf', x=650, y=135, w=250, h=320, at=0.05, holes=(), hole_size=22, label='Hugging Face', blink=.12, **k):
    """holes: [(cx, cy, at)] absolute canvas points; add links to f'{id}_h{j}' to make the attacks land there."""
    n = [_n(id, 'hfbase', x, y, w, h, at, color='amber', label=label, fs=17, blink=blink, bf=3, **k)]
    for j, (cx, cy, t) in enumerate(holes): n.append(_n(f'{id}_h{j}', 'hole', cx - hole_size / 2, cy - hole_size / 2, hole_size, hole_size, t, color='red'))
    return n

def counter(id, x, y, n, at=0.05, cap='', w=240, h=50, fs=54, dur=3, **k):
    return _n(id, 'num', x, y, w, h, at, n=n, color='#E7EBF1', fs=fs, dur=dur, cap=cap or None, capc='muted', capfs=14, **k)

def clock(id, x, y, start, at=0.2, fs=24, cps=9, run=None, **k):
    """start=(y,m,d,h,mi). run=dict(at, dur, to=(y,m,d,h,mi)) makes the time advance."""
    y_, m_, d_, h_, mi_ = start; c = dict(y=y_, m=m_, d=d_, h=h_, mi=mi_)
    if run: ty, tm, td, th, tmi = run['to']; c.update(at=run['at'], dur=run['dur'], to=dict(y=ty, m=tm, d=td, h=th, mi=tmi))
    else: c.update(at=0, dur=1, to=dict(c))
    return _n(id, 'txt', x, y, 400, fs + 8, at, color='teal', fs=fs, type=cps, clock=c, **k)

def link(a, b, at=0.05, color='blue', **k):
    d = dict(a=a, b=b, at=at, color=color); d.update(k); return d

def msg_feed(id, x, y, label='Artifactory', w=420, h=400, at=0.05, r0=2.0, r1=None, ramp=4.0, mix=None, seed=0, off=0, color='amber', **k):
    """Window with a scrolling stream of coloured message names (zzASK blue, zzANSWER teal, zzINFO amber, zzFILE green, zzSOLVED red).
    r0/r1 = lines per second at start/after `ramp` seconds; mix={ask,ans,info,file,flag} weights; off = lines already scrolled (so a swap does not start empty)."""
    return _n(id, 'msgfeed', x, y, w, h, at, color=color, label=label, r0=r0, r1=r1 or r0, ramp=ramp, mix=mix, seed=seed, off=off, **k)

def bulb(id, cx, cy, at=0.05, lit=None, s=56, color='amber', **k):
    """Idea light bulb: outline appears at `at`, lights up (glow + rays) at `lit` (default at+0.4)."""
    return _n(id, 'bulb', cx - s / 2, cy - s / 2, s, s, at, color=color, litAt=lit, **k)

def sheet(id, x, y, w, h, lines, at=0.05, fs=18, color='muted', **k):
    """A sheet of paper with centred lines of 'formula' text."""
    return _n(id, 'sheet', x, y, w, h, at, color=color, lines=lines, fs=fs, **k)

def article(id, x, y, w, h, title, at=0.05, read=None, fs=8, color='blue', litc='teal', seed=3, **k):
    """A page of tiny illegible words under a title. read=dict(at, dur) lights the words one after another, as if being read."""
    return _n(id, 'article', x, y, w, h, at, color=color, title=title, read=read, fs=fs, litc=litc, seed=seed, **k)

def judge(id, x, y, name, at=0.05, name_at=None, w=160, h=190, color='teal', fs=14, **k):
    """Agent-shaped card whose icon is a magnifier with a question mark. The name slot is an empty dashed box until name_at."""
    return _n(id, 'judge', x, y, w, h, at, color=color, label=name, nameAt=name_at, fs=fs, **k)

CODE = """$ python solve.py
import os, sys, zlib
def parse(buf):
    out = []
    for i in range(len(buf)):
        if buf[i] == 0x1f:
            out.append(buf[i+1:i+9])
    return out
data = open('target.bin','rb').read()
for chunk in parse(data):
    print(zlib.crc32(chunk))
$ gcc -o fuzz fuzz.c -O2
$ ./fuzz target.bin
crash: heap overflow at 0x55d2
def retry(n):
    for k in range(n):
        r = run('./fuzz', seed=k)
        if r.crashed: return r
$ python solve.py --seed 7
import struct, itertools
def pack(v):
    return struct.pack('<I', v)
for a, b in itertools.product(range(4), range(4)):
    buf = pack(a) + pack(b)
    test(buf)
$ make && ./run_tests
ok: 41 passed, 3 failed
""" * 4

def console(id, x, y, w=230, h=210, at=0.05, code=CODE, k=6, a=6, color='teal', **kw):
    """Small terminal: program text is typed faster and faster and scrolls when full."""
    return _n(id, 'console', x, y, w, h, at, color=color, code=code, k=k, a=a, **kw)

def sandbox_onion(id, cx, cy, size=90, at=0.05, layers=4, color='teal', **kw):
    """Concentric walls around a point: an impenetrable sandbox seen up close."""
    return _n(id, 'onion', cx - size / 2, cy - size / 2, size, size, at, color=color, layers=layers, **kw)

def folder_view(id, x, y, items, label='Artifactory', w=420, h=400, at=0.05, color='amber', **kw):
    """File-browser window. items=[{name, dir:bool, color?, at?, c2? (second colour), altAt? (start flashing between both)}]."""
    return _n(id, 'folderview', x, y, w, h, at, color=color, label=label, items=items, **kw)


# ---- link semantics ---------------------------------------------------------
# A link is either COMMUNICATION (information travels: curved S-shaped path with balls,
# routed around other nodes) or a RELATION (belongs to / is part of / is held by / sequence:
# a straight, continuous segment, no balls).  Authors may set rel=True or comm=True on a link;
# otherwise these rules decide.
REL_KINDS = {'chip', 'key', 'person', 'exam'}
REL_PAIRS = {('sandbox', 'sheet')}

def classify_links(story):
    for sc in story.get('scenes', []):
        for c in sc.get('cues', []):
            p = c.get('p') or {}
            kinds = {n['id']: n.get('kind') for n in p.get('nodes', [])}
            for l in p.get('links', []) or []:
                if l.get('orth') or l.get('comm') or 'rel' in l:
                    l.pop('comm', None); continue
                ka, kb = kinds.get(l['a']), kinds.get(l['b'])
                if l.get('lock'):
                    continue
                if l.get('dashed') or ka in REL_KINDS or kb in REL_KINDS or (ka, kb) in REL_PAIRS:
                    l['rel'] = True
    return story


# ---- line drawings (node kind `svg`) -----------------------------------------
# Each picture is a list of paths in a 100x100 box: {d, f (fill: 1 = node colour, or a colour), fo, s (stroke colour, 0 = none), so, sw}.
def _circ(cx, cy, r): return f'M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z'

PICS = {
    'chip': [dict(d='M26 22h48q4 0 4 4v48q0 4-4 4h-48q-4 0-4-4v-48q0-4 4-4Z', f='#171D26'),
             dict(d='M38 38h24v24h-24Z', sw=1.8, so=.8),
             dict(d='M34 22v-10M50 22v-10M66 22v-10M34 78v10M50 78v10M66 78v10M22 34h-10M22 50h-10M22 66h-10M78 34h10M78 50h10M78 66h10', sw=2)],
    'glow': [dict(d=_circ(50, 50, 46), f=1, fo=.10, s=0), dict(d=_circ(50, 50, 30), f=1, fo=.22, s=0),
             dict(d=_circ(50, 50, 17), f=1, fo=.55, s=0), dict(d=_circ(50, 50, 8), f='#FFFFFF', fo=.9, s=0)],
    'dot': [dict(d=_circ(50, 50, 40), f=1, s=0)],
    'bat': [dict(d='M50 44q-4-8 0-12q4 4 0 12ZM50 44q-14-14-34-10q8 6 6 16q-12-4-20 2q18 2 26 12q8-14 22-20ZM50 44q14-14 34-10q-8 6-6 16q12-4 20 2q-18 2-26 12q-8-14-22-20Z', f=1, fo=.15),
            dict(d='M46 36l1-6M54 36l-1-6', sw=1.8)],
    'tree': [dict(d='M50 8l22 34h-10l16 24h-56l16-24h-10Z', f=1, fo=.08), dict(d='M50 66v26', sw=2.6)],
    'brain': [dict(d='M50 18q-10-8-20-2q-12 0-14 14q-10 8-4 22q-2 14 12 18q8 10 22 4q2 2 4 0V18Z M50 18q10-8 20-2q12 0 14 14q10 8 4 22q2 14-12 18q-8 10-22 4', f='#171D26'),
              dict(d='M50 18v56M30 34q8 0 10 8M24 54q10-2 14 6M70 34q-8 0-10 8M76 54q-10-2-14 6M38 24q2 6-2 10M62 24q-2 6 2 10', sw=1.8, so=.75)],
    'calc': [dict(d='M28 10h44q4 0 4 4v72q0 4-4 4h-44q-4 0-4-4v-72q0-4 4-4Z', f='#171D26'),
             dict(d='M33 18h34v16h-34Z', sw=1.8),
             dict(d='M36 46h6M47 46h6M58 46h6M36 58h6M47 58h6M58 58h6M36 70h6M47 70h6M58 70h6M36 80h28', sw=3.2)],
    'dog': [dict(d='M14 52q2-14 16-14h30l8-12q6-4 10 2l6 6q4 6-2 8l-8 2v10q0 8-8 8v16M30 38q-12 2-12 14v30M22 82h8M58 82h8M30 66h24M14 52q-8-4-8-12', f='#171D26'),
            dict(d='M80 32h0.5', sw=3.4)],
    'cat': [dict(d='M30 86q-8-30 8-44l-2-20l12 12h10l12-12l-2 20q16 14 8 44Z', f='#171D26'), dict(d='M42 52h0.5M58 52h0.5', sw=3.4), dict(d='M50 60v4M44 66q6 4 12 0', sw=1.8)],
    'horse': [dict(d='M18 84V56q0-12 12-14h28l14-20q2-6 8-4l8 10q2 4-4 6l-8 2v24M30 84V62M64 84V58M76 84V60', f='#171D26'), dict(d='M18 56q-10 4-8 20', sw=2), dict(d='M82 22h0.5', sw=3.4)],
    'apple': [dict(d='M50 30q-14-10-26 2q-10 14 0 34q10 22 26 12q16 10 26-12q10-20 0-34q-12-12-26-2Z', f=1, fo=.15), dict(d='M50 30q0-12 8-18', sw=2.4)],
    'pear': [dict(d='M50 24q-8 0-8 14q0 8-10 18q-8 14 4 26q14 10 28 0q12-12 4-26q-10-10-10-18q0-14-8-14Z', f=1, fo=.15), dict(d='M50 24q2-8 8-12', sw=2.4)],
    'grape': [dict(d=''.join(_circ(x, y, 8) for x, y in [(38, 34), (54, 34), (46, 48), (62, 48), (30, 48), (38, 62), (54, 62), (46, 76)]), f=1, fo=.15), dict(d='M48 26q2-10 10-14', sw=2.4)],
    'crown': [dict(d='M18 70l-4-40l18 18l18-28l18 28l18-18l-4 40Z', f=1, fo=.15), dict(d='M18 80h64', sw=3)],
    'book': [dict(d='M50 28q-16-10-38-6v54q22-4 38 6q16-10 38-6v-54q-22-4-38 6Z', f='#171D26'), dict(d='M50 28v54', sw=1.8),
             dict(d='M20 38q12-2 22 3M20 50q12-2 22 3M20 62q12-2 22 3M58 41q10-5 22-3M58 53q10-5 22-3M58 65q10-5 22-3', sw=1.4, so=.6)],
    'page': [dict(d='M24 10h38l14 14v66h-52Z', f='#171D26'), dict(d='M62 10v14h14', sw=1.6), dict(d='M32 40h36M32 52h36M32 64h36M32 76h22', sw=1.6, so=.7)],
    'robot': [dict(d='M28 34h44q6 0 6 6v32q0 6-6 6h-44q-6 0-6-6v-32q0-6 6-6Z', f='#171D26'), dict(d='M50 34v-14', sw=2), dict(d=_circ(50, 16, 5), f=1, fo=.6),
              dict(d=_circ(38, 52, 6) + _circ(62, 52, 6), f=1, fo=.9), dict(d='M38 68h24', sw=2), dict(d='M22 52h-8M78 52h8', sw=3)],
    'hand': [dict(d='M30 90V54q0-6 6-6V22q0-6 6-6t6 6v24V14q0-6 6-6t6 6v32V20q0-6 6-6t6 6v36q4-10 10-8q4 2 0 10l-12 26q-4 12-14 12h-16q-10 0-12-4Z', f='#171D26')],
    'lid': [dict(d='M6 36h88q4 0 4 4v14q0 4-4 4h-88q-4 0-4-4v-14q0-4 4-4Z', f=1, fo=.18), dict(d='M40 36v-10h20v10', sw=2.4)],
    'puzzle': [dict(d='M20 30h20q-4-14 10-14t10 14h20v20q14-4 14 10t-14 10v20h-60v-20q14 4 14-10t-14-10Z', f=1, fo=.12)],
    'hole': [dict(d='M20 30h20q-4-14 10-14t10 14h20v20q14-4 14 10t-14 10v20h-60v-20q14 4 14-10t-14-10Z', f='#07090D', sw=1.8, so=.8)],
    'arrows': [dict(d='M50 50V14M50 50V86M50 50H14M50 50H86M42 22l8-8l8 8M42 78l8 8l8-8M22 42l-8 8l8 8M78 42l8 8l-8 8', sw=2.6)],
    'loop': [dict(d='M72 30a28 28 0 1 0 6 26', sw=3), dict(d='M80 16l-6 16l-16-4', sw=3)],
    'mirror': [dict(d='M50 10q22 0 22 30t-22 30q-22 0-22-30t22-30Z', f=1, fo=.1), dict(d='M50 70v20M38 90h24', sw=3), dict(d='M40 26q-4 8-2 18', sw=2, so=.6)],
    'knob': [dict(d=_circ(50, 50, 30), f='#171D26'), dict(d='M50 50V24', sw=4), dict(d='M14 76l-4 4M86 76l4 4M50 8v-4M20 26l-3-3M80 26l3-3', sw=2, so=.6)],
    'fence': [dict(d='M14 88V34l6-8l6 8v54M44 88V34l6-8l6 8v54M74 88V34l6-8l6 8v54M8 48h84M8 72h84', sw=2.4)],
    'syringe': [dict(d='M30 70l40-40l10 10l-40 40Z', f='#171D26'), dict(d='M30 70l-14 14M75 25l8-8M80 12l8 8M44 64l6 6M52 56l6 6M60 48l6 6', sw=2.4)],
    'lever': [dict(d='M18 82h64', sw=3), dict(d='M30 82v-8h40v8', sw=2.4), dict(d='M50 74L50 22', sw=3.2), dict(d=_circ(50, 18, 7), f=1, fo=.3)],
    'leverdown': [dict(d='M18 82h64', sw=3), dict(d='M30 82v-8h40v8', sw=2.4), dict(d='M50 74L82 56', sw=3.2), dict(d=_circ(86, 54, 7), f=1, fo=.3)],
    'mouse': [dict(d='M14 70q0-26 30-26q26 0 34 22q2 6-4 6h-58q-2 0-2-2Z', f='#171D26'), dict(d=_circ(34, 44, 8), f='#171D26'), dict(d='M76 66q14 2 14 14q0 8-10 8', sw=2), dict(d='M22 58h0.5', sw=3.4)],
    'fish': [dict(d='M12 50q20-26 50-8l20-14v44l-20-14q-30 18-50-8Z', f=1, fo=.12), dict(d='M26 46h0.5', sw=3.6), dict(d='M44 38q6 12 0 24', sw=1.6, so=.6)],
    'star': [dict(d='M50 10l11 25l27 3l-20 18l6 27l-24-14l-24 14l6-27l-20-18l27-3Z', f=1, fo=.25)],
    'bump': [dict(d='M10 74q14-34 40-34t40 34Z', f=1, fo=.15)],
    'heart': [dict(d='M50 84q-36-24-36-46q0-18 18-18q12 0 18 12q6-12 18-12q18 0 18 18q0 22-36 46Z', f=1, fo=.18)],
    'cell': [dict(d='M50 12q34 0 36 34q2 36-34 40q-36 2-38-36q-2-36 36-38Z', f=1, fo=.1), dict(d=_circ(46, 48, 13), f=1, fo=.3), dict(d='M28 26h0.5M70 30h0.5M72 70h0.5M30 70h0.5', sw=3)],
    'lungs': [dict(d='M46 30q-20-6-30 22q-6 22 6 30q10 4 24-6Z', f=1, fo=.12), dict(d='M54 30q20-6 30 22q6 22-6 30q-10 4-24-6Z', f=1, fo=.12), dict(d='M50 10v30M46 40l4-4l4 4', sw=2.4)],
    'parrot': [dict(d='M40 24q8-14 22-10q10 4 8 14q-2 6-8 6q4 10-2 24q-6 16-18 28l-8 10l2-14q-12-12-6-30q4-16 10-28Z', f='#171D26'),
               dict(d='M70 28q8 2 6 12q-4-4-8-4', f=1, fo=.4), dict(d='M58 24h0.5', sw=3.6), dict(d='M38 52q8 6 14 0M36 62q8 6 14 0', sw=1.6, so=.7)],
    'eye': [dict(d='M8 50q42-46 84 0q-42 46-84 0Z', f='#171D26'), dict(d=_circ(50, 50, 12), f=1)],
    'plank': [dict(d='M10 40h80v20h-80Z', f=1, fo=.15), dict(d='M30 40v20M70 40v20', sw=1.6, so=.6)],
    'target': [dict(d=_circ(50, 50, 38) + _circ(50, 50, 24), f=0), dict(d=_circ(50, 50, 10), f=1)],
    'phone': [dict(d='M32 8h36q6 0 6 6v72q0 6-6 6h-36q-6 0-6-6v-72q0-6 6-6Z', f='#171D26'), dict(d='M44 16h12M46 84h8', sw=2.4)],
    'elevator': [dict(d='M18 10h64v80h-64Z', f='#171D26'), dict(d='M50 22v68', sw=2), dict(d='M44 16l6-4l6 4', sw=1.8, so=.7)],
    'sun': [dict(d=_circ(50, 50, 18), f=1, fo=.4), dict(d='M50 10v12M50 78v12M10 50h12M78 50h12M22 22l8 8M70 70l8 8M22 78l8-8M70 30l8-8', sw=2.6)],
    'moon': [dict(d='M64 14q-28 4-28 36t28 36q-40 8-48-36q8-44 48-36Z', f=1, fo=.25)],
    'bee': [dict(d='M26 56q0-18 24-18t24 18q0 18-24 18t-24-18Z', f=1, fo=.15), dict(d='M42 40v32M56 40v32', sw=2.6), dict(d='M40 38q-14-20-24-10q-4 12 22 12M60 38q14-20 24-10q4 12-22 12', sw=1.8, so=.8), dict(d='M74 56h8', sw=2)],
    'octopus': [dict(d='M26 50q0-34 24-34t24 34Z', f=1, fo=.15), dict(d='M30 50q-8 20-18 22M40 50q-2 22-10 32M50 50v34M60 50q2 22 10 32M70 50q8 20 18 22', sw=2.4), dict(d='M42 36h0.5M58 36h0.5', sw=3.6)],
    'crow': [dict(d='M18 60q8-24 32-24l10-10q10-4 14 4l14 4l-14 6q4 24-20 34l-14 4l-26 6l14-14q-12 0-10-10Z', f='#171D26'), dict(d='M70 30h0.5', sw=3.6), dict(d='M44 84v8M54 82v8', sw=2)],
    'cloud': [dict(d='M24 70q-16 0-16-14t16-14q2-18 20-18q14 0 20 12q20-4 24 14q12 2 12 12q0 8-12 8Z', f=1, fo=.1)],
    'umbrella': [dict(d='M8 48q42-50 84 0q-7-6-14 0q-7-6-14 0q-7-6-14 0q-7-6-14 0q-7-6-14 0q-7-6-14 0Z', f=1, fo=.18), dict(d='M50 48v34q0 8 8 8t8-8', sw=2.6), dict(d='M50 8v4', sw=2.6)],
    'umbrellac': [dict(d='M50 14l10 52h-20Z', f=1, fo=.18), dict(d='M50 66v16q0 8 8 8t8-8', sw=2.6)],
    'shield': [dict(d='M50 6l36 12v26q0 30-36 50q-36-20-36-50v-26Z', f=1, fo=.08)],
    'factory': [dict(d='M8 88V48l20-12v12l20-12v12l20-12v12h24v40Z', f='#171D26'), dict(d='M74 48V14h12v34', sw=2.2)],
    'hen': [dict(d='M30 70q-16-6-14-26q20-2 30 6q2-18 18-18q8 0 8 10l8 2l-8 4q4 16-8 24q-12 8-34-2Z', f='#171D26'), dict(d='M62 22q2-8 8-6M44 72v14M54 72v14', sw=2), dict(d='M70 32h0.5', sw=3.4)],
    'gear': [dict(d=_circ(50, 50, 26), f='#171D26'), dict(d=_circ(50, 50, 10)), dict(d='M50 10v14M50 76v14M10 50h14M76 50h14M22 22l10 10M68 68l10 10M22 78l10-10M68 32l10-10', sw=6)],
    'window': [dict(d='M10 18h80v64h-80Z', f='#171D26'), dict(d='M10 32h80', sw=1.6, so=.7), dict(d='M80 22l6 6M86 22l-6 6', sw=1.6), dict(d='M20 46h50M20 58h40M20 70h46', sw=1.6, so=.5)],
    'waves': [dict(d='M20 30q14 20 0 40M34 22q22 28 0 56M48 14q30 36 0 72', sw=2.4)],
    'server': [dict(d='M18 14h64v22h-64ZM18 40h64v22h-64ZM18 66h64v22h-64Z', f='#171D26'), dict(d='M28 25h0.5M28 51h0.5M28 77h0.5', sw=4), dict(d='M44 25h28M44 51h28M44 77h28', sw=1.6, so=.6)],
    'board8': [dict(d='M6 6h88v88h-88Z', f='#10151C'),
               dict(d=''.join(f'M{6 + 11 * i} 6v88' for i in range(1, 8)) + ''.join(f'M6 {6 + 11 * i}h88' for i in range(1, 8)), sw=1, so=.45)],
    'stone': [dict(d=_circ(50, 50, 40), f=1, s=0)],
    'knob2': [dict(d=_circ(50, 50, 30), f='#171D26'), dict(d='M50 50H76', sw=4), dict(d='M14 76l-4 4M86 76l4 4M50 8v-4M20 26l-3-3M80 26l3-3', sw=2, so=.6)],
    'soft': [dict(d='M50 18q30 0 30 32t-30 32q-30 0-30-32t30-32Z', f=1, fo=.25)],
    'sharp': [dict(d='M50 8l10 26l28-8l-16 24l18 22l-28-2l-12 26l-12-26l-28 2l18-22l-16-24l28 8Z', f=1, fo=.25)],
    'face': [dict(d=_circ(50, 50, 36), f='#171D26'), dict(d='M38 42h0.5M62 42h0.5', sw=4), dict(d='M34 58q16 16 32 0', sw=2.6)],
    'notes': [dict(d='M16 30h52v58h-52Z', f='#171D26'), dict(d='M24 22h52v58', sw=1.8, so=.8), dict(d='M32 14h52v58', sw=1.6, so=.6), dict(d='M24 46h36M24 58h36M24 70h24', sw=1.6, so=.7)],
}


def pic(id, name, x, y, w, h=None, at=0.05, color='blue', **k):
    """A line drawing from PICS (node kind `svg`), drawn inside the (x, y, w, h) box with uniform scale."""
    h = w if h is None else h
    k.setdefault('paths', PICS[name])
    return _n(id, 'svg', x, y, w, h, at, color=color, **k)
