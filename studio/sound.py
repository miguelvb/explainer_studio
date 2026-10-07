"""Sound design: music styles (event-based synthesis), room ambience and sound effects driven by the cues.

Everything is synthesised with numpy/scipy, so nothing is downloaded and nothing is licensed.
Styles: pad (the original), pulse, cinema, bells, data.  All follow two curves taken from the story:
  intensity (0-1, per scene `intensity`, default arc)  and  tension (scene `mood: "tense"`).
"""
import json, wave
import numpy as np
from scipy import signal

SR = 44100
STYLES = ('pad', 'pulse', 'cinema', 'bells', 'data')
hz = lambda m: 440.0 * 2 ** ((np.asarray(m, dtype=np.float64) - 69) / 12)


# ------------------------------------------------------------------ curves
def curve_data(st, S, total):
    N = len(st['scenes'])
    ints = [sc.get('intensity') for sc in st['scenes']]
    arc = [.3 + .7 * (1 - abs(i / max(1, N - 1) - .7) / .7) if i / max(1, N - 1) <= .7 else 1 - (i / max(1, N - 1) - .7) / .3 * .6 for i in range(N)]
    ints = [x if x is not None else arc[i] for i, x in enumerate(ints)]
    mood = [1.0 if sc.get('mood') == 'tense' else 0.0 for sc in st['scenes']]
    keys = [(0, ints[0] * .8)] + [(S[f'S{i}']['s'] + 2, ints[i]) for i in range(N)] + [(total, 0)]
    mk = [(0, mood[0])] + [p for i in range(1, N) for p in ((S[f'S{i}']['s'], mood[i - 1]), (S[f'S{i}']['s'] + 3, mood[i]))] + [(total, mood[-1])]
    bounds = [(S[f'S{i}']['s'], ints[i], mood[i]) for i in range(N)]
    return keys, mk, bounds


def curves(root, D=None):
    D = D or json.load(open(f'{root}/build/data.json')); st = json.load(open(f'{root}/story.json'))
    total = D['total'] + 2; keys, mk, bounds = curve_data(st, D['sched'], total)
    return dict(total=total, keys=keys, mk=mk, bounds=bounds, meta=st['meta'])


def make_t(total):
    n = int(total * SR); return n, np.arange(n, dtype=np.float32) / SR


def interp(t, pts): return np.interp(t, [p[0] for p in pts], [p[1] for p in pts]).astype(np.float32)


# ------------------------------------------------------------------ dsp helpers
def lp(x, fc, order=2):
    fc = float(np.clip(fc, 30, SR / 2 - 500)); sos = signal.butter(order, fc, 'low', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def hp(x, fc, order=2):
    sos = signal.butter(order, float(fc), 'high', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def bp(x, f0, f1, order=2):
    sos = signal.butter(order, [float(f0), float(f1)], 'band', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def tt(d): return np.arange(int(d * SR), dtype=np.float32) / SR


def saw(f, d, ph=0.0):
    t = tt(d); return (2 * ((f * t + ph) % 1.0) - 1).astype(np.float32)


def adsr(d, a=.01, dec=.2, s=.0, r=.05):
    n = int(d * SR); t = np.arange(n, dtype=np.float32) / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(dec, 1e-4))); rr = np.clip((d - t) / max(r, 1e-4), 0, 1)
    return (e * rr).astype(np.float32)


def bell(f, d=2.5, bright=1.0, dec=1.4):
    t = tt(d); idx = 2.2 * bright * np.exp(-t * 3.0)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * dec) + .25 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * dec * 1.8)
    return (x * np.clip(t / .004, 0, 1)).astype(np.float32)


def put(buf, t0, x, g=1.0, pan=.5):
    i = int(t0 * SR)
    if i >= buf.shape[1] or i + len(x) <= 0: return
    a = max(0, -i); e = min(len(x), buf.shape[1] - i); gl = np.cos(pan * np.pi / 2) * g * 1.41; gr = np.sin(pan * np.pi / 2) * g * 1.41
    buf[0, i + a:i + e] += x[a:e] * gl; buf[1, i + a:i + e] += x[a:e] * gr


def reverb(buf, sec=3.0, wet=.35, seed=3, damp=3500):
    rng = np.random.default_rng(seed); n = int(sec * SR); t = np.arange(n) / SR
    ir = [lp((rng.standard_normal(n) * np.exp(-t * (6.9 / sec))).astype(np.float32), damp) for _ in range(2)]
    out = np.stack([signal.oaconvolve(buf[c], ir[c], mode='full')[:buf.shape[1]] for c in range(2)]).astype(np.float32)
    out *= wet / (np.abs(out).max() + 1e-9) * np.abs(buf).max() * 1.2; return buf * (1 - wet * .4) + out


# ------------------------------------------------------------------ progression
CH = [[38, 45, 50, 53, 57], [34, 41, 46, 50, 53], [31, 38, 43, 46, 50], [33, 40, 45, 49, 52]]   # Dm  Bb  Gm  A


