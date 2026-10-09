# Scene 6 · Lo que no la dejaron hacer
MUSIC = {'pad': 1}
MOOD = 'tense'
INTENSITY = 0.4
cues = []

# 6a — the ruler has no numbers yet
n = [D('ax', AXES + [dict(d='M14 82L92 18', sw=2)], 330, 270, 340, '6a', color='muted', move=[dict(at='6b', x=-200, y=100, dur=1.4)], until='6c'),
     person('w', 620, 330, '6a#Henrietta', color='amber', s=46, until='6c'),
     N('q', 'txt', 610, 200, 40, 50, '6a#números', color=WHITE, fs=40, text='?', until='6b')]
cues.append(K('6a', '6b', n, [], fs=1.0))

# 6b–6d — the North Polar Sequence; measuring is for computers, interpreting for men
PX, PY = 560, 250
n = [star('pol', PX, PY, '6b#Polar', s=26, color='blue', cap='Polar', capfs=12),
     person('w', 280, 330, '6b', color='amber', s=46)]
for j in range(12):
    a = 2 * math.pi * j / 12
    n.append(star(f'r{j}', PX + 130 * math.cos(a), PY + 130 * math.sin(a), f'6b#estrellas+{0.15 * j:.2f}', s=10, color='muted',
                  litAt=f'6d#referencia+{0.1 * j:.1f}'))
n += [chipT('me', 280, 420, 'medir', '6c#medir', color='amber'),
      person('m', 850, 120, '6c#Interpretar', color='blue', s=34), chipT('in', 850, 200, 'interpretar', '6c#Interpretar', color='blue'),
      chipT('std', PX, 440, 'estándar internacional', '6d#internacional', color='teal')]
cues.append(K('6b', '6e', n, [], fs=1.0))

# 6e — Hertzsprung puts numbers on her ruler
n = [DATE('d', 60, 40, '1913', '6e'),
     D('ax', AXES + [dict(d='M14 82L92 18', sw=2)], 400, 290, 340, '6e', color='teal'),
     person('hz', 720, 300, '6e#Hertzsprung', color='blue', s=46, cap='Hertzsprung', capfs=13)]
for j, v in enumerate(['1', '10', '100']):
    n.append(T(f'n{j}', 250 + 100 * j, 450, v, f'6e#escala+{0.4 * j:.1f}', color=AMB, fs=16))
cues.append(K('6e', 'E6', n, [], fs=1.0))
