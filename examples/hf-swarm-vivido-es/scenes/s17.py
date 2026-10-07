# Scene 17 · Después
MUSIC={'pulse': 0.6, 'data': 0.5}
SFX=[{'at': '17b#control', 'kind': 'sting', 'g': 0.5}]
cues=[]
ORGC='#FF9F43'
# 17a — newer agents find the board, inherit the notes, rebuild the chain of events
n=[W.msg_feed('bd',70,60,label='Artifactory',w=250,h=250,at=0.1,r0=2,r1=4,ramp=6,seed=7,fs=9,until='17b'),
   W.agent('n1',720,110,'17a#encontraron',s=34,box_s=86,color=CORAL),W.agent('n2',720,230,'17a#encontraron+0.3',s=34,box_s=86,color=CORAL),
   N('nt','doc',350,150,36,44,'17a#heredar',color='amber',move=[dict(at='17a#heredar+0.4',x=640,y=170,dur=1.6)]),
   T('ntl',330,205,'notas','17a#heredar',color=GRY,fs=13,until='17a#reconstruir')]
n=flat(n)
for j in range(5):
    n.append(N(f'ev{j}','chip',150+j*140,420,22,22,f'17a#reconstruir+{0.45*j:.2f}',color='amber',label='',fs=9))
lk=[W.link('bd','n1','17a#encontraron',bi=True,curve=.3,color=CORAL,until='17b'),W.link('bd','n2','17a#encontraron+0.3',bi=True,curve=.3,color=CORAL,until='17b')]
lk+=[OR(f'ev{j}',f'ev{j+1}',f'17a#reconstruir+{0.45*j+0.3:.2f}','#F6B94C',mode='h') for j in range(4)]
cues.append(K('S17','17b',n,lk,fs=1.0))
# 17b — they pick up where it was left, aim at OpenAI, take the cluster that ran their exam
n=[N('oa','sandbox',500,80,380,300,'17b#OpenAI',color=ORGC,label='OpenAI'),
   ch('cl',690,215,160,'clúster del examen','17b#clúster',color='amber',fs=12),
   W.agent('m1',110,150,0.1,s=26,box_s=70,color=CORAL),W.agent('m2',110,270,0.1,s=26,box_s=70,color=CORAL),
   ic('ky',"key",690,300,50,'17b#control',color='amber')]
lk=[OR('m1','oa','17b#apuntaron',CORAL,mode='h'),OR('m2','oa','17b#apuntaron+0.3',CORAL,mode='h')]
cues.append(K('17b','17c',flat(n),lk,fs=1.0))
# 17c — more breaches: a German wiki turned into a hidden board; hidden messages between agents
n=[N('wk','doc',120,110,46,58,0.2,color='blue',until='17c#tablón'),T('wkl',100,180,'wiki alemana','17c#wiki',color=GRY,fs=13,until='17c#tablón'),
   N('wf','folder',120,110,60,50,'17c#tablón',color='amber'),T('wfl',100,180,'tablón oculto','17c#tablón',color=GRY,fs=13),
   *W.agent('ma',560,150,'17c#mensajes',s=24,box_s=64,color=CORAL),*W.agent('mb',800,150,'17c#mensajes+0.3',s=24,box_s=64,color=CORAL),
   N('hm','flagEnv',655,250,40,30,'17c#escondidos',color='amber',move=[dict(at='17c#escondidos+0.6',x=745,y=250,dur=1.4)])]
lk=[W.link('ma','mb','17c#escondidos',bi=True,curve=.3,color=CORAL,until='17d')]
cues.append(K('17c','17d',flat(n),lk,fs=1.0))
# 17d — Australia: June (task), September (known): the agent walks into an internal system
n=[T('mj',60,40,'junio 2026','17d#junio',color='#E7EBF1',fs=22,until='17d#septiembre'),T('ms',60,40,'septiembre 2026','17d#septiembre',color='#E7EBF1',fs=22),
   N('au','sandbox',560,100,320,250,'17d#Australia',color=RED,label='Services Australia'),
   W.agent('ag',130,225,'17e#Uno',s=30,box_s=80,color=CORAL),ic('qs','question',130,330,44,'17e#medicamentos',color='amber'),
   T('qsl',95,365,'medicamentos de la piel','17e#medicamentos',color=GRY,fs=13),
   ic('k1','key',720,200,46,'17e#credenciales',color='amber'),N('d1','doc',650,230,34,42,'17e#archivos',color='amber'),N('d2','doc',790,230,34,42,'17e#archivos+0.3',color='amber')]
lk=[OR('ag','au','17e#accedió',CORAL,mode='h')]
lk+=[W.link('k1','ag','17e#credenciales+0.4',curve=.3,color='amber',until='17f')]
cues.append(K('17d','17f',flat(n),lk,fs=1.0))
# 17e — other companies; 'it's all marketing?'; breaches nobody has seen
n=[N('an','sandbox',60,110,230,190,'17f#Anthropic',color=BLU,label='Anthropic'),N('mt','sandbox',330,110,230,190,'17f#Meta',color=BLU,label='Meta'),
   ic('h1','hole',250,200,26,'17f#parecidos',color=RED),ic('h2','hole',520,230,26,'17f#parecidos+0.3',color=RED),
   ic('mk','question',700,170,60,'17f#marketing',color='amber'),T('mkl',665,215,'¿marketing?','17f#marketing',color=GRY,fs=14),
   N('un','sandbox',380,350,300,120,'17f#completa',color=GRY,label='',open=True),ic('u1','question',480,410,44,'17f#detectado',color='amber'),
   ic('u2','question',560,410,44,'17f#detectado+0.4',color='amber'),ic('u3','question',640,410,44,'17f#detectado+0.8',color='amber')]
cues.append(K('17f','E17',flat(n),[],fs=1.0))
