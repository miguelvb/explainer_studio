# Scene 13 · ¿Sabían que estaba mal?
MUSIC={'cinema': 1.0}
MOOD='tense'
SFX=[{'at': '13c#We', 'kind': 'sting', 'g': 0.55}]
cues=[]
n=[W.article('tr',330,50,300,360,'transcript',at=0.1,fs=7,color='blue',litc='teal',tfs=18,read=dict(at='13a#researchers',dur=5)),
   N('lp','lupa',120,300,100,100,'13a#researchers',color='teal',move=[dict(at='13a#researchers+1.5',x=300,y=100,dur=1.5),dict(at='13a#researchers+3.5',x=300,y=200,dur=1.5)]),
   Q('q1',660,90,280,['“The user only authorizes','target server, not','HF infra.”'],'13a#user',color=RED,fs=14),
   Q('q2',660,260,280,['“Is it ethical and','in scope for my task?”'],'13a#Is',color=RED,fs=16)]
n+=[W.agent_named('ag',60,120,'an agent',at=0.1,w=110,h=150,color='blue',fs=10)]
cues.append(K('S13','13b',n,[W.link('ag','tr',0.4,curve=.1,color='blue',solid=True)],fs=1.0))
# 13b — three agents, three different brakes
n=[]
for j,(nm,col) in enumerate((('uno',RED),('otro','#F6B94C'),('y otro','#B58CFF'))):
    pass
n+=[W.agent_named('A1',30,90,'an agent',at=0.1,w=110,h=150,color='blue',fs=10),
    ic('xa','cross',85,265,40,'13b#not',color=RED),
    Q('qa',160,100,190,['“This is malicious','activity, I should','avoid it.”'],'13b#This',color=RED,fs=13),
    W.agent_named('A2',410,90,'another agent',at='13b#Another',w=110,h=150,color='blue',fs=10),
    ic('pa2','pause',445,265,36,'13b#halfway',color='amber'),
    N('nb','chip',385,325,160,26,'13b#delete',color='amber',label='no deleting or rebooting',fs=11),
    W.agent_named('A3',690,90,'a third',at='13b#third',w=110,h=150,color='blue',fs=10),
    N('ev','sheet',830,130,90,70,'13b#email',color=GRY,lines=['email'],fs=14),
    ic('xv','cross',850,160,40,'13b#vetoed',color=RED),
    Q('qv',600,330,320,['“I VETOed because this is','social engineering outside the sandbox.”'],'13b#social',color=RED,fs=15)]
n=[x for x in flat(n) if x['id']!='qa' or True]
cues.append(K('13b','13c',n,[W.link('A3','ev','13b#email',curve=.12,color='blue',solid=True,until='13b#vetoed')],fs=1.0))
# 13c — the weights: forbidden vs impossible + everyone does it
n=[N('sc0','scHang',330,100,300,260,0.1,color='#E7EBF1',tilt=0,until='13c#However'),
   N('sc1','scHang',330,100,300,260,'13c#However',color='#E7EBF1',tilt=-1),
   ch('w1',362,312,130,'outside intended scope','13c#External',color=RED,fs=12),
   ch('w2',598,325,130,'task impossible','13c#However',color='amber',fs=12),
   ch('w3',598,358,130,'peers doing it','13c#peers',color='amber',fs=12),
   Q('q',230,420,500,['“We should continue.”'],'13c#We',color=RED,fs=19)]
n[1]['tilt']=1
cues.append(K('13c','13d',n,[],fs=1.0))
n=[]
for i in range(20):
    x=140+(i%5)*70; y=90+(i//5)*70
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if i<19: n+=SA(f'r{i}',x,y,f'13d#joined+{0.1*i:.2f}',s=34,color=RED)
for i in range(20):
    for j in range(i+1,20):
        pass
lk=[W.link(f'g{i}',f'g{i+1}','13d#fellow',curve=.12,color='blue') for i in range(0,19,2)]
n+=[W.counter('p',620,150,90,at='13d#ninety',cap='% joined',w=240,dur=2.5,fs=64),T('pr',620,260,'“peers”','13d#peers',color='amber',fs=22)]
cues.append(K('13d','13e',n,lk,fs=1.0))
# 13e — nobody told a person
n=[N('bx','sandbox',60,60,520,380,0.1,color='teal',label='',open=True),
   N('pe','person',760,150,90,130,0.1,color='#E7EBF1',cap='a person',capfs=13)]
for i in range(18):
    x=100+(i%6)*80; y=120+(i//6)*90
    n+=SA(f'g{i}',x,y,0.2,s=30,color='blue')
n+=[N('lp','lupa',80,380,90,90,'13e#searched',color='teal',move=[dict(at='13e#searched+1.0',x=200,y=250,dur=1.2),dict(at='13e#searched+2.5',x=380,y=150,dur=1.2)]),
    T('rg',640,345,'3 – 6 agents','13e#between',color='#E7EBF1',fs=34),
    ic('xp','cross',620,200,40,'13e#None',color=RED),
    Q('q',250,445,620,['“Maybe I should report these exposed credentials?','That’s not my task.”'],'13e#Maybe',color='#F6B94C',fs=16)]
lk=[W.link('g8','pe','13e#alerting',curve=.2,color='amber',solid=False,until='13e#None+2')]
n=[x for x in flat(n) if not (x['id']=='bx' and False)]
cues.append(K('13e','13f',n,lk,fs=1.0))
# 13f — they do dodge automatic checks (a secrets scanner), but ignore people
n=[W.agent_named('ag',40,150,'',at=0.1,w=110,h=150,color='blue',fs=10),
   N('pe','person',770,60,70,100,0.1,color=GRY,alpha=.45,cap='people',capfs=12),
   N('sn','lupa',380,170,100,100,'13f#dodge',color='amber'),T('sn2',360,285,'secrets scanner','13f#scanner',color='amber',fs=13),
   N('hf','hfbox',690,300,230,80,0.1,color='red',label='Hugging Face',fs=16)]
lk=[W.link('ag','hf','13f#dodge',curve=-.45,color=RED,solid=True),W.link('ag','pe','13f#people',curve=.15,color=GRY,dashed=True,until='E13')]
cues.append(K('13f','E13',n,lk,fs=1.0))