def chord_at(t, L):
    return CH[int(t // L) % 4]


# ------------------------------------------------------------------ styles
def style_pulse(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32)
    bpm = 96; beat = 60 / bpm; L = beat * 8
    pat = [0, 2, 3, 2, 1, 2, 4, 2]
    k = 0; ti = 0.0
    while ti < total - 1:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        # pad swell per bar
        if abs(ti % L) < beat / 2:
            for nt in ch[:4]:
                d = L + 1; x = sum(saw(float(hz(nt)) * (1 + dt), d, rng.random()) for dt in (-.004, .004)) / 2
                put(buf, ti - .3, lp(x, 600 + 1400 * ii) * adsr(d, 1.8, 3, .8, 2.5), .05 * (.4 + .6 * ii), rng.random() * .6 + .2)
        # bass on each beat (pumping)
        if k % 2 == 0:
            f = float(hz(ch[0])); x = lp(saw(f, beat * 1.6), 300 + 600 * ii)
            put(buf, ti, x * adsr(beat * 1.6, .005, .35, .05, .1), .16 * (.35 + .65 * ii), .5)
        # soft kick above intensity .55
        if k % 4 == 0 and ii > .55:
            tk = tt(.35); kick = np.sin(2 * np.pi * (48 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 9)
            put(buf, ti, kick.astype(np.float32), .22 * (ii - .4), .5)
        # arpeggio, eighth notes
        if ii > .2 and (k % 1 == 0):
            nt = ch[1 + pat[k % 8] % 4] + 12 * (1 if (k // 8) % 2 else 0) + (1 if te > .5 and k % 8 == 5 else 0)
            f = float(hz(nt)); d = beat * .9
            x = lp(saw(f, d, rng.random()), 700 + 4200 * ii * (1 - .4 * te)) * adsr(d, .004, .13, .0, .05)
            put(buf, ti, x, .1 * (.25 + .75 * ii), .25 + .5 * ((k % 4) / 3))
        ti += beat / 2; k += 1
    return reverb(buf, 2.4, .28)


def style_cinema(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32); L = 16.0
    # continuous low drone
    drone = np.zeros(n, np.float32)
    for m, a in ((26, .5), (38, .3), (45, .16)):
        drone += np.sin(2 * np.pi * float(hz(m)) * t + rng.random() * 6) * a
    drone *= (.6 + .4 * np.sin(2 * np.pi * .05 * t)) * (.35 + .65 * inten) * .22
    buf[0] += drone; buf[1] += drone * .96
    ti = 0.0
    while ti < total - 2:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        for j, nt in enumerate(ch[1:]):
            d = L + 4; x = sum(saw(float(hz(nt + 12 * (j % 2))) * (1 + dt), d, rng.random()) for dt in (-.006, 0, .006)) / 3
            x = lp(x, 450 + 1800 * ii) * adsr(d, 5.0, 5, .85, 5.0)
            if te > .3: x = x * (1 - .35 * te) + .35 * te * lp(saw(float(hz(nt + 1)), d, rng.random()), 800) * adsr(d, 5, 5, .85, 5)
            put(buf, ti - 2, x, .07 * (.3 + .7 * ii), .25 + .5 * ((j * .37) % 1))
        ti += L
    # hits and risers at scene boundaries
    prev = .3
    for (ts, ii, mo) in cv['bounds']:
        if ts > 4 and (ii - prev > .12 or mo > 0):
            tb = tt(3.5); boom = (np.sin(2 * np.pi * (34 + 40 * np.exp(-tb * 5)) * tb) * np.exp(-tb * 1.1)).astype(np.float32)
            put(buf, ts - .05, boom, .35 * (.4 + .6 * ii), .5)
            rs = tt(5.0); sweep = lp(rng.standard_normal(len(rs)).astype(np.float32), 400) ; sweep = bp(rng.standard_normal(len(rs)).astype(np.float32), 300, 2500) * (rs / 5.0) ** 3
            put(buf, ts - 5.0, sweep, .22 * ii, .5)
        prev = ii
    # tension: tremolo cluster
    ten_c = (np.sin(2 * np.pi * float(hz(62)) * t) + np.sin(2 * np.pi * float(hz(63)) * t + 1)) * (.55 + .45 * np.sin(2 * np.pi * 5.5 * t)) * ten * .03
    buf[0] += ten_c; buf[1] += ten_c * .9
    hb = (t * 54 / 60) % 1.0; thump = (np.sin(2 * np.pi * 44 * t) * (np.exp(-hb * 14) + .5 * np.exp(-np.clip(hb - .3, 0, 9) * 16) * (hb > .3))) * ten * .3
    buf[0] += thump; buf[1] += thump
    return reverb(buf, 4.0, .4)


def style_bells(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32); L = 24.0
    scale = [50, 53, 55, 57, 60, 62, 65, 67, 69, 72, 74, 77]   # D minor-ish pentatonic
    ti = 1.0
    while ti < total - 3:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        if abs(ti % L) < .5 or ti < 1.5:
            pass
        nt = int(rng.choice(ch[1:] + [ch[2] + 12, ch[3] + 12, ch[4] + 12]))
        if te > .5 and rng.random() < .35: nt -= 12 if nt > 60 else 0
        b = bell(float(hz(nt)), 4.0, .5 + .8 * ii, 1.1 + .6 * te)
        put(buf, ti, b, .16 * (.35 + .65 * ii), rng.random()); ti += rng.uniform(1.2, 4.8) * (1.5 - .9 * ii) * (1 + .5 * te)
    # pad
    ti = 0.0
    while ti < total:
        ch = chord_at(ti, L)
        for j, nt in enumerate(ch[:4]):
            d = L + 4; x = lp(sum(saw(float(hz(nt)) * (1 + dt), d, rng.random()) for dt in (-.005, .005)) / 2, 500 + 700 * float(inten[min(n - 1, int(ti * SR))])) * adsr(d, 6, 5, .8, 6)
            put(buf, ti - 2, x, .04, .3 + .4 * (j % 2))
        ti += L
    return reverb(buf, 5.0, .55, damp=5000)


def style_data(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32)
    bpm = 108; step = 60 / bpm / 4; L = step * 32; k = 0; ti = 0.0
    scale = [62, 65, 67, 69, 72, 74, 77, 79]
    while ti < total - 1:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        if k % 16 == 0:   # sub bass note
            d = step * 14; x = lp(saw(float(hz(ch[0])), d), 220 + 500 * ii) * adsr(d, .01, .8, .5, .3); put(buf, ti, x, .17 * (.4 + .6 * ii), .5)
        if rng.random() < .15 + .6 * ii:     # hat / tick
            d = .05; x = hp(rng.standard_normal(int(d * SR)).astype(np.float32), 6000) * adsr(d, .001, .015, 0, .01); put(buf, ti, x, .05 * (.3 + .7 * ii) * (1.4 if k % 4 == 2 else .8), rng.random())
        if rng.random() < .12 + .35 * ii:    # digital blip
            nt = scale[int(rng.integers(len(scale)))] + (1 if te > .5 and rng.random() < .3 else 0); d = .09
            x = np.sign(np.sin(2 * np.pi * float(hz(nt)) * tt(d))) * .5 * adsr(d, .001, .04, 0, .02); put(buf, ti, lp(x, 3500), .05 * (.4 + .6 * ii), rng.random())
        if k % 32 == 0:   # soft pad stab
            for nt in ch[1:4]:
                d = L; x = lp(saw(float(hz(nt)), d, rng.random()), 900) * adsr(d, 2, 3, .6, 2); put(buf, ti, x, .035, rng.random())
        if ii > .5 and k % 8 == 0:
            tk = tt(.3); kick = np.sin(2 * np.pi * (46 + 80 * np.exp(-tk * 28)) * tk) * np.exp(-tk * 10); put(buf, ti, kick.astype(np.float32), .2 * (ii - .3), .5)
        ti += step; k += 1
    return reverb(buf, 1.8, .22)


def style_pad(cv, n, t, rng):
    """The original music bed (kept as it was; see audio.music for the legacy implementation)."""
    return None


# ------------------------------------------------------------------ ambience
def ambience(cv, n, t, rng, level=1.0):
    inten = interp(t, cv['keys']); ten = interp(t, cv['mk'])
    nz = rng.standard_normal(n).astype(np.float32); room = lp(nz, 500) * .35
    hum = (np.sin(2 * np.pi * 50 * t) * .5 + np.sin(2 * np.pi * 100 * t + 1) * .35 + np.sin(2 * np.pi * 150 * t + 2) * .15) * (.8 + .2 * np.sin(2 * np.pi * .07 * t))
    air = bp(rng.standard_normal(n).astype(np.float32), 1800, 5200) * (.25 + .5 * ten) * (.5 + .5 * np.sin(2 * np.pi * .04 * t + 1.1) ** 2)
    base = (room + hum * .18 + air * .25) * (.5 + .5 * inten + .4 * ten) * .05 * level
    out = np.stack([base, np.roll(base, 530)]).astype(np.float32)   # tiny inter-channel delay for width
    return out


# ------------------------------------------------------------------ sfx
def sfx_sound(kind, rng):
    """Short synthesised effect (mono float32) for a named kind."""
    if kind.startswith('count'):      # 'count:<seconds>' - a counter running up: ticks that speed up and rise in pitch, closing with a soft chime
        d = float(kind.split(':')[1]); out = np.zeros(int((d + 1.2) * SR), np.float32); tk = 0.0
        while tk < d:
            u = tk / d; f = 900 + 1500 * u; a = int(tk * SR); t = tt(.05); n_ = len(t)
            out[a:a + n_] += (np.sin(2 * np.pi * f * t) * np.exp(-t * 70) * (.35 + .25 * u)).astype(np.float32); tk += 1 / (9 + 22 * u)
        ch = bell(float(hz(88)), 1.0, .8, 3.0); a = int(d * SR); out[a:a + len(ch)] += ch[:len(out) - a] * .5
        return out
    if kind == 'msg':         # a message from an agent arrives: short robotic buzz-chirp (ring-modulated, stepped pitch)
        def rb(f, d):
            t = tt(d); car = np.sign(np.sin(2 * np.pi * f * t)); mod = np.sin(2 * np.pi * (f * .5 + 37) * t)
            x = lp((car * (.55 + .45 * mod)).astype(np.float32), 3200) * np.minimum(1, t / .006) * np.exp(-np.maximum(0, t - d * .7) * 40)
            return x.astype(np.float32)
        return _mix_at([(0, rb(420, .09)), (.11, rb(560, .09)), (.22, rb(760, .16))]) * .6
    if kind == 'tick':        # list item / small element appears
        t = tt(.09); return (np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 55) * .6 + bp(rng.standard_normal(len(t)).astype(np.float32), 2500, 6000) * np.exp(-t * 90) * .3).astype(np.float32) * .8
    if kind == 'slide':       # something moves: short airy glide
        d = .38; t = tt(d); x = bp(rng.standard_normal(len(t)).astype(np.float32), 500, 2600) * np.sin(np.pi * t / d) ** 2
        return (x * .55 + np.sin(2 * np.pi * np.cumsum(260 + 340 * t / d) / SR) * np.sin(np.pi * t / d) ** 2 * .12).astype(np.float32)
    if kind == 'connect':     # a link is established: rising zip ending in a soft click
        d = .28; t = tt(d); z = np.sin(2 * np.pi * np.cumsum(500 + 1500 * (t / d) ** 2) / SR) * np.sin(np.pi * np.minimum(t / d, 1) * .5) ** 2 * np.exp(-np.maximum(0, t - .2) * 40) * .35
        return _mix_at([(0, z.astype(np.float32)), (d - .02, bell(float(hz(91)), .35, .8, 6.0))]) * .8
    if kind == 'ask':         # question: two notes going up and left hanging
        return _mix_at([(0, bell(float(hz(76)), .5, 1.0, 5.0)), (.13, bell(float(hz(83)), .8, 1.0, 4.0))]) * .5
    if kind == 'answer':      # answer: two notes coming down and resolving
        return _mix_at([(0, bell(float(hz(83)), .5, 1.0, 5.0)), (.13, bell(float(hz(76)), .9, 1.0, 3.5)), (.13, bell(float(hz(88)), .9, .5, 4.0))]) * .3
    if kind == 'info':        # information shared: one short neutral tick
        return _mix_at([(0, bell(float(hz(81)), .35, 1.0, 7.0))]) * .6
    if kind.startswith('scroll'):     # 'scroll:<seconds>:<r0>:<r1>' - soft ticks of a feed scrolling, speeding up
        _, d, r0, r1 = kind.split(':'); d = float(d); r0 = float(r0); r1 = float(r1); out = np.zeros(int(d * SR) + SR // 4, np.float32); tk = 0.0
        while tk < d:
            u = tk / d; a = int(tk * SR); n_ = int(.025 * SR); t = tt(.025)
            out[a:a + n_] += (bp(rng.standard_normal(n_).astype(np.float32), 1800, 5200) * np.exp(-t * 150) * (.35 + .4 * rng.random()) * (.5 + .5 * u)).astype(np.float32)
            tk += 1 / (r0 + (r1 - r0) * u + 1e-6) * (.8 + .4 * rng.random())
        return out * 1.2
    if kind == 'create':      # something new is made: bright rising pluck + a little sparkle
        return _mix_at([(i * .06, bell(float(hz(n_)), .7, .9, 5.0)) for i, n_ in enumerate((79, 84, 91))] + [(.14, bp(rng.standard_normal(int(.25 * SR)).astype(np.float32), 3000, 7000) * np.exp(-tt(.25) * 14) * .25)]) * .35
    if kind == 'spawn':       # an agent appears: soft upward bloop with a halo
        t = tt(.3); sw = np.sin(2 * np.pi * np.cumsum(180 + 520 * (t / .3) ** .7) / SR) * np.minimum(1, t / .01) * np.exp(-t * 7) * .6
        return _mix_at([(0, sw.astype(np.float32)), (.12, bell(float(hz(76)), 1.0, .6, 3.0))]) * .55
    if kind.startswith('alarm'):       # 'alarm:<seconds>' - soft, non-dramatic repeating two-note alert (a flag blinking)
        d = float(kind.split(':')[1]) if ':' in kind else 3.0; out = np.zeros(int(d * SR), np.float32); per = 1.15; k = 0
        while k * per + .5 < d:
            t = tt(.32); b = (np.sin(2 * np.pi * 740 * t) * .8 + np.sin(2 * np.pi * 1480 * t) * .12) * np.minimum(1, t / .015) * np.exp(-t * 9)
            t2 = tt(.4); b2 = (np.sin(2 * np.pi * 587 * t2) * .8 + np.sin(2 * np.pi * 1174 * t2) * .1) * np.minimum(1, t2 / .015) * np.exp(-t2 * 8)
            a = int(k * per * SR); g = 1 - .45 * (k * per / d); out[a:a + len(t)] += (b * g).astype(np.float32); a2 = a + int(.17 * SR); out[a2:a2 + len(t2)] += (b2 * g).astype(np.float32)[:len(out) - a2]; k += 1
        return out * .5
    if kind.startswith('engine'):      # 'engine:<seconds>' - a machine revving up while an agent shakes
        d = float(kind.split(':')[1]) if ':' in kind else 3.0; t = tt(d); u = t / d
        f = 48 + 120 * u ** 1.6 + 3 * np.sin(2 * np.pi * 7 * t); ph = 2 * np.pi * np.cumsum(f) / SR
        saw = sum(np.sin(ph * k) / k for k in (1, 2, 3, 4, 5)).astype(np.float32)
        trem = .72 + .28 * np.sin(2 * np.pi * (9 + 26 * u) * t)                      # chugging that speeds up with the revs
        rum = lp(rng.standard_normal(len(t)).astype(np.float32), 260) * 1.6
        env = np.minimum(1, t / .35) * (.55 + .45 * u) * np.exp(-np.maximum(0, t - (d - .5)) * 6)
        return ((lp(saw, 450) * (1 - u) + lp(saw, 2200) * u) * .55 + rum * .35) * trem * env * .7
    if kind == 'pop':
        t = tt(.12); return (np.sin(2 * np.pi * (380 + 260 * np.exp(-t * 40)) * t) * np.exp(-t * 32)).astype(np.float32) * .5
    if kind == 'zip':
        d = .3; x = bp(rng.standard_normal(int(d * SR)).astype(np.float32), 1200, 4800) * np.sin(np.pi * tt(d) / d) ** 2; return x * .5
    if kind == 'chime':
        return _mix_at([(0, bell(float(hz(81)), 1.2, .7, 3.2)), (.12, bell(float(hz(88)), 1.6, .7, 2.8))])
    if kind == 'flag':
        return _mix_at([(0, bell(float(hz(84)), 1.8, .8, 2.2)), (.09, bell(float(hz(91)), 1.5, .6, 2.4))])
    if kind == 'thud':
        t = tt(.7); return (np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 25)) * t) * np.exp(-t * 7)).astype(np.float32) + lp(rng.standard_normal(len(t)).astype(np.float32), 300) * np.exp(-t * 18) * .4
    if kind == 'deny':
        t = tt(.5); return (np.sin(2 * np.pi * 170 * t) * np.exp(-t * 7) * .7 + np.sin(2 * np.pi * 120 * t) * np.exp(-t * 5)).astype(np.float32) * .8
    if kind == 'error':      # two-tone buzzer: harsh, short, unmistakable "error"
        def buz(f, d):
            t = tt(d); sq = np.sign(np.sin(2 * np.pi * f * t)) * .6 + np.sin(2 * np.pi * f * 2.01 * t) * .25
            return (lp(sq.astype(np.float32), 2600) * np.minimum(1, t / .008) * np.exp(-np.maximum(0, t - d * .6) * 22)).astype(np.float32)
        return _mix_at([(0, buz(311, .17)), (.2, buz(208, .32))]) * .9
    if kind == 'spark':
        return _mix_at([(i * .07, bell(float(hz(93 + [0, 4, 7, 12][i])), .9, 1.0, 4.0)) for i in range(4)])
    if kind == 'key':
        return _mix_at([(i * .05, bell(float(hz(96 + [0, 4, 7][i])), .7, 1.4, 6.0)) for i in range(3)])
    if kind == 'power':
        d = 1.6; t = tt(d); f = 520 * np.exp(-t * 2.0) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
        fl = (np.sin(t * (30 + 24 * t / d)) > -.4 + t / d).astype(np.float32) * .8 + .2
        return (np.sin(ph) * np.exp(-t * 1.4) * fl).astype(np.float32) * .8
    if kind == 'whoosh':
        d = 1.1; t = tt(d); x = bp(rng.standard_normal(len(t)).astype(np.float32), 200, 3200) * np.sin(np.pi * t / d) ** 2; return x * .55
    if kind == 'burst':
        return _mix_at([(i * .045, sfx_sound('pop', rng) * (.5 + .5 * rng.random())) for i in range(7)])
    if kind == 'lock':
        t = tt(.3); click = hp(rng.standard_normal(len(t)).astype(np.float32), 2500) * np.exp(-t * 90) * .8; return click + (np.sin(2 * np.pi * 140 * t) * np.exp(-t * 18)).astype(np.float32) * .7
    if kind == 'swell':
        d = 2.4; t = tt(d); return lp(rng.standard_normal(len(t)).astype(np.float32), 900) * (t / d) ** 2 * .9 * np.clip((d - t) / .5, 0, 1)
    if kind == 'bell':
        return bell(float(hz(76)), 3.5, .6, 1.0)
    if kind == 'rise':
        d = 4.0; t = tt(d); x = bp(rng.standard_normal(len(t)).astype(np.float32), 400, 4000) * (t / d) ** 2; return x * .7
    if kind == 'idea':
        return _mix_at([(i * .09, bell(float(hz(m)), 1.4, 1.0, 3.0)) for i, m in enumerate((79, 83, 86, 91))] + [(.3, bp(rng.standard_normal(int(.5 * SR)).astype(np.float32), 5000, 9000) * np.exp(-tt(.5) * 6) * .25)])
    if kind == 'poweroff':
        d = 1.8; t = tt(d); f = 330 * np.exp(-t * 2.6) + 24; ph = 2 * np.pi * np.cumsum(f) / SR
        fl = (np.sin(t * (22 + 30 * t / d)) > -.2 + t / d * 1.1).astype(np.float32) * .85 + .15
        return (np.sin(ph) * np.exp(-t * 1.5) * fl + .25 * lp(rng.standard_normal(len(t)).astype(np.float32), 500) * np.exp(-t * 5)).astype(np.float32)
    if kind == 'impact':
        d = 3.2; t = tt(d); boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 7)) * t) * np.exp(-t * 1.5)
        return (boom + .5 * lp(rng.standard_normal(len(t)).astype(np.float32), 700) * np.exp(-t * 7)).astype(np.float32)
    if kind == 'sting':
        d = 1.6; t = tt(d); x = sum(np.sin(2 * np.pi * float(hz(m)) * t + i) for i, m in enumerate((50, 51, 56, 62))) * np.exp(-t * 2.2) * np.clip(t / .01, 0, 1)
        return lp(x.astype(np.float32), 1800) * .3
    if kind == 'heartbeat':
        t = tt(1.2); b = lambda t0: np.sin(2 * np.pi * 48 * np.clip(t - t0, 0, None)) * np.exp(-np.clip(t - t0, 0, None) * 14) * (t >= t0)
        return (b(0) + .6 * b(.28)).astype(np.float32)
    if kind == 'hole':
        t = tt(.35); return (np.sin(2 * np.pi * (160 - 80 * t / .35) * t) * np.exp(-t * 9)).astype(np.float32) * .8
    t = tt(.1); return np.zeros(len(t), np.float32)


