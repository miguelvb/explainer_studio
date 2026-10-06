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

def agent_named(id, x, y, name, at=0.05, w=170, h=240, color='blue', fs=14, blink=0.28, **k):
    return _n(id, 'acard', x, y, w, h, at, color=color, label=name, fs=fs, blink=blink, bf=4, **k)

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

def clock(id, x, y, start, at=0.2, fs=24, cps=22, run=None, **k):
    """start=(y,m,d,h,mi). run=dict(at, dur, to=(y,m,d,h,mi)) makes the time advance."""
    y_, m_, d_, h_, mi_ = start; c = dict(y=y_, m=m_, d=d_, h=h_, mi=mi_)
    if run: ty, tm, td, th, tmi = run['to']; c.update(at=run['at'], dur=run['dur'], to=dict(y=ty, m=tm, d=td, h=th, mi=tmi))
    else: c.update(at=0, dur=1, to=dict(c))
    return _n(id, 'txt', x, y, 400, fs + 8, at, color='teal', fs=fs, type=cps, clock=c, **k)

def link(a, b, at=0.05, color='blue', **k):
    d = dict(a=a, b=b, at=at, color=color); d.update(k); return d

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
