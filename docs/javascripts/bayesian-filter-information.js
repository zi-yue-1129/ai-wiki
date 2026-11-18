/* Original synthetic Kalman information and particle ESS sensitivity diagnostics. */
(function Information(){
  'use strict';
  const NS='http://www.w3.org/2000/svg',particles=[1,2.1,2.9,3.7,4.4,5.3,6.1,6.6,7.4,8.8];
  const T={
    en:{kalman:'Precision contributions to the posterior',particle:'Likelihood width and effective sample size',
      prior:a=>`Prior precision ${a.toFixed(3)}; measurement information arrives in the next step. Synthetic illustration.`,
      measured:(a,b)=>`Prior precision ${a.toFixed(3)}, measurement precision ${b.toFixed(3)}; posterior precision appears at correction.`,
      corrected:(a,b)=>`Precision adds: ${a.toFixed(3)} plus ${b.toFixed(3)} equals ${(a+b).toFixed(3)}; posterior variance ${(1/(a+b)).toFixed(3)}.`,
      pending:'No observation weighting has occurred; ESS sensitivity will appear after weighting.',
      ess:a=>`Pre-resampling ESS ${a.toFixed(3)} of 10. The curve holds the synthetic observation fixed and varies likelihood width, not systematic offset.`},
    zh:{kalman:'後驗精確度的兩個來源',particle:'概似寬度與有效樣本數',
      prior:a=>`先驗精確度 ${a.toFixed(3)}；下一步才會引入量測資訊。人工示意。`,
      measured:(a,b)=>`先驗精確度 ${a.toFixed(3)}、量測精確度 ${b.toFixed(3)}；修正階段才顯示後驗總量。`,
      corrected:(a,b)=>`精確度相加：${a.toFixed(3)} 加 ${b.toFixed(3)} 等於 ${(a+b).toFixed(3)}；後驗變異數 ${(1/(a+b)).toFixed(3)}。`,
      pending:'尚未根據觀測加權；下一階段才會顯示 ESS 對概似寬度的敏感度。',
      ess:a=>`重採樣前 ESS 為 ${a.toFixed(3)}／10。曲線固定人工觀測值、改變概似寬度，而非改變系統性重採樣偏移。`}
  };
  const E=(name,attrs={},value)=>{const e=document.createElementNS(NS,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(value!==undefined)e.textContent=String(value);return e;};
  const add=(s,name,a={},value)=>s.appendChild(E(name,a,value));
  const rect=(s,x,y,w,h,fill,a={})=>add(s,'rect',{x,y,width:Math.max(w,0),height:h,rx:3,fill,...a});
  const line=(s,x1,y1,x2,y2,stroke,a={})=>add(s,'line',{x1,y1,x2,y2,stroke,'stroke-width':2,...a});
  const label=(s,x,y,value,a={})=>add(s,'text',{x,y,'font-size':13,'font-family':'system-ui,sans-serif',fill:'#405b70',...a},value);
  const frame=(s,title,aria)=>{s.replaceChildren();s.setAttribute('viewBox','0 0 700 232');s.setAttribute('role','img');s.setAttribute('aria-label',aria);add(s,'title',{},aria);rect(s,0,0,700,232,'#f6f9fc',{rx:12});rect(s,12,10,676,212,'#fff',{rx:10,stroke:'#dce5ed'});label(s,24,36,title,{'font-size':16,'font-weight':700,fill:'#294457'});};
  const essAt=(y,sigma)=>{const w=particles.map(x=>Math.exp(-.5*((x-y)/sigma)**2)),total=w.reduce((a,b)=>a+b,0);return total*total/w.reduce((a,b)=>a+b*b,0);};
  function drawKalman(svg,values,stage,t){
    const [P,R]=values,prior=1/P,measure=1/R,total=prior+measure,x=171,w=470/total;
    frame(svg,'PRECISION / INFORMATION',t.kalman);
    [['Prior',76,prior,'#527ab8'],['Measure',125,measure,'#d88b35']].slice(0,stage>0?2:1).forEach(([name,y,q,color])=>{label(svg,29,y+17,name);rect(svg,x,y,q*w,24,color);});
    if(stage===2){label(svg,29,191,'Posterior');rect(svg,x,174,prior*w,24,'#527ab8');rect(svg,x+prior*w,174,measure*w,24,'#d88b35');line(svg,x+prior*w,174,x+prior*w,198,'#fff',{'stroke-width':1.5});label(svg,638,212,`Σ = ${total.toFixed(3)}`,{'text-anchor':'end'});}
    else label(svg,638,212,stage===0?'Await measurement':'Await correction',{'text-anchor':'end'});
    line(svg,x,56,x,205,'#849aa9',{'stroke-width':1});
    Object.assign(svg.dataset,{priorPrecision:prior.toFixed(9),measurementPrecision:measure.toFixed(9),posteriorPrecision:total.toFixed(9),posteriorVariance:(1/total).toFixed(9),stage:String(stage)});
    return stage===0?t.prior(prior):stage===1?t.measured(prior,measure):t.corrected(prior,measure);
  }
  function drawParticle(svg,values,stage,t){
    const [y,sd]=values,current=essAt(y,sd),xmin=94,xmax=643,top=65,bottom=181;
    frame(svg,'LIKELIHOOD WIDTH / ESS',t.particle);
    const px=s=>xmin+(s-.4)/2.6*(xmax-xmin),py=n=>bottom-(n-1)/9*(bottom-top);
    for(const n of [1,5,10]){line(svg,xmin,py(n),xmax,py(n),'#e0e9ef',{'stroke-width':1});label(svg,xmin-15,py(n)+5,n,{'text-anchor':'end','font-size':12});}
    label(svg,24,57,'ESS');
    for(const s of [.4,1,2,3])label(svg,px(s),210,s.toFixed(1),{'text-anchor':'middle','font-size':12});
    label(svg,665,211,'σ',{'text-anchor':'middle'});
    if(stage>0){
      let d='';for(let i=0;i<=78;i++){const s=.4+i*2.6/78;d+=(i?'L':'M')+px(s).toFixed(2)+' '+py(essAt(y,s)).toFixed(2)+' ';}
      add(svg,'path',{d,fill:'none',stroke:'#258f94','stroke-width':3.2,'stroke-linejoin':'round'});
      line(svg,px(sd),py(current),px(sd),bottom,'#d88b35',{'stroke-dasharray':'5,4','stroke-width':2});
      add(svg,'circle',{cx:px(sd),cy:py(current),r:7,fill:'#d88b35',stroke:'white','stroke-width':2});
      label(svg,px(sd)>560?px(sd)-14:px(sd)+13,Math.max(75,py(current)-13),`ESS ${current.toFixed(2)}`,{'text-anchor':px(sd)>560?'end':'start','font-size':12});
    }else label(svg,290,130,'After weighting',{'font-size':16,fill:'#7d8b9b'});
    Object.assign(svg.dataset,{currentEss:current.toFixed(9),essAtMin:essAt(y,.4).toFixed(9),essAtMax:essAt(y,3).toFixed(9),stage:String(stage)});
    return stage===0?t.pending:t.ess(current);
  }
  function enhance(host){
    if(host.dataset.bfInformationReady)return;
    const panel=host.querySelector('.bf-panel');if(!panel)return;
    const kind=host.dataset.lab,t=T[host.dataset.lang.startsWith('zh')?'zh':'en'];
    if(kind!=='kalman'&&kind!=='particle')return;
    host.dataset.bfInformationReady='true';
    const region=document.createElement('div');region.className='bf-graphic bf-insight bf-information';region.tabIndex=0;region.setAttribute('role','region');region.setAttribute('aria-label',t[kind]);
    const svg=E('svg');svg.dataset.bfInformation=kind;region.append(svg);
    const summary=document.createElement('p');summary.className='bf-insight-summary';summary.setAttribute('aria-live','polite');
    panel.querySelector('.bf-output').before(region,summary);
    const inputs=[...panel.querySelectorAll('.bf-ranges input')],output=panel.querySelector('.bf-output');
    const update=()=>{const vals=inputs.map(i=>Number(i.value)),stage=Number(panel.querySelector('.bf-step').value);summary.textContent=kind==='kalman'?drawKalman(svg,vals,stage,t):drawParticle(svg,vals,stage,t);};
    new MutationObserver(update).observe(output,{childList:true});host.addEventListener('input',update);update();
  }
  const init=()=>document.querySelectorAll('.bayesian-filter-lab[data-lab]').forEach(enhance);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  if(window.document$?.subscribe)window.document$.subscribe(init);
})();
