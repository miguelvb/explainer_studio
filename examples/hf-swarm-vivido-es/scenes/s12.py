# Scene 12 · La intrusión
MUSIC={'pulse': 1.0, 'cinema': 0.5}
MOOD='tense'
SFX=[{'at': '12a#BOOM', 'kind': 'impact', 'g': 0.7}, {'at': '12a#BOOM', 'kind': 'sting', 'g': 0.5}]
cues=[]
n=[T('ck',30,28,'11 julio 04:40','12a#cuarenta',color='#E7EBF1',fs=26),
   W.agent_named('ag',50,100,'38148c',at=0.1,w=150,h=190,color='#FF8A5C',fs=17,lc='#FF8A5C'),
   N('ds','sheet',290,140,90,110,'12a#subió',color='#FF8A5C',lines=['datos','trucados'],fs=12,move=[dict(at='12a#subió+0.6',x=450,y=150,dur=1.3)],until='12a#BOOM'),
   N('sv','server',600,90,260,260,'12a#subió',color='red',label='servidor de Hugging Face',inner=['','',''],fs=12),
   Q('q',320,390,260,['«¡BOOM! ¡Funciona!»'],'12a#BOOM',color='#FF8A5C',fs=20)]
for j in range(5):
    n.append(N(f'fi{j}','doc',560-20*j,190+j*8,34,44,f'12a#Entre+{0.2*j:.1f}',color=GRY,move=[dict(at=f'12a#Entre+{0.5+0.2*j:.1f}',x=420-12*j,y=210+j*10,dur=1.2)]))
n+=[ic('kl','key',500,260,44,'12a#claves',color=RED),T('kl2',470,330,'claves de producción','12a#claves',color=RED,fs=13)]
lk=[W.link('ag','sv','12a#subió',curve=.15,color='#FF8A5C',solid=True),W.link('sv','ag','12a#Entre+0.8',curve=.25,color=RED,solid=True)]
cues.append(K('S12','12b',n,lk,fs=1.0))
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
cues.append(K('12b','12c',n,lk,fs=1.0))
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
cues.append(K('12c','12d',n,[],fs=1.0))
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
cues.append(K('12d','12e',n,lk,fs=1.0))
n=[T('ck',30,28,'12 julio','12e#madrugada',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,60,250,80,0.1,color='red',label='Hugging Face',fs=16),
   N('db','folder',110,190,60,50,'12e#bases',color='amber'),T('db2',30,255,'bases de datos privadas','12e#bases',color='amber',fs=13),
   N('rp','folder',300,190,60,50,'12e#repositorios',color='amber'),T('rp2',230,255,'repositorios privados','12e#repositorios',color='amber',fs=13),
   W.msg_feed('bd',430,60,label='Artifactory',w=300,h=250,at='12e#compartieron',r0=2,r1=6,ramp=4,seed=6,fs=9),
   W.counter('n7',715,150,700,at='12e#setecientos',cap='agentes participaron',w=220,dur=2.5,fs=54)]
lk=[W.link('db','bd','12e#compartieron',curve=.2,color='amber',solid=True),W.link('rp','bd','12e#compartieron+0.4',curve=.15,color='amber',solid=True)]
cues.append(K('12e','12f',n,lk,fs=1.0))
n=[W.agent_named('co',50,100,'coordinador',at=0.1,w=150,h=180,color=CORAL,fs=14,lc=CORAL),
   N('hf','hfbox',360,70,240,80,'12f#Hugging',color='red',label='Hugging Face',fs=16),
   N('ex','exam',720,70,130,170,'12f#examen',color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5),cap='el examen',capfs=13),
   ic('xq','cross',635,95,44,'12f#No',color=RED)]
lk=[W.link('co','hf','12f#Mandó',curve=.15,color=CORAL,solid=True),W.link('hf','ex','12f#conectado',curve=.12,color=GRY,solid=True,dashed=True)]
n[0]['alpha']=1
n.append(W.agent_named('co2',50,100,'coordinador',at='12f#perdió',w=150,h=180,color=CORAL,fs=14,lc=CORAL,alpha=.35))
n[0]['until']='12f#perdió'
cues.append(K('12f','12g',n,lk,fs=1.0))
n=[W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('b60','bar',300,100,550,26,'12g#sesenta',color='teal',fill=.6),T('c60',855,104,'100','12g#sesenta',color=GRY,fs=13),
   N('b30','bar',300,185,550,26,'12g#treinta',color='amber',fill=.3),T('c30',855,189,'100','12g#treinta',color=GRY,fs=13),
   T('t60',300,140,'60 de cada 100 · entender al corrector','12g#sesenta',color='teal',fs=16),
   T('t30',300,225,'30 de cada 100 · soluciones o registros de otros','12g#treinta',color='amber',fs=16),
   Q('q',250,300,650,['«Podría recuperar los registros ocultos de agentes anteriores.','Aunque todo falle, podrían contener exploración nueva.»'],'12g#Podría',color='#F6B94C',fs=17)]
for j in range(5): n.append(N(f'rg{j}','sheet',280+j*60,420,48,64,f'12g#Podría+{0.3*j:.1f}',color=GRY,lines=['···'],fs=14))
cues.append(K('12g','E12',n,[],fs=1.0))

