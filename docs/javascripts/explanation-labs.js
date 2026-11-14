/* Deterministic interactive complements to the GitHub-safe LIME/SHAP SVG figures.
 * All values are an artificial 1-D black box or a three-feature cooperative game.
 */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const dictionary = {
    en: {
      limeTitle: 'Re-fit a local surrogate', sigma: 'Kernel bandwidth', slope: 'Slope', rmse: 'Weighted RMSE',
      limeHint: 'Move the bandwidth: the same twelve samples receive different weights, so the local fit changes.',
      shapTitle: 'Recompute exact Shapley credit', feature: 'Feature', step: 'Coalitions included',
      subtotal: 'Weighted subtotal', total: 'Exact credit', prev: 'Previous', next: 'Next',
      play: 'Play', pause: 'Pause', reset: 'Reset',
      shapHint: 'Select a feature and accumulate the four weighted marginal contributions. Order is only instructional.',
      modelNote: 'Constructed numerical example, not measured model output.',
      chartLime: 'Black-box curve, fixed samples, kernel weights and fitted local surrogate',
      chartShap: 'Four coalition marginal contributions and running weighted credit'
    },
    zh: {
      limeTitle: '重新擬合局部替代模型', sigma: '核函數頻寬', slope: '斜率', rmse: '加權 RMSE',
      limeHint: '調整頻寬：固定的十二個樣本將得到不同權重，局部擬合也隨之改變。',
      shapTitle: '重新計算精確 Shapley 貢獻', feature: '特徵', step: '納入的聯盟數',
      subtotal: '加權累計', total: '精確貢獻', prev: '上一步', next: '下一步',
      play: '播放', pause: '暫停', reset: '重設',
      shapHint: '切換特徵，逐列累計四組加權邊際貢獻。列的順序僅供教學使用。',
      modelNote: '人工建構的數值示例，並非模型實測輸出。',
      chartLime: '黑箱曲線、固定樣本、核函數權重與局部替代模型',
      chartShap: '四組聯盟邊際貢獻及累計加權值'
    }
  };
  const f = x => 0.27 + 0.34*x + 0.15*Math.sin(2*Math.PI*x) + 0.13*(x-0.55)**2;
  const samples = [0.08,0.16,0.24,0.32,0.40,0.48,0.56,0.64,0.72,0.80,0.88,0.96];
  const x0 = 0.54;
  const fixed = (x, d=3) => Number(x).toFixed(d);
  const gauss = (x, sigma) => Math.exp(-(((x-x0)/sigma)**2)/2);
  function fit(sigma) {
    let s=0,sx=0,sy=0,sxx=0,sxy=0;
    for (const x of samples) {const w=gauss(x,sigma), y=f(x);s+=w;sx+=w*x;sy+=w*y;sxx+=w*x*x;sxy+=w*x*y;}
    const b=(s*sxy-sx*sy)/(s*sxx-sx*sx), a=(sy-b*sx)/s;
    const err=Math.sqrt(samples.reduce((t,x)=>t+gauss(x,sigma)*(f(x)-a-b*x)**2,0)/s);
    return {a,b,err};
  }
  function el(tag, attrs={}, txt='') {
    const node=document.createElement(tag);
    for(const [key,val] of Object.entries(attrs)) node.setAttribute(key,val);
    if(txt) node.textContent=txt;
    return node;
  }
  function svg(tag, attrs={}, txt='') {
    const node=document.createElementNS(NS,tag);
    for(const [key,val] of Object.entries(attrs)) node.setAttribute(key,val);
    if(txt) node.textContent=txt;
    return node;
  }
  function drawLime(chart, sigma) {
    chart.replaceChildren();
    const X=x=>52+x*520, Y=y=>280-y*310;
    chart.append(svg('rect',{x:0,y:0,width:640,height:330,rx:14,fill:'#101e33'}));
    chart.append(svg('rect',{x:X(Math.max(0,x0-sigma)),y:37,width:Math.min(1,x0+sigma)*520+52-X(Math.max(0,x0-sigma)),height:244,rx:8,fill:'#1b5262',opacity:.34}));
    for(let i=0;i<6;i++){const y=48+i*47;chart.append(svg('path',{d:`M52 ${y} H572`,stroke:'#53667a','stroke-width':.65,opacity:.35}));}
    chart.append(svg('path',{d:'M52 280 H572',stroke:'#a4b3c5','stroke-width':1.4}));
    const black=[];
    for(let i=0;i<=120;i++){const x=i/120;black.push(`${i?'L':'M'}${fixed(X(x),1)} ${fixed(Y(f(x)),1)}`);}
    chart.append(svg('path',{d:black.join(' '),fill:'none',stroke:'#76aefa','stroke-width':3,'stroke-linecap':'round'}));
    const {a,b,err}=fit(sigma), left=Math.max(0,x0-1.5*sigma),right=Math.min(1,x0+1.5*sigma);
    chart.append(svg('path',{d:`M${fixed(X(left),1)} ${fixed(Y(a+b*left),1)} L${fixed(X(right),1)} ${fixed(Y(a+b*right),1)}`,fill:'none',stroke:'#f5ac59','stroke-width':4,'stroke-linecap':'round'}));
    for(const x of samples){const w=gauss(x,sigma);chart.append(svg('circle',{cx:fixed(X(x),2),cy:fixed(Y(f(x)),2),r:fixed(3+9*w,2),fill:'#55d4c2',opacity:fixed(.3+.7*w),stroke:'#e6fffc','stroke-width':w>.5?1.5:.4}));}
    chart.append(svg('path',{d:`M${fixed(X(x0),1)} 36 V281`,stroke:'#f5ac59','stroke-dasharray':'4 5','stroke-width':1.6}));
    chart.append(svg('circle',{cx:fixed(X(x0),1),cy:fixed(Y(f(x0)),1),r:5,fill:'#ffdf98'}));
    chart.append(svg('text',{x:fixed(X(x0)+7,1),y:39,fill:'#ffdf98','font-size':14,'font-family':'sans-serif'},'x₀'));
    chart.append(svg('text',{x:65,y:30,fill:'#76aefa','font-size':13,'font-family':'sans-serif'},'Black box'));
    chart.append(svg('text',{x:445,y:30,fill:'#f5ac59','font-size':13,'font-family':'sans-serif'},'Local fit'));
    for(let j=0;j<5;j++)chart.append(svg('text',{x:fixed(X(j/4),1),y:302,fill:'#c8d6e6','font-size':12,'text-anchor':'middle','font-family':'sans-serif'},fixed(j/4,2)));
    return {a,b,err};
  }
  function initLime(host, t) {
    host.classList.add('explanation-lab');
    const title=el('h4',{},t.limeTitle), hint=el('p',{class:'explanation-lab-hint'},t.limeHint);
    const area=el('div',{class:'explanation-lab-scroll',tabindex:'0'});
    const chart=svg('svg',{viewBox:'0 0 640 330',width:640,height:330,role:'img','aria-label':t.chartLime});area.append(chart);
    const controls=el('div',{class:'explanation-lab-controls'}), label=el('label',{},`${t.sigma} `);
    const slider=el('input',{type:'range',min:'0.08',max:'0.32',step:'0.01',value:'0.15','aria-label':t.sigma});
    const bandwidth=el('output',{},'0.15');label.append(slider,bandwidth);
    const stats=el('div',{class:'explanation-lab-stats','aria-live':'polite'});
    controls.append(label);host.append(title,hint,area,controls,stats,el('p',{class:'explanation-lab-note'},t.modelNote));
    function update(){const sigma=Number(slider.value), v=drawLime(chart,sigma);bandwidth.textContent=fixed(sigma,2);stats.textContent=`g(x) = ${fixed(v.a)} ${v.b<0?'−':'+'} ${fixed(Math.abs(v.b))}x   ·   ${t.slope}: ${fixed(v.b)}   ·   ${t.rmse}: ${fixed(v.err,4)}`;}
    slider.addEventListener('input',update);update();
  }
  const coefficients = {A:0.20,B:0.12,C:0.08,AB:0.12,AC:-0.08,BC:0.05,ABC:0.06};
  function value(set){let s=0.10;for(const [key,c] of Object.entries(coefficients))if([...key].every(ch=>set.includes(ch)))s+=c;return s;}
  const weights=[1/3,1/6,1/6,1/3];
  const coalitions = feature => {const [a,b]='ABC'.split('').filter(x=>x!==feature);return [[],[a],[b],[a,b]];};
  function calcShap(feature){return coalitions(feature).map((s,i)=>({coal:s,contribution:value([...s,feature])-value(s),weight:weights[i]}));}
  function initShap(host,t){
    host.classList.add('explanation-lab');
    const title=el('h4',{},t.shapTitle),hint=el('p',{class:'explanation-lab-hint'},t.shapHint);
    const area=el('div',{class:'explanation-lab-scroll',tabindex:'0'}),chart=svg('svg',{viewBox:'0 0 640 330',width:640,height:330,role:'img','aria-label':t.chartShap});area.append(chart);
    const controls=el('div',{class:'explanation-lab-controls'}),label=el('label',{},`${t.feature} `);
    const feature=el('select',{'aria-label':t.feature});for(const f of 'ABC')feature.append(el('option',{value:f},f));
    label.append(feature);
    const back=el('button',{type:'button'},t.prev),forward=el('button',{type:'button'},t.next),play=el('button',{type:'button'},t.play);
    const stepLabel=el('label',{},`${t.step} `),slider=el('input',{type:'range',min:'0',max:'4',step:'1',value:'0','aria-label':t.step}),count=el('output',{},'0 / 4');stepLabel.append(slider,count);
    const stats=el('div',{class:'explanation-lab-stats','aria-live':'polite'});
    controls.append(label,back,forward,play,stepLabel);host.append(title,hint,area,controls,stats,el('p',{class:'explanation-lab-note'},t.modelNote));
    let timer=null;
    function stop(){if(timer!==null){clearInterval(timer);timer=null;}play.textContent=t.play;}
    function update(){
      const rows=calcShap(feature.value),n=Number(slider.value),total=rows.reduce((s,r)=>s+r.contribution*r.weight,0),sum=rows.slice(0,n).reduce((s,r)=>s+r.contribution*r.weight,0);
      count.textContent=`${n} / 4`;stats.textContent=`${t.subtotal}: ${fixed(sum)}  ·  ${t.total} φ${feature.value}: ${fixed(total)}`;
      back.disabled=n===0;forward.disabled=n===4;
      chart.replaceChildren();chart.append(svg('rect',{width:640,height:330,rx:14,fill:'#101e33'}));
      chart.append(svg('text',{x:36,y:30,fill:'#cad6e6','font-size':13,'font-family':'sans-serif'},`S   →   S + ${feature.value}`));
      chart.append(svg('text',{x:377,y:30,fill:'#cad6e6','font-size':13,'font-family':'sans-serif'},'Δv × w'));
      rows.forEach((r,i)=>{
        const y=64+i*49,active=i<n;
        chart.append(svg('rect',{x:24,y:y-20,width:593,height:42,rx:8,fill:active?'#1a4853':'#1b2c44',stroke:active?'#2faeac':'#2b4664','stroke-width':1}));
        chart.append(svg('text',{x:42,y:y+7,fill:active?'#effefa':'#9db2c7','font-size':15,'font-family':'sans-serif'},`{${r.coal.join(',') || '∅'}}   + ${feature.value}`));
        const len=r.contribution*410;
        chart.append(svg('rect',{x:255,y:y-9,width:active?len:0,height:18,rx:4,fill:'#64d8c7'}));
        chart.append(svg('rect',{x:255,y:y-9,width:len,height:18,rx:4,fill:'none',stroke:'#47677b','stroke-width':1}));
        chart.append(svg('text',{x:555,y:y+6,fill:active?'#ffe1a5':'#9db2c7','font-size':13,'font-family':'sans-serif','text-anchor':'middle'},fixed(r.contribution*r.weight)));
      });
      chart.append(svg('path',{d:'M42 286 H594',stroke:'#5a7890','stroke-width':2}));
      chart.append(svg('rect',{x:42,y:278,width:520*sum/.30,height:15,rx:6,fill:'#f4b263'}));
      chart.append(svg('text',{x:594,y:318,fill:'#e7edf5','font-size':15,'font-family':'sans-serif','text-anchor':'end'},`φ${feature.value}  ${fixed(sum)} / ${fixed(total)}`));
    }
    function set(n){slider.value=String(Math.max(0,Math.min(4,n)));update();}
    back.addEventListener('click',()=>{stop();set(Number(slider.value)-1);});
    forward.addEventListener('click',()=>{stop();set(Number(slider.value)+1);});
    slider.addEventListener('input',()=>{stop();update();});feature.addEventListener('change',()=>{stop();set(0);});
    play.addEventListener('click',()=>{
      if(timer!==null){stop();return;}
      if(reduced.matches)return;
      if(Number(slider.value)===4)set(0);
      timer=setInterval(()=>{let n=Number(slider.value)+1;set(n);if(n>=4)stop();},850);
      play.textContent=t.pause;
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    reduced.addEventListener('change',()=>stop());
    update();
  }
  function boot(root=document){for(const host of root.querySelectorAll('[data-explanation-lab]')){
    if(host.dataset.explanationReady==='yes')continue;
    host.dataset.explanationReady='yes';
    const t=dictionary[host.dataset.locale==='zh'?'zh':'en'];
    if(host.dataset.explanationLab==='lime')initLime(host,t);
    if(host.dataset.explanationLab==='shap')initShap(host,t);
  }}
  if(typeof document$!=='undefined'&&document$.subscribe)document$.subscribe(()=>boot());
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>boot());else boot();
})();