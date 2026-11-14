/* Original illustrative simulations; no fitted neural parameters or measured recordings. */
(() => {
  const svgNS = 'http://www.w3.org/2000/svg';
  const words = {
    en: {step:'Step',previous:'Previous',next:'Next',play:'Play',pause:'Pause',seek:'Step',speed:'Speed',reset:'Reset',distractor:'Admit distractor X',replacement:'Admit replacement B',decay:'Trace time constant (steps)',refresh:'Refresh burst',store:'Memory',input:'Input',gate:'Gate',hold:'HOLD',write:'WRITE',none:'Empty',quiet:'Silent',burst:'Burst',trace:'Trace',spikes:'Spikes',remaining:'Trace value',interval:'Delay',off:'Off'},
    zh: {step:'步驟',previous:'上一步',next:'下一步',play:'播放',pause:'暫停',seek:'步驟進度',speed:'速度',reset:'重設',distractor:'允許干擾 X 寫入',replacement:'允許提示 B 寫入',decay:'隱藏痕跡衰減時間常數（步）',refresh:'啟用再活化脈衝',store:'記憶',input:'輸入',gate:'閘門',hold:'保持',write:'寫入',none:'空',quiet:'靜默',burst:'脈衝',trace:'痕跡',spikes:'放電',remaining:'痕跡值',interval:'延遲',off:'關閉'}
  };
  const make = (tag,cls,txt) => { const n=document.createElement(tag); if(cls)n.className=cls;if(txt!==undefined)n.textContent=txt;return n; };
  const svg = (tag,atts={}) => {const n=document.createElementNS(svgNS,tag);Object.entries(atts).forEach(([k,v])=>n.setAttribute(k,String(v)));return n;};
  const line = (parent,x1,y1,x2,y2,stroke='#77859c',width=2)=>parent.append(svg('line',{x1,y1,x2,y2,stroke,'stroke-width':width,'stroke-linecap':'round'}));
  const circle = (parent,cx,cy,r,fill)=>parent.append(svg('circle',{cx,cy,r,fill}));
  const text = (parent,x,y,s,fill='#334155',sz=14)=>{const n=svg('text',{x,y,fill,'font-size':sz,'font-family':'system-ui, sans-serif','text-anchor':'middle'});n.textContent=s;parent.append(n);};
  function init(root) {
    if(root.dataset.ready)return;
    root.dataset.ready='true';
    const kind=root.dataset.wmLab, lang=root.dataset.lang==='zh-TW'?'zh':'en',w=words[lang];
    const max=kind==='gate'?3:8;
    let step=0,delay=600,timer=null;
    root.setAttribute('role','group');root.setAttribute('aria-label',kind==='gate'?(lang==='zh'?'PBWM 閘控實驗':'PBWM gate lab'):(lang==='zh'?'活動靜默痕跡實驗':'Silent trace lab'));
    const settings=make('div','wm-lab-settings');
    function setting(label,type,min,maxValue,value,increment){const wrap=make('label','wm-setting');wrap.append(make('span','',label));let inp=make('input');inp.type=type;if(type==='range'){inp.min=String(min);inp.max=String(maxValue);inp.step=String(increment);}if(type==='checkbox')inp.checked=Boolean(value);else inp.value=String(value);wrap.append(inp);const valueLabel=make('output','wm-value');if(type==='range'){wrap.append(valueLabel);const setValue=()=>{valueLabel.textContent=Number(inp.value).toFixed(1);};inp.addEventListener('input',()=>{setValue();render();});setValue();}else inp.addEventListener('change',render);settings.append(wrap);return inp;}
    const admitX=kind==='gate'?setting(w.distractor,'checkbox',0,1,false,1):null;
    const admitB=kind==='gate'?setting(w.replacement,'checkbox',0,1,true,1):null;
    const tau=kind==='silent'?setting(w.decay,'range',1.5,8,4,0.5):null;
    const refresh=kind==='silent'?setting(w.refresh,'checkbox',0,1,true,1):null;
    const viewport=make('div','wm-lab-pan');viewport.tabIndex=0;viewport.setAttribute('role','region');viewport.setAttribute('aria-label',kind==='gate'?(lang==='zh'?'記憶閘控示意圖':'Memory gate diagram'):(lang==='zh'?'突觸痕跡時間序列':'Synaptic trace time series'));
    const board=svg('svg',{viewBox:'0 0 720 280',width:'720',height:'280',role:'img','aria-label':kind==='gate'?(lang==='zh'?'輸入、閘門選擇與記憶狀態':'Input, selected gate, resulting memory'):(lang==='zh'?'短暫脈衝與衰減中的隱藏突觸痕跡':'Bursts and decaying hidden synaptic trace')});viewport.append(board);
    const nav=make('div','wm-lab-controls');const prev=make('button','',w.previous),next=make('button','',w.next),play=make('button','',w.play),reset=make('button','',w.reset);
    for(const b of [prev,play,next,reset]){b.type='button';nav.append(b);}
    const seekWrap=make('label','wm-lab-seek');seekWrap.append(make('span','',w.seek));const seek=make('input');seek.type='range';seek.min='0';seek.max=String(max);seek.value='0';seekWrap.append(seek);nav.append(seekWrap);
    const speedWrap=make('label','wm-lab-speed');speedWrap.append(make('span','',w.speed));const speeds=make('select');for(const [value,title] of [[1200,'0.5×'],[600,'1×'],[300,'2×']]){const op=make('option','',title);op.value=String(value);if(value===600)op.selected=true;speeds.append(op);}speedWrap.append(speeds);nav.append(speedWrap);
    const status=make('p','wm-lab-status');status.setAttribute('aria-live','polite');status.setAttribute('aria-atomic','true');
    root.append(settings,viewport,nav,status);
    const stop=()=>{if(timer!==null){clearInterval(timer);timer=null;}play.textContent=w.play;play.setAttribute('aria-pressed','false');};
    const tick=()=>{if(step===max){stop();return;}step++;render();if(step===max)stop();};
    function gateFrame(){const events=[{value:'–',open:false},{value:'A',open:true},{value:'X',open:admitX.checked},{value:'B',open:admitB.checked}];let memory='–';for(let i=1;i<=step;i++)if(events[i].open)memory=events[i].value;const event=events[step];
      board.append(svg('rect',{x:25,y:45,width:670,height:174,rx:14,fill:'#f1f5f9'}));
      for(const [x,label] of [[132,'INPUT'],[358,'GATE'],[580,'STORE']])text(board,x,79,label,'#475569',14);
      line(board,196,144,300,144,'#94a3b8',4);line(board,412,144,512,144,'#94a3b8',4);
      board.append(svg('rect',{x:74,y:100,width:116,height:89,rx:16,fill:step?'#dbeafe':'#e2e8f0',stroke:'#93c5fd','stroke-width':2}));
      text(board,132,154,event.value,'#1d4ed8',36);
      board.append(svg('rect',{x:310,y:100,width:96,height:89,rx:16,fill:!step?'#e2e8f0':event.open?'#ccfbf1':'#fee2e2',stroke:!step?'#94a3b8':event.open?'#0d9488':'#dc2626','stroke-width':2}));
      text(board,358,151,step?(event.open?'OPEN':'CLOSE'):'–',step?(event.open?'#115e59':'#991b1b'):'#64748b',16);
      board.append(svg('rect',{x:522,y:100,width:116,height:89,rx:16,fill:'#d1fae5',stroke:'#059669','stroke-width':2}));text(board,580,154,memory,'#065f46',36);
      if(step)text(board,358,246,event.open?'WRITE':'HOLD',event.open?'#0f766e':'#b45309',17);
      status.textContent=w.step+" "+step+"/"+max+" · "+w.input+": "+event.value+" · "+w.gate+": "+(step?(event.open?w.write:w.hold):"–")+" · "+w.store+": "+memory;
    }
    function silentFrame(){const k=Number(tau.value),trace=[1],spike=[1];for(let t=1;t<=max;t++){const event=t===4&&refresh.checked?0.55:0;trace.push(trace[t-1]*Math.exp(-1/k)+event);spike.push(event?1:0);}
      board.append(svg('rect',{x:40,y:15,width:645,height:240,rx:14,fill:'#f8fafc'}));
      for(let t=0;t<=max;t++){const x=73+70*t;line(board,x,207,x,214,'#94a3b8',1);text(board,x,232,String(t),'#64748b',12);}line(board,73,209,633,209,'#94a3b8',2);
      text(board,42,66,'SPIKES','#475569',13);text(board,42,148,'TRACE','#475569',13);
      line(board,73,105,633,105,'#d1d5db',1);line(board,73,185,633,185,'#d1d5db',1);
      for(let t=0;t<=step;t++){const x=73+70*t;if(spike[t]){line(board,x,101,x,52,'#2563eb',6);circle(board,x,50,5,'#2563eb');}}
      let d='';for(let t=0;t<=step;t++){const x=73+70*t,y=187-65*trace[t];d+=(t===0?'M':'L')+x+' '+y+' ';circle(board,x,y,4,'#0f766e');}board.append(svg('path',{d,fill:'none',stroke:'#0f766e','stroke-width':4,'stroke-linecap':'round','stroke-linejoin':'round'}));
      const cx=73+70*step;line(board,cx,30,cx,206,'#f59e0b',1.8);
      const ev=spike[step]?'SPIKE':'QUIET';const st=trace[step].toFixed(3);
      text(board,610,41,ev,spike[step]?'#1d4ed8':'#64748b',14);
      status.textContent=w.step+" "+step+"/"+max+" · "+w.spikes+": "+(spike[step]?w.burst:w.quiet)+" · "+w.remaining+": "+st+" · τ="+k.toFixed(1);
    }
    function render(){board.replaceChildren();if(kind==='gate')gateFrame();else silentFrame();seek.value=String(step);prev.disabled=step===0;next.disabled=step===max;}
    prev.addEventListener('click',()=>{stop();step=Math.max(0,step-1);render();});next.addEventListener('click',()=>{stop();step=Math.min(max,step+1);render();});seek.addEventListener('input',()=>{stop();step=Number(seek.value);render();});
    play.addEventListener('click',()=>{if(timer!==null){stop();return;}if(step===max)step=0;play.textContent=w.pause;play.setAttribute('aria-pressed','true');render();timer=setInterval(tick,delay);});
    reset.addEventListener('click',()=>{stop();step=0;if(kind==='gate'){admitX.checked=false;admitB.checked=true;}else{tau.value='4';tau.dispatchEvent(new Event('input'));refresh.checked=true;}speeds.value='600';delay=600;render();});
    speeds.addEventListener('change',()=>{delay=Number(speeds.value);if(timer!==null){clearInterval(timer);timer=setInterval(tick,delay);}});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)stop();
    render();
  }
  const boot=()=>document.querySelectorAll('[data-wm-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  if(window.document$&&typeof window.document$.subscribe==='function')window.document$.subscribe(boot);
})();
