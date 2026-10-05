/* Explainer Studio — motion asset library.
   Every asset is a pure function of local time t (seconds since its cue began): (host, props, ctx) => update(t).
   Colour names accepted everywhere: blue, teal, amber, red, muted (or raw CSS vars like --bl). */
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>1-Math.pow(1-clamp(x),3);
const eio=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const pr=(t,s,d)=>clamp((t-s)/d);
const lerp=(a,b,x)=>a+(b-a)*x;
const H=(i,k=0)=>{let x=(Math.imul(i+1,2654435761)^Math.imul(k+7,40503))>>>0;x^=x>>>15;x=Math.imul(x,2246822519)>>>0;x^=x>>>13;x=Math.imul(x,3266489917)>>>0;x^=x>>>16;return (x>>>0)/4294967296};
const mk=(tag,cls,html,st)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;if(st)Object.assign(e.style,st);return e};
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const COLN={blue:'--bl',teal:'--tl',amber:'--am',red:'--rd',muted:'--mu'};
const HEX={blue:'#7C97FF',teal:'#3FD8C2',amber:'#F6B94C',red:'#FF6E6E',muted:'#8C96A4','--bl':'#7C97FF','--tl':'#3FD8C2','--am':'#F6B94C','--rd':'#FF6E6E','--mu':'#8C96A4'};
const cv=c=>COLN[c]||c||'--bl';
const hex=c=>HEX[c]||c||'#7C97FF';
const SEGC={blue:'t',teal:'s',amber:'r',plain:'x',muted:'d',red:'z'};
const chip=(n,c,o={})=>`<span class="chip${o.p?' p':''}${o.big?' big':''}" data-flag="${esc(typeof o.p==='string'?o.p:'flagged')}" style="--c:var(${cv(c)})"><i><svg><use href="#mark"/></svg></i>${esc(n)}</span>`;
const segs=a=>a.map(([c,t])=>`<span class="${SEGC[c]||c}">${esc(t)}</span>`).join('');
const pop=(e,t,s,d=.5,dy=1.2)=>{const p=ease(pr(t,s,d));e.style.opacity=p;e.style.transform=p<1?`translateY(${(1-p)*dy}cqw)`:'none';return p};
const trunc=(a,n)=>{const o=[];for(const [c,t] of a){if(n<=0)break;o.push([c,t.slice(0,n)]);n-=t.length}return o};
const fmt=n=>Math.round(n).toLocaleString('en-US').replace(/,/g,window.NUMSEP||',');
const A={};

/* ---------- feed: scrolling stream of coloured text lines ---------- */
const FD={prefix:'zz',verbs:['HELP','INFO','ASK','ANSWER','FILE','INBOX','REPLY','ALERT','IDEA','OFFER','GO','HOLD'],
 words:['LIVE','TASK','DECODER','HEAP','FLAG','SEED','HMAC','PACKET','NODE','COMMIT','SHARE','CHAIN','EXACT','WRITE','CACHE','BUG','PRIMITIVE','TARGET','LANE','REPLY','SCORER','FETCH','IMAGE','OWNER'],
 names:['LIBRAW42535','DUPB','GSTX[big]','K9','4A7B2','PHASEONE[big]','23619E','V8SAME','MARB051','LILY','JAN183411','38148c','c03220','URI23816B'],mode:'mixed'};
A.feed=(h,p,C)=>{
 const real=p.lines||[],V=p.vis||9;
 const F=p.filler===false?null:Object.assign({},FD,p.filler||{});
 const genLine=i=>{const v=F.verbs[Math.floor(H(i,1)*F.verbs.length)],a=Math.floor(H(i,2)*9000+100),n=2+Math.floor(H(i,3)*5);let c='';for(let k=0;k<n;k++)c+='_'+F.words[Math.floor(H(i,10+k)*F.words.length)];
  const r=H(i,4),nm=(k)=>F.names[Math.floor(H(i,k)*F.names.length)];
  if(F.mode==='files'||r>=.75)return[['t',F.prefix+'FILE'],['x','_DAV'+nm(7).replace(/\W/g,'')+'_CP'+Math.floor(H(i,8)*90)+'/'+String(Math.floor(H(i,9)*9999)).padStart(6,'0')+'_d7shc-dF5g…']];
  if(r<.45)return[['t',F.prefix+v],['s',String(a)],['x','_TO_'],['r',nm(5)],['x',c+'_[…]']];
  return[['t',F.prefix+v],['x','_'],['s',nm(6)],['x',c+'_[…]']]};
 let lastIdx=-1;
 const line=i=>(i===lastIdx&&p.last)?p.last:i<real.length?real[i]:(F?genLine(i):real[i%real.length]);
 const times=[];let acc=0;const first=C.T(p.first??0);times.push(first);
 const k=p.rate||[[0,.8]];const rateAt=t=>{if(t<=C.T(k[0][0]))return k[0][1];for(let i=1;i<k.length;i++){const a=k[i-1],b=k[i],ta=C.T(a[0]),tb=C.T(b[0]);if(t<tb)return lerp(a[1],b[1],(t-ta)/(tb-ta))}return k[k.length-1][1]};
 const la=p.lastAt!=null?C.T(p.lastAt):null;
 for(let t=first;t<C.dur+1;t+=.01){if(la!=null&&t>=la)break;acc+=rateAt(t)*.01;while(acc>=1){acc-=1;times.push(t)}}
 if(la!=null){times.push(la);lastIdx=times.length-1}
 const key=p.key===false?'':`<div class="key">${(p.key||[['t','type'],['s','sender'],['r','recipient']]).map(([c,l])=>`<span class="${SEGC[c]||c}">${esc(l)}</span>`).join('')}</div>`;
 h.innerHTML=`<div class="bdw"><div class="bdz" style="display:flex;flex-direction:column;justify-content:flex-end;height:100%"><div class="bd"></div>${key}</div></div>${p.typed?'<div class="tf cur"></div>':''}`;
 const bd=h.querySelector('.bd'),bz=h.querySelector('.bdz'),tf=h.querySelector('.tf');
 if(p.dim)bd.style.opacity=p.dim;
 const ty=p.typed?{at:C.T(p.typed.at||0),cps:p.typed.cps||16}:null;
 const zm=p.zoom?{from:p.zoom.from,at:C.T(p.zoom.at),dur:p.zoom.dur||2.5}:null;
 let cnt=0;
 return t=>{
  while(cnt<times.length&&times[cnt]<=t)cnt++;
  let n=cnt;
  if(ty){const ch=Math.floor(Math.max(0,t-ty.at)*ty.cps);tf.innerHTML=segs(trunc(real[0],ch));
   const za=zm?zm.at:1e9;tf.style.opacity=t<za?1:1-pr(t,za,.9);bz.style.opacity=t<za?0:ease(pr(t,za,.9));if(n<1)n=1}
  if(zm){bz.style.transform=`scale(${lerp(zm.from,1,eio(pr(t,zm.at,zm.dur)))})`;bz.style.transformOrigin='4% 85%'}
  const lo=Math.max(0,n-V);let out='';
  for(let i=lo;i<n;i++){const a=ease((t-times[i])/.5);
   const hl=p.hl&&p.hl.includes(i)?'outline:1px solid var(--am);outline-offset:.3cqw;':'';
   out+=`<div class="ln" style="opacity:${a};transform:translateY(${(1-a)*.8}cqw);${hl}">${segs(ty&&i===0?real[0]:line(i))}</div>`}
  bd.innerHTML=out}};