def _mix_at(parts):
    L = max(int(a * SR) + len(x) for a, x in parts); out = np.zeros(L, np.float32)
    for a, x in parts: out[int(a * SR):int(a * SR) + len(x)] += x
    return out


KIND_SFX = {   # world node kind -> (sfx, gain)
    'acard': ('spawn', .55), 'agent': ('spawn', .45), 'koA': ('error', .8), 'cross': ('error', .8), 'okA': ('chime', .55), 'check': ('chime', .55),
    'flFly': ('flag', .5), 'flag': ('flag', .5), 'ideaSpark': ('idea', .55), 'bulb': ('idea', .55), 'key': ('key', .45), 'sigLock': ('lock', .6),
    'hole': ('hole', .5), 'bell': ('bell', .45), 'crowd': ('swell', .5), 'msgfeed': ('burst', .4), 'scHang': ('thud', .5), 'person': ('spawn', .4),
    'orb': ('spark', .4), 'chip': ('tick', .4), 'quote': ('msg', .6), 'sheet': ('create', .55), 'flagTrophy': ('flag', .5),
}


def sfx_events(root, D):
    from .spec import resolve, cue_times
    S = D['sched']; ev = []
    for i in range(len(D['scenes'])) if isinstance(D['scenes'], list) else range(D['scenes']):
        if f'S{i}' in S and i > 0: ev.append((S[f'S{i}']['s'] - .15, 'whoosh', .5, .5))
    for c in D.get('cues', []):
        try: cs, ce = cue_times(c, S)
        except Exception: continue
        if c.get('a') == 'seal': ev.append((cs + .2, 'rise', .45, .5)); continue
        if c.get('a') != 'world': continue
        T = lambda v: (cs + float(v)) if isinstance(v, (int, float)) else resolve(v, S)
        for lk in c.get('p', {}).get('links', []) or []:
            if lk.get('at') is not None and not lk.get('rel'):
                try: ev.append((T(lk['at']), 'connect', .3, .5))
                except Exception: pass
        for nd in c.get('p', {}).get('nodes', []):
            k = nd.get('kind'); ta = T(nd.get('at', 0))
            if nd.get('flick'): ev.append((T(nd['flick']['at']), 'power', .5, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960)); continue
            if nd.get('until') is not None and k in ('agent', 'acard') and (nd.get('alpha', 1) or 1) > .2:
                try:
                    tu = T(nd['until'])
                    if tu < ce - 1.5: ev.append((tu + .1, 'poweroff', .3, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
                except Exception: pass
            if k == 'flFly' and nd.get('blink') and nd.get('bat') is not None:
                try:
                    tb = T(nd['bat']); te = T(nd['until']) if nd.get('until') is not None else ce; dd = min(6.0, te - tb)
                    if dd >= 1.2: ev.append((tb, f'alarm:{dd:.1f}', .5, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
                except Exception: pass
            for it in nd.get('items', []) or []:
                if it.get('dir') and it.get('at') is not None:
                    try: ev.append((T(it['at']), 'create', .55, .55))
                    except Exception: pass
            for m in nd.get('move', []) or []:
                try: ev.append((T(m['at']), 'slide', .4, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
                except Exception: pass
            for it in nd.get('items', []) or []:
                if not it.get('dir') and it.get('at') is not None:
                    try: ev.append((T(it['at']), 'tick', .35, .55))
                    except Exception: pass
            if k == 'chip' and nd.get('label') in ('zzASK', 'zzANSWER', 'zzINFO'):
                ev.append((ta + .05, nd['label'][2:].lower(), .6, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
            if k == 'flFly' and nd.get('move') and nd.get('until') is not None:
                try:
                    m = nd['move'][-1]; ev.append((T(m['at']) + float(m.get('dur', 1)), 'validate', .6, (m.get('x', 480)) / 960))
                except Exception: pass
            if k == 'num' and nd.get('dur'):
                ev.append((ta, f"count:{min(6.0, float(nd['dur'])):.1f}", .45, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
            if k == 'msgfeed':
                try:
                    te = T(nd['until']) if nd.get('until') is not None else ce; dd = min(14.0, te - ta); r0 = float(nd.get('r0', 6)); r1 = float(nd.get('r1', 12))
                    if dd >= 1.5: ev.append((ta, f'scroll:{dd:.1f}:{min(r0, 14):.1f}:{min(max(r1, r0), 22):.1f}', .45, .5))
                except Exception: pass
            if k == 'folderview' and (nd.get('alpha', 1) or 1) > .2:
                ev.append((ta, 'whoosh', .75, .4))
                for m in nd.get('move', []) or []:
                    try: ev.append((T(m['at']), 'whoosh', .7, .5))
                    except Exception: pass
            if nd.get('shake') and k in ('agent', 'acard'):
                try:
                    sh = nd['shake']; dd = min(7.0, float(sh.get('dur', 1.2)))
                    if dd >= 1.0: ev.append((T(sh['at']), f'engine:{dd:.1f}', .45, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
                except Exception: pass
            if k == 'bulb' and nd.get('litAt') is not None:
                try: ev.append((T(nd['litAt']), 'idea', .5, .5))
                except Exception: pass
            if k in KIND_SFX and not nd.get('nosfx') and (nd.get('alpha', 1) or 1) > .2 and ta > cs - .01:
                s_, g = KIND_SFX[k]; ev.append((ta + .05, s_, g, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
    try: stj = json.load(open(f'{root}/story.json'))
    except Exception: stj = {'scenes': []}
    for sc in stj.get('scenes', []):
        for e in sc.get('sfx', []) or []:
            try: ev.append((resolve(e['at'], S), e['kind'], float(e.get('g', .6)), float(e.get('pan', .5))))
            except Exception: pass
    ev.sort()
    out = []; last = {}
    for t_, s_, g, p in ev:        # thin out dense bursts so the film does not rattle
        gap = {'validate': .8, 'msg': .8, 'tick': .08, 'slide': .15, 'connect': .5, 'spawn': .25, 'create': .3, 'pop': .35, 'swell': 3, 'whoosh': 1, 'poweroff': .6, 'idea': .5}.get(s_, .12)
        if t_ - last.get(s_, -9) < gap: continue
        last[s_] = t_; out.append((t_, s_, g, min(.95, max(.05, p))))
    return out


def render_sfx(root, D, t0=0.0, tot=None, out=None, level=1.0):
    tot = tot or D['total']; n = int((tot + 3) * SR); buf = np.zeros((2, n), np.float32); rng = np.random.default_rng(11); cache = {}
    for t_, s_, g, p in sfx_events(root, D):
        if not (t0 - 1 <= t_ < t0 + tot): continue
        cache.setdefault(s_, sfx_sound(s_, rng)); put(buf, t_ - t0, cache[s_], g * level, p)
    buf = reverb(buf, 1.6, .22) if buf.any() else buf
    out = out or f'{root}/build/sfx.wav'; write_wav(out, buf[:, :int(tot * SR)]); return out


# ------------------------------------------------------------------ output
def write_wav(path, buf, peak=.7):
    m = float(np.abs(buf).max()) or 1.0; x = (buf / m * peak) if peak else buf
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x.T, -1, 1) * 32767).astype('<i2').tobytes())
    return path


def render_style(style, cv, seed=7, ambience_level=1.0):
    n, t = make_t(cv['total']); rng = np.random.default_rng(seed)
    fn = dict(pulse=style_pulse, cinema=style_cinema, bells=style_bells, data=style_data)[style]
    buf = fn(cv, n, t, rng)
    if ambience_level: buf = buf + ambience(cv, n, t, np.random.default_rng(seed + 1), ambience_level) * float(np.abs(buf).max()) * 6
    fi = max(.05, float(cv['meta'].get('fadein', 4))); fo = float(cv['meta'].get('fadeout', 4))
    buf *= (np.clip(t / fi, 0, 1) * np.clip((cv['total'] - 2 - t) / fo, 0, 1))[None]
    return buf


def demo_curves(total=48.0):
    keys = [(0, .25), (8, .35), (16, .6), (26, .95), (36, .6), (total, 0)]; mk = [(0, 0), (14, 0), (17, 1), (30, 1), (34, 0), (total, 0)]
    return dict(total=total, keys=keys, mk=mk, bounds=[(0, .25, 0), (16, .6, 1), (30, .9, 1), (36, .6, 0)], meta=dict(fadein=2, fadeout=4))


def demos(outdir, total=48.0):
    import os; os.makedirs(outdir, exist_ok=True); cv = demo_curves(total); res = []
    for s in ('pulse', 'cinema', 'bells', 'data'):
        res.append(write_wav(f'{outdir}/music_{s}.wav', render_style(s, cv)))
    return res


def sfx_sampler(path):
    rng = np.random.default_rng(5); kinds = ['whoosh', 'pop', 'zip', 'chime', 'flag', 'spark', 'key', 'lock', 'deny', 'thud', 'hole', 'burst', 'power', 'error', 'validate', 'msg', 'tick', 'slide', 'connect', 'count:2', 'ask', 'answer', 'info', 'scroll:2:6:12', 'engine:3', 'alarm:3', 'create', 'spawn', 'bell', 'swell', 'rise']
    buf = np.zeros((2, int((len(kinds) * 2.2 + 3) * SR)), np.float32)
    for i, k in enumerate(kinds): put(buf, 1 + i * 2.2, sfx_sound(k, rng), 1.0, .5)
    return write_wav(path, reverb(buf, 1.6, .22))


# ------------------------------------------------------------------ mix of styles by chapter
def _norm_mix(m, default):
    if m is None: m = default
    if isinstance(m, str): m = {m: 1.0}
    return {k: float(v) for k, v in m.items()}


def render_mix(root, D=None, out=None, log=print):
    """meta.music_style = 'mix': every scene has `music` = style or {style: weight}; layers crossfade over 4 s at scene boundaries.
    Memory-lean: each layer is rendered once, parked on disk as int16 and the final mix is streamed in 20 s blocks."""
    import os, tempfile, gc, shutil
    from . import audio
    D = D or json.load(open(f'{root}/build/data.json')); st = json.load(open(f'{root}/story.json')); S = D['sched']; meta = st['meta']
    cv = curves(root, D); n = int(cv['total'] * SR); N = len(st['scenes']); default = meta.get('music_default', {'cinema': 1.0})
    mixes = [_norm_mix(sc.get('music'), default) for sc in st['scenes']]; styles = sorted({k for m in mixes for k in m})
    out = out or f'{root}/build/music.wav'; tmpd = tempfile.mkdtemp(prefix='mix_')

    def gain_pts(sname):
        pts = [(0, mixes[0].get(sname, 0))]
        for i in range(1, N):
            tb = S[f'S{i}']['s']; pts += [(tb - 2.0, mixes[i - 1].get(sname, 0)), (tb + 2.0, mixes[i].get(sname, 0))]
        pts.append((cv['total'], mixes[-1].get(sname, 0))); return pts

    def park(name, x, pts=None):
        peak = float(np.abs(x).max()) or 1.0
        if pts is not None:
            tg = np.arange(0, x.shape[1], SR, dtype=np.float32) / SR; g = np.interp(tg, [p[0] for p in pts], [p[1] for p in pts]); act = np.repeat(g > .05, SR)[:x.shape[1]]
            rms = float(np.sqrt((x[:, act] ** 2).mean())) if act.any() else 1.0
        else:
            rms = float(np.sqrt((x ** 2).mean())) or 1.0
        mm = np.lib.format.open_memmap(f'{tmpd}/{name}.npy', mode='w+', dtype=np.int16, shape=x.shape)
        for i in range(0, x.shape[1], SR * 30): mm[:, i:i + SR * 30] = (x[:, i:i + SR * 30] / peak * 32767).astype(np.int16)
        mm.flush(); del mm
        return dict(peak=peak, rms=rms)

    L = {}
    for sname in sorted(styles, key=lambda k: (k != 'pad', k)):      # the legacy pad is the hungriest: do it first
        log(f'  music layer: {sname}'); gc.collect()
        if sname == 'pad':
            tmp = f'{tmpd}/pad.wav'; audio.music(root, tmp, style='pad', ambience=0); gc.collect()
            with wave.open(tmp, 'rb') as w: x = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).T.astype(np.float32) / 32768
            os.remove(tmp); x = x[:, :n] if x.shape[1] >= n else np.pad(x, ((0, 0), (0, n - x.shape[1])))
        else:
            x = render_style(sname, cv, ambience_level=0)[:, :n]
        L[sname] = park(sname, x, gain_pts(sname)); L[sname]['pts'] = gain_pts(sname); del x; gc.collect()
    lvl = float(meta.get('ambience', 1.0)); amb = None
    if lvl > 0:
        nn, t = make_t(cv['total']); a = ambience(cv, nn, t, np.random.default_rng(9), 1.0)[:, :n]; del t; amb = park('amb', a); del a; gc.collect()
    fi = max(.05, float(meta.get('fadein', 4))); fo = float(meta.get('fadeout', 4)); tot = D['total']
    mms = {k: np.load(f'{tmpd}/{k}.npy', mmap_mode='r') for k in list(L) + (['amb'] if amb else [])}
    B = SR * 20

    def block(i0, i1):
        tb = np.arange(i0, i1, dtype=np.float32) / SR; acc = np.zeros((2, i1 - i0), np.float32)
        for k, meta_ in L.items():
            g = np.interp(tb, [p[0] for p in meta_['pts']], [p[1] for p in meta_['pts']]).astype(np.float32)
            acc += mms[k][:, i0:i1].astype(np.float32) * (meta_['peak'] / 32767 * .11 / max(meta_['rms'], 1e-6)) * g[None]
        if amb: acc += mms['amb'][:, i0:i1].astype(np.float32) * (amb['peak'] / 32767 * .012 * lvl / max(amb['rms'], 1e-6))
        return acc * (np.clip(tb / fi, 0, 1) * np.clip((tot - tb) / fo, 0, 1))[None]
    mx = max(float(np.abs(block(i, min(n, i + B))).max()) for i in range(0, n, B)) or 1.0
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        for i in range(0, n, B):
            x = block(i, min(n, i + B)) / mx * .7; w.writeframes((np.clip(x.T, -1, 1) * 32767).astype('<i2').tobytes())
    del mms; shutil.rmtree(tmpd, ignore_errors=True); return out
