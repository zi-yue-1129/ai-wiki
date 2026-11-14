/* Two self-contained, deterministic teaching simulators for Bayesian filtering.
 * No external resources or eval. All data are synthetic and values are computed live.
 */
(() => {
  'use strict';
  const states = new WeakMap();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const particles = [1.0, 2.1, 2.9, 3.7, 4.4, 5.3, 6.1, 6.6, 7.4, 8.8];
  const text = {
    en: { prior:'Prior variance P', noise:'Measurement variance R', observation:'Observation y', scale:'Likelihood SD', offset:'Systematic offset', previous:'Previous', next:'Next', play:'Play', pause:'Pause', reset:'Reset', speed:'Speed', predicted:'Predicted', likelihood:'Weights', cumulative:'Cumulative', resampled:'Resampled', gain:'Kalman gain', innovation:'Innovation', posterior:'Posterior mean', variance:'Posterior variance', ess:'Effective sample size', ancestor:'Ancestor indices (zero-based)', step:'Step', help:'Use Previous/Next to inspect the intermediate Bayesian update. All values and samples are illustrative.', fallback:'Interactive numerical experiment requires JavaScript. The static animation and worked example above remain available.', values:'Current computed values', priorLabel:'Prior', measureLabel:'Observation', postLabel:'Posterior', weights:'Weights', particles:'Particles', cdf:'CDF', descendants:'Descendants' },
    zh: { prior:'預測變異數 P', noise:'量測變異數 R', observation:'觀測值 y', scale:'概似標準差', offset:'系統性抽樣偏移', previous:'上一步', next:'下一步', play:'播放', pause:'暫停', reset:'重設', speed:'速度', predicted:'預測粒子', likelihood:'概似加權', cumulative:'累積分布', resampled:'重採樣後', gain:'卡爾曼增益', innovation:'創新量', posterior:'後驗平均值', variance:'後驗變異數', ess:'有效樣本數', ancestor:'祖先索引（從 0 開始）', step:'步驟', help:'使用上一步／下一步檢視貝氏更新的中間運算。所有數值與樣本均為人工示例。', fallback:'互動數值實驗需要 JavaScript；上方靜態圖及手算範例仍可閱讀。', values:'目前計算結果', priorLabel:'先驗', measureLabel:'量測', postLabel:'後驗', weights:'權重', particles:'粒子', cdf:'累積權重', descendants:'後代' }
  };
  const svgNS = 'http://www.w3.org/2000/svg';
  const el = (tag, name, str) => { const n=document.createElement(tag); if(name)n.className=name; if(str!=null)n.textContent=str; return n; };
  const svgEl = (tag, attrs={}) => { const n=document.createElementNS(svgNS,tag); Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v))); return n; };
  const fmt = n => Number(n).toFixed(3);
  const num = (x, a,b) => Math.max(a,Math.min(b,Number(x)));
  const makeRange=(group, label, value, min,max,step, change) => {
    const row=el('label','bf-range');
    const name=el('span','bf-range-name',label); const output=el('output','bf-range-value',String(value));
    const inp=el('input'); inp.type='range'; inp.min=min; inp.max=max;inp.step=step;inp.value=value;
    inp.setAttribute('aria-label',label); inp.addEventListener('input',()=>{output.textContent=Number(inp.value).toFixed(step<.1?2:1);change(Number(inp.value));});
    row.append(name,output,inp);group.append(row);return inp;
  };
  const NS=svgNS;
  function line(svg,x1,y1,x2,y2,color,width=2,opacity=1){svg.append(svgEl('line',{x1,y1,x2,y2,stroke:color,'stroke-width':width,opacity}));}
  function label(svg,x,y,s,align='start'){const e=svgEl('text',{x,y,'text-anchor':align,'font-size':13,fill:'#52677d','font-family':'system-ui, sans-serif'});e.textContent=s;svg.append(e);}
  function plotKalman(svg,s){
    const width=700,height=280, left=48,right=662,top=38,bottom=222;
    const gain=s.P/(s.P+s.R), mean=3+gain*(s.y-3), post=(1-gain)*s.P;
    const data=[{m:3,v:s.P,c:'#527ab8',dash:'6,5'},{m:s.y,v:s.R,c:'#d88b35',dash:'3,5'},{m:mean,v:post,c:'#209e9a'}];
    svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.setAttribute('role','img');svg.setAttribute('aria-label','Gaussian prior, observation likelihood, and corrected posterior');
    [1,3,5,7,9].forEach(x=>{const px=left+(x/10)*(right-left);line(svg,px,top,px,bottom,'#e3eaf0',1);label(svg,px,bottom+22,String(x),'middle');});
    line(svg,left,bottom,right,bottom,'#90a1b3',1.5);
    const visible = s.stage===0?1:s.stage===1?2:3;
    const curves=data.slice(0,visible);
    curves.forEach((d,i)=>{
      const group=svgEl('g',{opacity:(i===0?1:(i===1?.95:1))});svg.append(group);
      let path='';for(let j=0;j<=260;j++){const x=j/26;const density=Math.exp(-.5*(x-d.m)**2/d.v);const px=left+(x/10)*(right-left);const py=bottom-density*156;path+=(j?'L':'M')+px.toFixed(2)+' '+py.toFixed(2)+' ';}
      const e=svgEl('path',{d:path,stroke:d.c,'stroke-width':i===2?4:2.5,fill:'none',...(d.dash?{'stroke-dasharray':d.dash}:{})});group.append(e);

    });
    label(svg,48,24,'GAUSSIAN FUSION');
    [{name:'Prior',x:320,c:'#527ab8',dash:'6,5'},{name:'Observation',x:432,c:'#d88b35',dash:'3,5'},{name:'Posterior',x:565,c:'#209e9a'}].slice(0,visible).forEach(d=>{const l=svgEl('line',{x1:d.x,y1:20,x2:d.x+20,y2:20,stroke:d.c,'stroke-width':3,...(d.dash?{'stroke-dasharray':d.dash}:{})});svg.append(l);label(svg,d.x+24,24,d.name)});
    label(svg,656,259,'state x','end');
    return {gain,mean,post};
  }
  function calcParticle(s){
    const raw=particles.map(x=>Math.exp(-0.5*((x-s.y)/s.sd)**2));const total=raw.reduce((a,b)=>a+b,0);
    const weights=raw.map(x=>x/total),cdf=[];weights.reduce((a,b)=>{cdf.push(a+b);return a+b},0);
    const idx=Array.from({length:10},(_,j)=>{const target=s.offset+j/10;return Math.min(9,cdf.findIndex(c=>c>=target-1e-12)<0?9:cdf.findIndex(c=>c>=target-1e-12));});
    const ess=1/weights.reduce((a,b)=>a+b*b,0);
    return {weights,cdf,idx,ess};
  }
  function plotParticle(svg,s){
    const {weights,cdf,idx,ess}=calcParticle(s);svg.replaceChildren();svg.setAttribute('viewBox','0 0 700 300');svg.setAttribute('role','img');svg.setAttribute('aria-label','Particle likelihood weights, cumulative distribution, and systematic descendants');
    label(svg,40,25,s.stage===0?'PREDICTED PARTICLES':s.stage===1?'OBSERVATION WEIGHTS':s.stage===2?'CUMULATIVE WEIGHTS':'SYSTEMATIC RESAMPLING');
    line(svg,42,218,658,218,'#96a9bb',1.6);
    particles.forEach((x,i)=>{
      const px=42+x/10*616;
      if(s.stage===0){svg.append(svgEl('circle',{cx:px,cy:146,r:7,fill:'#527ab8'}));}
      if(s.stage>=1){const h=(s.stage===2?cdf[i]:weights[i])*120;
        svg.append(svgEl('rect',{x:px-10,y:212-h,width:20,height:h,rx:3,fill:s.stage===2?'#7a9bc4':'#d88b35'}));
        if(s.stage===3){const count=idx.filter(k=>k===i).length; if(count) { svg.append(svgEl('circle',{cx:px,cy:62,r:Math.max(5,5+count*2.3),fill:'#209e9a',opacity:.9}));label(svg,px,50,String(count),'middle');}}
      }
      label(svg,px,238,String(i),'middle');
    });
    const ox=42+s.y/10*616;line(svg,ox,36,ox,220,'#d45e50',2,0.8);label(svg,Math.max(55,Math.min(645,ox+9)),51,'y');
    if(s.stage===2||s.stage===3){const threshold= s.offset;label(svg,46,278,`u₀=${threshold.toFixed(3)}  ·  ESS=${ess.toFixed(2)}`);}
    else label(svg,46,278,'ancestor index (0-based)');
    return {weights,cdf,idx,ess};
  }
  function initialise(host){
    if(states.has(host))return;
    const lang=host.dataset.lang==='zh'?'zh':'en',T=text[lang],kind=host.dataset.lab==='particle'?'particle':'kalman';
    const state=kind==='kalman'?{P:1.44,R:.64,y:7,stage:0}:{y:6.6,sd:1.3,offset:.045,stage:0};
    const fallback=host.querySelector('.bayesian-filter-fallback');
    const panel=el('section','bf-panel');panel.setAttribute('aria-label',kind==='kalman'?'Kalman fusion lab':'Particle resampling lab');
    const ranges=el('div','bf-ranges');panel.append(ranges);
    const controls=el('div','bf-controls');panel.append(controls);
    const graphic=el('div','bf-graphic');graphic.tabIndex=0;const svg=svgEl('svg');graphic.append(svg);panel.append(graphic);
    const outputs=el('div','bf-output');outputs.setAttribute('role','status');outputs.setAttribute('aria-live','polite');outputs.setAttribute('aria-atomic','true');panel.append(outputs);
    const hint=el('p','bf-hint',T.help);panel.append(hint);
    let timer=null,speed=1;
    const stop=()=>{if(timer){clearInterval(timer);timer=null;}};
    const last=kind==='kalman'?2:3;
    const parts=[];
    const refresh=()=>{
      if(!host.isConnected){stop();return;}
      const calc=kind==='kalman'?plotKalman(svg,state):plotParticle(svg,state);
      const phase=kind==='kalman'?['Predict','Innovate','Correct'][state.stage]:[T.predicted,T.likelihood,T.cumulative,T.resampled][state.stage];
      const lines=kind==='kalman'?(state.stage===0?[`x⁻ = 3.000`,`P⁻ = ${fmt(state.P)}`]:state.stage===1?[`${T.gain}: ${fmt(calc.gain)}`,`${T.innovation}: ${fmt(state.y-3)}`]:[`${T.gain}: ${fmt(calc.gain)}`,`${T.innovation}: ${fmt(state.y-3)}`,`${T.posterior}: ${fmt(calc.mean)}`,`${T.variance}: ${fmt(calc.post)}`]):(state.stage===0?[`N = 10`,`y = ${fmt(state.y)}`]:state.stage===1?[`${T.ess}: ${fmt(calc.ess)}`,`Σw = ${fmt(calc.weights.reduce((a,b)=>a+b,0))}`]:state.stage===2?[`${T.ess}: ${fmt(calc.ess)}`,`CDF₁₀ = ${fmt(calc.cdf[9])}`]:[`${T.ess}: ${fmt(calc.ess)}`,`${T.ancestor}: ${calc.idx.join(', ')}`]);
      outputs.replaceChildren();const head=el('strong',null,`${T.step} ${state.stage+1}/${last+1} · ${phase}`);outputs.append(head);
      const values=el('div','bf-stats');lines.forEach(t=>values.append(el('span',null,t)));outputs.append(values);
      progress.value=String(state.stage);
      play.textContent=timer?T.pause:T.play;play.setAttribute('aria-pressed',timer?'true':'false');
    };
    if(kind==='kalman'){
      makeRange(ranges,T.prior,state.P,.2,4,.02,x=>{state.P=x;refresh()});
      makeRange(ranges,T.noise,state.R,.15,4,.01,x=>{state.R=x;refresh()});
      makeRange(ranges,T.observation,state.y,1,9,.1,x=>{state.y=x;refresh()});
    }else{
      makeRange(ranges,T.observation,state.y,1,9,.1,x=>{state.y=x;refresh()});
      makeRange(ranges,T.scale,state.sd,.4,3,.05,x=>{state.sd=x;refresh()});
      makeRange(ranges,T.offset,state.offset,0,.099,.001,x=>{state.offset=x;refresh()});
    }
    const button=(t,fn)=>{const n=el('button','bf-button',t);n.type='button';n.addEventListener('click',fn);controls.append(n);return n;};
    const setStage=n=>{state.stage=num(n,0,last);refresh();};
    button(`◀ ${T.previous}`,()=>{stop();setStage(state.stage-1)});
    const play=button(T.play,()=>{if(timer)stop();else {if(state.stage===last)state.stage=0;timer=setInterval(()=>{state.stage=(state.stage+1)%(last+1);refresh()},1200/speed);}refresh();});
    button(`${T.next} ▶`,()=>{stop();setStage(state.stage+1)});
    const progress=el('input','bf-step');progress.type='range';progress.min='0';progress.max=String(last);progress.step='1';progress.value='0';progress.setAttribute('aria-label',T.step);progress.addEventListener('input',()=>{stop();setStage(Number(progress.value))});controls.append(progress);
    const speedBtn=button(`${speed}×`,()=>{speed=speed===1?2:speed===2?.5:1;speedBtn.textContent=`${speed}×`;if(timer){stop();timer=setInterval(()=>{state.stage=(state.stage+1)%(last+1);refresh()},1200/speed);}refresh()});speedBtn.setAttribute('aria-label',T.speed);
    button(T.reset,()=>{stop();const values=kind==='kalman'?{P:1.44,R:.64,y:7,stage:0}:{y:6.6,sd:1.3,offset:.045,stage:0};Object.assign(state,values);ranges.querySelectorAll('input').forEach((input,i)=>{input.value=String(Object.values(values)[i]);input.previousElementSibling.textContent=Number(input.value).toFixed(Number(input.step)<.1?2:1)});speed=1;speedBtn.textContent='1×';refresh();});
    host.append(panel);fallback?.remove();states.set(host,{stop});
    document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();refresh();}});
    reduced.addEventListener?.('change',event=>{if(event.matches){stop();refresh();}});
    refresh();
  }
  function enhance(root=document){root.querySelectorAll('.bayesian-filter-lab[data-lab]').forEach(initialise)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>enhance());else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(()=>enhance());
})();