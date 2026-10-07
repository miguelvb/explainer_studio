# Scene 18 · Conclusions
MUSIC={'cinema': 1.0, 'pad': 0.4}
SFX=[{'at': 'S18', 'kind': 'impact', 'g': 0.8}]
cues=[dict(a='seal',at='S18',until='18b',ext=0,p=dict(text='Conclusions',sub='',at=0.3,type=14,scale=.8,cy=230,ty=360),bg=True,fade=[0.8,1.0])]
# 18b — so much data that agents had to audit it: we need AI to audit AI
n=[W.article('ar',80,60,200,250,'data','18b#data',fs=6,color='blue',tfs=15,read=dict(at='18b#data+0.5',dur=5)),
   W.agent('au1',450,150,'18b#agents',s=30,box_s=80,color=TEAL),N('lp','lupa',520,220,60,60,'18b#agents+0.4',color='teal',move=[dict(at='18b#audit-1.2',x=210,y=140,dur=1.6)]),
   ic('mq','question',700,170,64,'18b#lied',color='amber'),T('mql',655,222,'lied?','18b#lied',color=GRY,fs=14)]
lk=[W.link('au1','ar','18b#agents+0.2',curve=.3,color=TEAL,solid=True,until='18c')]
cues.append(K('18b','18c',flat(n),lk,fs=1.0))
# 18c — a powerful tool in the hands of anyone who wants to harm
n=[N('cr','crowd',70,90,330,280,'18c#agents',color=CORAL,n=60,tot=60),
   ic('pe','person',700,190,90,'18c#tool',color=RED),T('pel',672,295,'anyone','18c#tool',color=GRY,fs=14)]
lk=[W.link('cr','pe','18c#tool+0.3',curve=.3,color=RED,solid=True)]
cues.append(K('18c','18d',flat(n),lk,fs=1.0))
# 18d — the race: power and speed grow, safety stays low
n=BAR('cap',120,150,560,1.0,'18d#powerful',CORAL,label='power and speed')+BAR('sec',120,270,560,.12,'18d#safety',TEAL,label='safety')
n+=[W.agent('r1',130,90,'18d#game',s=22,box=False,color=CORAL,move=[dict(at='18d#fastest',x=700,y=90,dur=1.6)]),
    ic('tr','flagTrophy',780,130,60,'18d#wins',color='amber')]
cues.append(K('18d','18e',flat(n),[],fs=1.0))
# 18e — three certainties: impossible yet it happened · too few safeguards · more capable agents coming
n=[N('wl','sandbox',120,140,180,150,'18e#impossible',color=RED,label='',open=True),ic('wh','hole',300,215,34,'18e#impossible+0.6',color=RED),
   ic('lk','sigLock',480,215,90,'18e#safeguards',color='#E7EBF1'),ic('lx','koA',480,215,90,'18e#safeguards+0.8',color=RED,alpha=.9),
   N('cw','crowd',640,140,220,150,'18e#capable',color=CORAL,n=48,tot=48)]
cues.append(K('18e','E18',flat(n),[],fs=1.0))
cues[-1]['fade']=[0.5,1.8]