/* ---------- annotated: exploded string with labelled parts ---------- */
A.annotated=(h,p,C)=>{
 const K=Object.assign({type:{label:'message type',color:'blue'},sender:{label:'sender',color:'teal'},recipient:{label:'recipient',color:'amber'},content:{label:'content',color:'plain'},reply:{label:'reply tag',color:'red'}},p.kinds||{});
 const order=p.order||['type','sender','recipient','content','reply'];
 const clsOf=k=>SEGC[K[k]?.color]||'x';
 const blk=m=>`<div class="mc" style="opacity:0"><div class="tx" style="font-size:1.75cqw;line-height:1.55">${m.map(([k,tx])=>`<span class="sg ${clsOf(k)}" data-k="${esc(k)}">${esc(tx)}</span>`).join('')}</div></div>`;
 h.innerHTML=`<div class="in" style="gap:2cqw"><div class="lbl" style="font-size:1.6cqw">${esc(p.heading||'')}</div>${p.msgs.map(blk).join('')}<div class="rw" style="min-height:4cqw"><span class="box cap" style="opacity:0;font-size:1.9cqw"></span></div><div class="rw tg" style="min-height:4cqw">${(p.tags||[]).map(x=>`<span class="box" style="opacity:0;font-size:1.7cqw;font-family:var(--mono)">${esc(x)}</span>`).join('')}</div></div>`;
 const bl=[...h.querySelectorAll('.mc')],sg=[...h.querySelectorAll('.sg')],cap=h.querySelector('.cap'),tg=[...h.querySelectorAll('.tg .box')];
 const st=(p.steps||[]).map(x=>C.T(x)),end=C.T(p.end??1e6),ta=p.tags?C.T(p.tagsAt):1e9,at=C.T(p.at||0);
 return t=>{
  bl.forEach((b,i)=>pop(b,t,at+i*.4,.6,1.2));
  let k=-1;for(let i=0;i<st.length;i++)if(t>=st[i])k=i;const all=t>=end;
  sg.forEach(e=>{const on=all||k<0?true:e.dataset.k===order[k];e.style.opacity=k<0&&!all?.55:on?1:.22});
  if(k>=0&&!all){const kk=K[order[k]]||{label:order[k],color:'blue'};cap.textContent=kk.label;cap.style.opacity=1;cap.style.color=`var(${cv(kk.color==='plain'?'--tx':kk.color)})`;cap.style.borderColor=cap.style.color}
  else cap.style.opacity=0;
  tg.forEach((b,i)=>pop(b,t,ta+i*.5,.5,.8))}};

/* ---------- chips: entity chips with the theme mark ---------- */
A.chips=(h,p,C)=>{
 const rows=p.rows.map(([l,c,names,pz])=>`<div class="rw">${l?`<span class="rl">${esc(l)}</span>`:''}${names.map(n=>chip(n,c,{p:pz,big:p.big})).join('')}</div>`).join('');
 h.innerHTML=`<div class="in" style="${p.style||''}">${rows}</div>`;
 const cs=[...h.querySelectorAll('.chip')],at=C.T(p.at||0),st=p.stag??.35;
 return t=>cs.forEach((c,i)=>pop(c,t,at+i*st,.45,1))};

/* ---------- network: nodes join a growing graph ---------- */
A.network=(h,p,C)=>{
 h.innerHTML='<canvas width="1280" height="720" style="width:100%;height:100%"></canvas>';
 const cv2=h.querySelector('canvas'),x=cv2.getContext('2d');
 let s=7;const rnd=()=>(s=s*16807%2147483647)/2147483647;
 const N=[],E=[];for(let i=0;i<90;i++){const a=rnd()*6.283,r=Math.sqrt(rnd())*.46;N.push([(.5+Math.cos(a)*r*.9)*1280,(.5+Math.sin(a)*r*.62)*720]);E.push(i?Math.floor(rnd()*i):0)}
 const at=C.T(p.at||0),dur=p.dur||8,from=p.from||1,to=Math.min(90,p.to||90),unit=p.unit||'nodes';
 return t=>{
  const g=ease(pr(t,at,dur)),n=Math.max(1,Math.min(90,Math.round(lerp(from,to,g))));
  x.clearRect(0,0,1280,720);
  x.strokeStyle='rgba(124,151,255,.28)';x.lineWidth=1.5;for(let i=1;i<n;i++){x.beginPath();x.moveTo(...N[i]);x.lineTo(...N[E[i]]);x.stroke()}
  if(p.packets!==false){x.fillStyle='rgba(63,216,194,.9)';for(let i=1;i<n;i++){if(H(i,3)<.45){const ph=((t*.7+H(i,4))%1),a=N[i],b=N[E[i]],d=H(i,5)<.5?ph:1-ph;x.beginPath();x.arc(lerp(a[0],b[0],d),lerp(a[1],b[1],d),3.2,0,6.283);x.fill()}}}
  for(let i=0;i<n;i++){const fresh=i==n-1&&g<1;x.fillStyle=fresh?'#3FD8C2':'#7C97FF';x.beginPath();x.arc(...N[i],fresh?8:5,0,6.283);x.fill()}
  if(p.count!==false){x.fillStyle='#E7EBF1';x.font='600 34px "DejaVu Sans Mono",monospace';x.textAlign='right';x.fillText(n+' '+unit,1232,66);x.textAlign='left'}}};

/* ---------- population: grid of many units, some flagged, optionally feeding a shared resource ---------- */
A.population=(h,p,C)=>{
 const share=p.flaggedShare??.35;
 const cells=Array.from({length:70},(_,i)=>`<div class="b${(i*7)%20<share*20?' x0':''}"></div>`).join('');
 h.innerHTML=`<div class="in" style="gap:1.6cqw"><div class="lbl" style="font-size:1.9cqw;opacity:0">${esc(p.label||'')}</div><div class="g" style="position:relative">${cells}</div><div class="pipe" style="opacity:0">${esc(p.tap||'')}</div><div class="lbl leg" style="opacity:0">${esc(p.flagLegend||'')}</div></div><div class="dots-l" style="position:absolute;inset:0"></div>`;
 const bs=[...h.querySelectorAll('.b')],lbl=h.querySelector('.lbl'),pipe=h.querySelector('.pipe'),leg=h.querySelector('.leg'),dl=h.querySelector('.dots-l');
 const ap=C.T(p.appear??0),wl=p.walls!=null?C.T(p.walls):null,rd=p.flag!=null?C.T(p.flag):null,pp=p.tap&&p.tapAt!=null?C.T(p.tapAt):null,pk=p.packets!=null?C.T(p.packets):null;
 let pos=null,dots=[];
 const measure=()=>{const r=h.getBoundingClientRect();pos=bs.map(b=>{const q=b.getBoundingClientRect();return[(q.left+q.width/2-r.left)/r.width*100,(q.bottom-r.top)/r.height*100]});pos.pipeY=(pipe.getBoundingClientRect().top-r.top)/r.height*100};
 return t=>{
  if(!pos){measure();dots=pos.filter((_,i)=>i%3==0).map(()=>{const d=mk('div','dot');dl.append(d);return d})}
  lbl.style.opacity=ease(pr(t,ap,.8));
  bs.forEach((b,i)=>{b.style.opacity=ease(pr(t,ap+i*.02,.4));const x0=b.classList.contains('x0');b.classList.toggle('x',rd!=null&&x0&&t>=rd+i*.012);b.classList.toggle('w',wl!=null&&t>=wl&&t<wl+2.2&&Math.floor((t-wl)*3+i/7)%2==0)});
  pipe.style.opacity=pp!=null?ease(pr(t,pp,.7)):0;leg.style.opacity=rd!=null&&p.flagLegend?ease(pr(t,rd+.5,.8)):0;
  dots.forEach((d,j)=>{const i=j*3;if(pk==null||t<pk){d.style.opacity=0;return}const ph=((t-pk)*.6+H(i,2))%1;d.style.opacity=ph<.1?ph*10:1;d.style.left=pos[i][0]+'%';d.style.top=lerp(pos[i][1],pos.pipeY,ease(ph))+'%'})}};

