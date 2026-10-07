# Scene 1 · La aceleración
MUSIC = {'pad': 0.8, 'data': 0.5}
INTENSITY = 0.5
cues = []
# erdosproblems.com list: 14 rows (#721..#734); #728 is row 7
WX, WY, WW, RH = 640, 40, 250, 22
ROW0 = WY + 48
rc = lambda j: ROW0 + j * RH                       # centre y of row j
ITEMS = [dict(name=f'#{721 + j}') for j in range(14)]
ITEMS[-1] = dict(name='#734')
TLY = 488                                           # timeline bar
TX = dict(dic=80, ene=215, may=360, ago=520, sep=670, oct=830)
FLX = WX + WW + 8
n = [W.folder_view('erd', WX, WY, ITEMS, label='erdosproblems.com', w=WW, h=48 + 14 * RH + 8, rh=RH, fs=12, at='1a#web'),
     N('pe', 'person', 560, 110, 36, 62, '1a#Erdős', color='amber', cap='Erdős', capfs=13),
     N('tl', 'bar', 60, TLY, 840, 6, '1b#diciembre', color='muted', fill=1),
     ch('t_dic', TX['dic'], 514, 100, 'diciembre 2025', '1b#diciembre', color='muted'),
     # 1b — hobbyists + GPT-5.2 work on the list, #728 turns green and gets a seal
     N('hb', 'person', 60, 150, 36, 62, '1b#aficionados', color='blue', cap='aficionados', capfs=12, until='1c'),
     AN('g52', 190, 120, 'GPT-5.2', at='1b#GPT', color='blue', until='1c'),
     ic('sl', 'sigSeal', 585, rc(7), 30, '1b#comprobaron', color='teal'),
     ch('slc', 585, rc(7) + 28, 70, 'verificado', '1b#comprobaron+0.2', color='teal', fs=11)]
# grey placeholder flags next to every row, lit green as they are solved
for j in range(14):
    n.append(N(f'fg{j}', 'flag', FLX, rc(j) - 12, 20, 24, '1a#problemas+%.2f' % (0.05 * j), color='muted', dashed=True, until={7: '1b#Resolvieron', 13: '1e#Navier'}.get(j, {0: '1c#enero', 1: '1c#enero+0.3', 2: '1c#enero+0.6', 3: '1c#enero+0.9'}.get(j, '1c#mayo+%.2f' % (0.3 * (j - 4)) if j < 8 else '1c#mayo+%.2f' % (0.3 * (j - 5))))))
lit = {7: '1b#Resolvieron'}
lit.update({j: '1c#enero+%.1f' % (0.3 * j) for j in range(4)})
lit.update({j: '1c#mayo+%.1f' % (0.3 * i) for i, j in enumerate([4, 5, 6, 8, 9, 10, 11, 12, 13])})
for j, t in lit.items():
    n.append(N(f'fl{j}', 'flag', FLX, rc(j) - 12, 20, 24, t, color='teal', until=('1e#Navier' if j == 13 else None)))
n.append(N('fl13b', 'flag', FLX, rc(13) - 12, 20, 24, '1e#Navier', color='amber'))
n.append(ch('rev', 580, rc(13), 100, 'en revisión', '1e#revisando', color='amber', fs=11))
# timeline marks
n += [ch('t_ene', TX['ene'], 514, 100, 'enero 2026', '1c#enero', color='muted'),
      ch('t_may', TX['may'], 514, 100, 'mayo 2026', '1c#mayo', color='muted'),
      ch('t_ago', TX['ago'], 514, 100, 'agosto 2026', '1e#agosto', color='muted'),
      ch('t_sep', TX['sep'], 514, 120, 'septiembre 2026', '1e#septiembre', color='muted'),
      ch('t_oct', TX['oct'], 514, 100, 'octubre 2026', '1f#octubre', color='teal')]
# 1c — DeepMind walks the dates
n += [N('dm', 'agent', TX['ene'] - 16, 448, 32, 32, '1c#DeepMind', color='teal', tag='DeepMind', tagc='teal',
        move=[dict(at='1c#mayo', x=TX['may'] - 16, y=448, dur=2.0)], until='1d')]
n += [W.counter('cA', 70, 330, 1, '1b#Resolvieron', cap='problemas resueltos', w=200, dur=0.8, fs=54, until='1c#enero'),
      W.counter('cB', 70, 330, 5, '1c#enero', cap='problemas resueltos', w=200, dur=1.5, fs=54, until='1c#mayo+0.2', **{'from': 1}),
      W.counter('cB2', 70, 330, 14, '1c#mayo+0.2', cap='problemas resueltos', w=200, dur=3.0, fs=54, until='1e#cien', **{'from': 5}),
      ch('c4', 170, 305, 70, '+4', '1c#enero+0.4', color='teal', fs=13, until='1c#mayo'),
      ch('c9', 170, 305, 110, '9 de 353', '1c#mayo+0.2', color='teal', fs=13, until='1d')]
# 1d — OpenAI claims, three mathematicians approve
n += [N('ck', 'txt', 30, 30, 330, 32, '1d#veinte', color='teal', fs=24, type=9, text='20 mayo 2026', until='1e'),
      AN('oa', 60, 150, 'OpenAI', at='1d#OpenAI', color='blue', until='1e')]
for j, nm in enumerate(['Alon', 'Wood', 'Bloom']):
    y = 80 + 110 * j
    n += [N(f'p{j}', 'person', 340, y, 36, 62, f'1d#{nm}', color='amber', cap=nm, capfs=13, until='1e'),
          ic(f'ap{j}', 'okA', 410, y + 31, 30, f'1d#revisaron+{0.5 + 0.7 * j:.1f}', color='teal', until='1e')]
# 1e — Astra, then OpenAI in September; counter climbs to 100+
n += [N('as', 'agent', TX['ago'] - 16, 448, 32, 32, '1e#Astra', color='violet' if False else '#B58CFF', tag='Astra', tagc='#B58CFF', until='1f'),
      N('oa2', 'agent', TX['sep'] - 16, 448, 32, 32, '1e#septiembre', color='blue', tag='OpenAI', tagc='blue', until='1f'),
      W.counter('cC', 70, 330, 100, '1e#cien', cap='problemas abiertos resueltos', w=200, dur=2.0, fs=54, suf='+', until='1f#setecientos-0.3', **{'from': 14})]
# 1f — the same line, the agent grows, counter 10 -> 100 -> 722
n += [N('big', 'agent', TX['oct'] - 30, 430, 60, 60, '1f#En', color='teal', tag='OpenAI', tagc='teal'),
      W.counter('cE', 70, 330, 722, '1f#setecientos', cap='manuscritos', w=200, dur=2.5, fs=54, until='E1', **{'from': 10})]
lk = [link('g52', 'erd', '1b#Resolvieron', color='blue', bi=True, until='1c'),
      link('oa', 'p0', '1d#OpenAI+0.6', color='blue', comm=True, bi=True, until='1e'),
      link('oa', 'p1', '1d#OpenAI+1.0', color='blue', comm=True, bi=True, until='1e'),
      link('oa', 'p2', '1d#OpenAI+1.4', color='blue', comm=True, bi=True, until='1e')]
cues.append(K('S1', 'E1', n, lk, fs=1.0))
