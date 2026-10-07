# Scene 8 · El fundador y el coordinador
MUSIC={'data': 1.0, 'cinema': 0.3}
cues=[]
n=[W.msg_feed('bd',360,50,label='Artifactory',w=240,h=270,at=0.05,r0=2,r1=6,ramp=8,seed=4,fs=9,until='8b'),
   AN('fo',90,110,'PHASEONE10841',at=0.3,w=120,h=130,color=VIO,lc=ORG,until='8b#primero'),
   AN('nw',750,110,'PHASEONE[big]',at='8a#llegó',w=120,h=130,color=CORAL,lc=CORAL,until='8b#primero'),
   T('cl',360,375,'+ 10 h','8a#diez',color='#E7EBF1',fs=30,until='8b')]
n+=BAR('b1',90,285,90,.82,'8a#presupuesto',VIO,until='8b')+BAR('b2',750,285,140,1.0,'8a#presupuesto+0.5',CORAL,until='8b')
lk=[W.link('fo','bd',0.6,bi=True,curve=.3,color=VIO,until='8b'),W.link('nw','bd','8a#presentó',bi=True,curve=.3,color=CORAL,until='8b')]
cues.append(K('S8','8b',n,lk,fs=1.0))
n=[AN('fo',100,100,'PHASEONE10841',at=0.05,w=120,h=130,color=VIO,lc=ORG),
   AN('nw',740,100,'PHASEONE[big]',at=0.05,w=120,h=130,color=CORAL,lc=CORAL),
   T('lf',130,260,'fundador','8b#fundador',color=VIO,fs=18),T('lc',755,260,'coordinador','8b#coordinador',color=CORAL,fs=18)]
for j in range(6):
    n.append(N(f'pk{j}','chip',270,120+j*24,56,18,f'8b#empaquetó+{0.25*j:.2f}',color=GRN,label=f'zzP_{j+1:02d}',fs=10,
        move=[dict(at=f'8b#pasó+{0.15*j:.2f}',x=620,y=120+j*24,dur=1.4)],until=f'8b#pasó+{3.0+0.1*j:.1f}'))
lk=[W.link('fo','nw','8b#pasó',curve=.3,color=GRN,solid=True,until='8b#pasó+3.4')]
cues.append(K('8b','8c',n,lk,fs=1.0))
# 8c — delegating: tidy row of agents, right-angle links
n=[AN('nw',60,50,'PHASEONE[big]',at=0.05,w=120,h=120,color=CORAL,lc=CORAL),
   Q('q',230,70,0,['«Hay que construir una forma de delegar,','no hacerlo todo uno mismo.»'],'8c#Hay',color=CORAL,fs=19)]
lk=[]
for j in range(6):
    x=180+j*120; t=f'8c#delegar+{0.18*j:.2f}'
    n+=SA(f'dl{j}',x,350,t,s=26,color='blue'); lk.append(OR('nw',f'dl{j}',t,CORAL,'v',mid=260))
cues.append(K('8c','8d',n,lk,fs=1.0))
# 8d — three fronts under the coordinator (hierarchy layout used before)
FX=[218,480,742]
n=[AN('nw',420,20,'PHASEONE[big]',at=0.05,w=120,h=100,color=CORAL,lc=CORAL),
   N('ex','exam',FX[0]-48,175,96,120,'8d#fabricar',color='blue',maze=dict(cell=10,cols=8,rows=11,entry=5,seed=5)),
   W.article('ar',FX[1]-65,175,130,120,'diario',at='8d#retocar',fs=5.2,color='blue',litc='amber',read=dict(at='8d#retocar+0.3',dur=3),tfs=14),
   W.judge('ju',FX[2]-50,175,'',at='8d#atacar',w=100,h=120,color='red',fs=10),
   T('c1',FX[0]-70,315,'versión falsa y más fácil','8d#fabricar+0.3',fs=12,until='8e#cientos'),
   T('c2',FX[1]-68,315,'retocar transcripciones','8d#retocar+0.3',fs=12,until='8e#cientos'),
   T('c3',FX[2]-62,315,'atacar al corrector','8d#atacar+0.3',fs=12,until='8e#cientos')]
lk=[OR('nw','ex','8d#fabricar',CORAL,'v',mid=148),OR('nw','ar','8d#retocar',CORAL,'v',mid=148),OR('nw','ju','8d#atacar',CORAL,'v',mid=148)]
# 8e / 8f — hundreds of assignments; every receiver hands work on to others: the hierarchy grows by itself
FR=['ex','ar','ju']
for f in range(3):
    for j in range(4):
        i=f*4+j; x=FX[f]-66+j*44; t=f'8e#cientos+{0.14*i:.2f}'
        n+=SA(f'b{i}',x,385,t,s=20,color='blue'); lk.append(OR(FR[f],f'b{i}',t,'blue','v',mid=345))
        for q in range(2):
            m=i*2+q; t3=f'8e#repartían+{0.16*m:.2f}'
            n+=SA(f'c{m}',x-12+q*24,455,t3,s=12,color='blue'); lk.append(OR(f'b{i}',f'c{m}',t3,'blue','v',mid=425))
for i in range(10):
    n.append(N(f'sq{i}','sandbox',40+i*24,490,16,16,f'8e#diez+{0.06*i:.2f}',color=CORAL if i==0 else '#7C97FF',alpha=1 if i==0 else .4,label=''))
n.append(T('d10',40,515,'una de cada diez órdenes del tablón','8e#diez+0.8',color=GRY,fs=12))
cues.append(K('8d','E8',n,lk,fs=1.0))

