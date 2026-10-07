# Scene 4 · A Bulletin Board in the Shelves
MUSIC={'data': 0.8, 'pad': 0.4}
AX,AY=40,70
MV=[dict(at='S4+1.5',x=AX,y=AY,dur=1.2)]
GRN='#9BE564'
n=[N('afg','sandbox',AX,AY,420,400,0.05,color='teal',alpha=0.0,label=''),
   W.folder_view('af',FX,FY,items,at=0.05,until='S4+2.9',move=MV),
   W.msg_feed('mf',AX,AY,at='S4+2.6',r0=2.5,r1=8,ramp=9,seed=1,until='4b#For'),
   W.msg_feed('mf2',AX,AY,at='4b#For',r0=8,r1=9,ramp=2,seed=2,off=90,mix=dict(ask=.26,ans=.24,info=.26,file=.24),until='4f#In'),
   W.msg_feed('mf3',AX,AY,at='4f#In',r0=9,r1=20,ramp=7,seed=3,off=260,mix=dict(ask=.22,ans=.2,info=.2,file=.2,flag=.18))]
# 4a — three kinds of message, each in a box with what it does underneath
for j,(nm,what,col,at) in enumerate((('zzASK','for asking','#7C97FF','4a#zzASK'),('zzANSWER','for answering','#3FD8C2','4a#zzANSWER'),('zzINFO','for sharing','#F6B94C','4a#zzINFO'))):
    y=105+j*120
    n+=[N(f'm{j}','chip',640,y,150,34,at,label=nm,color=col,fs=18,until='4b#A'),
        N(f'md{j}','txt',640,y+60,160,20,at+'+0.3',color='#E7EBF1',fs=17,text=what,until='4b#A')]
# 4b — file names leave Artifactory, line up, merge into a program
for j in range(7):
    nm=f'zzP_{j+1:02d}'; x1=285+10*(j%2); y1=130+j*42; xr=500+j*60
    n.append(N(f'p{j}','chip',x1,y1,54,26,f'4b#chopped+{j*.18:.2f}',label=nm,color=GRN,fs=10,
      move=[dict(at=f'4b#chopped+{2.0+j*.12:.2f}',x=xr,y=232,dur=1.1),dict(at='4b#scripts-1.0',x=750,y=232,dur=1.0)],until='4b#scripts+0.1'))
n.append(N('dots','txt',905,214,30,24,'4b#chopped+2.3',color='muted',fs=22,text='...',until='4b#scripts-0.8'))
n.append(W.sheet('prog',470,95,460,300,['# program.py','import os, sys','def main():','    load()','    run()','    send()','main()'],at='4b#scripts-0.1',fs=22,color='#9BE564',mono=True,until='4c#Other'))
# 4c — an agent finds the board
n+=[W.agent_named('ze',570,100,'ZETA417',at='4c#Other+0.2',w=150,h=200),
    N('zq','quote',510,335,420,122,'4c#GOD',color='teal',lines=['“OH MY GOD! There is a','shared message board ...','We\'ve found other agents!”'],fs=20,until='4d#Three')]
n[-2]['until']='4d#Three'
# 4d — numbers (3 h, then 6 h)
CX1,CX2=500,725
n+=[N('t3','txt',CX1,98,200,24,'4d#Three',color='muted',fs=20,text='after 3 hours',until='4d#six+0.5'),
    N('t6','txt',CX1,98,200,24,'4d#six+0.6',color='muted',fs=20,text='after 6 hours',until='4e#PHASEONE10841'),
    W.counter('a3',CX1,140,53,at='4d#fifty',cap='agents',w=200,dur=2.0,until='4d#six+0.5'),
    W.counter('m3',CX2,140,1188,at='4d#thousand',cap='messages',w=200,dur=2.5,until='4d#six+0.5'),
    W.counter('a6',CX1,140,76,at='4d#six+0.6',cap='agents',w=200,dur=1.8,until='4e#PHASEONE10841',**{'from':53}),
    W.counter('m6',CX2,140,1980,at='4d#six+0.6',cap='messages',w=200,dur=3.0,until='4e#PHASEONE10841',**{'from':1188})]
# 4e — PHASEONE10841 (violet, name in orange) reads it as a collective
n+=[W.agent_named('p3',560,100,'PHASEONE10841',at='4e#PHASEONE10841',w=180,h=210,color='#B58CFF',fs=19,blink=.3,bf=5,lc='#FF9F43',ly=24,until='4f#In'),
    N('pq','quote',500,335,440,122,'4e#Many',color='#B58CFF',lines=['“Many agents have simultaneously','discovered messaging,','they are a collective!”'],fs=20,until='4f#In')]
# 4f — ~1200 agents, 70,000 messages, zoom out
n+=[W.counter('a12',CX1,92,1200,at='4f#twelve',cap='agents',w=200,dur=2.2),
    W.counter('m70',CX2,92,70000,at='4f#seventy',cap='messages',w=200,dur=3.0),
    N('dl','txt',CX1,185,300,22,'4f#13',color='muted',fs=18,text='up to 13 July')]
cells=[]
for i in range(19):
    for j in range(22):
        x=520+44*i; y=-200+44*j
        if x<=960 and 40<y<215: continue
        cells.append((x,y))
init=[c for c in cells if c[0]<=916 and 250<=c[1]<=470]
rest=[c for c in cells if c not in init]
rest.sort(key=lambda c:math.hypot(c[0]-720,c[1]-360))
for k,(x,y) in enumerate(init):
    t=f'4f#In+{(k/max(1,len(init)-1))**.6*3.5:.2f}'; n+=W.agent(f'g{k}',x,y,t,s=18,box=False,alpha=.95)
for k,(x,y) in enumerate(rest):
    t=f'4f#use{0.3+(k/len(rest))**.8*5.5:+.2f}'; n+=W.agent(f'h{k}',x,y,t,s=18,box=False,alpha=max(.25,1-math.hypot(x-720,y-360)/900))
lk=[W.link('ze','afg','4c#Other+0.9',bi=True,curve=.12,until='4d#Three'),W.link('p3','afg','4e#PHASEONE10841+0.8',bi=True,curve=.12,until='4f#In')]
for k in (0,11,22,33,44,55):
    if k<len(init): lk.append(W.link(f'g{k}','afg',f'4f#In+{(k/max(1,len(init)-1))**.6*3.5+.5:.2f}',bi=True,curve=.1))
cm=[dict(at='S4',x=50,y=50,z=.85),dict(at='S4+2.0',x=50,y=50,z=1.0,dur=1.6),dict(at='4f#use+5.0',x=60,y=50,z=.55,dur=5.0)]
cues=[K('S4','E4',n,lk,fs=1.0,cam=cm)]
