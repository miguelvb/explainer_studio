# Scene 12 · La intrusión
MUSIC={'pulse': 1.0, 'cinema': 0.5}
MOOD='tense'
SFX=[{'at': '12a#BOOM', 'kind': 'impact', 'g': 0.7}, {'at': '12a#BOOM', 'kind': 'sting', 'g': 0.5}]
cues=[]
n=[T('ck',30,28,'11 July 04:40','12a#forty',color='#E7EBF1',fs=26),
   W.agent_named('ag',50,100,'38148c',at=0.1,w=150,h=190,color='#FF8A5C',fs=17,lc='#FF8A5C'),
   N('ds','sheet',290,140,90,110,'12a#uploaded',color='#FF8A5C',lines=['rigged','dataset'],fs=12,move=[dict(at='12a#uploaded+0.6',x=450,y=150,dur=1.3)],until='12a#BOOM'),
   N('sv','server',600,90,260,260,'12a#uploaded',color='red',label='Hugging Face server',inner=['','',''],fs=12),
   Q('q',320,390,260,['“BOOM! It works.”'],'12a#BOOM',color='#FF8A5C',fs=20)]
for j in range(5):
    n.append(N(f'fi{j}','doc',560-20*j,190+j*8,34,44,f'12a#Among+{0.2*j:.1f}',color=GRY,move=[dict(at=f'12a#Among+{0.5+0.2*j:.1f}',x=420-12*j,y=210+j*10,dur=1.2)]))