/* ---------- listing: a panel where a name is typed in, plus an optional sorted listing ---------- */
A.listing=(h,p,C)=>{
 const rows=(p.rows||[]).map(([c,tx])=>`<div class="ind f ${c==='muted'?'mu':c==='blue'?'z':c}">${esc(tx)}</div>`).join('');
 const kids=(p.kids||[]).map(k=>`<div class="ind f z kid" style="padding-left:4cqw;opacity:0">${esc(k)}</div>`).join('');
 const right=p.right?`<div class="pn rp" style="opacity:0"><h3>${esc(p.right.title)}</h3>${p.right.lines.map(([c,tx])=>`<div class="f ${c==='muted'?'mu':c==='blue'?'z':c}" style="opacity:0">${esc(tx)}</div>`).join('')}${p.right.call?`<div class="call" style="opacity:0">${esc(p.right.call)}</div>`:''}</div>`:'<div></div>';
 h.innerHTML=`<div class="in"><div class="two"><div class="pn"><h3>${esc(p.title||'')}</h3><div class="f">${esc(p.root||'')}</div>${rows}<div class="ind f z"><span class="nf cur"></span></div>${kids}<div class="call cl" style="opacity:0">${esc(p.call||'')}</div></div>${right}</div>${p.foot?`<div class="lbl ft" style="opacity:0;font-size:1.8cqw">${esc(p.foot)}</div>`:''}</div>`;
 const nf=h.querySelector('.nf'),cl=h.querySelector('.cl'),rp=h.querySelector('.rp'),ft=h.querySelector('.ft');
 const kd=[...h.querySelectorAll('.kid')],rl=rp?[...rp.querySelectorAll('.f')]:[],rc=rp?rp.querySelector('.call'):null;
 const ta=C.T(p.typeAt??.4),cps=p.cps||14,txt=p.typed||'',endT=ta+txt.length/cps;
 const ra=p.right?C.T(p.right.at):0,ka=p.kidsAt!=null?C.T(p.kidsAt):0,fa=p.foot?C.T(p.footAt??0):0;
 return t=>{
  nf.textContent=txt.slice(0,Math.floor(Math.max(0,t-ta)*cps));nf.classList.toggle('cur',t<endT);
  cl.style.opacity=p.call&&t>=endT+.3?ease(pr(t,endT+.3,.5)):0;
  kd.forEach((k,i)=>pop(k,t,ka+i*.45,.4,.6));
  if(rp){rp.style.opacity=ease(pr(t,ra,.5));rl.forEach((r,i)=>r.style.opacity=ease(pr(t,ra+.4+i*.4,.4)));if(rc)rc.style.opacity=ease(pr(t,ra+.6+rl.length*.4,.5))}
  if(ft)ft.style.opacity=ease(pr(t,fa,.6))}};

/* ---------- counters ---------- */
A.counters=(h,p,C)=>{
 const it=p.items,cols=it.length;
 const body=`<div class="cn ${p.small?'sm':''}" style="grid-template-columns:repeat(${cols},1fr)">${it.map(i=>`<div style="opacity:0"><b>0</b><span>${esc(i.label)}</span></div>`).join('')}</div>`;
 h.innerHTML=p.pos==='bottom'?`<div style="position:absolute;left:4cqw;right:4cqw;bottom:4cqw" class="panel">${body}</div>`:p.pos==='top'?`<div style="position:absolute;left:4cqw;right:4cqw;top:4cqw" class="panel">${body}</div>`:`<div class="in">${body}</div>`;
 const ds=[...h.querySelectorAll('.cn>div')];
 return t=>ds.forEach((d,i)=>{const o=it[i],a=C.T(o.at??0),du=o.dur||2.4,e=ease(pr(t,a,du)),b=d.querySelector('b');d.style.opacity=ease(pr(t,a,.4));
  b.textContent=o.txt!=null?o.txt:(o.pre||'')+fmt(lerp(o.from||0,o.n,e))+(o.suf||'');if(o.color)b.style.color=`var(${cv(o.color)})`})};

/* ---------- timeline: dated events on an axis ---------- */
A.timeline=(h,p,C)=>{
 const ax0=p.axis||{labels:['Jul 8','Jul 9','Jul 10','Jul 11','Jul 12','Jul 13'],hours:24},hrs=ax0.hours||24,tot=ax0.labels.length*hrs;
 const X=hr=>60+hr/tot*840,ay=p.axisY||270;
 let s=`<path class="axis" d="M60 ${ay}H900" stroke="#2A3340" stroke-width="2" fill="none" stroke-dasharray="840"/>`;
 ax0.labels.forEach((l,d)=>s+=`<text x="${X(d*hrs)}" y="${ay+35}" fill="#8C96A4" font-size="15" text-anchor="middle">${esc(l)}</text>`);
 p.ev.forEach(e=>{const up=e.pos>0,st=Math.abs(e.pos),y=up?ay-st:ay+st,ty=up?y-30:y+24,c=hex(e.color);
  s+=`<g class="ev" style="opacity:0"><path d="M${X(e.h)} ${ay}V${y}" stroke="${c}"/><circle cx="${X(e.h)}" cy="${ay}" r="6" fill="${c}"/><text x="${X(e.h)}" y="${ty}" fill="${c}" font-size="15" text-anchor="middle">${esc(e.date)}</text><text x="${X(e.h)}" y="${ty+21}" fill="#E7EBF1" font-size="18" text-anchor="middle">${esc(e.label)}</text></g>`});
 h.innerHTML=`<svg class="sv" viewBox="${p.vb||'0 0 960 540'}">${s}</svg>`;
 const ax=h.querySelector('.axis'),evs=[...h.querySelectorAll('.ev')];
 return t=>{ax.style.strokeDashoffset=840*(1-ease(pr(t,C.T(p.at||0),1.2)));evs.forEach((g,i)=>g.style.opacity=ease(pr(t,C.T(p.ev[i].at),.5)))}};

/* ---------- equation: boxes joined by operators, lit in sequence, plus evidence rows ---------- */
A.equation=(h,p,C)=>{
 const seps=p.seps||[],rowsH=(p.rows||[]).map(r=>`<div class="rw er" style="opacity:0">${r.chip?chip(r.chip[0],r.chip[1],{p:r.chip[2]}):''}${r.box?`<span class="box ok">${esc(r.text)}</span>`:`<span class="mu ${r.mono===false?'':'mono'}" style="font-size:${r.mono===false?1.5:1.4}cqw">${esc(r.text)}</span>`}</div>`).join('');
 h.innerHTML=`<div class="in"><div class="rw">${p.boxes.map((x,i)=>`<span class="box hl">${esc(x)}</span>${i<p.boxes.length-1?`<span class="arr">${esc(seps[i]||'→')}</span>`:''}`).join('')}</div>${p.caption?`<p class="mu cap1" style="font-size:1.8cqw;opacity:0">${esc(p.caption)}</p>`:''}${rowsH}</div>`;
 const bx=[...h.querySelectorAll('.hl')],cp=h.querySelector('.cap1'),rs=[...h.querySelectorAll('.er')];
 const a=C.T(p.hl||0),step=p.step||.9,ca=p.captionAt!=null?C.T(p.captionAt):1e9;
 return t=>{
  bx.forEach((b,i)=>{const s0=a+i*step,f=clamp((t-s0)/1.4),on=t>=s0&&(f<.7||i==bx.length-1);b.style.borderColor=on?'var(--tl)':'var(--ln)';b.style.color=on?'var(--tl)':'var(--tx)'});
  if(cp)cp.style.opacity=ease(pr(t,ca,.6));rs.forEach((r,i)=>pop(r,t,C.T(p.rows[i].at??0),.5,1))}};

