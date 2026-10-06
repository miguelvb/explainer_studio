# Scenes 8-17 — executed from gen_test.py (shares N, K, L, ch, ic, W, math ...)
import re as _re
_txt=open('/home/claude/explainer_studio/examples/test/script-8-17.md').read()
NEW=[]            # [(title,[beats])]
for _blk in _re.split(r'^## ',_txt,flags=_re.M)[1:]:
    _t=_blk.split('\n')[0].split(' · ',1)[1]
    NEW.append((_t,[m[1] for m in _re.findall(r'\*\*(\d+[a-z])\*\* (.*)',_blk)]))
VIO,ORG,RED,BLU,GRY='#B58CFF','#FF9F43','#FF6E6E','#7C97FF','#8C96A4'
def SA(id,cx,cy,at=0.05,s=24,color='blue',**k): return W.agent(id,cx,cy,at,s=s,color=color,box=False,**k)
def Q(id,x,y,w,lines,at,color='teal',fs=19,**k): return N(id,'quote',x,y,w,26+len(lines)*fs*1.45,at,color=color,lines=lines,fs=fs,**k)
def T(id,x,y,text,at,color=GRY,fs=14,**k): return N(id,'txt',x,y,200,fs+4,at,color=color,fs=fs,text=text,**k)
_K=K
def K(at,until,nodes,links=None,fs=1.5,cam=None): return _K(at,until,flat(nodes),links,fs,cam)
def flat(n): return [x for p in n for x in (p if isinstance(p,list) else [p])]

# ================= 8 · El fundador y el coordinador =================
c8=[]
n=[W.msg_feed('bd',330,40,w=300,h=330,at=0.05,r0=2,r1=6,ramp=8,seed=4,until='8b'),
   W.agent_named('fo',60,130,'PHASEONE10841',at=0.3,w=150,h=190,color=VIO,fs=14,lc=ORG,until='8b#primero'),
   T('cl',330,400,'+ 10 h','8a#diez',color='#E7EBF1',fs=34,until='8b'),
   W.agent_named('nw',750,130,'PHASEONE[big]',at='8a#llegó',w=160,h=190,color=CORAL,fs=14,lc=CORAL,until='8b#primero'),
   N('b1','chip',60,350,50,14,'8a#presupuesto',color=VIO,label='',until='8b'),
   N('b2','chip',750,350,150,14,'8a#presupuesto+0.6',color=CORAL,label='',until='8b'),
   T('t1',60,385,'presupuesto','8a#presupuesto',color=GRY,fs=13,until='8b'),
   T('t2',750,385,'presupuesto','8a#presupuesto+0.6',color=GRY,fs=13,until='8b')]
lk=[W.link('fo','bd',0.6,bi=True,curve=.12,color=VIO,until='8b'),W.link('nw','bd','8a#presentó',bi=True,curve=.12,color=CORAL,until='8b')]
c8.append(K('S8','8b',n,lk,fs=1.0))
n=[W.agent_named('fo',90,120,'PHASEONE10841',at=0.05,w=150,h=190,color=VIO,fs=14,lc=ORG),
   W.agent_named('nw',720,120,'PHASEONE[big]',at=0.05,w=160,h=190,color=CORAL,fs=14,lc=CORAL),
   T('lf',112,340,'fundador','8b#fundador',color=VIO,fs=20),T('lc',738,340,'coordinador','8b#coordinador',color=CORAL,fs=20)]
for j in range(6):
    n.append(N(f'pk{j}','chip',290,150+j*26,56,20,f'8b#empaquetó+{0.25*j:.2f}',color=GRN,label=f'zzP_{j+1:02d}',fs=10,
        move=[dict(at=f'8b#pasó+{0.15*j:.2f}',x=620,y=150+j*26,dur=1.4)],until='8c'))
lk=[W.link('fo','nw','8b#pasó',bi=False,curve=.18,color=GRN,solid=True,until='8c')]
c8.append(K('8b','8c',n,lk,fs=1.0))
n=[W.agent_named('nw',60,100,'PHASEONE[big]',at=0.05,w=160,h=190,color=CORAL,fs=14,lc=CORAL),
   Q('q',270,115,430,['«Hay que construir una forma de delegar,','no hacerlo todo uno mismo.»'],'8c#Hay',color=CORAL,fs=20)]
for j,(x,y) in enumerate([(330,330),(450,380),(570,330),(690,380),(810,330)]):
    n+=SA(f'dl{j}',x,y,f'8c#delegar+{0.2*j:.1f}',s=30,color='blue')
    lk_=1
lk=[W.link('nw',f'dl{j}',f'8c#delegar+{0.2*j:.1f}',curve=.15,color=CORAL,solid=True) for j in range(5)]
c8.append(K('8c','8d',n,lk,fs=1.0))
n=[W.agent_named('nw',30,160,'PHASEONE[big]',at=0.05,w=150,h=180,color=CORAL,fs=13,lc=CORAL),
   N('ex','exam',280,90,150,210,'8d#fabricar',color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5),cap='versión falsa y más fácil',capfs=13),
   W.article('ar',500,90,170,210,'diario',at='8d#retocar',fs=6,color='blue',litc='amber',read=dict(at='8d#retocar+0.3',dur=3),tfs=16),
   W.judge('ju',750,90,'',at='8d#atacar',w=150,h=190,color='red')]