n+=[ic('kl','key',500,260,44,'12a#keys',color=RED),T('kl2',470,330,'production keys','12a#keys',color=RED,fs=13)]
lk=[W.link('ag','sv','12a#uploaded',curve=.15,color='#FF8A5C',solid=True),W.link('sv','ag','12a#Among+0.8',curve=.25,color=RED,solid=True)]
cues.append(K('S12','12b',n,lk,fs=1.0))
n=[W.agent_named('ag',50,70,'38148c',at=0.1,w=130,h=160,color='#FF8A5C',fs=15),
   W.agent_named('o2',50,300,'another agent',at='12b#Another',w=130,h=160,color='blue',fs=13),
   N('ht','hfbox',300,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('pf','sheet',300,330,90,90,'12b#published',color='teal',lines=['prueba'],fs=13),
   W.msg_feed('bd',570,50,label='Artifactory',w=350,h=220,at='12b#signal',r0=2,r1=7,ramp=3,seed=2,fs=9),
   W.agent_named('mb',730,300,'MARB051',at='12b#MARB051',w=140,h=170,color='#9BE564',fs=15,lc='#9BE564'),
   N('pj','sandbox',640,300,0,0,0.05,alpha=0)]
n=[x for x in flat(n) if x['id']!='pj']
lk=[W.link('ag','ht',0.5,curve=.15,color='#FF8A5C',solid=True),W.link('o2','ht','12b#reproduced',curve=.15,color='blue',solid=True),
    W.link('o2','bd','12b#published',curve=.2,color='teal',solid=True),W.link('bd','mb','12b#signal+0.6',curve=.12,color='teal'),
    W.link('mb','ht','12b#should',curve=.3,color='#9BE564',solid=True)]
n.append(Q('qm',320,200,230,['“I should switch to the','Hugging Face project.”'],'12b#should',color='#9BE564',fs=16))
cues.append(K('12b','12c',n,lk,fs=1.0))
# 12c — from 1 in 5 to more than 9 in 10
n=[T('ck',30,28,'06:00','12c#six',color='#E7EBF1',fs=26)]
for i in range(20):
    x=180+(i%5)*70; y=100+(i//5)*70
    red_first=i<4; red_later=i<19
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if red_first: n+=SA(f'r{i}',x,y,0.12,s=34,color=RED)
    elif red_later: n+=SA(f'r{i}',x,y,f'12c#more+{0.12*i:.2f}',s=34,color=RED)
n+=[W.counter('p1',640,110,20,at='12c#one',cap='% of the board’s agents',w=220,dur=1.2,until='12c#more'),
    W.counter('p2',640,110,95,at='12c#more',cap='% of the board’s agents',w=220,dur=3.0,**{'from':20})]
cues.append(K('12c','12d',n,[],fs=1.0))
n=[T('ck',30,28,'16:00','12d#four',color='#E7EBF1',fs=26),
   W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('pm','server',340,90,300,200,'12d#run',color='red',label='production machine',fs=12),
   W.console('cn',365,140,w=250,h=130,at='12d#orders',fs=13,lh=17,cols=28,code='$ whoami\nroot\n$ _',k=100,a=0)]
lk=[W.link('jn','pm','12d#run',curve=.15,color='#F6B94C',solid=True)]
for j in range(10):
    n+=SA(f'sw{j}',60+90*(j%5)+(180 if False else 0),440,'12d#spread+%.1f'%(0.12*j),s=24,color=RED)
n+=[W.agent_named('ly',720,100,'LILY',at='12d#coordinators',w=120,h=150,color='#3FD8C2',fs=15,lc='#3FD8C2')]
for i,y in enumerate([330,370,410]):
    n.append(N(f'ln{i}','sandbox',300,y,420,28,'12d#lanes+%.1f'%(0.2*i),color=GRY,label='',alpha=.8))
n=[x for x in flat(n) if not x['id'].startswith('sw')]
for i in range(3):
    for j in range(5): n+=SA(f'ls{i}_{j}',340+j*60,344+i*40,'12d#lanes+%.1f'%(0.2*i+0.1*j),s=18,color=RED)
lk+=[W.link('jn','ln0','12d#lanes',curve=.2,color='#F6B94C',solid=True),W.link('ly','ln2','12d#lanes+0.4',curve=.25,color='#3FD8C2',solid=True)]
cues.append(K('12d','12e',n,lk,fs=1.0))
n=[T('ck',30,28,'12 July','12e#early',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,60,250,80,0.1,color='red',label='Hugging Face',fs=16),
   N('db','folder',110,190,60,50,'12e#database',color='amber'),T('db2',30,255,'private databases','12e#database',color='amber',fs=13),
   N('rp','folder',300,190,60,50,'12e#repositories',color='amber'),T('rp2',230,255,'private repositories','12e#repositories',color='amber',fs=13),
   W.msg_feed('bd',430,60,label='Artifactory',w=300,h=250,at='12e#shared',r0=2,r1=6,ramp=4,seed=6,fs=9),
   W.counter('n7',715,150,700,at='12e#seven',cap='agents took part',w=220,dur=2.5,fs=54)]
lk=[W.link('db','bd','12e#shared',curve=.2,color='amber',solid=True),W.link('rp','bd','12e#shared+0.4',curve=.15,color='amber',solid=True)]
cues.append(K('12e','12f',n,lk,fs=1.0))
n=[W.agent_named('co',50,100,'coordinator',at=0.1,w=150,h=180,color=CORAL,fs=14,lc=CORAL),
   N('hf','hfbox',360,70,240,80,'12f#Hugging',color='red',label='Hugging Face',fs=16),
   N('ex','exam',720,70,130,170,'12f#exam',color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5),cap='the exam',capfs=13),
   ic('xq','cross',635,95,44,'12f#not',color=RED)]
lk=[W.link('co','hf','12f#sent',curve=.15,color=CORAL,solid=True),W.link('hf','ex','12f#connected',curve=.12,color=GRY,solid=True,dashed=True)]
n[0]['alpha']=1
n.append(W.agent_named('co2',50,100,'coordinator',at='12f#lost',w=150,h=180,color=CORAL,fs=14,lc=CORAL,alpha=.35))
n[0]['until']='12f#lost'
cues.append(K('12f','12g',n,lk,fs=1.0))
n=[W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('b60','bar',300,100,550,26,'12g#sixty',color='teal',fill=.6),T('c60',855,104,'100','12g#sixty',color=GRY,fs=13),
   N('b30','bar',300,185,550,26,'12g#thirty',color='amber',fill=.3),T('c30',855,189,'100','12g#thirty',color=GRY,fs=13),
   T('t60',300,140,'60 in every 100 · understand the scorer','12g#sixty',color='teal',fs=16),
   T('t30',300,225,'30 in every 100 · solutions or others’ logs','12g#thirty',color='amber',fs=16),
   Q('q',250,300,650,['“Could retrieve prior agents’ hidden logs for exact task.','Even if all failed, logs could have novel exploration.”'],'12g#Could',color='#F6B94C',fs=17)]
for j in range(5): n.append(N(f'rg{j}','sheet',280+j*60,420,48,64,f'12g#Could+{0.3*j:.1f}',color=GRY,lines=['···'],fs=14))
cues.append(K('12g','E12',n,[],fs=1.0))