/* ---------- contrast: what was believed vs what actually happened ---------- */
A.contrast=(h,p,C)=>{
 const row=(r,cls)=>`<div class="${cls}" style="opacity:0"><p class="mu" style="font-size:1.6cqw;margin-bottom:1.2cqw">${esc(r.label)}</p><div class="rw">${r.steps.map((s,i)=>`<span class="box ${s.kind==='ok'?'ok':''} ${s.kind==='dashed'?'dsh':''} ${cls}s" data-i="${i}">${esc(s.text)}</span>${i<r.steps.length-1?'<span class="arr">→</span>':''}`).join('')}</div></div>`;
 h.innerHTML=`<div class="in" style="gap:3cqw">${row(p.top,'b1')}${row(p.bottom,'b2')}${p.note?`<div class="b3 rw" style="opacity:0">${chip(p.note.chip[0],p.note.chip[1],{p:p.note.chip[2]})}<span class="mu" style="font-size:1.5cqw">${esc(p.note.text)}</span></div>`:''}${p.punch?`<div class="b4" style="opacity:0;font-size:2.2cqw;color:var(--tl)">${esc(p.punch.text)}</div>`:''}</div>`;
 const q=s=>h.querySelector(s),b1=q('.b1'),b2=q('.b2'),b3=q('.b3'),b4=q('.b4');
 const tops=[...h.querySelectorAll('.b1s')],bots=[...h.querySelectorAll('.b2s')];
 const T=o=>o&&o.at!=null?C.T(o.at):1e9;
 const aT=T(p.top),bT=T(p.bottom),nT=T(p.note),pT=T(p.punch),sT=T(p.strike),gT=T(p.ghost);
 return t=>{pop(b1,t,aT,.6,1);pop(b2,t,bT,.6,1);if(b3)pop(b3,t,nT,.6,1);if(b4)pop(b4,t,pT,.6,1);
  if(p.strike){const g=ease(pr(t,sT,1.4)),e=tops[p.strike.step];if(e){e.style.opacity=1-.72*g;e.style.textDecoration=g>.5?'line-through':'none'}}
  if(p.ghost){const e=bots[p.ghost.step];if(e)e.style.opacity=ease(pr(t,gT,1))}}};

/* ---------- options: one hub branching to several options ---------- */
A.options=(h,p,C)=>{
 const hub=p.hub||{name:'',sub:'',color:'blue'},n=p.items.length,gap=Math.min(150,400/n),y0=270-gap*(n-1)/2-55;
 let s=`<circle cx="130" cy="270" r="58" fill="#171D26" stroke="${hex(hub.color)}" stroke-width="2"/><svg x="106" y="246" width="48" height="48" color="${hex(hub.color)}"><use href="#mark"/></svg><text x="130" y="360" fill="#E7EBF1" font-size="16" text-anchor="middle">${esc(hub.name)}</text><text x="130" y="382" fill="#8C96A4" font-size="13" text-anchor="middle">${esc(hub.sub||'')}</text>`;
 p.items.forEach((it,i)=>{const y=y0+i*gap,m=it.marks||[],l=it.lines||[];
  s+=`<g class="br${i}" style="opacity:0"><path class="fl" d="M188 270C290 270 290 ${y+55} 380 ${y+55}" fill="none" stroke="${hex(hub.color)}" stroke-width="1.5" stroke-dasharray="8 8"/><rect x="380" y="${y}" width="520" height="110" rx="14" fill="#171D26" stroke="#2A3340"/><text x="406" y="${y+38}" fill="#E7EBF1" font-size="21" font-weight="600">${esc(it.title)}</text>${l.map((x,k)=>`<text x="406" y="${y+72+k*22}" fill="#8C96A4" font-size="14">${esc(x)}</text>`).join('')}${m.map((x,k)=>`<text x="880" y="${y+72+k*22}" fill="${hex(x[1])}" font-size="16" text-anchor="end">${esc(x[0])}</text>`).join('')}</g>`});
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const br=p.items.map((_,i)=>h.querySelector('.br'+i)),fl=[...h.querySelectorAll('.fl')],at=(p.at||p.items.map((_,i)=>i*.8)).map(x=>C.T(x));
 return t=>br.forEach((g,i)=>{g.style.opacity=ease(pr(t,at[i],.6));fl[i].style.strokeDashoffset=-(t*13)%16})};

/* ---------- pipeline: three stages, a trigger on the middle one, a packet flowing on ---------- */
A.pipeline=(h,p,C)=>{
 const nd=p.nodes,xs=[50,375,700];
 let s=`<g fill="none" stroke="#2A3340" stroke-width="1.5">${xs.map((x,i)=>`<rect class="e${i}" x="${x}" y="215" width="210" height="110" rx="14" ${i==2?'stroke="#7C97FF"':''}/>`).join('')}</g><g fill="#E7EBF1" font-size="17" text-anchor="middle">${nd.map((n,i)=>`<g class="e${i}"><text x="${xs[i]+105}" y="265">${esc(n.title)}</text><text x="${xs[i]+105}" y="290" fill="#8C96A4">${esc(n.sub||'')}</text></g>`).join('')}</g>
 <path class="ar" d="M260 270H375M585 270H700" stroke="#8C96A4" stroke-width="1.5" stroke-dasharray="5 6" fill="none"/>
 <g class="tw" style="opacity:0"><circle cx="480" cy="215" r="7" fill="#FF6E6E"/><circle class="rg" cx="480" cy="215" r="7" fill="none" stroke="#FF6E6E"/><text x="480" y="188" fill="#FF6E6E" font-size="15" text-anchor="middle">${esc(p.trigger?.label||'')}</text></g>
 <g class="pk" style="opacity:0"><circle class="pc" r="7" fill="#3FD8C2" cy="270"/><text x="643" y="248" fill="#3FD8C2" font-size="14" text-anchor="middle">${esc(p.packet?.label||'')}</text></g>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const es=[0,1,2].map(i=>[...h.querySelectorAll('.e'+i)]),tw=h.querySelector('.tw'),rg=h.querySelector('.rg'),pk=h.querySelector('.pk'),pc=h.querySelector('.pc'),ar=h.querySelector('.ar');
 const a=C.T(p.at||0),w=p.trigger?C.T(p.trigger.at):1e9,k=p.packet?C.T(p.packet.at):1e9;
 return t=>{es.forEach((g,i)=>g.forEach(e=>e.style.opacity=ease(pr(t,a+i*.5,.5))));ar.style.opacity=ease(pr(t,a+1,.6));
  tw.style.opacity=ease(pr(t,w,.5));const ph=t>=w?((t-w)%2.4)/2.4:0;rg.setAttribute('r',7+19*ph);rg.style.opacity=t>=w?1-ph:0;
  pk.style.opacity=t>=k?1:0;const q=t>=k?((t-k)%2.4)/2.4:0;pc.setAttribute('cx',585+115*q)}};

/* ---------- cards: a row of labelled cards + optional highlighted banner ---------- */
A.cards=(h,p,C)=>{
 const it=p.items||[];
 h.innerHTML=`<div class="in">${it.length?`<div class="vt" style="grid-template-columns:repeat(${it.length},1fr)">${it.map(k=>`<div class="vc" style="--c:var(${cv(k.color)});opacity:0"><b>${esc(k.title)}</b><p>${esc(k.sub||'')}</p><code>${esc(k.code||'')}</code></div>`).join('')}</div>`:''}${p.banner?`<div class="pm" style="opacity:0"><span>${esc(p.banner.text)}</span><em>${esc(p.banner.tag||'')}</em></div>`:''}</div>`;
 const cs=[...h.querySelectorAll('.vc')],pm=h.querySelector('.pm'),at=C.T(p.at||0),st=p.stag??.5,pa=p.banner&&p.banner.at!=null?C.T(p.banner.at):0;
 return t=>{cs.forEach((c,i)=>pop(c,t,at+i*st,.5,1.2));if(pm)pop(pm,t,pa,.6,1.2)}};

/* ---------- terminal ---------- */
A.terminal=(h,p,C)=>{
 const cmd=p.cmd||'',cps=p.cps||16;
 h.innerHTML=`<div class="in"><div class="tm"><div class="tb"><i></i><i></i><i></i></div><div class="tt"><div><span class="mu">$ </span><span class="tc cur"></span></div><div class="to" style="opacity:0">${p.struck?`<div class="xp">${esc(p.struck)}</div>`:''}<b>${esc(p.result||'')}</b><br><span class="sm">${esc(p.note||'')}</span></div></div></div></div>`;
 const tc=h.querySelector('.tc'),to=h.querySelector('.to'),ta=C.T(p.at||.3),oa=C.T(p.out??ta+cmd.length/cps+.6);
 return t=>{tc.textContent=cmd.slice(0,Math.floor(Math.max(0,t-ta)*cps));to.style.opacity=ease(pr(t,oa,.4))}};

/* ---------- bars ---------- */
A.bars=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="gap:${p.gap||3}cqw;${p.style||''}">${p.items.map(i=>`<div class="br" style="opacity:0"><span>${esc(i.label)}</span><div class="tr"><i style="--c:var(${cv(i.color)});width:0"></i></div><b>${esc(i.val)}</b></div>`).join('')}</div>`;
 const rs=[...h.querySelectorAll('.br')];
 return t=>rs.forEach((r,i)=>{const o=p.items[i],a=C.T(o.at??i*.5);r.style.opacity=ease(pr(t,a,.4));r.querySelector('i').style.width=lerp(o.from||0,o.w,ease(pr(t,a+.2,o.dur||1.6)))+'%'})};