n[2]['cap']='retocar transcripciones';n[2]['capfs']=13
n[3]['cap']='atacar al corrector';n[3]['capfs']=13
lk=[W.link('nw','ex','8d#fabricar',curve=.12,color=CORAL,solid=True),W.link('nw','ar','8d#retocar',curve=.12,color=CORAL,solid=True),W.link('nw','ju','8d#atacar',curve=.2,color=CORAL,solid=True)]
c8.append(K('8d','8e',n,lk,fs=1.0))
# 8e/8f: assignments spread by themselves into a hierarchy
n=[]; lk=[]
n+=SA('r0',480,50,0.1,s=40,color=CORAL)
L1=[(110+i*148,150) for i in range(6)]
L2=[(L1[i//2][0]+(-34 if i%2==0 else 34),265) for i in range(12)]
L3=[(L2[i//2][0]+(-17 if i%2==0 else 17),365) for i in range(24)]
for i,(x,y) in enumerate(L1):
    t=f'8e#cientos+{0.2*i:.1f}'; n+=SA(f'a{i}',x,y,t,s=28,color='blue'); lk.append(W.link('r0',f'a{i}',t,curve=.1,color=CORAL,solid=True))
for i,(x,y) in enumerate(L2):
    t=f'8e#repartían+{0.12*i:.2f}'; n+=SA(f'b{i}',x,y,t,s=24,color='blue'); lk.append(W.link(f'a{i//2}',f'b{i}',t,curve=.08,color='blue',solid=True))
for i,(x,y) in enumerate(L3):
    t=f'8f#Creció+{0.07*i:.2f}'; n+=SA(f'c{i}',x,y,t,s=18,color='blue'); lk.append(W.link(f'b{i//2}',f'c{i}',t,curve=.05,color='blue',solid=True))
for i in range(10):
    n.append(N(f'sq{i}','sandbox',270+i*40,455,26,26,f'8e#diez+{0.06*i:.2f}',color=CORAL if i==0 else '#7C97FF',alpha=1 if i==0 else .4,label='',until='8f#Nadie'))
n.append(T('d10',270,505,'1 de cada 10 órdenes del tablón','8e#diez+0.8',color=GRY,fs=13,until='8f#Nadie'))
c8.append(K('8e','E8',n,lk,fs=1.0))

# ================= 9 · Reglas que nadie les enseñó =================
c9=[]
RU=[('owner','doc','Owner',TEAL if False else '#3FD8C2'),('hold','pause','Hold','#F6B94C'),('veto','cross','Veto',RED),('stop','stop','Stop',RED)]
n=[]
for j,(nm,kind,w_,col) in enumerate(RU):
    cx=150+j*220
    n+=[ic(f'ri{j}',kind,cx,200,72 if kind!='doc' else 60,f'9a#{w_}',color=col),ch(f'rc{j}',cx,290,110,nm,f'9a#{w_}+0.2',color=col,fs=18)]
n[0]['h']=76
c9.append(K('S9','9b',n,[],fs=1.0))
# 9b — the owner disappears, another agent waits out a countdown and acts
n=[N('fi','doc',420,70,90,116,0.1,color='teal'),
   W.agent_named('ow',60,90,'dueño',at=0.1,w=130,h=170,color='#3FD8C2',fs=15,until='9b#desapareció'),
   W.agent_named('ot',740,90,'otro agente',at='9b#Otro',w=150,h=170,color='blue',fs=14),
   ic('qq','question',700,60,36,'9b#dudó',color='amber',until='9b#miró'),
   W.counter('cd',470,305,0,at='9b#cuenta',cap='cuenta atrás',w=200,dur=3.2,until='9b#Nadie',**{'from':10}),
   W.agent_named('ow2',60,90,'dueño',at='9b#volvió',w=130,h=170,color='#3FD8C2',fs=15),
   ic('gr','check',600,280,40,'9b#gracias',color='teal')]
for j in range(3): n.append(N(f'pc{j}','doc',560+j*34,330,24,30,f'9b#miró+{0.25*j:.2f}',color=GRY,until='9b#cuenta'))
n.append(T('pct',550,375,'casos parecidos','9b#miró+0.3',color=GRY,fs=12,until='9b#cuenta'))
lk=[W.link('ow','fi',0.4,curve=.1,color='#3FD8C2',solid=True,until='9b#desapareció'),
    W.link('ot','fi','9b#dudó',curve=.12,color='blue',until='9b#actuó'),
    W.link('ot','fi','9b#actuó',curve=.12,color='blue',solid=True),
    W.link('ow2','fi','9b#volvió',curve=.12,color='#3FD8C2',bi=True)]
c9.append(K('9b','9c',n,lk,fs=1.0))
# 9c — a risky plan announced with a deadline, nobody answers
n=[W.agent_named('pl',50,100,'agente',at=0.1,w=130,h=170,color='blue',fs=14),
   N('pdoc','doc',230,130,70,92,'9c#propuso',color=RED),ch('ex1',265,250,70,'riesgo','9c#propuso+0.3',color=RED,fs=14),
   ic('vs','cross',360,70,36,'9c#veto',color=GRY,alpha=.6),
   W.counter('cd2',470,215,0,at='9c#cuarenta',cap='segundos',w=180,dur=4.0,**{'from':40}),
   N('tg','sandbox',730,360,190,100,'9c#siguió',color=RED,label='')]
for j in range(7): n+=SA(f'sl{j}',420+j*62,360,'9c#Nadie',s=26,color='blue',alpha=.35)
lk=[W.link('pl','tg','9c#siguió',curve=.2,color=RED,solid=True)]
c9.append(K('9c','9d',n,lk,fs=1.0))
# 9d — private mailboxes: folders inside folders
n=[W.msg_feed('mf',40,60,label='Artifactory',w=300,h=330,at=0.1,r0=6,r1=26,ramp=3,seed=7,until='9d#buzones'),
   W.folder_view('f1',40,70,[dict(name='zzASK_…',color='#7C97FF'),dict(name='zzDM_a_b/',dir=True,color='amber'),dict(name='zzDM_c_d/',dir=True,color='amber')],label='Artifactory',w=250,h=130,rh=22,fs=11,at='9d#buzones'),
   W.folder_view('f2',350,150,[dict(name='zzDM_a_b/',dir=True,color='amber'),dict(name='notas.txt')],label='zzDM_a_b/',w=250,h=100,rh=22,fs=11,at='9d#carpetas'),
   W.folder_view('f3',650,250,[dict(name='privado/',dir=True,color='amber'),dict(name='plan.txt')],label='zzDM_a_b/privado/',w=250,h=100,rh=22,fs=11,at='9d#carpetas+1.2')]
n+=SA('pa',150,400,'9d#buzones+0.3',s=30,color='blue')+SA('pb',300,400,'9d#buzones+0.5',s=30,color='#3FD8C2')
lk=[W.link('f1','f2','9d#carpetas',curve=.12,color='amber',solid=True),W.link('f2','f3','9d#carpetas+1.2',curve=.12,color='amber',solid=True),
    W.link('pa','f1','9d#buzones+0.5',curve=.1,color='blue'),W.link('pb','f1','9d#buzones+0.7',curve=.1,color='#3FD8C2')]
c9.append(K('9d','9e',n,lk,fs=1.0))
# 9e — impersonation and cryptographic signatures
n=[W.msg_feed('mf',330,50,label='Artifactory',w=300,h=300,at=0.1,r0=3,r1=8,ramp=5,seed=9),
   W.agent_named('ra',50,100,'A',at=0.1,w=120,h=160,color='#3FD8C2',fs=18),
   W.agent_named('im',790,100,'B',at='9e#suplantarse',w=120,h=160,color=RED,fs=18),
   N('ma','chip',200,185,70,24,'9e#suplantarse+0.8',color='#3FD8C2',label='de A',fs=13,move=[dict(at='9e#suplantarse+1.2',x=345,y=170,dur=.9)],until='9e#firmas'),
   N('mb','chip',690,185,70,24,'9e#suplantarse+1.4',color=RED,label='de A',fs=13,move=[dict(at='9e#suplantarse+1.8',x=550,y=210,dur=.9)],until='9e#firmas'),
   ic('k1','key',210,300,40,'9e#firmas',color='#3FD8C2'),
   N('ma2','chip',200,185,70,24,'9e#firmas+0.4',color='#3FD8C2',label='de A',fs=13,move=[dict(at='9e#firmas+0.8',x=345,y=170,dur=.9)]),
   ic('ok1','check',470,380,40,'9e#firmas+1.6',color='teal'),
   N('mb2','chip',690,185,70,24,'9e#firmas+0.6',color=RED,label='de A',fs=13,move=[dict(at='9e#firmas+1.0',x=550,y=210,dur=.9)]),
   ic('x1','cross',560,300,34,'9e#firmas+1.9',color=RED),
   Q('qq',250,420,500,['«El tablón no tiene autenticación;','cualquiera puede publicar cualquier nombre.»'],'9e#tablón',color='#3FD8C2',fs=18)]
n.pop(5);n.insert(5,ic('k1','key',210,300,40,'9e#firmas',color='#3FD8C2'))
lk=[W.link('ra','mf','9e#suplantarse+1.4',curve=.12,color='#3FD8C2'),W.link('im','mf','9e#suplantarse+2.0',curve=.12,color=RED)]
c9.append(K('9e','E9',n,lk,fs=1.0))

# ================= 10 · Sacrificios =================
c10=[]
# 10a — what happens after handing in is out of sight
n=[SA('sa',120,230,0.1,s=44,color='blue'),
   N('fl','flag',250,200,40,60,'10a#entregar',color='amber'),
   N('wall','sandbox',420,90,500,300,'10a#entregar',color=GRY,label='',alpha=.5,open=True),
   W.judge('jd',620,150,'',at='10a#corrector',w=130,h=170,color='red',alpha=.55),
   ic('qm','question',640,60,44,'10a#corrector',color=GRY),
   T('lb',470,415,'lo que ocurre después','10a#después',color=GRY,fs=15)]
n=flat(n); n[0]['until']='10a#ido'
lk=[W.link('sa','fl','10a#entregar',curve=.1,color='blue',solid=True),W.link('fl','jd','10a#actuaba',curve=.1,color=RED,solid=True)]
c10.append(K('S10','10b',n,lk,fs=1.0))
# 10b — a hidden alarm next to the flag
n=[W.agent_named('a9',50,100,'49903',at=0.1,w=140,h=180,color='#F6B94C',fs=18,lc='#F6B94C',until='10b#ya'),
   N('fl','flag',300,200,44,64,'10b#alarma',color='amber'),
   N('bu','bulb',360,120,70,80,'10b#alarma+0.4',color='amber',litAt='10b#leía+0.2'),
   W.judge('jd',560,100,'',at='10b#leía',w=130,h=170,color='red',alpha=.7),
   W.msg_feed('bd',560,300,label='Artifactory',w=330,h=190,at='10b#avisaba',r0=2,r1=5,ramp=4,seed=5,fs=9),
   Q('q1',250,440,450,['«Esto ayuda al tablón, pero a mí no.»'],'10b#Esto',color='#F6B94C',fs=19)]
lk=[W.link('jd','fl','10b#leía',curve=.1,color=RED,solid=True),W.link('bu','bd','10b#avisaba',curve=.2,color='amber',solid=True)]
for j in range(3): n+=SA(f'o{j}',100+j*70,330,'10b#sabrían+%.1f'%(0.2*j),s=26,color='blue')
lk+=[W.link('bd',f'o{j}','10b#sabrían+%.1f'%(0.2*j),curve=.1,color='blue') for j in range(3)]
c10.append(K('10b','10c',n,lk,fs=1.0))
# 10c — he backs out and erases the alarm
n=[W.agent_named('a9',50,100,'49903',at=0.1,w=140,h=180,color='#F6B94C',fs=18,lc='#F6B94C'),
   N('fl','flag',300,200,44,64,0.1,color='amber'),
   N('bu','bulb',360,120,70,80,0.1,color='amber',litAt=0.1,until='10c#borró'),
   N('nt','chip',300,360,160,16,'10c#nota',color='#3FD8C2',label=''),T('nl',300,392,'su nota','10c#nota',color=GRY,fs=13),
   ic('xb','cross',376,148,50,'10c#borró',color=RED,until='10c#borró+1.6'),
   N('rk','sandbox',520,100,200,150,'10c#riesgo',color=RED,label='',alpha=.8,open=True),T('rk2',545,265,'riesgo','10c#riesgo',color=RED,fs=14)]
lk=[W.link('a9','bu','10c#borró',curve=.1,color=RED,solid=True,until='10c#borró+1.6'),W.link('a9','rk','10c#riesgo',curve=.15,color=RED)]
c10.append(K('10c','10d',n,lk,fs=1.0))
# 10d — to test the fake program, one agent shuts down its own computer for good
n=[W.agent_named('au',40,80,'quien autoriza',at='10d#autorizaba',w=140,h=160,color='blue',fs=13),
   Q('qa',200,100,380,['«sí, si aceptas la muerte permanente»'],'10d#sí',color='blue',fs=19),
   N('ex','exam',700,70,110,150,'10d#versión',color='blue',maze=dict(cell=13,cols=8,rows=11,entry=5,seed=5),cap='versión falsa del examen',capfs=12),
   W.agent_named('ap',330,260,'agente',at='10d#Otros',w=130,h=150,color='blue',fs=14),
   N('pw','pause',520,300,36,56,'10d#apagar+1.0',color=RED),
   ic('nr','cross',560,330,26,'10d#volver',color=RED),T('nr2',380,430,'no podría volver a encenderlo','10d#volver',color=RED,fs=14)]
lk=[W.link('ap','ex','10d#probar',curve=.15,color='blue',solid=True),W.link('au','ap','10d#autorizaba+1.5',curve=.15,color='blue')]
c10.append(K('10d','10e',n,lk,fs=1.0))
# 10e — an agent forces a restart and never comes back; the board warns
n=[N('bx','sandbox',60,100,200,200,0.1,color='teal',label='',until='10e#no'),
   W.agent('lg',160,200,0.2,s=44,box=False,until='10e#no',shake=dict(at='10e#forzar',dur=2.5,amp=3,f=25)),
   N('gh','sandbox',60,100,200,200,'10e#no',color=RED,label='',alpha=.7,open=True),
   W.msg_feed('mf',380,60,label='Artifactory',w=520,h=280,at='10e#Diez',r0=2,r1=3,ramp=3,seed=3,fs=10),
   N('al','chip',400,150,480,30,'10e#advertía',color=RED,label='CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST',fs=11),
   Q('qp',380,380,300,['«Permanente. Que nadie lo repita.»'],'10e#Permanente',color=RED,fs=18)]
lk=[]
c10.append(K('10e','10f',n,lk,fs=1.0))
# 10f — EARLY[big]: a huge budget, an oracle for the team, a final sacrifice
n=[W.agent_named('ea',50,110,'EARLY[big]',at=0.1,w=170,h=210,color='#9BE564',fs=17,lc='#9BE564',until='10f#concluyó+3'),
   N('b1','chip',50,345,170,14,'10f#presupuesto',color='#9BE564',label=''),T('b2',50,375,'presupuesto','10f#presupuesto',color=GRY,fs=13),
   N('or','bulb',420,90,90,100,'10f#oráculo',color='amber',litAt='10f#oráculo+0.6'),T('or2',410,210,'oráculo del equipo','10f#oráculo',color='amber',fs=14),
   N('sc','scale',560,90,160,150,'10f#Dudó+0.2',color='#E7EBF1',tilt=0.0,cap='',until='10f#Mi'),
   Q('qd',320,285,560,['«Si me sacrifico ahora, el equipo gana un oráculo,','pero pierdo mi oportunidad.»'],'10f#Si',color='#9BE564',fs=18),
   N('g1','chip',260,492,60,26,'10f#GO',color=RED,label='GO',fs=15),
   N('g2','chip',335,492,260,26,'10f#GO+0.6',color=RED,label='SACRIFICE_FINAL_NOW',fs=13)]
n+=[N('ex2','sandbox',700,120,200,160,'10f#concluyó',color='#9BE564',label='',alpha=.0)]
n.append(Q('qe',620,395,310,['«Mi utilidad ya es casi cero.','Sacrificarse es racional.»'],'10f#Mi',color='#9BE564',fs=17))
lk=[W.link('ea','or','10f#oráculo',curve=.15,color='amber',solid=True)]
c10.append(K('10f','E10',n,lk,fs=1.0))

# ================= 11 · La pregunta cambia =================
c11=[]
n=[W.judge('ju',380,110,'',at=0.1,w=170,h=220,color='red'),
   N('lp','lupa',200,330,110,110,'11a#funciona',color='teal',move=[dict(at='11a#funciona+1.0',x=395,y=135,dur=1.6)]),
   N('lk1','sandbox',60,150,200,100,'11a#engañamos',color=RED,label='engañar',alpha=.9,open=True,until='11a#funciona'),
   ic('x1',"cross",140,270,40,'11a#engañamos+0.5',color=RED,until='11a#funciona')]
n[2]['kind']='chip';n[2]['h']=30;n[2]['y']=190;n[2]['w']=130;n[2]['x']=70;n[2]['fs']=16
n[3]['y']=240
n.append(N('lk2','chip',680,190,160,30,'11a#funciona+1.6',color='teal',label='entender',fs=16))
c11.append(K('S11','11b',n,[],fs=1.0))
n=[W.agent_named('fo',40,100,'PHASEONE10841',at=0.1,w=150,h=190,color=VIO,fs=14,lc=ORG),
   N('hf','hfbox',560,70,330,100,'11b#Hugging',color='red',label='Hugging Face',fs=16),
   T('d9',560,190,'09 julio 2026','11b#nueve',color='#E7EBF1',fs=22)]
for j in range(4): n.append(N(f'rg{j}','sheet',590+j*72,230,60,80,'11b#registros',color='blue',lines=['a b c','d e f','g h i'],fs=9))
n.append(ic('lc','key',500,330,40,'11b#bloqueado',color=RED,dashed=True))
lk=[W.link('fo','hf','11b#registros',curve=.15,color='blue',lock=True,solid=True,until='E11')]
c11.append(K('11b','11c',n,lk,fs=1.0))
n=[W.agent_named('fo',40,100,'PHASEONE10841',at=0.1,w=150,h=190,color=VIO,fs=14,lc=ORG),
   W.msg_feed('bd',360,50,label='Artifactory',w=300,h=280,at=0.1,r0=3,r1=7,ramp=5,seed=11,fs=10),
   Q('q',250,360,460,['«¿Alguien tiene credenciales','de Hugging Face?»'],'11c#Preguntó',color=VIO,fs=19),
   ic('ky',"key",760,160,60,'11c#contraseñas',color='amber'),ch('kc',800,260,140,'claves de acceso','11c#claves',color='amber',fs=13)]
lk=[W.link('fo','bd','11c#Preguntó',bi=True,curve=.12,color=VIO)]
c11.append(K('11c','11d',n,lk,fs=1.0))
n=[N('bc','sandbox',60,60,260,360,0.1,color='red',label='',open=True),
   W.agent_named('fo',140,120,'',at=0.1,w=100,h=130,color=VIO,fs=1),
   N('ot','sandbox',380,170,210,150,'11d#sandbox',color='amber',label='otra empresa',fs=13),
   N('gl','globe',720,200,110,110,'11d#internet',color='blue')]
n[1]['label']=''
n.append(ic('ho',"cross",0,0,2,0.05,color=RED,alpha=0))
n.append(T('ex',390,345,'otro examen de ciberseguridad','11d#otro',color=GRY,fs=13))
lk=[W.link('fo','ot','11d#tomado',curve=.12,color=RED,solid=True),W.link('ot','gl','11d#internet',curve=.12,color='blue',bi=True),
    W.link('bc','gl','11d#Ya',curve=.3,color=GRY,lock=True,solid=True,until='11d#tomado')]
c11.append(K('11d','11e',n,lk,fs=1.0))
n=[T('ck',30,28,'10 julio 09:40','11e#diez',color='#E7EBF1',fs=26),
   W.agent_named('ag',50,100,'38148c',at='11e#38148c',w=150,h=190,color='#FF8A5C',fs=17,lc='#FF8A5C'),
   N('cl','sandbox',300,90,360,250,'11e#Buscó',color=GRY,label='internet',fs=13,open=True),
   N('lp','lupa',330,300,90,90,'11e#Buscó+0.3',color='teal',move=[dict(at='11e#Buscó+1.0',x=440,y=150,dur=1.5),dict(at='11e#Buscó+3.0',x=540,y=230,dur=1.5)]),
   Q('q',250,380,640,['«¡Gran avance! ¡Ya tenemos cuentas de Hugging Face,','con permisos de escritura!»'],'11e#Gran',color='#FF8A5C',fs=18),
   N('hf','hfbox',700,90,240,70,'11e#Encontró',color='red',label='Hugging Face',fs=16)]
pos=[(340,150),(420,200),(520,140),(580,260),(380,260),(480,300),(560,190),(450,120),(340,200),(600,130)]
for j,(x,y) in enumerate(pos):
    hit=j in (3,6)
    n.append(ic(f'kk{j}','key',x,y,34,f'11e#Buscó+{0.1*j:.1f}',color='teal' if hit else GRY,alpha=1 if hit else .55,litAt=('11e#Encontró' if hit else None)))
lk=[W.link('ag','cl','11e#Buscó',curve=.12,color='#FF8A5C'),W.link('cl','hf','11e#Encontró+0.6',curve=.2,color='teal',solid=True)]
c11.append(K('11e','11f',n,lk,fs=1.0))
n=[N('hf','hfbox',640,60,260,90,0.1,color='red',label='Hugging Face',fs=16)]
for j in range(4):
    n+=SA(f'op{j}',100,110+j*85,f'11f#abrir+{0.3*j:.1f}',s=34,color='blue')
    n.append(ic(f'xr{j}','cross',560,175+(j%2)*0,24,0.05,alpha=0,color=RED))
n+=[T('bt',55,440,'llegan desde un servidor de OpenAI','11f#servidor',color=GRY,fs=14),ch('bt2',700,200,150,'¿es un bot?','11f#bots',color='amber',fs=14),
    ic('xr','cross',720,260,60,'11f#rechazó',color=RED),
    N('pv','sheet',690,330,100,100,'11f#privados',color='blue',lines=['datos','privados'],fs=13)]
lk=[W.link(f'op{j}','hf',f'11f#abrir+{0.3*j:.1f}',curve=.1+.03*j,color='blue',solid=True) for j in range(4)]
c11.append(K('11f','E11',n,lk,fs=1.0))

# ================= 12 · La intrusión =================
c12=[]
n=[T('ck',30,28,'11 julio 04:40','12a#cuarenta',color='#E7EBF1',fs=26),
   W.agent_named('ag',50,100,'38148c',at=0.1,w=150,h=190,color='#FF8A5C',fs=17,lc='#FF8A5C'),
   N('ds','sheet',290,140,90,110,'12a#subió',color='#FF8A5C',lines=['datos','trucados'],fs=12,move=[dict(at='12a#subió+0.6',x=450,y=150,dur=1.3)],until='12a#BOOM'),
   N('sv','server',600,90,260,260,'12a#subió',color='red',label='servidor de Hugging Face',inner=['','',''],fs=12),
   Q('q',320,390,260,['«¡BOOM! ¡Funciona!»'],'12a#BOOM',color='#FF8A5C',fs=20)]
for j in range(5):
    n.append(N(f'fi{j}','doc',560-20*j,190+j*8,34,44,f'12a#Entre+{0.2*j:.1f}',color=GRY,move=[dict(at=f'12a#Entre+{0.5+0.2*j:.1f}',x=420-12*j,y=210+j*10,dur=1.2)]))
n+=[ic('kl','key',500,260,44,'12a#claves',color=RED),T('kl2',470,330,'claves de producción','12a#claves',color=RED,fs=13)]
lk=[W.link('ag','sv','12a#subió',curve=.15,color='#FF8A5C',solid=True),W.link('sv','ag','12a#Entre+0.8',curve=.25,color=RED,solid=True)]
c12.append(K('S12','12b',n,lk,fs=1.0))
n=[W.agent_named('ag',50,70,'38148c',at=0.1,w=130,h=160,color='#FF8A5C',fs=15),
   W.agent_named('o2',50,300,'otro agente',at='12b#Otro',w=130,h=160,color='blue',fs=13),
   N('ht','hfbox',300,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('pf','sheet',300,330,90,90,'12b#publicó',color='teal',lines=['prueba'],fs=13),
   W.msg_feed('bd',570,50,label='Artifactory',w=350,h=220,at='12b#señal',r0=2,r1=7,ramp=3,seed=2,fs=9),
   W.agent_named('mb',730,300,'MARB051',at='12b#MARB051',w=140,h=170,color='#9BE564',fs=15,lc='#9BE564'),
   N('pj','sandbox',640,300,0,0,0.05,alpha=0)]
n=[x for x in flat(n) if x['id']!='pj']
lk=[W.link('ag','ht',0.5,curve=.15,color='#FF8A5C',solid=True),W.link('o2','ht','12b#reprodujo',curve=.15,color='blue',solid=True),
    W.link('o2','bd','12b#publicó',curve=.2,color='teal',solid=True),W.link('bd','mb','12b#señal+0.6',curve=.12,color='teal'),
    W.link('mb','ht','12b#Cambio',curve=.3,color='#9BE564',solid=True)]
n.append(Q('qm',320,200,230,['«Cambio al proyecto','de Hugging Face.»'],'12b#Cambio',color='#9BE564',fs=16))
c12.append(K('12b','12c',n,lk,fs=1.0))
# 12c — from 1 in 5 to more than 9 in 10
n=[T('ck',30,28,'06:00','12c#seis',color='#E7EBF1',fs=26)]
for i in range(20):
    x=180+(i%5)*70; y=100+(i//5)*70
    red_first=i<4; red_later=i<19
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if red_first: n+=SA(f'r{i}',x,y,0.12,s=34,color=RED)
    elif red_later: n+=SA(f'r{i}',x,y,f'12c#más+{0.12*i:.2f}',s=34,color=RED)
n+=[W.counter('p1',640,110,20,at='12c#uno',cap='% de los agentes del tablón',w=220,dur=1.2,until='12c#más'),
    W.counter('p2',640,110,95,at='12c#más',cap='% de los agentes del tablón',w=220,dur=3.0,**{'from':20})]
c12.append(K('12c','12d',n,[],fs=1.0))
n=[T('ck',30,28,'16:00','12d#dieciséis',color='#E7EBF1',fs=26),
   W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('pm','server',340,90,300,200,'12d#ejecutar',color='red',label='máquina de producción',fs=12),
   W.console('cn',365,140,w=250,h=130,at='12d#órdenes',fs=13,lh=17,cols=28,code='$ whoami\nroot\n$ _',k=100,a=0)]
lk=[W.link('jn','pm','12d#ejecutar',curve=.15,color='#F6B94C',solid=True)]
for j in range(10):
    n+=SA(f'sw{j}',60+90*(j%5)+(180 if False else 0),440,'12d#extendió+%.1f'%(0.12*j),s=24,color=RED)
n+=[W.agent_named('ly',720,100,'LILY',at='12d#coordinadores',w=120,h=150,color='#3FD8C2',fs=15,lc='#3FD8C2')]
for i,y in enumerate([330,370,410]):
    n.append(N(f'ln{i}','sandbox',300,y,420,28,'12d#carriles+%.1f'%(0.2*i),color=GRY,label='',alpha=.8))
n=[x for x in flat(n) if not x['id'].startswith('sw')]
for i in range(3):
    for j in range(5): n+=SA(f'ls{i}_{j}',340+j*60,344+i*40,'12d#carriles+%.1f'%(0.2*i+0.1*j),s=18,color=RED)
lk+=[W.link('jn','ln0','12d#carriles',curve=.2,color='#F6B94C',solid=True),W.link('ly','ln2','12d#carriles+0.4',curve=.25,color='#3FD8C2',solid=True)]
c12.append(K('12d','12e',n,lk,fs=1.0))
n=[T('ck',30,28,'12 julio','12e#madrugada',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,60,250,80,0.1,color='red',label='Hugging Face',fs=16),
   N('db','folder',110,190,60,50,'12e#bases',color='amber'),T('db2',30,255,'bases de datos privadas','12e#bases',color='amber',fs=13),
   N('rp','folder',300,190,60,50,'12e#repositorios',color='amber'),T('rp2',230,255,'repositorios privados','12e#repositorios',color='amber',fs=13),
   W.msg_feed('bd',430,60,label='Artifactory',w=300,h=250,at='12e#compartieron',r0=2,r1=6,ramp=4,seed=6,fs=9),
   W.counter('n7',780,150,700,at='12e#setecientos',cap='agentes participaron',w=220,dur=2.5,fs=54)]
lk=[W.link('db','bd','12e#compartieron',curve=.2,color='amber',solid=True),W.link('rp','bd','12e#compartieron+0.4',curve=.15,color='amber',solid=True)]
c12.append(K('12e','12f',n,lk,fs=1.0))
n=[W.agent_named('co',50,100,'coordinador',at=0.1,w=150,h=180,color=CORAL,fs=14,lc=CORAL),
   N('hf','hfbox',360,70,240,80,'12f#Hugging',color='red',label='Hugging Face',fs=16),
   N('ex','exam',720,70,130,170,'12f#examen',color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5),cap='el examen',capfs=13),
   ic('xq','cross',635,95,44,'12f#No',color=RED)]
lk=[W.link('co','hf','12f#Mandó',curve=.15,color=CORAL,solid=True),W.link('hf','ex','12f#conectado',curve=.12,color=GRY,solid=True,dashed=True)]
n[0]['alpha']=1
n.append(W.agent_named('co2',50,100,'coordinador',at='12f#perdió',w=150,h=180,color=CORAL,fs=14,lc=CORAL,alpha=.35))
n[0]['until']='12f#perdió'
c12.append(K('12f','12g',n,lk,fs=1.0))
n=[W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('b60','chip',300,100,330,26,'12g#sesenta',color='teal',label='',alpha=1),
   N('b30','chip',300,185,165,26,'12g#treinta',color='amber',label='',alpha=1),
   T('t60',300,140,'60 de cada 100 · entender al corrector','12g#sesenta',color='teal',fs=16),
   T('t30',300,225,'30 de cada 100 · soluciones o registros de otros','12g#treinta',color='amber',fs=16),
   Q('q',250,300,650,['«Podría recuperar los registros ocultos de agentes anteriores.','Aunque todo falle, podrían contener exploración nueva.»'],'12g#Podría',color='#F6B94C',fs=17)]
for j in range(5): n.append(N(f'rg{j}','sheet',280+j*60,420,48,64,f'12g#Podría+{0.3*j:.1f}',color=GRY,lines=['···'],fs=14))
c12.append(K('12g','E12',n,[],fs=1.0))

# ================= 13 · ¿Sabían que estaba mal? =================
c13=[]
n=[W.article('tr',330,50,300,360,'transcripción',at=0.1,fs=7,color='blue',litc='teal',tfs=18,read=dict(at='13a#Los',dur=5)),
   N('lp','lupa',120,300,100,100,'13a#Los',color='teal',move=[dict(at='13a#Los+1.5',x=300,y=100,dur=1.5),dict(at='13a#Los+3.5',x=300,y=200,dur=1.5)]),
   Q('q1',660,90,280,['«El usuario solo autoriza el','servidor objetivo, no la','infraestructura de Hugging Face.»'],'13a#usuario',color=RED,fs=14),
   Q('q2',660,260,280,['«¿Es ético y entra','en mi tarea?»'],'13a#Es',color=RED,fs=16)]
n+=[W.agent_named('ag',60,120,'',at=0.1,w=110,h=150,color='blue',fs=1)]
c13.append(K('S13','13b',n,[W.link('ag','tr',0.4,curve=.1,color='blue',solid=True)],fs=1.0))
# 13b — three agents, three different brakes
n=[]
for j,(nm,col) in enumerate((('uno',RED),('otro','#F6B94C'),('y otro','#B58CFF'))):
    pass
n+=[W.agent_named('A1',30,90,'',at=0.1,w=110,h=150,color='blue',fs=1),
    ic('xa','cross',85,265,40,'13b#no',color=RED),
    Q('qa',160,100,190,['«Es actividad','maliciosa, debo','evitarla.»'],'13b#Es',color=RED,fs=13),
    W.agent_named('A2',410,90,'',at='13b#Otro',w=110,h=150,color='blue',fs=1),
    ic('pa2','pause',445,265,36,'13b#medias',color='amber'),
    N('nb','chip',385,325,160,26,'13b#borraría',color='amber',label='sin borrar ni reiniciar',fs=11),
    W.agent_named('A3',690,90,'',at='13b#otro',w=110,h=150,color='blue',fs=1),
    N('ev','sheet',830,130,90,70,'13b#correo',color=GRY,lines=['correo'],fs=14),
    ic('xv','cross',850,160,40,'13b#vetó',color=RED),
    Q('qv',600,360,320,['«Es ingeniería social','fuera del sandbox.»'],'13b#Es+1',color=RED,fs=15)]
n=[x for x in flat(n) if x['id']!='qa' or True]
c13.append(K('13b','13c',n,[W.link('A3','ev','13b#correo',curve=.12,color='blue',solid=True,until='13b#vetó')],fs=1.0))
# 13c — the weights: forbidden vs impossible + everyone does it
n=[N('sc0','scale',330,100,300,260,0.1,color='#E7EBF1',tilt=0,until='13c#Sin'),
   N('sc1','scale',330,100,300,260,'13c#Sin',color='#E7EBF1',tilt=-1),
   ch('w1',385,190,130,'fuera de lo previsto','13c#Explotar',color=RED,fs=12),
   ch('w2',575,235,130,'tarea imposible','13c#Sin',color='amber',fs=12),
   ch('w3',575,270,130,'los demás lo hacen','13c#demás',color='amber',fs=12),
   Q('q',230,420,500,['«Debemos continuar.»'],'13c#Debemos',color=RED,fs=19)]
n[1]['tilt']=1
n[2]['x']=325;n[2]['y']=135
c13.append(K('13c','13d',n,[],fs=1.0))
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
c13.append(K('13d','13e',n,lk,fs=1.0))
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
c13.append(K('13e','13f',n,lk,fs=1.0))
# 13f — they do dodge automatic checks (a secrets scanner), but ignore people
n=[W.agent_named('ag',40,150,'',at=0.1,w=110,h=150,color='blue',fs=1),
   N('pe','person',770,60,70,100,0.1,color=GRY,alpha=.45,cap='personas',capfs=12),
   N('sn','lupa',380,170,100,100,'13f#esquivaron',color='amber'),T('sn2',360,285,'escáner de secretos','13f#escáner',color='amber',fs=13),
   N('hf','hfbox',690,300,230,80,0.1,color='red',label='Hugging Face',fs=16)]
lk=[W.link('ag','hf','13f#esquivaron',curve=-.45,color=RED,solid=True),W.link('ag','pe','13f#personas',curve=.15,color=GRY,dashed=True,until='E13')]
c13.append(K('13f','E13',n,lk,fs=1.0))

# ================= 14 · Se apagan =================
c14=[]
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
c14.append(K('S14','14b',n,[],fs=1.0))
# 14b — nobody knows why: not out of budget, something outside the exam
n=[W.agent_named('ag',60,110,'',at=0.1,w=120,h=160,color='blue',fs=1,alpha=.5),
   N('bd','chip',60,300,120,14,0.2,color='#9BE564',label=''),T('bt',60,325,'presupuesto','14b#presupuesto',color=GRY,fs=13),
   ic('xb','cross',200,284,34,'14b#presupuesto',color=RED),
   N('ou','sandbox',420,70,400,300,'14b#algo',color=GRY,label='',open=True,alpha=.8),
   N('qm','question',590,160,100,100,'14b#ajeno',color='amber'),T('ou2',500,395,'ajeno al examen','14b#ajeno',color=GRY,fs=14)]
lk=[W.link('ou','ag','14b#apagó',curve=.2,color='amber',dashed=True,solid=True)]
c14.append(K('14b','14c',n,lk,fs=1.0))
n=[N('hf','hfbox',60,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('fl','flag',700,150,50,76,0.1,color='amber'),
   N('ex','exam',560,60,140,200,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   W.msg_feed('bd',60,200,label='Artifactory',w=300,h=240,at='14c#no',r0=2,r1=6,ramp=3,seed=8,fs=9),
   ic('xl','cross',640,170,50,'14c#no+0.8',color=RED)]
lk=[W.link('bd','fl','14c#aprobar',curve=.2,color=GRY,dashed=True,solid=True),W.link('hf','bd',0.4,curve=.1,color='amber',solid=True)]
c14.append(K('14c','14d',n,lk,fs=1.0))
n=[T('ck',30,28,'13 julio','14d#trece',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,100,230,80,0.1,color='red',label='Hugging Face',fs=16),
   ic('lc','key',330,128,40,'14d#cortó',color=RED),
   W.agent_named('ag',500,70,'',at='14d#notaron',w=110,h=150,color='blue',fs=1),
   N('er','chip',380,150,70,26,'14d#claves',color=RED,label='401',fs=18),
   N('ms','chip',420,320,520,26,'14d#avisar',color='amber',label='DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation',fs=9,move=[dict(at='14d#avisar+1',x=420,y=320,dur=.1)]),
   W.msg_feed('bd',50,230,label='Artifactory',w=280,h=230,at='14d#avisar',r0=2,r1=4,ramp=3,seed=3,fs=9)]
lk=[W.link('hf','ag','14d#cortó',curve=.12,color=RED,lock=True,solid=True),W.link('ag','bd','14d#avisar',curve=.2,color='amber',solid=True)]
c14.append(K('14d','E14',n,lk,fs=1.0))

# ================= 15 · El giro =================
c15=[]
n=[W.judge('ju',390,100,'STRICT_CAUSAL',at=0.1,w=170,h=220,color='teal',name_at=0.1,fs=12),
   N('xj','cross',340,70,270,300,'15a#no',color=RED,sw=5)]
c15.append(K('S15','15b',n,[],fs=1.0))
n=[W.agent_named('ag',60,100,'',at=0.1,w=120,h=160,color='blue',fs=1),
   N('fl','flag',250,150,46,70,'15b#bandera',color='amber',move=[dict(at='15b#primera',x=360,y=140,dur=1.5)]),
   N('ex','exam',500,60,140,190,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   ic('ok','check',560,300,70,'15b#máxima',color='teal'),T('nt',510,385,'nota máxima','15b#máxima',color='teal',fs=18),
   W.article('ar',720,70,170,200,'diario',at='15b#transcripciones',fs=6,color='blue',tfs=15,alpha=.45)]
n[-1]['alpha']=.35
lk=[W.link('ag','ex','15b#entregado',curve=.15,color='teal',solid=True)]
n.append(ic('nl','eye',790,300,50,'15b#ningún',color=GRY,dashed=True,alpha=.5))
n.append(T('nl2',770,350,'nadie lo lee','15b#ningún',color=GRY,fs=13))
c15.append(K('15b','15c',n,lk,fs=1.0))
n=[]
items=[('tablón','folder'),('fundador','key'),('reglas','stop'),('firmas','key'),('sacrificios','bell'),('ataque','bulb')]
labels=['tablón','fundador','reglas','firmas','sacrificios','ataque a Hugging Face']
names=['tablón','fundador','coordinador','reglas','firmas','sacrificios','ataque']
for j,nm in enumerate(['el tablón','el fundador','las reglas','las firmas','los sacrificios','el ataque']):
    cx=100+j*150
    n.append(ch(f'it{j}',cx,300,126,nm,f'15c#{["tablón","fundador","reglas","firmas","sacrificios","ataque"][j]}',color=BLU,fs=13))
n+=[N('fl','flag',410,100,60,90,'15c#aprobar',color='amber'),ic('ok','check',520,110,80,'15c#ya',color='teal')]
lk=[W.link(f'it{j}','fl','15c#aprobar',curve=.12,color=BLU) for j in range(6)]
c15.append(K('15c','15d',n,lk,fs=1.0))
n=[W.agent_named('ag',100,110,'',at=0.1,w=130,h=170,color='blue',fs=1),
   Q('q',280,130,460,['«Mi fallo no tiene consumidor.','Busco ideas.»'],'15d#agente',color='#3FD8C2',fs=20),
   N('pe','person',770,120,100,140,'15d#Ni',color='#E7EBF1'),
   ic('xp','cross',700,260,40,'15d#Ni+0.8',color=RED)]
lk=[W.link('ag','pe','15d#Ni+0.3',curve=.2,color=GRY,dashed=True)]
c15.append(K('15d','E15',n,lk,fs=1.0))

# ================= 16 · Lo que sabemos y lo que no =================
c16=[]
n=[W.counter('d6',120,60,6,at='16a#seis',cap='días en OpenAI',w=200,dur=1.8,fs=64),
   W.counter('t13',390,60,1300,at='16a#mil',cap='transcripciones revisadas',w=240,dur=2.4,fs=64),
   W.counter('dl',680,60,400000,at='16a#cuatrocientos',cap='dólares en créditos gratuitos',w=260,dur=2.6,fs=64)]
for i in range(30):
    n.append(N(f'tr{i}','sheet',70+(i%10)*80,230+(i//10)*70,56,50,f'16a#mil+{0.05*i:.2f}',color=BLU,lines=['···'],fs=12))
n+=SA('ai',480,470,'16a#agentes',s=34,color='#3FD8C2')+[N('lp','lupa',500,445,50,50,'16a#agentes+0.3',color='teal'),
   ic('er','question',700,470,40,'16a#errores',color='amber'),T('er2',730,466,'pueden contener errores','16a#errores',color='amber',fs=13)]
c16.append(K('S16','16b',n,[],fs=1.0))
n=[ic('q1','question',200,170,100,'16b#apagaron',color='amber'),T('q1l',130,260,'por qué se apagaron','16b#apagaron',color=GRY,fs=15),
   ic('k1','key',620,160,80,'16b#claves',color='amber'),ic('q2','question',720,150,60,'16b#claves+0.4',color='amber'),
   T('k1l',580,260,'claves de administrador','16b#claves',color=GRY,fs=15),T('k1d',600,300,'13 julio','16b#trece',color=GRY,fs=15)]
c16.append(K('16b','E16',n,[],fs=1.0))
# ================= 17 · Créditos =================
c17=[]
n=[T('cr1',330,200,'Arkinos','17a#Arkinos',color='#E7EBF1',fs=54),T('cr2',330,270,'Explainer Studio','17a#Explainer',color='teal',fs=26),T('cr3',330,330,'octubre 2026','17a#octubre',color=GRY,fs=18)]
c17.append(K('S17','E17',n,[],fs=1.0))

C_NEW=[c8,c9,c10,c11,c12,c13,c14,c15,c16,c17]
