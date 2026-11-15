/* Original calculated diagrams for the existing Bayesian filter labs. Synthetic data only. */
(() => {
  'use strict';
  const NS='http://www.w3.org/2000/svg', xs=[1,2.1,2.9,3.7,4.4,5.3,6.1,6.6,7.4,8.8];
  const T={en:{k:'Scalar Kalman innovation and correction',p:'Systematic resampling via inverse cumulative weights',s:(k,d,v)=>'Kalman gain '+k.toFixed(3)+', correction '+d.toFixed(3)+', posterior variance '+v.toFixed(3)+'; synthetic values.',a:(e,id,n)=>'Pre-resampling ESS '+e.toFixed(2)+' of 10; '+(n===3?'selected zero-based ancestors '+id.join(', '):'thresholds and ancestors appear at later steps')+'.'},zh:{k:'一維卡爾曼創新量與增益修正',p:'利用累積權重的反函數進行系統性重採樣',s:(k,d,v)=>'卡爾曼增益 '+k.toFixed(3)+'，均值修正 '+d.toFixed(3)+'，後驗變異數 '+v.toFixed(3)+'；均為人工示意。',a:(e,id,n)=>'重採樣前 ESS 為 '+e.toFixed(2)+'／10；'+(n===3?'祖先索引 '+id.join('、'):'後續階段顯示門檻與祖先')+'。'}};
  const E=(name,attrs={},value)=>{const e=document.createElementNS(NS,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(value!==undefined)e.textContent=value;return e;};
  const box=(s,x,y,w,h,color,extra={})=>s.append(E('rect',{x,y,width:Math.max(w,0),height:h,fill:color,...extra}));
  const stroke=(s,x,y,u,v,color,width=2,extra={})=>s.append(E('line',{x1:x,y1:y,x2:u,y2:v,stroke:color,'stroke-width':width,...extra}));
  const txt=(s,x,y,value,extra={})=>s.append(E('text',{x,y,'font-size':13,'font-family':'system-ui,sans-serif',fill:'#405b70',...extra},String(value)));
  const frame=(s,title,aria)=>{s.replaceChildren();s.setAttribute('viewBox','0 0 700 230');s.setAttribute('role','img');s.setAttribute('aria-label',aria);s.append(E('title',{},aria));box(s,0,0,700,230,'#f7fafc',{rx:14});box(s,12,10,676,210,'white',{rx:10,stroke:'#dbe6ed'});txt(s,24,36,title,{'font-size':17,'font-weight':700,fill:'#263f52'});};
  function kalman(svg,[P,R,y],stage,aria){
    const K=P/(P+R),d=K*(y-3),v=(1-K)*P,px=n=>180+(n-1)*55;
    frame(svg,'INNOVATION / CORRECTION',aria);
    const rows=[['Prior',3,69,'#527ab8'],['Observation',y,112,'#d88b35'],['Posterior',3+d,155,'#209e9a']];
    rows.slice(0,stage+1).forEach(([name,mean,yy,color],i)=>{txt(svg,24,yy+5,name);stroke(svg,180,yy,630,yy,'#e2eaf0');if(i)stroke(svg,px(3),yy,px(mean),yy,color,4,{'stroke-opacity':'.43'});svg.append(E('circle',{cx:px(mean),cy:yy,r:7,fill:color,stroke:'white','stroke-width':2}));});
    [1,3,5,7,9].forEach(n=>txt(svg,px(n),191,n,{'text-anchor':'middle','font-size':12}));
    if(stage>0)txt(svg,24,211,'K = '+K.toFixed(3));
    if(stage===2){txt(svg,204,211,'Shift = '+d.toFixed(3));txt(svg,415,211,'P+ = '+v.toFixed(3));}
    Object.assign(svg.dataset,{gain:K.toFixed(6),shift:d.toFixed(6),posteriorVariance:v.toFixed(6)});
    return {K,d,v};
  }
  function particle(svg,[y,sd,u0],stage,aria){
    const r=xs.map(x=>Math.exp(-.5*((x-y)/sd)**2)),tot=r.reduce((a,b)=>a+b,0),w=r.map(x=>x/tot),cdf=[0];
    w.forEach(x=>cdf.push(cdf.at(-1)+x));
    const u=Array.from({length:10},(_,i)=>u0+i/10),idx=u.map(t=>Math.max(0,cdf.findIndex((c,i)=>i>0&&c>=t-1e-12)-1));
    const ess=1/w.reduce((a,b)=>a+b*b,0);
    frame(svg,'INVERSE CDF / SYSTEMATIC DRAW',aria);
    txt(svg,45,67,stage===0?'Uniform initial weights':'Weight intervals');
    const edges=stage===0?Array.from({length:11},(_,i)=>i/10):cdf;
    for(let i=0;i<10;i++){const a=65+570*edges[i],b=65+570*edges[i+1];box(svg,a,78,b-a,41,['#527ab8','#d88b35','#209e9a'][i%3],{'fill-opacity':'.82'});if(b-a>25)txt(svg,(a+b)/2,104,i,{'text-anchor':'middle','font-size':12,fill:'white'});}
    if(stage>=2)u.forEach((t,i)=>{const x=65+570*t;stroke(svg,x,125,x,153,'#263f52',1.8);if(stage===3)txt(svg,x,175,idx[i],{'text-anchor':'middle','font-size':12});});
    txt(svg,44,199,stage===3?'Selected ancestor index (0-based)':stage===2?'Systematic thresholds':'Cumulative mass: 0 to 1');
    Object.assign(svg.dataset,{ess:ess.toFixed(6),ancestors:idx.join(','),weightSum:w.reduce((a,b)=>a+b,0).toFixed(6)});
    return {ess,idx};
  }
  function init(host){
    if(host.dataset.bfInsightReady)return;
    const panel=host.querySelector('.bf-panel');if(!panel)return;
    const kind=host.dataset.lab,L=T[host.dataset.lang==='zh'?'zh':'en'];if(kind!=='kalman'&&kind!=='particle')return;
    host.dataset.bfInsightReady='true';
    const region=document.createElement('div');region.className='bf-graphic bf-insight';region.tabIndex=0;region.setAttribute('role','region');region.setAttribute('aria-label',L[kind==='kalman'?'k':'p']);
    const svg=E('svg');svg.dataset.bfDiagnostic=kind;region.append(svg);panel.querySelector('.bf-graphic').insertAdjacentElement('afterend',region);
    const summary=document.createElement('p');summary.className='bf-insight-summary';summary.setAttribute('aria-live','polite');region.insertAdjacentElement('afterend',summary);
    const inputs=[...panel.querySelectorAll('.bf-ranges input')],output=panel.querySelector('.bf-output');
    const update=()=>{const values=inputs.map(i=>Number(i.value)),stage=Number(panel.querySelector('.bf-step').value);const v=kind==='kalman'?kalman(svg,values,stage,L.k):particle(svg,values,stage,L.p);summary.textContent=kind==='kalman'?L.s(v.K,v.d,v.v):L.a(v.ess,v.idx,stage);};
    new MutationObserver(update).observe(output,{childList:true});host.addEventListener('input',update);update();
  }
  const enhance=()=>document.querySelectorAll('.bayesian-filter-lab[data-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();