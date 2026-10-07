# Scene 15 · The Twist
MUSIC={'bells': 0.8, 'pad': 0.5}
SFX=[{'at': 'S15', 'kind': 'rise', 'g': 0.5}, {'at': '15a#not', 'kind': 'impact', 'g': 0.5}]
cues=[]
n=[W.judge('ju',390,100,'STRICT_CAUSAL',at=0.1,w=170,h=220,color='teal',name_at=0.1,fs=12),
   N('xj','koA',390,90,170,200,'15a#not',color=RED)]
cues.append(K('S15','15b',n,[],fs=1.0))
n=[W.agent_named('ag',60,100,'',at=0.1,w=120,h=160,color='blue',fs=10),
   N('fl','flFly',250,150,46,70,'15b#flag',color='amber',move=[dict(at='15b#first',x=360,y=140,dur=1.5)]),
   N('ex','exam',500,60,140,190,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   ic('ok','check',560,300,70,'15b#maximum',color='teal'),T('nt',510,385,'maximum score','15b#maximum',color='teal',fs=18),
   W.article('ar',720,70,170,200,'diary',at='15b#transcripts',fs=6,color='blue',tfs=15,alpha=.45)]
n[-1]['alpha']=.35
lk=[W.link('ag','ex','15b#turned',curve=.15,color='teal',solid=True)]
n.append(ic('nl','orb',790,300,50,'15b#not',color=GRY,dashed=True,alpha=.5))
n.append(T('nl2',770,350,'nobody reads it','15b#not',color=GRY,fs=13))
cues.append(K('15b','15c',n,lk,fs=1.0))
n=[]
items=[('board','folder'),('founder','key'),('rules','stop'),('signatures','key'),('sacrifices','bell'),('attack','ideaSpark')]
labels=['board','founder','rules','signatures','sacrifices','attack on Hugging Face']
names=['board','founder','coordinator','rules','signatures','sacrifices','attack']
for j,nm in enumerate(['the board','the founder','the rules','the signatures','the sacrifices','the attack']):
    cx=100+j*150
    n.append(ch(f'it{j}',cx,300,126,nm,f'15c#{["board","founder","rules","signatures","sacrifices","attack"][j]}',color=BLU,fs=13))
n+=[N('fl','flFly',410,100,60,90,'15c#pass',color='amber'),ic('ok','check',520,110,80,'15c#already',color='teal')]
lk=[W.link(f'it{j}','fl','15c#pass',curve=.12,color=BLU) for j in range(6)]
cues.append(K('15c','15d',n,lk,fs=1.0))
n=[W.agent_named('ag',100,110,'',at=0.1,w=130,h=170,color='blue',fs=10),
   Q('q',280,130,460,['“My failure has no consumer.','Seeking ideas.”'],'15d#agent',color='#3FD8C2',fs=20),
   N('pe','person',770,120,100,140,'15d#Not',color='#E7EBF1'),
   ic('xp','cross',700,260,40,'15d#Not+0.8',color=RED)]
lk=[W.link('ag','pe','15d#Not+0.3',curve=.2,color=GRY,dashed=True)]
cues.append(K('15d','E15',n,lk,fs=1.0))