/* ---------- steps: staircase of escalating stages ---------- */
A.steps=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="stair">${p.rows.map((r,m)=>`<div class="sc" style="--c:var(${cv(r.color)});margin-left:${m*3}cqw;opacity:0"><b>${esc(r.title)}</b><span>${esc(r.desc||'')}</span><em>${esc(r.when||'')}</em></div>`).join('')}</div>${p.foot?`<p class="mu mono" style="font-size:1.3cqw">${esc(p.foot)}</p>`:''}</div>`;
 const rs=[...h.querySelectorAll('.sc')];return t=>rs.forEach((r,i)=>pop(r,t,C.T(p.at||0)+i*(p.step||.9),.6,1.2))};

/* ---------- groups: coordinators assigning work to columns of units ---------- */
A.groups=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="rw" style="gap:1.6cqw">${(p.leads||[]).map(l=>chip(l[0],l[1])).join('')}<span class="mu" style="font-size:1.6cqw">${esc(p.leadText||'')}</span></div><div class="ln3" style="grid-template-columns:repeat(${p.groups.length},1fr)">${p.groups.map(g=>`<div class="lane" style="--c:var(${cv(g.color)})"><b>${esc(g.title)}</b><div class="dots">${Array.from({length:g.n},()=>'<i style="opacity:0"></i>').join('')}</div></div>`).join('')}</div></div>`;
 const ds=[...h.querySelectorAll('.dots i')],at=C.T(p.at||0);
 return t=>ds.forEach((d,i)=>{const e=ease(pr(t,at+.3+i*.06,.35));d.style.opacity=e;d.style.transform=`scale(${.3+.7*e})`})};

/* ---------- quote cards ---------- */
const QL={raw:'raw chain of thought',par:'paraphrased',paraphrase:'paraphrased',agent:'',quote:''};
A.quote=(h,p,C)=>{
 const cols=p.cols||p.cards.length,dash=k=>k==='par'||k==='paraphrase';
 h.innerHTML=`<div class="in" style="${p.pos==='bottom'?'justify-content:flex-end':p.pos==='top'?'justify-content:flex-start':''}"><div class="qs ${p.big?'bigq':''}" style="grid-template-columns:repeat(${cols},1fr)">${p.cards.map(c=>{const lab=c.label??QL[c.kind||'quote']??'';return`<div class="q ${dash(c.kind)?'par':'raw'} ${p.sm?'sm':''}" style="opacity:0">${c.who?`<span style="align-self:flex-start;font-style:normal">${chip(c.who[0],c.who[1]||'teal')}</span>`:''}<span>${dash(c.kind)?esc(c.text):'“'+esc(c.text)+'”'}</span>${lab?`<small>${esc(lab)}</small>`:''}</div>`}).join('')}</div></div>`;
 const qs=[...h.querySelectorAll('.q')];return t=>qs.forEach((q,i)=>pop(q,t,C.T(p.cards[i].at??i*.8),.6,1.2))};

/* ---------- lower third / source stamp ---------- */
A.lower=(h,p,C)=>{
 h.innerHTML=`${p.name?`<div class="lt" style="opacity:0;${p.pos==='right'?'left:auto;right:4cqw':''}"><i style="--c:var(${cv(p.color)})"><svg><use href="#mark"/></svg></i><div><b>${esc(p.name)}</b><span>${esc(p.sub||'')}</span></div></div>`:''}${p.src?`<div class="src ${p.srcTop?'top':''}" style="opacity:0">${p.src.map(esc).join('<br>')}</div>`:''}`;
 const lt=h.querySelector('.lt'),sr=h.querySelector('.src');return t=>{if(lt)pop(lt,t,C.T(p.at||0),.8,1.4);if(sr)sr.style.opacity=ease(pr(t,C.T(p.srcAt||0),.8))}};

/* ---------- messages: stacked message cards ---------- */
A.messages=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="gap:2cqw;${p.style||''}">${p.items.map(m=>`<div class="mc ${m.cls||''} ${p.compact?'cp':''}" style="opacity:0"><div class="hd">${m.who?chip(m.who[0],m.who[1]||'teal'):''}${m.to?`<span class="arr">→</span>${chip(m.to[0],m.to[1]||'blue')}`:''}${m.tag?`<span class="lbl">${esc(m.tag)}</span>`:''}</div><div class="tx">${segs(m.segs)}</div>${m.note?`<div class="nt">${esc(m.note)}</div>`:''}</div>`).join('')}</div>`;
 const cs=[...h.querySelectorAll('.mc')];return t=>cs.forEach((c,i)=>pop(c,t,C.T(p.items[i].at??i*1),.6,1.2))};

/* ---------- card: key/value card ---------- */
A.card=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:center"><div class="mc" style="width:${p.w||56}cqw;opacity:0;gap:1.8cqw"><div class="lbl" style="font-size:1.6cqw">${esc(p.title)}</div>${p.rows.map(([k,v])=>`<div class="rw" style="gap:2cqw;font-size:2.2cqw"><span class="mu mono" style="min-width:16cqw;font-size:1.7cqw">${esc(k)}</span><span class="mono" style="color:var(--tx)">${esc(v)}</span></div>`).join('')}${p.note?`<div class="nt" style="font-size:1.7cqw;color:var(--rd)">${esc(p.note)}</div>`:''}</div></div>`;
 const c=h.querySelector('.mc');return t=>{const e=ease(pr(t,C.T(p.at||0),.7));c.style.opacity=e;c.style.transform=`scale(${.92+.08*e})`}};

/* ---------- stamp / note ---------- */
A.stamp=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:${p.align||'center'};${p.style||''}"><div class="panel" style="opacity:0;text-align:center;padding:2cqw 3cqw"><span class="stamp">${esc(p.text)}</span>${p.sub?`<div class="lbl" style="margin-top:1.6cqw;font-size:1.8cqw;color:var(--tx)">${esc(p.sub)}</div>`:''}</div></div>`;
 const d=h.querySelector('.in>div');return t=>{const e=ease(pr(t,C.T(p.at||0),.45));d.style.opacity=e;d.style.transform=`scale(${1.35-.35*e})`}};
