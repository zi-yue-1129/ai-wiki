/* Original synthetic Kalman and particle-filter comparisons. */
(() => {
'use strict';
const NS='http://www.w3.org/2000/svg', xs=[1,2.1,2.9,3.7,4.4,5.3,6.1,6.6,7.4,8.8];
const E=(tag,a={},t)=>{const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(a))e.setAttribute(k,String(v));if(t!==undefined)e.textContent=String(t);return e;};
const txt=(s,x,y,t,a={})=>s.append(E('text',{x,y,'font-size':12,'font-family':'system-ui,sans-serif',fill:'#3c5369',...a},t));
const ln=(s,x,y,u,v,c,w=2,d)=>s.append(E('line',{x1:x,y1:y,x2:u,y2:v,stroke:c,'stroke-width':w,...(d?{'stroke-dasharray':d}:{})}));
const mark=(s,x,y,c,r=8)=>s.append(E('circle',{cx:x,cy:y,r,fill:c,stroke:'white','stroke-width':2}));
const at=v=>120+(v-1)*62.75;
function frame(s,title,alt){s.replaceChildren();s.setAttribute('viewBox','0 0 700 224');s.setAttribute('role','img');s.setAttribute('aria-label',alt);
s.append(E('title',{},alt),E('rect',{x:0,y:0,width:700,height:224,rx:13,fill:'#f7fafc'}),E('rect',{x:12,y:10,width:676,height:204,rx:9,fill:'white',stroke:'#d7e4ed'}));
txt(s,28,36,title,{'font-size':17,'font-weight':700,fill:'#253f53'});ln(s,120,169,622,169,'#a1b2c0',1.5);for(const n of [1,3,5,7,9]){ln(s,at(n),164,at(n),174,'#a1b2c0',1);txt(s,at(n),202,n,{'font-size':11,'text-anchor':'middle'});}}
function kalman(s,[P,R,y],phase,zh){const K=P/(P+R),mu=3+K*(y-3),variance=P*R/(P+R);
frame(s,'KALMAN / TRUST ALLOCATION',zh?'卡爾曼平均值的觀測權重':'Kalman prior-observation trust allocation');
txt(s,28,83,'Prior');mark(s,at(3),78,'#527ab8');
if(phase>=1){txt(s,28,116,'Measure');mark(s,at(y),111,'#d88b35');s.append(E('rect',{x:120,y:53,width:500*(1-K),height:12,rx:3,fill:'#527ab8'}),E('rect',{x:120+500*(1-K),y:53,width:500*K,height:12,rx:3,fill:'#d88b35'}));txt(s,120,47,'1−K = '+(1-K).toFixed(3),{'font-size':11});txt(s,620,47,'K = '+K.toFixed(3),{'font-size':11,'text-anchor':'end'});}
if(phase===2){txt(s,28,151,'Posterior');mark(s,at(mu),146,'#209e9a');ln(s,at(3),78,at(mu),146,'#209e9a',1.7,'5 4');txt(s,642,150,'P+ = '+variance.toFixed(3),{'text-anchor':'end'});}
Object.assign(s.dataset,{posteriorMean:mu.toFixed(8),posteriorVariance:variance.toFixed(8),gain:K.toFixed(8),stage:phase});return {K,mu,variance};}
function particle(s,[y,sd,u0],phase,zh){const raw=xs.map(x=>Math.exp(-.5*((x-y)/sd)**2)),sum=raw.reduce((a,b)=>a+b,0),w=raw.map(x=>x/sum);let c=0;const cdf=w.map(x=>(c+=x));const idx=Array.from({length:10},(_,j)=>{const z=cdf.findIndex(x=>x>=u0+j/10-1e-12);return z<0?9:z;});
const weighted=xs.reduce((a,x,i)=>a+x*w[i],0),sample=idx.reduce((a,i)=>a+xs[i],0)/10;
frame(s,'PARTICLE / MEAN SHIFT',zh?'粒子加權平均與重採樣平均':'Particle weighted versus resampled mean');
if(phase===0)txt(s,32,98,'Predicted',{'font-size':13});
if(phase>=1){txt(s,28,91,'Weighted');mark(s,at(weighted),86,'#527ab8');txt(s,640,90,weighted.toFixed(3),{'text-anchor':'end'});}
if(phase===3){txt(s,28,140,'Drawn');mark(s,at(sample),135,'#d88b35');ln(s,at(weighted),86,at(sample),135,'#a37f86',2,'5 4');txt(s,640,140,sample.toFixed(3),{'text-anchor':'end'});txt(s,28,61,'Δ = '+(sample-weighted).toFixed(3),{'font-size':13,'font-weight':600});}
Object.assign(s.dataset,{weightedMean:weighted.toFixed(8),resampledMean:sample.toFixed(8),meanShift:(sample-weighted).toFixed(8),stage:phase});return {weighted,sample,shift:sample-weighted};}
function init(host){if(host.dataset.bfComparisonReady)return;const panel=host.querySelector('.bf-panel');if(!panel)return;const kind=host.dataset.lab,zh=host.dataset.lang==='zh';if(!['kalman','particle'].includes(kind))return;host.dataset.bfComparisonReady='true';
const region=document.createElement('div');region.className='bf-graphic bf-insight bf-comparison';region.tabIndex=0;region.setAttribute('role','region');region.setAttribute('aria-label',kind==='kalman'?(zh?'卡爾曼增益與加權平均值':'Kalman gain and weighted mean'):(zh?'粒子重採樣前後平均值':'Particle mean before and after resampling'));
const s=E('svg');s.dataset.bfComparison=kind;region.append(s);const note=document.createElement('p');note.className='bf-insight-summary';note.setAttribute('aria-live','polite');panel.querySelector('.bf-output').before(region,note);
const inputs=[...panel.querySelectorAll('.bf-ranges input')],output=panel.querySelector('.bf-output');const update=()=>{const a=inputs.map(i=>Number(i.value)),phase=Number(panel.querySelector('.bf-step').value),z=kind==='kalman'?kalman(s,a,phase,zh):particle(s,a,phase,zh);
if(kind==='kalman')note.textContent=phase===0?(zh?'只有預測平均值；尚未使用觀測。':'Prediction only: no observation used yet.'):phase===1?(zh?'增益 K = '+z.K.toFixed(3)+'；權重相加為 1，尚未顯示後驗。':'Gain K = '+z.K.toFixed(3)+'; weights sum to one. Posterior not yet revealed.'):(zh?'後驗平均值 '+z.mu.toFixed(3)+' = (1−K)×3 + K×y；後驗變異數 '+z.variance.toFixed(3)+'。':'Posterior mean '+z.mu.toFixed(3)+' = (1−K)×3 + K×y; variance '+z.variance.toFixed(3)+'.');
else note.textContent=phase===0?(zh?'只有預測粒子；尚未進行觀測加權。':'Predicted particles only; no observation weighting yet.'):phase<3?(zh?'加權平均值 '+z.weighted.toFixed(3)+'；重採樣結果尚未揭露。':'Weighted mean '+z.weighted.toFixed(3)+'; resampling not yet revealed.'):(zh?'加權平均值 '+z.weighted.toFixed(3)+'，重採樣平均值 '+z.sample.toFixed(3)+'；差值 '+z.shift.toFixed(3)+' 是人工抽樣的有限樣本差異。':'Weighted mean '+z.weighted.toFixed(3)+', resampled mean '+z.sample.toFixed(3)+'; difference '+z.shift.toFixed(3)+' is finite-sample variation in this illustrative draw.');};
new MutationObserver(update).observe(output,{childList:true});host.addEventListener('input',update);update();}
const enhance=()=>document.querySelectorAll('.bayesian-filter-lab[data-lab]').forEach(init);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();
