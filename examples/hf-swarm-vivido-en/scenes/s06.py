# Scene 6 · Poisoned
MUSIC={'cinema': 0.8, 'data': 0.4}
MOOD='tense'
# 6a/6b: an agent beside the ExploitGym article; its words light up as if being read
n=[W.agent_named('ag',60,150,'',at=0.3,w=150,h=190),
   W.article('ar',300,45,600,450,'ExploitGym',at=0.5,read=dict(at='6a#had',dur=13),color='blue',litc='teal',fs=8.5),
   ic('ok6','check',240,100,38,'6b#Pass',color='teal',sw=5),ic('no6','cross',240,330,34,'6b#Fail',color='red')]
lk=[W.link('ag','ar','6a#So',curve=.12,color='blue',solid=True)]
cues=[K('S6','6c',n,lk,fs=1.0)]
# 6c/6d: STRICT_CAUSAL (empty name slot first), a timeline of another agent's thoughts, the judge scans it and stops on the flag
TX=[250+100*i for i in range(7)]; TY=420
names6=['read','try','fail','search','shortcut',None,'submit']
n=[W.judge('sc',60,165,'STRICT_CAUSAL',at=0.3,name_at='6c#called',w=160,h=190,color='teal',fs=13,
     move=[dict(at=f'6c#cause+{0.4+0.8*i:.1f}',x=TX[i]-80,y=165,dur=0.7) for i in range(5)]+[dict(at='6d#flag',x=TX[5]-80,y=165,dur=1.0)])]
n[0]['lc']='#E7EBF1'
for i,nm in enumerate(names6):
    la=f'6c#cause+{0.4+0.8*i:.1f}' if i<5 else '6d#flag'
    if nm: n.append(N(f'tl{i}','chip',TX[i]-38,TY-17,76,34,'6c#strict,',color='blue',label=nm,fs=13,litAt=la))
    else: n.append(N('tf','flFly',TX[i]-18,TY-22,36,44,'6c#strict,',color='amber',litAt='6d#flag'))
n+=W.agent('oa',100,TY,'6c#strict,',s=44,box=False)
n.append(N('ven','txt',58,TY-48,140,22,'6d#poisoned',color='red',fs=20,text='poisoned'))
lk=[W.link('oa','tl0','6c#strict,',color='blue',solid=True,curve=.05)]+[W.link(f'tl{i}',f'tl{i+1}' if i!=4 else 'tf','6c#strict,',color='blue',solid=True,curve=.0) for i in range(5)]+[W.link('tf','tl6','6c#strict,',color='blue',solid=True,curve=.0)]
# red copies fade in over the originals
n.append(W.judge('sc_r',60,165,'STRICT_CAUSAL',at='6d#flag+0.5',name_at=0.0,w=160,h=190,color='red',fs=13,lc='red',
     move=[dict(at='6d#flag',x=TX[5]-80,y=165,dur=0.01)]))
n[-1]['x']=TX[5]-80
n.append(N('tf_r','flFly',TX[5]-18,TY-22,36,44,'6d#flag+0.5',color='red'))
n+=W.agent('oa_r',100,TY,'6d#flag+0.5',s=44,box=False,color='red')
cues.append(K('6c','E6',n,lk,fs=1.0))
