/* Original CC BY-SA 4.0. Deterministic, accessible attention-computation labs. */
(() => {
  'use strict';
  const labels={
    en:{window:'Causal window explorer',linear:'Recurrent state explorer',query:'Query',width:'Window width',time:'Time step',value:'Token 3 value',prev:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',visible:'Visible keys',pairs:'Allowed pairs',initial:'Initial zero state',state:'State after step',note:'Synthetic values — not model measurements'},
    zh:{window:'因果注意力視窗實驗',linear:'遞迴狀態運算實驗',query:'查詢位置',width:'視窗寬度',time:'時間步驟',value:'第 3 個 Token 的值',prev:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',visible:'可讀取的鍵',pairs:'允許的配對',initial:'初始零狀態',state:'目前累積狀態',note:'人工示例數值，非模型實測'}
  };
  const ns='http://www.w3.org/2000/svg';
  const fmt=n=>Number.isFinite(n)?Number(n.toFixed(3)).toString():'—';
  function elt(tag,attrs={},txt=''){const node=document.createElement(tag);Object.entries(attrs).forEach(([k,v])=>node.setAttribute(k,v));node.textContent=txt;return node;}
  function S(tag,attrs={},txt){const node=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>node.setAttribute(k,v));if(txt!==undefined)node.textContent=txt;return node;}
  const rect=(s,x,y,w,h,fill,stroke='#e2e8f0')=>s.append(S('rect',{x,y,width:w,height:h,rx:3,fill,stroke}));
  const txt=(s,x,y,t,size=12,fill='#1e293b')=>s.append(S('text',{x,y,'font-size':size,fill,'font-family':'sans-serif'},String(t)));
  function mount(root){
    if(root.dataset.ready==='yes')return;
    const kind=root.dataset.lab;if(!['window','linear'].includes(kind))return;
    const T=labels[root.dataset.lang==='zh'?'zh':'en'];
    let step=kind==='window'?8:0, factor=kind==='window'?4:3, speed=1, task=null;
    const max=kind==='window'?12:4,min=kind==='window'?1:0;
    root.dataset.ready='yes';
    const controls=elt('div',{class:'attention-lab-controls'}),buttons=elt('div',{class:'attention-lab-actions'});
    function input(key,label,lo,hi,val){
      const field=elt('label',{class:'attention-lab-range'}),name=elt('span',{},label+': '),out=elt('output',{'data-out':key},String(val));
      name.append(out);const range=elt('input',{type:'range','data-range':key,min:lo,max:hi,step:1,value:val,'aria-label':label});
      field.append(name,range);controls.append(field);return range;
    }
    const slider=input('step',kind==='window'?T.query:T.time,min,max,step);
    const knob=input('factor',kind==='window'?T.width:T.value,kind==='window'?1:-1,kind==='window'?8:5,factor);
    function button(action,label){const node=elt('button',{type:'button','data-act':action},label);buttons.append(node);return node;}
    const prev=button('previous',T.prev),play=button('play',T.play),next=button('next',T.next),reset=button('reset',T.reset),speedBtn=button('speed',T.speed+': 1×');
    const stage=elt('div',{class:'attention-lab-stage',tabindex:0,'aria-label':kind==='window'?T.window:T.linear});
    const svg=S('svg',{viewBox:kind==='window'?'0 0 650 344':'0 0 650 300',role:'img','aria-label':kind==='window'?'Causal mask and current visible keys':'Feature-weighted recurrent state and output'});
    stage.append(svg);
    const stats=elt('p',{class:'attention-lab-stats'}),trace=elt('div',{class:'attention-lab-table'}),status=elt('p',{class:'attention-lab-live',role:'status','aria-live':'polite'});
    root.replaceChildren(elt('h4',{},kind==='window'?T.window:T.linear),controls,buttons,stage,stats,trace,status,elt('p',{class:'attention-lab-note'},T.note));
    function stop(){if(task!==null){clearInterval(task);task=null;}play.textContent=T.play;play.setAttribute('aria-pressed','false');}
    function setStep(n){step=Math.min(max,Math.max(min,n));slider.value=step;draw();}
    function drawWindow(){
      svg.replaceChildren(S('title',{},'Banded causal attention mask'));
      const x=57,y=36,p=18,n=12;
      txt(svg,57,21,'Key →',13);txt(svg,16,326,'Query ↓',13);
      for(let j=1;j<=n;j++)txt(svg,x+(j-1)*p+4,32,j,10);
      for(let i=1;i<=n;i++){
        txt(svg,36,y+(i-1)*p+13,i,10);
        for(let j=1;j<=n;j++){
          const valid=j<=i&&j>=i-factor+1,active=i===step,hit=valid&&active;
          rect(svg,x+(j-1)*p,y+(i-1)*p,17,17,hit?'#0d9488':active?'#ffedd5':valid?'#cbd5e1':'#f0f3f7',active?'#f59e0b':'#e2e8f0');
        }
      }
      const lo=Math.max(1,step-factor+1),total=Array.from({length:n},(_,i)=>Math.min(i+1,factor)).reduce((a,b)=>a+b,0);
      txt(svg,327,28,'Token stream',14);
      for(let i=1;i<=n;i++){
        const hit=i>=lo&&i<=step;
        rect(svg,330+(i-1)*24,75,21,35,i===step?'#f59e0b':hit?'#0d9488':'#e2e8f0','none');
        txt(svg,335+(i-1)*24,97,i,10,hit?'#fff':'#334155');
      }
      txt(svg,330,150,'q = '+step+'     w = '+factor,15);
      txt(svg,330,177,'keys ['+lo+', '+step+']',15);
      txt(svg,330,215,total+' / 78 pairs',17);
      txt(svg,330,246,'O(nw) local edges',12,'#64748b');
      stats.textContent=T.visible+': '+lo+'–'+step+' · '+T.pairs+': '+total+' / 78';
      trace.textContent='';status.textContent=stats.textContent;
    }
    function drawLinear(){
      svg.replaceChildren(S('title',{},'Normalised scalar recurrence'));
      const keys=[1,2,1,2],values=[1,0,factor,2];let a=0,z=0;
      txt(svg,26,22,'Token inputs',14);
      for(let i=0;i<4;i++){
        const x=24+i*148,used=i<step;
        rect(svg,x,40,125,83,used?'#d2f4ed':'#edf2f7',used?'#0d9488':'#cbd5e1');
        txt(svg,x+10,60,'t'+(i+1),12);txt(svg,x+10,82,'k='+keys[i]+'  v='+values[i],13);
        txt(svg,x+10,103,'ΔS='+keys[i]*values[i],13,used?'#047857':'#64748b');
        if(used){a+=keys[i]*values[i];z+=keys[i];}
        rect(svg,x+60,128,4,used?33:16,used?'#0d9488':'#cbd5e1','none');
      }
      txt(svg,26,194,'S = Σ(k·v)',15);txt(svg,235,194,'S = '+fmt(a),18);
      txt(svg,26,237,'z = Σk',15);txt(svg,235,237,'z = '+z,18);
      rect(svg,390,179,235,76,'#f0fdfa','#14b8a6');
      txt(svg,408,207,'y = S / z    φ(q)=1',14);
      txt(svg,408,237,step?'= '+fmt(a/z):'= —',21);
      stats.textContent=step?T.state+' '+step+': S='+fmt(a)+', z='+z+', y='+fmt(a/z):T.initial;
      const table=elt('table',{'aria-label':'Scalar recurrent attention trace'}),head=elt('tr');
      ['t','k','v','ΔS','S','z','y'].forEach(t=>head.append(elt('th',{},t)));
      table.append(elt('thead'));table.querySelector('thead').append(head);
      const body=elt('tbody');let s=0,den=0;
      for(let i=0;i<4;i++){
        s+=keys[i]*values[i];den+=keys[i];const used=i<step;
        const tr=elt('tr',used&&i===step-1?{class:'attention-lab-current'}:{});
        [i+1,keys[i],values[i],keys[i]*values[i],used?s:'—',used?den:'—',used?fmt(s/den):'—'].forEach(t=>tr.append(elt('td',{},String(t))));
        body.append(tr);
      }
      table.append(body);trace.replaceChildren(table);status.textContent=stats.textContent;
    }
    function draw(){
      root.querySelector('[data-out="step"]').textContent=step;
      root.querySelector('[data-out="factor"]').textContent=factor;
      prev.disabled=step===min;next.disabled=step===max;
      if(kind==='window')drawWindow();else drawLinear();
    }
    slider.addEventListener('input',()=>{stop();setStep(Number(slider.value));});
    knob.addEventListener('input',()=>{stop();factor=Number(knob.value);draw();});
    prev.addEventListener('click',()=>{stop();setStep(step-1);});
    next.addEventListener('click',()=>{stop();setStep(step+1);});
    reset.addEventListener('click',()=>{stop();step=kind==='window'?8:0;factor=kind==='window'?4:3;speed=1;slider.value=step;knob.value=factor;speedBtn.textContent=T.speed+': 1×';draw();});
    function start(){
      if(step===max)setStep(min);
      stop();play.textContent=T.pause;play.setAttribute('aria-pressed','true');
      task=setInterval(()=>{if(document.hidden||step===max){stop();return;}setStep(step+1);},800/speed);
    }
    play.addEventListener('click',()=>task===null?start():stop());
    speedBtn.addEventListener('click',()=>{speed=speed===.5?1:speed===1?2:.5;speedBtn.textContent=T.speed+': '+speed+'×';if(task!==null){stop();start();}});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    draw();
  }
  function enhance(){document.querySelectorAll('.attention-lab[data-lab]').forEach(mount);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();
