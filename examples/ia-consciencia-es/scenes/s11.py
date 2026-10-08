# Scene 11 · Cierre
MUSIC = {'bells': 0.8, 'pad': 0.6}
INTENSITY = 0.35
cues = []

# 11a — the layered building again, with the loop on top
TX, TB = 300, 470
tw, TY = tower('t', TX, TB, '11a#hipótesis', step=0.15)
n = list(tw) + [P('lp', 'loop', TX, TY[4] - 70, 64, '11a#hipótesis+0.8', color='amber', blink=.5, bf=4)]
# 11b — the loop turns; the building and the brain side by side
n += [P('br', 'brain', 680, 270, 230, '11b#máquinas', color='amber'),
      # 11c — slow zoom towards the glow inside the brain
      glow('bg', 680, 265, '11c#enciende', s=80, color='amber')]
cm = [dict(at='11a', x=50, y=50, z=1), dict(at='11c#nosotros', x=50, y=50, z=1), dict(at='>11c', to='bg', z=2.6, dur=5.0)]
cues.append(K('11a', '11d', n, [], fs=1.0, cam=cm))

# 11d — the brain's glow and the chip's glow reflect each other as in a mirror
n = [P('br2', 'brain', 260, 270, 200, '11d', color='amber'), glow('g1', 260, 265, '11d', s=70, color='amber'),
     N('mx', 'bar', 478, 120, 4, 300, '11d#espejo', color='muted', fill=1, rx=0, alpha=.5)]
n += chip('cp', 700, 270, '11d', s=110, box=False) + [glow('g2', 700, 270, '11d#espejo', s=70, color='amber')]
for x in n: x['until'] = '11e'
# 11e — the counter from scene 1 comes back to the centre, its '?' blinking
n += [N('q', 'txt', 445, 200, 70, 110, '11e#número', color='#E7EBF1', fs=110, text='?', blink=.45, bf=3)]
cues.append(K('11d', '11f', n, [], fs=1.0))

# 11f — fade to black; credits and sources (plain-text sources go in a small world cue, as in ia-matematicas-es)
SRC = ['Fuentes',
       'Sam Harris con Cameron Berg · Making Sense, ep. 487 · 31 julio 2026',
       'David Chalmers · «Are LLMs conscious?» · Taormina, mayo 2023',
       'David Chalmers · «When we talk to AI, what are we talking to?» · UC Berkeley, 07 mayo 2026',
       'Thomas Nagel · «What Is It Like to Be a Bat?» · 1974  ·  Douglas Hofstadter · «I Am a Strange Loop» · 2007',
       'Noa Weiss · charla sobre consciencia en inteligencia artificial']
cues += [dict(a='seal', at='11f', until='E11', p=dict(text='Arkinos · Explainer Studio', sub='Arkinos @ oct 2026', scale=1.0, cy=150, ty=330, at=0.8,
              black=dict(at='E11-3', dur=3)), bg=True, fade=[1.4, 0]),
         dict(a='world', at='11f+1.5', until='E11-2', p=dict(fs=1.0, links=[], nodes=[
             N('src', 'ctxt', 40, 380, 880, 140, 0.2, color='#5EC8FF', fs=13, lines=SRC)]), bg=False, fade=[1.0, 2.0])]
