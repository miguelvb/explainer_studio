# Scene 6 · Lo que está en juego
MUSIC = {'pad': 1, 'cinema': 0.5}
MOOD = 'tense'
INTENSITY = 0.5
# 6a: 235 of 372 have Lean; the 137 others are grey documents that "could have errors"
n = [N('rp', 'folder', 80, 85, 60, 50, 0.3, color=AMB), T('rpl', 56, 148, 'openai/math', 0.3, color=GRY, fs=13),
     N('c1', 'num', 50, 235, 230, 60, '6a#formalización', n=235, color=TEAL, fs=54, dur=2.2, cap='de 372 con Lean', capc='muted', capfs=14),
     N('gb', 'sandbox', 360, 90, 560, 340, '6a#formalización', color=GRY, open=True, label='137 sin Lean')]
for j in range(3):
    for i in range(6):
        k = j * 6 + i
        n.append(N(f'g{k}', 'doc', 405 + 85 * i, 140 + 95 * j, 40, 50, f'6a#formalización+{0.9 + 0.12 * k:.2f}', color=GRY, dashed=True))
for k, (i, j) in enumerate([(1, 0), (4, 1), (2, 2), (5, 2)]):
    n.append(ic(f'e{k}', 'cross', 405 + 85 * i + 20, 140 + 95 * j + 25, 22, f'6a#errores+{0.25 * k:.2f}', color=RED, sw=3))
n.append(T('er', 520, 395, 'podrían tener errores', '6a#errores', color=RED, fs=14))
lk = [link('rp', 'gb', '6a#repositorio', color=GRY, rel=True)]
cues = [K('S6', '6b', n, lk, fs=1.0)]
# 6b: a person next to a huge pile of documents nobody reads
n = [N('pe', 'person', 70, 250, 70, 100, 0.3, color='#E7EBF1', cap='Thomas Bloom', capfs=13)]
base = 440; k = 0
for r in range(7):
    for c in range(7 - r):
        x = 470 + (c - (6 - r) / 2) * 40 - 12 + 40; y = base - 44 * (r + 1)
        n.append(N(f'p{k}', 'doc', x, y, 34, 42, f'6b#demostraciones+{0.04 * k:.2f}', color=GRY if k % 3 else BLU)); k += 1
n += [N('ey', 'eye', 640, 100, 60, 34, '6b#ningún', color=GRY, dashed=True), ic('ex', 'cross', 670, 117, 56, '6b#ningún+0.4', color=RED, sw=4),
      Q('q', 60, 110, 0, ['«Ningún humano', 'lo ha leído»'], '6b#ningún', color=AMB, fs=17)]
cues.append(K('6b', '6c', n, [], fs=1.0))
# 6c: Alon walks away from Erdős problems; 25 Fields medallists send a letter to OpenAI
n = [N('al', 'person', 70, 60, 60, 90, 0.3, color='#E7EBF1', cap='Noga Alon', capfs=13),
     Q('qa', 180, 70, 0, ['«Si la IA los resuelve,', 'ya no tiene sentido»'], '6c#dejó', color=AMB, fs=17),
     N('pr', 'flFly', 640, 70, 34, 52, '6c#Alon', color=AMB, until='6c#dejó+1.2'), T('prl', 620, 130, 'problemas de Erdős', '6c#Alon', color=GRY, fs=13, until='6c#dejó+1.2'),
     N('mb', 'sandbox', 50, 290, 620, 110, '6c#veinticinco', color=AMB, label='25 medallistas Fields'),
     AN('oa', 790, 280, 'OpenAI', '6c#carta', color='blue')]
for i in range(25):
    n.append(N(f'm{i}', 'person', 70 + 24 * i, 322, 20, 32, f'6c#veinticinco+{0.05 * i:.2f}', color='#E7EBF1'))
n.append(T('ct', 696, 316, 'carta', '6c#carta', color=AMB, fs=14))
lk = [link('mb', 'oa', '6c#carta', color=AMB)]
cues.append(K('6c', '6d', n, lk, fs=1.0))
# 6d: advisory group at the IAS: its arrow towards OpenAI stops halfway
n = [N('ias', 'sandbox', 60, 190, 300, 200, 0.3, color=TEAL, label='Grupo asesor · IAS'),
     ch('ci', 130, 150, 100, 'importancia', '6d#importancia', color='teal'), ch('cd', 270, 150, 100, 'divulgación', '6d#divulgación', color='teal'),
     N('st', 'stop', 480, 262, 46, 46, '6d#ritmo', color=RED), T('sr', 410, 322, 'no decide el ritmo', '6d#ritmo', color=RED, fs=14),
     AN('oa', 700, 225, 'OpenAI', 0.3, color='blue')]
for i in range(9):
    n.append(N(f'ip{i}', 'person', 105 + 80 * (i % 3), 225 + 50 * (i // 3), 34, 40, f'6d#grupo+{0.08 * i:.2f}', color='#E7EBF1'))
lk = [link('ias', 'st', '6d#asesora', color=TEAL), link('st', 'oa', '6d#ritmo', color=TEAL)]
cues.append(K('6d', 'E6', n, lk, fs=1.0))
