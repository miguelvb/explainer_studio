# Scene 2 · ¿De qué hablamos?
MUSIC = {'pad': 1}
INTENSITY = 0.3
cues = []

# 2a–2c — one point; Nagel's bat flies at night between trees, echoes, a glow inside the bat
n = [P('pt', 'dot', 480, 270, 14, '2a#aclarar', color='muted', until='2b'),
     T('y74', 40, 36, '1974', '2b#1974', color=TEAL, fs=24),
     P('t1', 'tree', 560, 360, 130, '2b#murciélago', color='teal', alpha=.8),
     P('t2', 'tree', 710, 320, 170, '2b#murciélago+0.2', color='teal', alpha=.8),
     P('t3', 'tree', 860, 370, 120, '2b#murciélago+0.4', color='teal', alpha=.8),
     P('bat', 'bat', 120, 160, 90, '2b#murciélago', color='blue',
       move=[dict(at='2b#murciélago+2.4', x=250, y=175, dur=2.4), dict(at='2c#ecos', x=330, y=205, dur=2.0)]),
     P('wv', 'waves', 475, 250, 70, '2c#ecos', color='blue', blink=.8, bf=6, until='2c#imaginar+1.5'),
     P('wb', 'waves', 440, 260, 60, '2c#imaginar', color='teal', blink=.8, bf=6, until='2c#seguro', paths=[dict(d='M80 30q-14 20 0 40M66 22q-22 28 0 56M52 14q-30 36 0 72', sw=2.4)]),
     glow('gb', 375, 252, '2c#siente', s=34, color='amber')]
cues.append(K('S2', '2d', n, [], fs=1.0))

# 2d — a human silhouette; the same glow inside it
n = [person('hu', 300, 300, '2d#Eso', color='blue', s=90), glow('gh', 300, 270, '2d#ser', s=46, color='amber'),
     # 2e — a calculator multiplies at full speed; inside it, darkness
     P('ca', 'calc', 660, 270, 150, '2e#calculadora', color='muted'),
     W.counter('cn', 660, 150, 98765432, '2e#multiplica', w=240, fs=30, dur=2.6),
     *noexp('dk', 660, 385, '2e#nadie', until='E2')]
n[-2]['x'] = 540
cues.append(K('2d', '2f', n, [], fs=1.0))

# 2f — the chip talks fluently: many message balls
n = chip('cp', 640, 380, '2f', s=60) + [person('rx', 880, 380, '2f', color='muted', s=40)]
lk = [link('cp_box', 'rx', '2f#hablar', color='teal', speed=1.1, comm=True), link('cp_box', 'rx', '2f#trampa', color='teal', speed=.8, comm=True)]
# 2g — two people: one sends a ball and both glow. Cut: the chip sends the same ball, its glow is a question
n += [person('a1', 150, 200, '2g', color='blue', s=56), person('a2', 400, 200, '2g', color='blue', s=56),
      glow('g1', 150, 185, '2g#sentía', s=34), glow('g2', 400, 185, '2g#sentía+0.5', s=34),
      N('qq', 'question', 620, 360, 40, 40, '2g#regla', color='amber')]
lk += [link('a1', 'a2', '2g#contaba', color='amber', comm=True)]
cues.append(K('2f', '2h', n, lk, fs=1.0))

# 2h — sentience: the glow inside the silhouette turns warm, then cold
n = [person('se', 480, 290, 0.05, color='blue', s=100),
     glow('gw', 480, 255, '2h#bien', s=54, color='amber', until='2h#mal'),
     glow('gc', 480, 255, '2h#mal', s=54, color='blue'),
     # 2i — what can suffer deserves care: a soft protective shield around it
     P('sh', 'shield', 480, 270, 300, '2i#cuidado', color='teal', alpha=.7)]
cues.append(K('2h', 'E2', n, [], fs=1.0))
