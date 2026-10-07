# Scene 1 · Cajas selladas
MUSIC={'bells': 0.7, 'pad': 0.6}
cues=[]
GX0,GY0,GP=350,200,30
sol={13,34,50,71,88}; CH=41
n=[W.agent_named('ac',60,150,'PHASEONE10841',at=0.4),
   W.console('co',265,160,w=250,h=230,at='1a#ordenador',until='1b#copias',fs=13,lh=17,cols=28),
   ]
lk=[W.link('ac','co','1a#ordenador',bi=True,curve=.12,until='1b#copias')]
for i in range(96):
    x=GX0+GP*(i%12); y=GY0+GP*(i//12); t0='1b#copias+%.2f'%(0.04*i)
    if i==CH: n+=W.agent('chs',x,y,t0,s=18,box=False)
    else: n+=W.agent(f'gr{i}',x,y,t0,s=18,color='teal' if i in sol else 'blue',box=False,until='1c#caja')
n+=[ch('t1',445,150,100,'HPIM ~95 %','1b#HPIM',color='blue',until='1c#caja'),ch('t2',575,150,135,'GPT-5.6 Sol ~5 %','1b#GPT',color='teal',until='1c#caja')]
n+=[W.sandbox_onion('on',GX0+GP*5,GY0+GP*3,size=90,layers=3,core=22,sw=1.5,at='1c#caja+1.0')]
n+=[W.folder_view('art',620,205,[dict(name='docker-remote/',dir=True),dict(name='pypi-remote/',dir=True),dict(name='numpy-1.26.4.whl'),dict(name='torch-2.4.0.whl')],w=230,h=140,rh=21,fs=10,at='1d#Salvo+0.3')]
lk+=[W.link('on','art','1d#Salvo+1.0',bi=True,curve=.1)]
cm=[dict(at='S1',x=50,y=50,z=1),dict(at='1c#caja',x=50,y=50,z=1),dict(at='1c#caja+2.5',x=(GX0+GP*5)/9.6,y=(GY0+GP*3)/5.4,z=3.5,dur=2.5),
    dict(at='1d#Salvo',x=(GX0+GP*5+735)/2/9.6,y=(GY0+GP*3)/5.4,z=1.6,dur=1.6)]
# the same agent card fades out with the others
n[0]['until']='1c#caja'
cues.append(K('S1','E1',n,lk,fs=1.0,cam=cm))
