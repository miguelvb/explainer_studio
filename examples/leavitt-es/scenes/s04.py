# Scene 4 · Una vida interrumpida
MUSIC = {'pad': 1}
INTENSITY = 0.3
cues = []

# 4a–4b — the empty desk; Europe, Beloit
n = [person('w', 480, 230, '4a', color='amber', s=46, until='4a#familia'),
     N('dk', 'bar', 420, 270, 120, 8, '4a', color='muted', fill=1, until='4b'),
     chipT('eu', 260, 400, 'Europa', '4b#Europa', color='teal'),
     chipT('bl', 700, 400, 'Beloit · Wisconsin', '4b#Beloit', color='teal'),
     person('t', 260, 340, '4b#Europa', color='amber', s=34, move=[dict(at='4b#Beloit', x=685, y=286, dur=1.6)]),
     P('art', 'page', 780, 320, 44, '4b#arte', color='muted')]
lk = [OR('eu', 'bl', '4b#Beloit', 'muted')]
cues.append(K('4a', '4c', n, lk, fs=1.0))

# 4c–4d — the letter of 13 May 1902 and the answer
n = [chipT('bl', 200, 420, 'Beloit', '4c', color='teal'), chipT('hv', 760, 420, 'Harvard', '4c', color='red'),
     field('snow', 40, 120, 220, 160, 160, '4c#frío', seed=4, color='muted', r=(.8, 1.6)),
     D('l1', LETTER, 200, 300, 70, '4c#escribió', color='amber', cap='13 mayo 1902', capfs=12),
     D('l2', LETTER, 760, 300, 70, '4d', color='blue'),
     T('p25', 700, 200, '0,25 $', '4d#veinticinco', color=GRY, fs=16),
     T('p30', 790, 200, '0,30 $ / hora', '4d#treinta', color=AMB, fs=18),
     person('w', 200, 360, '4d#aceptó', color='amber', s=30, move=[dict(at='4d#aceptó+0.3', x=747, y=312, dur=1.6)])]
lk = [link('l1', 'l2', '4c#escribió+0.6', color='amber', comm=True, until='4d'),
      link('l2', 'l1', '4d', color='blue', comm=True)]
cues.append(K('4c', '4e', n, lk, fs=1.0))

# 4e–4f — Garden Street: the uncle's house and the observatory on the same street; then Linnaean Street
n = [N('st', 'bar', 100, 380, 760, 4, '4e', color='muted', fill=1, cap='Garden Street', capfs=12),
     D('hs', HOUSE, 230, 310, 120, '4e#casa', color='amber', cap='casa del tío', capfs=12),
     D('ob', DOME, 720, 310, 120, '4e#observatorio', color='blue', cap='observatorio', capfs=12),
     person('w', 300, 360, '4e#calle', color='amber', s=30, move=[dict(at='4e#calle+0.5', x=630, y=331, dur=2.4), dict(at='4e#casó', x=286, y=331, dur=2.4)]),
     D('ch', CHURCH, 470, 210, 70, '4e#iglesia', color='blue', alpha=.8),
     DATE('d1', 60, 40, '1911', '4f#1911', color=GRY), DATE('d2', 160, 40, '1916', '4f#1916', color=GRY),
     person('fa', 120, 140, '4f#padre', color='muted', s=28, flick=dict(at='4f#1911', dur=1.2, end='off')),
     person('un', 200, 140, '4f#tío', color='muted', s=28, flick=dict(at='4f#1916', dur=1.2, end='off')),
     person('mo', 560, 470, '4f#madre', color='blue', s=28, move=[dict(at='4f#Linnaean', x=757, y=165, dur=1.6)]),
     N('ln', 'sandbox', 720, 130, 150, 80, '4f#Linnaean', color='teal', label='')]
cues.append(K('4e', '4g', n, [], fs=1.0))

# 4g–4h — who she was, in Solon Bailey's words
n = [FOTO('por', 80, 60, 300, 380, 'retrato.jpg', 'Henrietta Leavitt', '4g')]
for j, (w_, a_) in enumerate([('callada', '4g#callada'), ('seria', '4g#seria'), ('deber', '4g#deber'), ('justicia', '4g#justicia'), ('lealtad', '4g#lealtad')]):
    n.append(T(f'w{j}', 460, 110 + 40 * j, w_, a_, color=WHITE, fs=18, until='4h'))
n.append(Q('q', 430, 150, 500, ['«el feliz don de apreciar', 'todo lo que hay de digno', 'y amable en los demás»'], '4h#feliz', color='amber', fs=15))
cues.append(K('4g', 'E4', n, [], fs=1.0))
