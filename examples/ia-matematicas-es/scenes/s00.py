# Scene 0 · Gancho
MUSIC = {'bells': 1, 'pad': 0.3}
INTENSITY = 0.35
cues = []


def mt_tower(prefix, cx, bottom, cols=6, rows=14, t0=0.1, dt=0.05, src=None, until=None, color='blue', dw=18, dh=22, px=22, py=25):
    """Tower of small documents (cols x rows), filled from the bottom row up; `src`=(x,y) makes each document come out of there."""
    n = []
    x0 = cx - cols * px / 2
    for i in range(cols * rows):
        r, c = i // cols, i % cols
        x, y = x0 + c * px + (px - dw) / 2, bottom - (r + 1) * py + (py - dh) / 2
        t = f'{t0}+{dt * i:.2f}' if isinstance(t0, str) else t0 + dt * i
        k = dict(until=until) if until else {}
        if src:
            ta = t if not isinstance(t, str) else t
            nd = N(f'{prefix}{i}', 'doc', src[0], src[1], dw, dh, ta, color=color, **k)
            tt = f'{t0}+{dt * i + 0.9:.2f}' if isinstance(t0, str) else t0 + dt * i + 0.9
            nd['move'] = [dict(at=tt, x=round(x), y=round(y), dur=0.8)]
        else:
            nd = N(f'{prefix}{i}', 'doc', x, y, dw, dh, t, color=color, **k)
        n.append(nd)
    return n


# 0a — title seal
cues.append(dict(a='seal', at='S0', until='0b', ext=0, p=dict(text='Las matemáticas se aceleran:|722 teoremas de una IA', sub='Arkinos @ oct 2026  ·  Explainer Studio', at=0.5, type=14, scale=1.0, cy=215, ty=392), bg=True, fade=[0.8, 2.0]))

# 0b — GPT-5 and ten flags that turn red; the note "ya estaba publicado"
n = [N('ck0', 'txt', 30, 30, 300, 32, '0b#octubre', color='teal', fs=24, type=9, text='octubre 2025'),
     AN('gp', 245, 250, 'GPT-5', at=0.3, color='blue', w=130, h=150),
     W.sheet('nt', 560, 230, 240, 110, ['ya estaba', 'publicado'], at='0b#solo', fs=22, color='amber')]
for j in range(10):
    x = 212 + 44 * (j % 5); y = 80 + 46 * (j // 5)
    n.append(N(f'g{j}', 'flag', x, y, 28, 36, f'0b#diez+{0.16 * j:.2f}', color='teal', until=f'0b#falso+{0.3 * j:.2f}'))
    n.append(N(f'r{j}', 'flag', x, y, 28, 36, f'0b#falso+{0.3 * j:.2f}', color='red', state='poisoned'))
lk = [link('gp', 'nt', '0b#encontrado', color='amber', comm=True)]
cues.append(K('0b', '0c', n, lk, fs=1.0))

# 0c + 0d — the date, the folder opens, the documents pile into a tower, the counter climbs; then the small verifier looks at the tower
FX, FY = 120, 330
n = [N('ck1', 'txt', 30, 30, 340, 32, '0c#seis', color='teal', fs=24, type=9, text='06 octubre 2026'),
     N('fo', 'folder', FX, FY, 120, 90, '0c#seis+0.8', color='amber', cap='openai/math', capfs=13, until='0d'),
     N('twb', 'sandbox', 400, 112, 164, 370, '0c#publicó', color='blue', label='')]
n += mt_tower('d', 480, 470, t0='0c#publicó', dt=0.05, src=(FX + 50, FY + 30))
n += [W.counter('n722', 640, 250, 722, '0c#publicó', cap='manuscritos', w=200, dur=4.5, fs=60),
      N('vf', 'agent', 203, 283, 34, 34, '0d#sobre', color='teal', label='verificador'),
      N('qq', 'question', 255, 255, 30, 30, '0d#comprueba', color='amber')]
lk = [link('vf', 'twb', '0d#sobre+0.8', color='teal', bi=True)]
cues.append(K('0c', 'E0', n, lk, fs=1.0))
