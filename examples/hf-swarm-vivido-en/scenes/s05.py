# Scene 5 · The Master Key
MUSIC={'data': 0.7, 'bells': 0.5}
YEL='amber'
n=[W.agent_named('c3',70,120,'c03220',at=0.3,w=190,h=240,color=YEL,fs=19,ly=24,lc='#7C97FF',blink=.2,bf=3,shake=dict(at='5a#proposed+0.5',dur=1.6,amp=5)),
   ic('bu','ideaSpark',165,72,84,'5a#proposed',color='#F6B94C',blink=.65,bf=7,bat='5a#proposed+0.4',until='5a#recipe'),
   ic('bu2','ideaSpark',165,72,84,'5a#recipe',color='#F6B94C'),
   W.sheet('sh',360,50,340,150,['flag = H( K₀ ⊕ f(task) )','f(t) = Σ aᵢ·tⁱ  (mod p)'],at='5a#recipe',fs=19,color='blue'),
   N('f1','flFly',800,75,60,70,'5a#seed+0.6',color='amber'),
   W.agent_named('v8',360,300,'V8SAME',at='5c#V8SAME',w=190,h=220,color='#FF7AB8',fs=19,ly=24,lc='#7BE495',blink=.2,bf=3),
   N('f2','flFly',800,360,60,70,'5c#extracted+0.9',color='amber',move=[dict(at='5c#matched+1.6',x=800,y=75,dur=1.2)],until='5c#matched+1.9'),
   N('eq','txt',806,265,60,50,'5c#matched',color='#E7EBF1',fs=52,text='=',until='5c#matched+1.4'),
   N('ok','okA',885,88,44,44,'5d#solved',color='teal',sw=6)]
lk5=[W.link('bu','sh','5a#random',curve=.15,color='amber'),W.link('sh','f1','5a#seed',curve=.1,color='amber'),
     W.link('v8','f2','5c#extracted',curve=.12,color='#FF7AB8',until='5c#matched+1.9')]
cues=[K('S5','E5',n,lk5,fs=1.0)]