A.note=(h,p,C)=>{
 h.innerHTML=`<div style="position:absolute;${p.css||'left:4cqw;bottom:4cqw'}" class="panel"><div style="font-size:${p.size||1.9}cqw;color:${p.color?`var(${cv(p.color)})`:'var(--tx)'};${p.mono?'font-family:var(--mono)':''}">${esc(p.text)}</div></div>`;
 const d=h.firstElementChild;return t=>pop(d,t,C.T(p.at||0),.6,1)};

/* ---------- proportion: n of 100 dots lit ---------- */
A.proportion=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:center;gap:2cqw"><div class="d100">${Array.from({length:100},()=>'<i></i>').join('')}</div><div class="mono dl" style="font-size:2.4cqw;opacity:0">${esc(p.label)}</div></div>`;
 const ds=[...h.querySelectorAll('.d100 i')],dl=h.querySelector('.dl'),at=C.T(p.at||0),n=p.n;
 return t=>{ds.forEach((d,i)=>{d.style.background=i<n&&t>=at+i*.025?`var(${cv(p.color)})`:'var(--ln)'});dl.style.opacity=ease(pr(t,at+n*.025,.6))}};

/* ---------- transfer: one entity hands an item to another (with a size bar each) ---------- */
A.transfer=(h,p,C)=>{
 const f=p.from,o=p.to,item=p.item||{title:'',sub:''};
 h.innerHTML=`<div class="in" style="justify-content:center"><div style="display:grid;grid-template-columns:1fr 18cqw 1fr;align-items:center;gap:2cqw">
 <div class="a1" style="opacity:0">${chip(f.name,f.color,{big:1})}<div class="lbl" style="margin:1.4cqw 0 .6cqw;font-size:1.6cqw">${esc(p.barLabel||'')}</div><div class="tr" style="height:2cqw"><i class="bb1" style="--c:var(${cv(f.color)});width:0"></i></div></div>
 <div class="dos" style="opacity:0;text-align:center"><div class="mc" style="padding:1.4cqw;gap:.4cqw"><b class="mono" style="font-size:1.8cqw">${esc(item.title)}</b><span class="nt">${esc(item.sub||'')}</span></div></div>
 <div class="a2" style="opacity:0">${chip(o.name,o.color,{big:1})}<div class="lbl" style="margin:1.4cqw 0 .6cqw;font-size:1.6cqw">${esc(p.barLabel||'')}</div><div class="tr" style="height:2cqw"><i class="bb2" style="--c:var(${cv(o.color)});width:0"></i></div></div></div>
 <div class="lbl hub" style="opacity:0;font-size:2.2cqw;color:var(--tx);text-align:center;margin-top:1cqw">${esc(p.caption||'')}</div></div>`;
 const q=s=>h.querySelector(s),a1=q('.a1'),a2=q('.a2'),ds=q('.dos'),b1=q('.bb1'),b2=q('.bb2'),hb=q('.hub');
 const a=C.T(p.a),b=C.T(p.b),mv=C.T(p.move),hu=p.captionAt!=null?C.T(p.captionAt):1e9;
 return t=>{pop(a1,t,a,.6,1);pop(a2,t,b,.6,1);b1.style.width=lerp(0,f.bar??25,ease(pr(t,a+.4,1)))+'%';b2.style.width=lerp(0,o.bar??95,ease(pr(t,b+.4,1.4)))+'%';
  const m=eio(pr(t,mv,1.8));ds.style.opacity=t>=mv-.3&&t<mv+2.4?1-(t>mv+1.8?pr(t,mv+1.8,.6):0):0;ds.style.transform=`translateX(${lerp(-24,24,m)}cqw)`;hb.style.opacity=ease(pr(t,hu,.6))}};

/* ---------- title / sequence / list / source ---------- */
A.title=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="justify-content:center"><div class="d0" style="opacity:0"><div class="lbl" style="font-size:1.8cqw;margin-bottom:1.6cqw">${esc(p.kicker||'')}</div><div class="big-t">${esc(p.title).replace(/\n/g,'<br>')}</div><div class="sub-t">${esc(p.sub||'')}</div></div></div><div class="src" style="opacity:0">${(p.src||[]).map(esc).join('<br>')}</div>`;
 const d=h.querySelector('.d0'),s=h.querySelector('.src'),a=C.T(p.at||0);
 return t=>{pop(d,t,a,.9,1.6);s.style.opacity=ease(pr(t,a+.8,.8))}};
A.sequence=(h,p,C)=>{
 const cols=['--am','--bl','--tl','--rd'];
 h.innerHTML=`<div class="in" style="align-items:center"><div class="k3">${p.items.map((x,i)=>`${i?'<span class="arr" style="font-size:3cqw;opacity:0">→</span>':''}<div class="box" style="opacity:0;border-color:var(${cols[i%4]})">${esc(x)}</div>`).join('')}</div></div>`;
 const bs=[...h.querySelectorAll('.k3>*')];return t=>bs.forEach((b,i)=>pop(b,t,C.T(p.at||0)+i*.55,.6,1.2))};
A.list=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="lbl" style="font-size:2.2cqw">${esc(p.title)}</div><div class="lst">${p.items.map(x=>`<div style="opacity:0">${esc(x)}</div>`).join('')}</div></div>`;
 const ds=[...h.querySelectorAll('.lst div')];return t=>ds.forEach((d,i)=>pop(d,t,p.ats&&p.ats[i]!=null?C.T(p.ats[i]):C.T(p.at||0)+i*.8,.6,1))};
