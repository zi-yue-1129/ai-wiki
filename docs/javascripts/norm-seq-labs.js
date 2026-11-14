/* Original, deterministic teaching labs for LayerNorm and fixed-context Seq2Seq.
 * GitHub continues to display the separate reviewed static SVG figures.
 */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const dict = {
    en: { start:'Play', pause:'Pause', previous:'Previous', next:'Next', reset:'Reset', speed:'Speed',
      shift:'Common shift', spike:'Change feature 3', mean:'Mean', std:'Std dev.', difference:'Max |Δz|',
      step:'Step', order:'Read order', reverse:'Reversed (paper)', forward:'Original', context:'Context',
      encoder:'Encoder', decoder:'Decoder', zero:'Initial state',
      status:'Schematic values — no trained model outputs.' },
    zh: { start:'播放', pause:'暫停', previous:'上一步', next:'下一步', reset:'重設', speed:'速度',
      shift:'全體平移', spike:'特徵 3 擾動', mean:'平均值', std:'標準差', difference:'最大 |Δz|',
      step:'步驟', order:'讀取順序', reverse:'反向（原論文）', forward:'原始順序', context:'脈絡向量',
      encoder:'編碼器', decoder:'解碼器', zero:'初始狀態',
      status:'僅為人工教學數值，並非訓練模型輸出。' }
  };
  const nice = n => (Math.abs(n) < .0005 ? 0 : n).toFixed(2);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const element = (tag, attrs={}, body='') => {
    const el = document.createElement(tag);
    Object.entries(attrs).forEach(([k,v]) => el.setAttribute(k,String(v)));
    if (body) el.textContent=body;
    return el;
  };
  const graph = str => { const div=document.createElement('div'); div.className='ns-graph-scroll';div.tabIndex=0;div.setAttribute('role','region');div.setAttribute('aria-label','Scrollable visualisation');div.innerHTML=str;return div; };
  const frame = (root,title,description) => {
    root.replaceChildren();root.classList.add('ns-lab');
    const heading=element('h4',{},title), note=element('p',{class:'ns-note'},description);
    const toolbar=element('div',{class:'ns-toolbar'}), metrics=element('div',{class:'ns-metrics'}),status=element('p',{class:'ns-status',role:'status','aria-live':'polite'});
    root.append(heading,note,toolbar,metrics,status);
    return {toolbar,metrics,status};
  };
  const slider=(parent,label,min,max,step,value,handler) => {
    const wrap=element('label',{class:'ns-slider'});
    const name=element('span',{},label+' '), output=element('output',{},String(value));
    const input=element('input',{type:'range',min,max,step,value,'aria-label':label});
    input.addEventListener('input',()=>{ output.textContent=input.value;handler(Number(input.value)); });
    wrap.append(name,output,input);parent.append(wrap);return {input,output};
  };
  const button=(parent,label,handler) => {const b=element('button',{type:'button',class:'ns-button'},label);b.addEventListener('click',handler);parent.append(b);return b;};
  const metric=(name,value) => `<div class="ns-metric"><span>${name}</span><strong>${value}</strong></div>`;
  const svgText=(x,y,text,cls='')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="middle">${text}</text>`;
  const line=(coords,cls)=>`<polyline class="${cls}" points="${coords.map(([x,y])=>`${x},${y.toFixed(2)}`).join(' ')}"/>`;
  const circle=(x,y,cls)=>`<circle class="${cls}" cx="${x}" cy="${y.toFixed(2)}" r="7"/>`;
  const BASE=[1,3,5,7,9], eps=1e-5;
  function norm(x){const mu=x.reduce((a,b)=>a+b,0)/x.length;const sd=Math.sqrt(x.reduce((a,b)=>a+(b-mu)**2,0)/x.length+eps);return {mu,sd,z:x.map(v=>(v-mu)/sd)};}
  function initNorm(root,lang){const L=dict[lang];let shift=2,spike=0;
    const {toolbar,metrics,status}=frame(root,lang==='zh'?'LayerNorm · 單樣本特徵':'LayerNorm · Feature Axis',L.status);
    const s=slider(toolbar,L.shift,-4,4,1,shift,v=>{shift=v;draw();});
    const p=slider(toolbar,L.spike,-3,3,1,spike,v=>{spike=v;draw();});
    button(toolbar,L.reset,()=>{shift=2;spike=0;s.input.value='2';s.output.textContent='2';p.input.value='0';p.output.textContent='0';draw();});
    const chart=graph('<svg class="ns-svg" viewBox="0 0 720 334" role="img" aria-label="Five raw and standardised feature values"><title>LayerNorm live feature-axis calculation</title><g class="ns-dynamic"></g></svg>');
    metrics.before(chart);const dynamic=chart.querySelector('.ns-dynamic');
    function draw(){const x=BASE.map((v,i)=>v+shift+(i===2?spike:0)),result=norm(x),base=norm(BASE),xs=[96,220,344,468,592];
      const raw=xs.map((v,i)=>[v,150-(x[i]+6)*5.7]);
      const zn=xs.map((v,i)=>[v,250-result.z[i]*29]);
      const zb=xs.map((v,i)=>[v,250-base.z[i]*29]);
      let a=`<rect class="ns-panel" x="14" y="18" width="692" height="142" rx="12"/><rect class="ns-panel" x="14" y="182" width="692" height="142" rx="12"/>`;
      a+=svgText(86,40,'Raw features','ns-caption')+svgText(103,205,'Normalised','ns-caption');
      a+=`<line class="ns-gridline" x1="50" y1="150" x2="662" y2="150"/><line class="ns-gridline" x1="50" y1="250" x2="662" y2="250"/>`;
      a+=line(raw,'ns-raw-line')+line(zb,'ns-baseline-line')+line(zn,'ns-norm-line');
      xs.forEach((v,i)=>{a+=circle(v,raw[i][1],'ns-raw-dot')+circle(v,zn[i][1],'ns-norm-dot');
        a+=svgText(v,raw[i][1]<64?raw[i][1]+23:raw[i][1]-13,String(x[i]),'ns-small');
        a+=svgText(v,zn[i][1]<238?zn[i][1]+22:zn[i][1]-14,nice(result.z[i]),'ns-small');
        a+=svgText(v,319,`f${i+1}`,'ns-axis');});
      dynamic.innerHTML=a;
      const delta=Math.max(...result.z.map((v,i)=>Math.abs(v-base.z[i])));
      metrics.innerHTML=metric(L.mean,nice(result.mu))+metric(L.std,nice(result.sd))+metric(L.difference,nice(delta));
      status.textContent=`x = [${x.join(', ')}] · z = [${result.z.map(nice).join(', ')}]. ${L.status}`;
    }draw();
  }
  const emb={A:[1,.2],B:[.2,.9],C:[-.6,.4],D:[.6,-.8],BOS:[.1,.15],y1:[.15,-.25],y2:[-.2,.3]};
  function buildStates(reverse){const order=reverse?['D','C','B','A']:['A','B','C','D'];let h=[0,0], states=[[0,0]];
    for(const t of order){h=h.map((v,i)=>.65*v+emb[t][i]);states.push(h);}
    let dec=h.slice();const outs=[emb.BOS,emb.y1,emb.y2];
    for(const vec of outs){dec=dec.map((v,i)=>.7*v+vec[i]);states.push(dec);}return {order,states};}
  function initSeq(root,lang){const L=dict[lang];let step=0,reverse=true,speed=1,timer=null;
    const {toolbar,metrics,status}=frame(root,lang==='zh'?'Seq2Seq · 單一脈絡交接':'Seq2Seq · Single Context Handoff',L.status);
    const orderLabel=element('label',{class:'ns-choice'},L.order+' '),select=element('select',{'aria-label':L.order});
    select.append(element('option',{value:'reverse'},L.reverse),element('option',{value:'forward'},L.forward));orderLabel.append(select);toolbar.append(orderLabel);
    const buttons=element('div',{class:'ns-button-row'});toolbar.append(buttons);
    const prev=button(buttons,L.previous,()=>change(step-1));
    const play=button(buttons,L.start,()=>{if(timer)stop();else start();});
    const next=button(buttons,L.next,()=>change(step+1));
    button(buttons,L.reset,()=>{stop();change(0);});
    const seek=slider(toolbar,L.step,0,7,1,0,v=>change(v));
    const speedLabel=element('label',{class:'ns-choice'},L.speed+' '),speedSelect=element('select',{'aria-label':L.speed});
    for(const v of [.5,1,2])speedSelect.append(element('option',{value:v},v+'×'));
    speedSelect.value='1';speedLabel.append(speedSelect);toolbar.append(speedLabel);
    const chart=graph('<svg class="ns-svg" viewBox="0 0 720 318" role="img" aria-label="Recurrent encoder context and decoder state"><title>Fixed-context encoder–decoder state transitions</title><g class="ns-dynamic"></g></svg>');metrics.before(chart);
    const dynamic=chart.querySelector('.ns-dynamic');
    const stop=()=>{if(timer){clearInterval(timer);timer=null;}play.textContent=L.start;};
    const change=v=>{step=clamp(v,0,7);seek.input.value=String(step);seek.output.textContent=String(step);render();};
    const start=()=>{if(reduced.matches)return; if(step===7)change(0);play.textContent=L.pause;timer=setInterval(()=>{if(step>=7){stop();return;}change(step+1);},950/speed);};
    speedSelect.addEventListener('change',()=>{speed=Number(speedSelect.value);if(timer){stop();start();}});
    select.addEventListener('change',()=>{reverse=select.value==='reverse';stop();change(0);});
    reduced.addEventListener?.('change',e=>{if(e.matches)stop();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    function render(){const {order,states}=buildStates(reverse);const current=states[step],final=states[4];
      let a=`<rect class="ns-panel" x="12" y="14" width="696" height="146" rx="13"/><rect class="ns-panel" x="12" y="176" width="696" height="130" rx="13"/>`;
      a+=svgText(78,39,'Encoder','ns-caption')+svgText(82,198,'Decoder','ns-caption');
      order.forEach((token,i)=>{const x=88+139*i,active=step===i+1,done=step>=i+1;
        a+=`<rect class="ns-token ${active?'ns-current':done?'ns-done':''}" x="${x-34}" y="60" width="68" height="55" rx="9"/>`;
        a+=svgText(x,93,token,'ns-token-text');if(i<3)a+=`<path class="ns-arrow" d="M${x+37} 87H${x+100}"/>`;});
      a+=`<path class="ns-arrow" d="M540 118L600 118L600 189"/>`;
      const ready=step>=4;
      a+=`<rect class="ns-context ${ready?'ns-done':''}" x="560" y="202" width="124" height="54" rx="9"/>`;
      a+=svgText(622,221,'v','ns-token-text')+svgText(622,242,ready?`(${nice(final[0])}, ${nice(final[1])})`:'—','ns-vector');
      for(let i=1;i<=3;i++){const x=123+139*(i-1),done=step>=i+4,active=step===i+4;
        a+=`<rect class="ns-token ${active?'ns-current':done?'ns-done':''}" x="${x-35}" y="219" width="70" height="52" rx="9"/>`;
        a+=svgText(x,242,`y${i}`,'ns-token-text');a+=svgText(x,260,done?`(${nice(states[i+4][0])},${nice(states[i+4][1])})`:'·','ns-vector');
        if(i<3)a+=`<path class="ns-arrow" d="M${x+39} 244H${x+100}"/>`;
      }
      a+=svgText(345,135,`h = (${nice(states[Math.min(step,4)][0])}, ${nice(states[Math.min(step,4)][1])})`,'ns-vector');
      dynamic.innerHTML=a;prev.disabled=step===0;next.disabled=step===7;
      metrics.innerHTML=metric(L.step,`${step} / 7`)+metric(L.context,ready?`(${final.map(nice).join(', ')})`:'—')+metric('State',`(${current.map(nice).join(', ')})`);
      status.textContent=`${step===0?L.zero:step<=4?`${L.encoder}: ${order[step-1]}`:`${L.decoder}: y${step-4}`} · ${L.status}`;
    }render();
  }
  function enhance(){document.querySelectorAll('[data-norm-seq-lab]').forEach(root=>{
    if(root.dataset.nsEnhanced==='yes')return;root.dataset.nsEnhanced='yes';
    const lang=root.dataset.lang==='zh'?'zh':'en';
    if(root.dataset.normSeqLab==='layernorm')initNorm(root,lang);
    if(root.dataset.normSeqLab==='seq2seq')initSeq(root,lang);
  });}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(typeof window.document$!=='undefined'&&typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();