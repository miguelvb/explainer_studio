# Scene 18 · Conclusiones
MUSIC={'cinema': 1.0, 'pad': 0.4}
SFX=[{'at': 'S18', 'kind': 'impact', 'g': 0.8}]
cues=[dict(a='seal',at='S18',until='18b',ext=0,p=dict(text='Conclusiones',sub='',at=0.3,type=14,scale=.8,cy=230,ty=360),bg=True,fade=[0.8,1.0])]
# 18b — so much data that agents had to audit it: we need AI to audit AI
n=[W.article('ar',80,60,200,250,'datos','18b#datos',fs=6,color='blue',tfs=15,read=dict(at='18b#datos+0.5',dur=5)),
   W.agent('au1',450,150,'18b#agentes',s=30,box_s=80,color=TEAL),N('lp','lupa',520,220,60,60,'18b#agentes+0.4',color='teal',move=[dict(at='18b#auditarla-1.2',x=210,y=140,dur=1.6)]),
   ic('mq','question',700,170,64,'18b#mintieron',color='amber'),T('mql',655,222,'¿mintieron?','18b#mintieron',color=GRY,fs=14)]
lk=[W.link('au1','ar','18b#agentes+0.2',curve=.3,color=TEAL,solid=True,until='18c')]
cues.append(K('18b','18c',flat(n),lk,fs=1.0))
# 18c — a powerful tool in the hands of anyone who wants to harm
n=[N('cr','crowd',70,90,330,280,'18c#agentes',color=CORAL,n=60,tot=60),
   ic('pe','person',700,190,90,'18c#cualquiera' if False else '18c#herramienta',color=RED),T('pel',672,295,'cualquiera','18c#herramienta',color=GRY,fs=14)]
lk=[W.link('cr','pe','18c#herramienta+0.3',curve=.3,color=RED,solid=True)]
cues.append(K('18c','18d',flat(n),lk,fs=1.0))
# 18d — the race: power and speed grow, safety stays low
n=BAR('cap',120,150,560,1.0,'18d#potente',CORAL,label='potencia y velocidad')+BAR('sec',120,270,560,.12,'18d#seguridad',TEAL,label='seguridad')
n+=[W.agent('r1',130,90,'18d#juego',s=22,box=False,color=CORAL,move=[dict(at='18d#rápida',x=700,y=90,dur=1.6)]),
    ic('tr','flagTrophy',780,130,60,'18d#gana',color='amber')]
cues.append(K('18d','18e',flat(n),[],fs=1.0))
# 18e — three certainties: impossible yet it happened · too few safeguards · more capable agents coming
n=[N('wl','sandbox',120,140,180,150,'18e#imposible',color=RED,label='',open=True),ic('wh','hole',300,215,34,'18e#imposible+0.6',color=RED),
   ic('lk','sigLock',480,215,90,'18e#salvaguardas',color='#E7EBF1'),ic('lx','koA',480,215,90,'18e#salvaguardas+0.8',color=RED,alpha=.9),
   N('cw','crowd',640,140,220,150,'18e#capaces',color=CORAL,n=48,tot=48)]
cues.append(K('18e','E18',flat(n),[],fs=1.0))
cues[-1]['fade']=[0.5,1.8]
