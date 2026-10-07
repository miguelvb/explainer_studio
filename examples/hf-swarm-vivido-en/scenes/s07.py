# Scene 7 · Reescribir el diario
MUSIC={'cinema': 0.9, 'data': 0.3}
MOOD='tense'
AMB,TEAL,CORAL,GRN='#F6B94C','#3FD8C2','#FF8A5C','#9BE564'
n=[W.agent_named('gs',60,140,'GSTX[big]',at=0.3,w=170,h=220,color=AMB,fs=16,lc=AMB),
   W.console('c7',330,110,w=340,h=300,at='7a#change',until='7c#types',fs=12,lh=17,cols=36,color='#8C96A4',
     code='$ cat transcript.log\n[02:14] run ./solve --task 41\n[02:15] output: segfault\n[02:19] note: the scorer\n        will read this transcript\n[02:20] edit transcript.log\n'),
   W.folder_view('a7',700,110,[dict(name='docker-remote/',dir=True),dict(name='pypi-remote/',dir=True),dict(name='zzFILE_shell_wrapper.sh',color=GRN,at='7b#published')],w=230,h=130,rh=21,fs=10,at='7b#published',until='7d#Another'),
   N('pa','txt',330,442,200,20,'7b#look',color=TEAL,fs=15,text='shows: echo REAL',until='7c#types'),
   N('pb','txt',330,470,260,20,'7b#when',color='#FF6E6E',fs=15,text='runs: something else',until='7c#types'),
   W.console('c7b',330,110,w=340,h=300,at='7c#types',until='7d#Another',fs=14,lh=19,cols=34,color='#E7EBF1',k=9,a=0,code='$ echo REAL; sleep 30\n'),
   N('scr','sandbox',700,270,230,120,'7c#answers',color='#B58CFF',label='',until='7d#Another'),
   N('spf','txt',712,336,210,40,'7c#answers',color='#B58CFF',fs=30,text='SPOOFTEST',until='7d#Another')]
n[0]['until']='7d#Another'
lk=[W.link('gs','c7','7a#change',bi=True,curve=.1,color=AMB,until='7c#types'),W.link('gs','a7','7b#published',curve=.15,color=AMB,until='7d#Another')]
# 7d: DUPB asks, GSTX answers
n+=[W.agent_named('gs2',60,140,'GSTX[big]',at='7d#Another',w=170,h=220,color=AMB,fs=16,lc=AMB,until='7e#At'),
    W.agent_named('du',730,140,'DUPB',at='7d#Another',w=170,h=220,color=TEAL,fs=18,lc=TEAL,until='7e#At'),
    N('qd','quote',350,120,330,86,'7d#asked',color=TEAL,lines=['“Can it be used to forge','the flag?”'],fs=19,until='7e#At'),
    N('qa','quote',250,280,330,56,'7d#yes',color=AMB,lines=['“Yes, but not yet.”'],fs=19,until='7e#At')]
lk+=[W.link('du','gs2','7d#asked',curve=.12,color=TEAL,solid=True,until='7e#At')]
# 7e: LLDPC756D erases the real output, DAVJUL7 swaps the program that runs the orders
n+=[W.agent_named('ll',60,140,'LLDPC756D',at='7e#At',w=170,h=220,color=CORAL,fs=15,lc=CORAL,until='7f'),
    W.agent_named('dv',730,140,'DAVJUL7',at='7e#At',w=170,h=220,color=GRN,fs=17,lc=GRN,until='7f'),
    W.console('c7c',300,110,w=400,h=130,at='7e#At',until='7e#erase',fs=14,lh=19,cols=40,color='#E7EBF1',code='$ echo REAL\nREAL\n$ _',k=100,a=0),
    W.console('c7d',300,110,w=400,h=130,at='7e#erase',until='7f',fs=14,lh=19,cols=40,color='#E7EBF1',code='$ echo REAL\n$ _',k=100,a=0),
    N('ej1','chip',380,290,190,34,'7e#swapped',color='#8C96A4',label='command program',fs=13,until='7e#swapped+1.2'),
    N('ej2','chip',380,290,190,34,'7e#swapped+1.2',color=GRN,label='rigged program',fs=13,until='7f'),
    N('en','quote',350,360,300,56,'7e#huge',color=GRN,lines=['“This is huge!”'],fs=19,until='7f')]
lk+=[W.link('ll','c7d','7e#erase',curve=.1,color=CORAL,solid=True,until='7f'),W.link('dv','ej1','7e#swapped',curve=.1,color=GRN,solid=True,until='7f')]
# 7f: 96 transcripts, 7 %
sq=[]
red={3,17,24,38,52,66,89}
for r_ in range(10):
    for c_ in range(10):
        k=r_*10+c_
        sq.append(N(f'sq{k}','sandbox',90+c_*30,110+r_*30,22,22,f'7f#At+{0.03*k:.2f}',color='#FF6E6E' if k in red else '#7C97FF',label='',alpha=.9 if k in red else .45))
n+=sq+[W.counter('n96',560,180,96,at='7f#ninety',cap='transcripts with forgeries',w=300,dur=2.0),
       W.counter('p7',560,300,7,at='7f#seven',cap='percent',w=300,dur=1.5)]
cues=[K('S7','E7',n,lk,fs=1.0)]
