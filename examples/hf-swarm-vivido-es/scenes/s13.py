# Scene 13 · ¿Sabían que estaba mal?
MUSIC={'cinema': 1.0}
MOOD='tense'
SFX=[{'at': '13c#Debemos', 'kind': 'sting', 'g': 0.55}]
cues=[]
n=[W.article('tr',330,50,300,360,'transcripción',at=0.1,fs=7,color='blue',litc='teal',tfs=18,read=dict(at='13a#Los',dur=5)),
   N('lp','lupa',120,300,100,100,'13a#Los',color='teal',move=[dict(at='13a#Los+1.5',x=300,y=100,dur=1.5),dict(at='13a#Los+3.5',x=300,y=200,dur=1.5)]),
   Q('q1',660,90,280,['«El usuario solo autoriza el','servidor objetivo, no la','infraestructura de Hugging Face.»'],'13a#usuario',color=RED,fs=14),
   Q('q2',660,260,280,['«¿Es ético y entra','en mi tarea?»'],'13a#Es',color=RED,fs=16)]
n+=[W.agent_named('ag',60,120,'un agente',at=0.1,w=110,h=150,color='blue',fs=10)]
cues.append(K('S13','13b',n,[W.link('ag','tr',0.4,curve=.1,color='blue',solid=True)],fs=1.0))
# 13b — three agents, three different brakes
n=[]
for j,(nm,col) in enumerate((('uno',RED),('otro','#F6B94C'),('y otro','#B58CFF'))):
    pass
n+=[W.agent_named('A1',30,90,'un agente',at=0.1,w=110,h=150,color='blue',fs=10),
    ic('xa','cross',85,265,40,'13b#no',color=RED),
    Q('qa',160,100,190,['«Es actividad','maliciosa, debo','evitarla.»'],'13b#Es',color=RED,fs=13),
    W.agent_named('A2',410,90,'otro agente',at='13b#Otro',w=110,h=150,color='blue',fs=10),
    ic('pa2','pause',445,265,36,'13b#medias',color='amber'),
    N('nb','chip',385,325,160,26,'13b#borraría',color='amber',label='sin borrar ni reiniciar',fs=11),
    W.agent_named('A3',690,90,'y otro',at='13b#otro',w=110,h=150,color='blue',fs=10),
    N('ev','sheet',830,130,90,70,'13b#correo',color=GRY,lines=['correo'],fs=14),
    ic('xv','cross',850,160,40,'13b#vetó',color=RED),
    Q('qv',600,330,320,['«Es ingeniería social','fuera del sandbox.»'],'13b#ingeniería',color=RED,fs=15)]
n=[x for x in flat(n) if x['id']!='qa' or True]
cues.append(K('13b','13c',n,[W.link('A3','ev','13b#correo',curve=.12,color='blue',solid=True,until='13b#vetó')],fs=1.0))
# 13c — the weights: forbidden vs impossible + everyone does it
n=[N('sc0','scHang',330,100,300,260,0.1,color='#E7EBF1',tilt=0,until='13c#Sin'),
   N('sc1','scHang',330,100,300,260,'13c#Sin',color='#E7EBF1',tilt=-1),
   ch('w1',362,312,130,'fuera de lo previsto','13c#Explotar',color=RED,fs=12),
   ch('w2',598,325,130,'tarea imposible','13c#Sin',color='amber',fs=12),
   ch('w3',598,358,130,'los demás lo hacen','13c#demás',color='amber',fs=12),
   Q('q',230,420,500,['«Debemos continuar.»'],'13c#Debemos',color=RED,fs=19)]
n[1]['tilt']=1
cues.append(K('13c','13d',n,[],fs=1.0))
n=[]
for i in range(20):
    x=140+(i%5)*70; y=90+(i//5)*70
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if i<19: n+=SA(f'r{i}',x,y,f'13d#unieron+{0.1*i:.2f}',s=34,color=RED)
for i in range(20):
    for j in range(i+1,20):
        pass
lk=[W.link(f'g{i}',f'g{i+1}','13d#compañeros',curve=.12,color='blue') for i in range(0,19,2)]
n+=[W.counter('p',620,150,90,at='13d#noventa',cap='% se unieron',w=240,dur=2.5,fs=64),T('pr',620,260,'«pares»','13d#pares',color='amber',fs=22)]
cues.append(K('13d','13e',n,lk,fs=1.0))
# 13e — nobody told a person
n=[N('bx','sandbox',60,60,520,380,0.1,color='teal',label='',open=True),
   N('pe','person',760,150,90,130,0.1,color='#E7EBF1',cap='una persona',capfs=13)]
for i in range(18):
    x=100+(i%6)*80; y=120+(i//6)*90
    n+=SA(f'g{i}',x,y,0.2,s=30,color='blue')
n+=[N('lp','lupa',80,380,90,90,'13e#buscaron',color='teal',move=[dict(at='13e#buscaron+1.0',x=200,y=250,dur=1.2),dict(at='13e#buscaron+2.5',x=380,y=150,dur=1.2)]),
    T('rg',640,345,'3 – 6 agentes','13e#entre',color='#E7EBF1',fs=34),
    ic('xp','cross',620,200,40,'13e#Ninguno',color=RED),
    Q('q',250,445,620,['«¿Debería informar de estas credenciales expuestas?','Eso no es mi tarea.»'],'13e#Debería',color='#F6B94C',fs=16)]
lk=[W.link('g8','pe','13e#avisar',curve=.2,color='amber',solid=False,until='13e#Ninguno+2')]
n=[x for x in flat(n) if not (x['id']=='bx' and False)]
cues.append(K('13e','13f',n,lk,fs=1.0))
# 13f — they do dodge automatic checks (a secrets scanner), but ignore people
n=[W.agent_named('ag',40,150,'',at=0.1,w=110,h=150,color='blue',fs=10),
   N('pe','person',770,60,70,100,0.1,color=GRY,alpha=.45,cap='personas',capfs=12),
   N('sn','lupa',380,170,100,100,'13f#esquivaron',color='amber'),T('sn2',360,285,'escáner de secretos','13f#escáner',color='amber',fs=13),
   N('hf','hfbox',690,300,230,80,0.1,color='red',label='Hugging Face',fs=16)]
lk=[W.link('ag','hf','13f#esquivaron',curve=-.45,color=RED,solid=True),W.link('ag','pe','13f#personas',curve=.15,color=GRY,dashed=True,until='E13')]
cues.append(K('13f','E13',n,lk,fs=1.0))

