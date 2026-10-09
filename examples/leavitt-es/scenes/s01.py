# Scene 1 · Una hija de pastor
MUSIC = {'pad': 1, 'bells': 0.3}
INTENSITY = 0.3
cues = []

# 1a — birth, seven siblings, a minister's family on the move
n = [DATE('d', 60, 40, '04 julio 1868', '1a'),
     chipT('pl', 160, 100, 'Lancaster, Massachusetts', '1a#Lancaster'),
     D('house', HOUSE, 400, 230, 110, '1a', color='amber', move=[dict(at='1a#mudaba', x=595, y=175, dur=1.6)]),
     D('ch', CHURCH, 500, 225, 90, '1a#pastor', color='blue', move=[dict(at='1a#mudaba', x=715, y=180, dur=1.6)])]
for j in range(7):
    k = dict(flick=dict(at=f'1a#dos+{0.4 * (j - 4):.1f}', dur=1.4, end='dim')) if j in (4, 6) else {}
    n.append(person(f'h{j}', 300 + 46 * j, 420, f'1a#mayor+{0.15 * j:.2f}', color='amber' if j == 0 else 'blue', s=40 if j == 0 else 30, **k))
cues.append(K('1a', '1b', n, [], fs=1.0))

# 1b — what was expected of a woman
n = [person('w', 480, 300, '1b', color='amber', s=56),
     D('ring', RING, 340, 200, 60, '1b#casara', color='muted'),
     D('hs', HOUSE, 620, 200, 70, '1b#casa', color='muted'),
     P('bk', 'book', 480, 120, 64, '1b#universidad', color='blue', alpha=.35, move=[dict(at='1b#ciencia', x=820, y=40, dur=2)])]
cues.append(K('1b', '1c', n, [], fs=1.0))

# 1c — the Harvard Annex and the certificate
n = [N('hv', 'sandbox', 120, 140, 300, 240, '1c', color='red', label='Harvard'),
     N('ax', 'sandbox', 560, 220, 160, 160, '1c#Anexo', color='teal', label='Anexo'),
     person('w', 480, 460, '1c', color='amber', s=46, move=[dict(at='1c#Anexo+0.4', x=619, y=270, dur=1.6)]),
     P('cert', 'page', 820, 280, 80, '1c#certificado', color='amber', cap='certificado', capfs=12),
     T('note', 600, 420, '«…si hubiera sido un hombre»', '1c#hombre', color=AMB, fs=15)]
cues.append(K('1c', '1d', n, [], fs=1.0))

# 1d — the astronomy course
n = [DATE('d', 60, 40, '1892', '1d'), person('w', 480, 330, '1d', color='amber', s=56),
     P('st', 'star', 480, 190, 50, '1d#astronomía', color='amber', blink=.3, bf=2)]
cues.append(K('1d', '1e', n, [], fs=1.0))

# 1e — the deafness: sound waves die out before they reach her
n = [person('w', 600, 300, '1e', color='amber', s=56)]
for j in range(3):
    n.append(P(f'wv{j}', 'waves', 260, 280, 70, f'1e#oído+{0.9 * j:.1f}', color='blue', alpha=.8 - .25 * j,
               move=[dict(at=f'1e#oído+{0.9 * j + 0.1:.1f}', x=380 - 20 * j, y=245, dur=1.6)], until=f'1e#oído+{0.9 * j + 1.7:.1f}'))
n.append(P('wv3', 'waves', 300, 280, 60, '1e#sordera', color='blue', alpha=.25))
cues.append(K('1e', 'E1', n, [], fs=1.0))
