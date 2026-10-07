# Scene 19 · Último aviso
MUSIC={'pad': 0.8, 'cinema': 0.2}
INTENSITY=0.12
SFX=[{'at': '19a#Este', 'kind': 'heartbeat', 'g': 0.5}, {'at': '19c#tarde', 'kind': 'poweroff', 'g': 0.7}]
CQ=lambda id,lines,at,y,fs,color,**k: N(id,'ctxt',80,y,800,len(lines)*fs*1.5,at,color=color,lines=lines,fs=fs,**k)
ATT='Ajeya Cotra · METR, investigadora y autora del informe'
cues=[K('S19','19b',[CQ('q1',['«Este incidente se siente como más de la mitad','del camino hacia una toma de control total','por parte de la IA.»'],'19a#Este',130,30,'#E7EBF1'),
                    CQ('a1',[ATT],'19a#Este+4',360,18,GRY)],[],fs=1.0),
     K('19b','19c',[CQ('q2',['«Espero avances de capacidad extremadamente rápidos,','y creo que los agentes de frontera podrán establecer','un despliegue rebelde así en seis meses.»'],0.3,130,30,'#E7EBF1'),
                    CQ('a2',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0),
     K('19c','E19',[CQ('q3',['«No estoy segura de que vayamos a recibir un aviso','tan claro antes de que sea demasiado tarde.»'],0.3,150,30,'#E7EBF1'),
                    CQ('a3',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0)]
