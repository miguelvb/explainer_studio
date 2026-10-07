# Scene 14 · Se apagan
MUSIC={'cinema': 0.8, 'bells': 0.5}
MOOD='tense'
SFX=[{'at': '14a#desaparecieron', 'kind': 'poweroff', 'g': 0.8},
 {'at': '14a#desaparecieron', 'kind': 'heartbeat', 'g': 0.5}]
cues=[]
n=[T('ck',30,28,'12 julio 01:30','14a#una',color='#E7EBF1',fs=26,until='14a#amanecer')]
for i in range(40):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'g{i}',x,y,0.1,s=28,color=RED)
    n+=SA(f'd{i}',x,y,'14a#detuvo',s=28,color='#8C96A4',alpha=.9)
for i in range(11):
    pass
n=[x for x in flat(n) if not x['id'].startswith('d')]
for i in range(40): n[1+i]['until']='14a#detuvo'
for i in range(40):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'd{i}',x,y,'14a#detuvo',s=28,color='#566170',alpha=.9)
for i in range(11):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'k{i}',x,y,'14a#coordinadores',s=28,color='#F6B94C',until=f'14a#desaparecieron+{0.2*i:.1f}')
n+=[T('ck2',30,28,'05:00','14a#amanecer',color='#E7EBF1',fs=26)]
cues.append(K('S14','14b',n,[],fs=1.0))
# 14b — nobody knows why: not out of budget, something outside the exam
n=[W.agent_named('ag',60,110,'',at=0.1,w=120,h=160,color='blue',fs=1,alpha=.5),
   *BAR('bd',60,300,120,.92,0.2,GRN,label='presupuesto'),
   N('ou','sandbox',420,70,400,300,'14b#algo',color=GRY,label='',open=True,alpha=.8),
   N('qm','question',590,160,100,100,'14b#ajeno',color='amber'),T('ou2',500,395,'ajeno al examen','14b#ajeno',color=GRY,fs=14)]
lk=[W.link('ou','ag','14b#apagó',curve=.2,color='amber',dashed=True,solid=True)]
cues.append(K('14b','14c',n,lk,fs=1.0))
n=[N('hf','hfbox',60,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('fl','flFly',700,150,50,76,0.1,color='amber'),
   N('ex','exam',560,60,140,200,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   W.msg_feed('bd',60,200,label='Artifactory',w=300,h=240,at='14c#no',r0=2,r1=6,ramp=3,seed=8,fs=9),
   ic('xl','cross',640,170,50,'14c#no+0.8',color=RED)]
lk=[W.link('bd','fl','14c#aprobar',curve=.2,color=GRY,dashed=True,solid=True),W.link('hf','bd',0.4,curve=.1,color='amber',solid=True)]
cues.append(K('14c','14d',n,lk,fs=1.0))
n=[T('ck',30,28,'13 julio','14d#trece',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,100,230,80,0.1,color='red',label='Hugging Face',fs=16),
   ic('lc','key',330,128,40,'14d#cortó',color=RED),
   W.agent_named('ag',500,70,'',at='14d#notaron',w=110,h=150,color='blue',fs=10),
   N('er','chip',380,150,70,26,'14d#claves',color=RED,label='401',fs=18),
   N('ms','chip',420,320,520,26,'14d#avisar',color='amber',label='DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation',fs=9,move=[dict(at='14d#avisar+1',x=420,y=320,dur=.1)]),
   W.msg_feed('bd',50,230,label='Artifactory',w=280,h=230,at='14d#avisar',r0=2,r1=4,ramp=3,seed=3,fs=9)]
lk=[W.link('hf','ag','14d#cortó',curve=.12,color=RED,lock=True,solid=True),W.link('ag','bd','14d#avisar',curve=.2,color='amber',solid=True)]
cues.append(K('14d','E14',n,lk,fs=1.0))