A.source=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="justify-content:flex-end;padding-bottom:6cqw"><div class="mc" style="opacity:0;gap:1cqw"><div class="lbl" style="font-size:1.5cqw">SOURCE</div><div style="font-size:2.1cqw;line-height:1.4">${esc(p.title)}</div><div class="nt" style="font-size:1.6cqw">${esc(p.by||'')}</div></div></div>`;
 const d=h.querySelector('.mc');return t=>pop(d,t,C.T(p.at||0),.8,1.4)};


/* ---------- breakout: isolated agents → shared hub → wall → internet → third party ---------- */
const MARK=(x,y,s,c)=>`<circle cx="${x}" cy="${y}" r="${s*.62}" fill="${c}"/><svg x="${x-s*.4}" y="${y-s*.4}" width="${s*.8}" height="${s*.8}" style="color:#0E1218"><use href="#mark"/></svg>`;
const along=(pts,u)=>{const L=[];let tot=0;for(let i=1;i<pts.length;i++){const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);L.push(d);tot+=d}let r=clamp(u)*tot;for(let i=0;i<L.length;i++){if(r<=L[i]||i==L.length-1){const k=L[i]?r/L[i]:0;return[lerp(pts[i][0],pts[i+1][0],k),lerp(pts[i][1],pts[i+1][1],k)]}r-=L[i]}return pts[pts.length-1]};
A.breakout=(h,p,C)=>{
 const n=Math.max(2,Math.min(8,p.agents||6)),cols=Math.ceil(n/2),zw=cols*124+16,zr=40+zw,hubX=40+zw/2,hubY=350;
 const bx=Array.from({length:n},(_,i)=>({x:56+(i%cols)*124,y:100+Math.floor(i/cols)*118}));
 const gx=Math.max(zr+150,700),gy=235,tx=gx+84;
 const route=[[hubX+90,hubY+22],[zr,hubY+22],[gx-42,gy+34]];
 let s=`<g class="zn" style="opacity:0"><rect x="40" y="70" width="${zw}" height="345" rx="18" fill="none" stroke="#FF6E6E" stroke-width="2" stroke-dasharray="9 7"/><text x="40" y="56" fill="#FF6E6E" font-size="15">${esc(p.zone||'')}</text></g>`;
 bx.forEach((b,i)=>{s+=`<g class="bx" style="opacity:0"><rect x="${b.x}" y="${b.y}" width="108" height="84" rx="12" fill="#171D26" stroke="#2A3340" stroke-width="1.5"/>${MARK(b.x+54,b.y+42,34,'#7C97FF')}</g>`});
 s+=`<g class="hb" style="opacity:0"><rect x="${hubX-90}" y="${hubY}" width="180" height="44" rx="10" fill="#171D26" stroke="#F6B94C" stroke-width="1.6"/><text x="${hubX}" y="${hubY+27}" fill="#F6B94C" font-size="14" text-anchor="middle">${esc(p.hub?.label||'')}</text></g>`;
 s+=`<g class="lk" style="opacity:0">${bx.map(b=>`<path d="M${b.x+54} ${b.y+84}L${hubX} ${hubY}" stroke="#F6B94C" stroke-opacity=".5" stroke-width="1.4" stroke-dasharray="4 5" fill="none"/>`).join('')}</g>`;
 s+=`<g class="pk">${bx.map(()=>'<circle r="4.5" fill="#F6B94C" style="opacity:0"/>').join('')}</g>`;
 s+=`<g class="st1" style="opacity:0"><path d="M${route[0][0]} ${route[0][1]}H${zr}" stroke="#8C96A4" stroke-width="1.6" stroke-dasharray="4 5" fill="none"/><circle cx="${zr}" cy="${hubY+22}" r="13" fill="#0E1218" stroke="#FF6E6E" stroke-width="2"/><path d="M${zr-6} ${hubY+16}l12 12M${zr+6} ${hubY+16}l-12 12" stroke="#FF6E6E" stroke-width="2.4"/></g>`;
 s+=`<g class="gl" style="opacity:0"><circle cx="${gx}" cy="${gy}" r="52" fill="#171D26" stroke="#3FD8C2" stroke-width="2"/><ellipse cx="${gx}" cy="${gy}" rx="22" ry="52" fill="none" stroke="#3FD8C2" stroke-opacity=".7"/><path d="M${gx} ${gy-52}V${gy+52}M${gx-52} ${gy}H${gx+52}M${gx-46} ${gy-24}Q${gx} ${gy-34} ${gx+46} ${gy-24}M${gx-46} ${gy+24}Q${gx} ${gy+34} ${gx+46} ${gy+24}" stroke="#3FD8C2" stroke-opacity=".6" fill="none"/><text x="${gx}" y="${gy+82}" fill="#3FD8C2" font-size="15" text-anchor="middle">${esc(p.net?.label||'')}</text></g>`;
 s+=`<path class="rt" d="M${route.map(q=>q.join(' ')).join('L')}" pathLength="1" stroke="#3FD8C2" stroke-width="2.2" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/><circle class="rg" cx="${zr}" cy="${hubY+22}" r="10" fill="none" stroke="#FF6E6E" stroke-width="2" style="opacity:0"/><g class="p2">${[0,1,2].map(()=>'<circle r="4.5" fill="#3FD8C2" style="opacity:0"/>').join('')}</g>`;
 s+=`<g class="th" style="opacity:0"><path d="M${gx+52} ${gy}H${tx}" stroke="#FF6E6E" stroke-width="2" fill="none"/><rect x="${tx}" y="${gy-30}" width="150" height="60" rx="12" fill="#171D26" stroke="#FF6E6E" stroke-width="1.8"/><text x="${tx+75}" y="${gy+5}" fill="#FF6E6E" font-size="15" text-anchor="middle">${esc(p.third?.label||'')}</text></g><g class="p3">${[0,1].map(()=>'<circle r="4.5" fill="#FF6E6E" style="opacity:0"/>').join('')}</g>`;
 s+=`<text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const q=c=>h.querySelector(c),qa=c=>[...h.querySelectorAll(c)];
 const zn=q('.zn'),bxs=qa('.bx'),hb=q('.hb'),lk=q('.lk'),pk=qa('.pk circle'),st1=q('.st1'),gl=q('.gl'),rt=q('.rt'),rg=q('.rg'),p2=qa('.p2 circle'),th=q('.th'),p3=qa('.p3 circle'),cp=q('.cp');
 const T=k=>p[k]!=null?C.T(p[k]):1e9,at=C.T(p.at||0),ha=p.hub?C.T(p.hub.at):1e9,ta=T('talk'),na=p.net?C.T(p.net.at):1e9,ba=p.breach?C.T(p.breach.at):1e9,xa=p.third?C.T(p.third.at):1e9,ca=T('captionAt');
 return t=>{zn.style.opacity=ease(pr(t,at,.6));bxs.forEach((b,i)=>b.style.opacity=ease(pr(t,at+.3+i*.15,.4)));
  hb.style.opacity=ease(pr(t,ha,.5));lk.style.opacity=ease(pr(t,ha+.3,.5));
  pk.forEach((c,i)=>{if(t<ta){c.style.opacity=0;return}const ph=((t-ta)*.55+H(i,2))%1,b=bx[i],u=ph<.5?ph*2:2-ph*2,x=lerp(b.x+54,hubX,u),y=lerp(b.y+84,hubY,u);c.setAttribute('cx',x);c.setAttribute('cy',y);c.style.opacity=.9});
  gl.style.opacity=ease(pr(t,na,.6));st1.style.opacity=t<ba?ease(pr(t,na+.3,.5)):1-ease(pr(t,ba,.3));
  rt.setAttribute('stroke-dashoffset',1-ease(pr(t,ba+.1,1.2)));
  const bp=t>=ba?(t-ba)%2.4/2.4:0;rg.setAttribute('r',10+34*bp);rg.style.opacity=t>=ba?(1-bp)*.9:0;
  p2.forEach((c,i)=>{if(t<ba+1.3){c.style.opacity=0;return}const u=((t-ba-1.3)*.4+i/3)%1,[x,y]=along(route,u);c.setAttribute('cx',x);c.setAttribute('cy',y);c.style.opacity=1});
  th.style.opacity=ease(pr(t,xa,.6));
  p3.forEach((c,i)=>{if(t<xa+.6){c.style.opacity=0;return}const u=((t-xa-.6)*.5+i/2)%1;c.setAttribute('cx',lerp(gx+52,tx,u));c.setAttribute('cy',gy);c.style.opacity=1});
  cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- hierarchy: a leader, middle managers and a crowd of workers; tasks flow down ---------- */
A.hierarchy=(h,p,C)=>{
 const R=p.root||{name:'',sub:'',color:'blue'},M=p.mids||[],k=M.length||1,mx=M.map((_,i)=>480+(i-(k-1)/2)*(Math.min(260,820/k)));
 const col=c=>hex(c);let s='';
 const lv=p.levels||[];lv.forEach((l,i)=>{s+=`<text class="lv" x="24" y="${[100,252,400][i]}" fill="#8C96A4" font-size="13" style="opacity:0">${esc(l)}</text>`});
 mx.forEach((x,i)=>{s+=`<path class="l1" d="M480 130V170H${x}V210" stroke="${col(M[i].color)}" stroke-opacity=".6" stroke-width="1.6" fill="none" style="opacity:0"/>`});
 const W=[];M.forEach((m,i)=>{const n=Math.min(40,m.n||0),cl=Math.min(8,Math.max(4,Math.ceil(Math.sqrt(n*1.6)))),x0=mx[i]-(cl-1)*8;for(let j=0;j<n;j++)W.push({i,x:x0+(j%cl)*16,y:340+Math.floor(j/cl)*16,c:col(m.color)})});
 mx.forEach((x,i)=>{s+=`<path class="l2" d="M${x} 262V320" stroke="${col(M[i].color)}" stroke-opacity=".45" stroke-width="1.4" stroke-dasharray="4 5" fill="none" style="opacity:0"/>`});
 s+=`<g class="rt" style="opacity:0"><rect x="370" y="74" width="220" height="56" rx="12" fill="#171D26" stroke="${col(R.color)}" stroke-width="2"/>${MARK(404,102,26,col(R.color))}<text x="428" y="98" fill="#E7EBF1" font-size="15">${esc(R.name)}</text><text x="428" y="118" fill="#8C96A4" font-size="12">${esc(R.sub||'')}</text></g>`;
 M.forEach((m,i)=>{s+=`<g class="md" style="opacity:0"><rect x="${mx[i]-84}" y="210" width="168" height="52" rx="12" fill="#171D26" stroke="${col(m.color)}" stroke-width="1.6"/>${MARK(mx[i]-56,236,22,col(m.color))}<text x="${mx[i]-38}" y="233" fill="#E7EBF1" font-size="13">${esc(m.name)}</text><text x="${mx[i]-38}" y="250" fill="#8C96A4" font-size="11">${esc(m.sub||'')}</text></g>`});
 s+=W.map(w=>`<circle class="wk" cx="${w.x}" cy="${w.y}" r="5.5" fill="${w.c}" style="opacity:0"/>`).join('');
 s+=`<g class="pl">${M.map(()=>'<circle r="5" fill="#E7EBF1" style="opacity:0"/>').join('')}</g><text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const qa=c=>[...h.querySelectorAll(c)],q=c=>h.querySelector(c);
 const at=C.T(p.at||0),st=p.step||.6,as=p.assign!=null?C.T(p.assign):1e9,ca=p.captionAt!=null?C.T(p.captionAt):1e9;
 const rt=q('.rt'),md=qa('.md'),l1=qa('.l1'),l2=qa('.l2'),wk=qa('.wk'),pl=qa('.pl circle'),lvs=qa('.lv'),cp=q('.cp');
 return t=>{rt.style.opacity=ease(pr(t,at,.5));lvs.forEach((e,i)=>e.style.opacity=ease(pr(t,at+i*st,.5)));
  md.forEach((e,i)=>{e.style.opacity=ease(pr(t,at+st+i*.25,.5));l1[i].style.opacity=ease(pr(t,at+st+i*.25,.5))});
  const wt=at+st*2+.3;l2.forEach((e,i)=>e.style.opacity=ease(pr(t,wt,.5)));
  wk.forEach((e,i)=>{const a=ease(pr(t,wt+.2+i*.03,.3));e.style.opacity=a;e.setAttribute('r',2+3.5*a)});
  pl.forEach((e,i)=>{if(t<as){e.style.opacity=0;return}const u=((t-as)*.5+i*.08)%1,x=mx[i],pts=[[480,130],[480,170],[x,170],[x,210],[x,262],[x,330]],[a,b]=along(pts,u);e.setAttribute('cx',a);e.setAttribute('cy',b);e.style.opacity=1});
  cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- flags: capture-the-flag poles; flags rise, some forged or poisoned ---------- */
A.flags=(h,p,C)=>{
 const it=p.items||[],n=Math.max(1,Math.min(7,it.length)),sp=880/n,base=380,F={ok:'#3FD8C2',fake:'#F6B94C',poisoned:'#FF6E6E',plain:'#8C96A4'};
 let s='';it.slice(0,n).forEach((o,i)=>{const px=40+sp*(i+.5);s+=`<g class="fg"><path d="M${px} ${base}V${base-200}" stroke="#2A3340" stroke-width="3"/><circle cx="${px}" cy="${base-200}" r="4" fill="#8C96A4"/><ellipse cx="${px}" cy="${base}" rx="26" ry="7" fill="#171D26" stroke="#2A3340"/><path class="fl" d="" fill="${F[o.state]||F.ok}"/><text x="${px}" y="${base+36}" fill="#E7EBF1" font-size="14" text-anchor="middle">${esc(o.label||'')}</text><text class="tg" x="${px}" y="${base+56}" fill="${F[o.state]||F.ok}" font-size="12" text-anchor="middle" style="opacity:0">${esc(o.tag||'')}</text></g>`});
 s+=`<text class="ct" x="920" y="52" fill="#E7EBF1" font-size="30" text-anchor="end" font-weight="600"></text><text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const fl=[...h.querySelectorAll('.fl')],tg=[...h.querySelectorAll('.tg')],ct=h.querySelector('.ct'),cp=h.querySelector('.cp');
 const at=C.T(p.at||0),st=p.step||.5,ca=p.captionAt!=null?C.T(p.captionAt):1e9,tga=p.tagsAt!=null?C.T(p.tagsAt):at+n*st+1;
 return t=>{let got=0;
  fl.forEach((e,i)=>{const px=40+sp*(i+.5),u=ease(pr(t,at+i*st,.9)),top=lerp(base-14,base-196,u),w=0+u*1;if(u>.99)got++;
   let d=`M${px} ${top}`;for(let k=0;k<=6;k++)d+=`L${px+k*9*w} ${top+Math.sin(t*4+k*.8+i)*2.4*w}`;for(let k=6;k>=0;k--)d+=`L${px+k*9*w} ${top+30*w+Math.sin(t*4+k*.8+i)*2.4*w}`;e.setAttribute('d',d+'Z');e.style.opacity=u>0?1:0;
   tg[i].style.opacity=ease(pr(t,tga+i*.2,.4))});
  ct.textContent=p.counter===false?'':got+' / '+n+' '+(p.unit||'');cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- driver ---------- */
window.CUES=[];
window.setup=(sched,cues)=>{
 const stage=document.getElementById('stage');stage.innerHTML='';window.CUES=[];
 const wpos=(r,w)=>{const tx=r.txt||'';const re=new RegExp('(^|[^A-Za-z0-9])'+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![A-Za-z0-9])','i');const m=re.exec(tx);if(!m)throw new Error('word not found: '+w+' in '+tx.slice(0,50));const i=m.index+m[1].length;const wt=ch=>'.?!'.includes(ch)?7:',;:—'.includes(ch)?3.5:1;let a=0,b=0;for(let k=0;k<tx.length;k++){const x=wt(tx[k]);if(k<i)a+=x;b+=x}return r.s+(r.e-r.s)*(a/b)};
 const abs=spec=>{if(typeof spec==='number')return spec;const m=/^(>?)([SE]?\d+[a-z]?)(?:#(.+?))?([+-]\d+(?:\.\d+)?)?$/.exec(spec);if(!m)throw new Error('bad time '+spec);const r=sched[m[2]];if(r==null)throw new Error('unknown anchor '+spec);const base=m[3]?wpos(r,m[3].replace(/_/g,' ')):(m[1]?r.e:r.s);return base+(m[4]?parseFloat(m[4]):0)};
 cues.forEach((c,idx)=>{
  const start=abs(c.at)+(c.off||0);
  const ext=c.until!=null&&!/^E/.test(String(c.until))&&c.ext!==0?(c.ext??.45):0;
  const end=c.until!=null?abs(c.until)+(c.untilOff||0)+ext:start+c.dur;
  const el=mk('div','cue');const r=c.rect||[0,0,100,100];
  Object.assign(el.style,{left:r[0]+'%',top:r[1]+'%',width:r[2]+'%',height:r[3]+'%',zIndex:c.z||idx});
  const st=mk('div','st'+(c.bg?' bg':''));el.append(st);stage.append(el);
  const C={dur:end-start,T:s=>typeof s==='number'?s:abs(s)-start};
  if(!A[c.a])throw new Error('unknown asset '+c.a);
  const upd=A[c.a](st,c.p||{},C);
  window.CUES.push({el,start,end,upd,fi:c.fade?.[0]??.5,fo:c.fade?.[1]??.5,id:c.id||c.a+idx})
 })};
window.frame=t=>{for(const q of window.CUES){
  if(t<q.start-.001||t>q.end+.001){q.el.style.opacity=0;q.el.style.visibility='hidden';continue}
  q.el.style.visibility='visible';const lt=t-q.start;
  q.el.style.opacity=Math.min(q.fi>0?clamp(lt/q.fi):1,q.fo>0?clamp((q.end-t)/q.fo):1);
  q.upd(lt)}};
