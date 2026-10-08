# Scene 7 · Cierre
MUSIC = {'pad': 1, 'bells': 0.4}
INTENSITY = 0.3
# 7a: the same timeline as scene 1 (dic 2025 -> oct 2026); the agent grows from repeating others' solutions to refuting Erdős and proposing pi proofs
TLY = 420
TX = dict(dic=80, ene=215, may=360, ago=520, sep=670, oct=830)
TL = dict(dic='diciembre 2025', ene='enero 2026', may='mayo 2026', ago='agosto 2026', sep='septiembre 2026', oct='octubre 2026')
n = [N('tl', 'bar', 60, TLY, 840, 6, 0.3, color='muted', fill=1, rx=0)]
for i, (k_, x_) in enumerate(TX.items()):
    n += [N('tk_' + k_, 'bar', x_ - 3, TLY - 13, 6, 32, 0.35 + 0.05 * i, color='muted', fill=1, rx=0),
          ch('t_' + k_, x_, TLY + 46, 120 if k_ == 'sep' else 100, TL[k_], 0.35 + 0.05 * i, color='teal' if k_ == 'oct' else 'muted')]
n += [N('ag0', 'agent', TX['dic'] - 16, TLY - 52, 32, 32, 0.6, color='blue', until='7a#proponer+0.6',
        move=[dict(at='7a#refutar', x=TX['may'] - 16, y=TLY - 52, dur=1.4), dict(at='7a#proponer', x=TX['oct'] - 16, y=TLY - 52, dur=1.6)]),
      N('n10', 'num', 70, 130, 140, 50, '7a#repetir', n=10, color=RED, fs=46, dur=1.2, cap='falsos', capc='muted', capfs=13),
      N('fe', 'flFly', 460, 200, 34, 52, '7a#refutar+0.6', color=TEAL),
      N('ag1', 'agent', TX['oct'] - 30, TLY - 80, 60, 60, '7a#proponer+0.6', color='blue'),
      N('n722', 'num', 650, 110, 250, 60, '7a#proponer+0.8', n=722, color=TEAL, fs=52, dur=2.4, cap='manuscritos', capc='muted', capfs=14)]
lk = []
cues = [K('S7', '7b', n, lk, fs=1.0)]
# 7b: the tower again, the Lean (green) and unchecked (grey) bars, the small verifier still working
n = []; k = 0
for r in range(7):
    for c in range(7 - r):
        x = 330 + (c - (6 - r) / 2) * 40 - 12 + 40; y = 440 - 44 * (r + 1)
        n.append(N(f'p{k}', 'doc', x, y, 34, 42, f'7b#setecientos+{0.04 * k:.2f}', color=GRY if k % 3 else BLU)); k += 1
n += W.judge('vj', 90, 250, '', 0.3, w=90, h=110, color='teal', fs=10, move=[dict(at='7b#resistirán', x=150, y=260, dur=1.5), dict(at='7b#revisar', x=190, y=330, dur=1.5), dict(at='7b#produce', x=150, y=250, dur=1.5)]) if False else []
n.append(W.judge('vj', 70, 250, '', 0.3, w=90, h=110, color='teal', fs=10,
                 move=[dict(at='7b#resistirán', x=90, y=290, dur=1.5), dict(at='7b#revisar', x=70, y=230, dur=1.5), dict(at='7b#produce', x=100, y=300, dur=1.5)]))
n += BAR('bl', 640, 200, 260, 0.63, '7b#resistirán', TEAL, label='con Lean')
n += BAR('bg', 640, 270, 260, 0.37, '7b#resistirán+0.4', GRY, label='sin comprobar')
cues.append(K('7b', '7c', n, [], fs=1.0))
# 7c: everything fades except the verifier and the flag
n = [W.judge('vj', 340, 170, '', 0.3, w=120, h=150, color='teal', fs=10), N('fl', 'flFly', 560, 180, 48, 74, '7c#cuello', color=TEAL)]
cues.append(K('7c', 'E7', n, [], fs=1.0))
