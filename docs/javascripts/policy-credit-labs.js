/* Original deterministic REINFORCE / GRPO instructional labs. No external data or scripts. */
(() => {
  'use strict';
  const M = window.PolicyCreditMath;
  const active = new Map();
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const words = {
    en: { reward:'Final-step reward r₂', gamma:'Discount γ', baseline:'Baseline b', fourth:'Reward D', second:'Reward B', same:'Equal rewards (zero variance)', raw:'Rewards', credit:'Reward-to-go', advantage:'Advantage weight', mean:'Group mean', std:'Population SD', status:'Stage', prev:'Previous', next:'Next', play:'Play', pause:'Pause', reset:'Reset', speed:'Speed', initial:'Episode', returns:'Discounted returns', weights:'Centred return factors', group:'Group rewards', centered:'Centered rewards', normalized:'Normalised advantages', zero:'All rewards are equal: σ=0, so standardisation is undefined. For display only, all advantages are shown as 0.', artificial:'Synthetic arithmetic only; not a policy gradient vector, model training or measured output.', caption:'Numbers on bars are illustrative; a weight is not a gradient direction.' },
    zh: { reward:'最後一步獎勵 r₂', gamma:'折扣率 γ', baseline:'基線 b', fourth:'答案 D 獎勵', second:'答案 B 獎勵', same:'全部獎勵相同（零變異）', raw:'獎勵', credit:'折扣回報', advantage:'優勢權重', mean:'組內平均', std:'母體標準差', status:'階段', prev:'上一步', next:'下一步', play:'播放', pause:'暫停', reset:'重設', speed:'播放速度', initial:'回合', returns:'折扣回報', weights:'中心化回報因子', group:'群組獎勵', centered:'中心化獎勵', normalized:'標準化優勢', zero:'所有獎勵相同，σ=0，標準化沒有定義。畫面僅將優勢權重設為 0，以防除以零。', artificial:'僅為人工數值示例；非策略梯度向量、模型訓練或實測輸出。', caption:'長條數值為人工示意；加權係數不代表梯度方向。' }
  };
  const n = (tag, cls, value) => { const e=document.createElement(tag); if(cls)e.className=cls; if(value!==undefined)e.textContent=value; return e; };
  const fmt = x => Math.abs(x)<0.0005?'0.000':x.toFixed(3);
  const clamp = (x,a,b)=>Math.max(a,Math.min(b,x));
  const S='http://www.w3.org/2000/svg';
  const el=(tag,attrs,text)=>{const e=document.createElementNS(S,tag);for(const [k,v] of Object.entries(attrs||{}))e.setAttribute(k,String(v));if(text!==undefined)e.textContent=String(text);return e;};
  function init(host) {
    const type=host.dataset.policyLab, L=words[host.dataset.lang==='zh'?'zh':'en'];
    if(!['reinforce','grpo'].includes(type)||host.dataset.ready)return;
    host.dataset.ready='1';
    let gamma=.8,reward=4,r0=0,r1=0,base=2,ra=1,rb=2,rc=4,rd=5,allEqual=false,step=0,playing=false,raf=0,last=0,progress=0;
    const sliders=[]; let preset;
    const final=type==='reinforce'?2:3;
    const root=n('section','pcl-panel');
    const fields=n('div','pcl-fields'), scroll=n('div','pcl-scroll');
    scroll.setAttribute('role','region');scroll.setAttribute('tabindex','0');
    scroll.setAttribute('aria-label',host.dataset.lang==='zh'?'獎勵與回報圖表，可水平捲動':'Reward and return chart; scroll horizontally');
    const plot=el('svg',{viewBox:'0 0 700 328',width:700,height:328,role:'img','aria-label':host.dataset.lang==='zh'?'人工獎勵與中心化回報示意圖':'Synthetic rewards and centred returns'});
    const read=n('output','pcl-read');read.setAttribute('aria-live','polite');
    const note=n('p','pcl-note',L.artificial);const controls=n('div','pcl-controls');
    const state=n('output','pcl-stage');state.setAttribute('aria-live','off');
    function stop(){playing=false;cancelAnimationFrame(raf);raf=0;last=0;progress=0;updateButtons();}
    function slider(label,min,max,value,inc,assign) {
      const wrap=n('label','pcl-field'),head=n('span','pcl-label'),out=n('output','pcl-num',String(value));
      head.append(n('span','',label),out);
      const inp=n('input');inp.type='range';inp.min=min;inp.max=max;inp.step=inc;inp.value=value;inp.setAttribute('aria-label',label);
      inp.addEventListener('input',()=>{assign(+inp.value);out.textContent=inp.value;stop();render();});
      wrap.append(head,inp);fields.append(wrap);sliders.push({inp,out,assign});
    }
    if(type==='reinforce') {
      slider('r₀',0,5,0,.25,v=>r0=v);slider('r₁',0,5,0,.25,v=>r1=v);slider(L.reward,0,5,4,.25,v=>reward=v);slider(L.gamma,0,1,.8,.05,v=>gamma=v);slider(L.baseline,0,4,2,.05,v=>base=v);
    } else {
      slider(host.dataset.lang==='zh'?'答案 A 獎勵':'Reward A',0,6,1,.25,v=>ra=v);slider(L.second,0,6,2,.25,v=>rb=v);slider(host.dataset.lang==='zh'?'答案 C 獎勵':'Reward C',0,6,4,.25,v=>rc=v);slider(L.fourth,0,6,5,.25,v=>rd=v);
      const wrap=n('label','pcl-check');const input=n('input');input.type='checkbox';input.addEventListener('change',()=>{allEqual=input.checked;stop();render();});wrap.append(input,n('span','',L.same));fields.append(wrap);
    }
    preset=n('select','pcl-preset');
    preset.setAttribute('aria-label',host.dataset.lang==='zh'?'數值範例':'Example preset');
    for(const [value,label] of (type==='reinforce'?
      [['terminal',host.dataset.lang==='zh'?'終端獎勵':'Terminal reward'],['mixed',host.dataset.lang==='zh'?'中途獎勵':'Intermediate reward']]:
      [['terminal','[1, 2, 4, 5]'],['mixed','[1, 3, 0, 2]']])) {
      const option=n('option','',label);option.value=value;preset.append(option);
    }
    preset.addEventListener('change',()=>{
      stop(); step=0; allEqual=false;
      const values=type==='reinforce'?(preset.value==='mixed'?[1,0,2,.9,1.9]:[0,0,4,.8,2]):(preset.value==='mixed'?[1,3,0,2]:[1,2,4,5]);
      sliders.forEach((field,i)=>{field.inp.value=String(values[i]);field.out.textContent=String(values[i]);field.assign(values[i]);});
      const checkbox=fields.querySelector('input[type="checkbox"]');if(checkbox)checkbox.checked=false;
      render();
    });
    fields.prepend(preset);
    const button=(label,symbol,handler)=>{const b=n('button','pcl-btn',symbol);b.type='button';b.setAttribute('aria-label',label);b.addEventListener('click',handler);return b;};
    const previous=button(L.prev,'←',()=>{stop();step=clamp(step-1,0,final);render();});
    const play=button(L.play,'▶',()=>{if(playing){stop();return;}if(reduce.matches)return;if(step===final)step=0;playing=true;last=0;progress=0;raf=requestAnimationFrame(tick);render();});
    const next=button(L.next,'→',()=>{stop();step=clamp(step+1,0,final);render();});
    const reset=button(L.reset,'↺',()=>{stop();step=0;gamma=.8;reward=4;r0=0;r1=0;base=2;ra=1;rb=2;rc=4;rd=5;allEqual=false;preset.value='terminal';fields.querySelectorAll('input[type="range"]').forEach(i=>{const label=i.closest('.pcl-field');const init=i.getAttribute('data-default');i.value=init;label.querySelector('output').textContent=init;});const c=host.querySelector('.pcl-check input');if(c)c.checked=false;seek.value='0';rate.value='1';render();});
    const seek=n('input','pcl-seek');seek.type='range';seek.min='0';seek.max=String(final);seek.step='1';seek.value='0';seek.setAttribute('aria-label',L.status);seek.addEventListener('input',()=>{const target=+seek.value;stop();step=target;render();});
    const rate=n('select','pcl-rate');rate.setAttribute('aria-label',L.speed);
    for(const v of [.5,1,2]){const o=n('option','',`${v}×`);o.value=String(v);if(v===1)o.selected=true;rate.append(o);}
    controls.append(previous,play,next,reset,seek,rate,state);
    fields.querySelectorAll('input[type="range"]').forEach(i=>i.setAttribute('data-default',i.value));
    scroll.append(plot);root.append(fields,scroll,read,controls,note);host.replaceChildren(root);
    function tick(t){if(!host.isConnected){active.get(host)?.();active.delete(host);return;}if(!playing)return;if(last)progress+=(t-last)*Number(rate.value)/950;last=t;
      if(progress>=1){const count=Math.floor(progress);progress-=count;step=clamp(step+count,0,final);render();}
      if(step>=final){stop();return;}raf=requestAnimationFrame(tick);
    }
    function updateButtons(){play.setAttribute('aria-pressed',String(playing));previous.disabled=step===0;next.disabled=step===final;play.disabled=reduce.matches;play.textContent=playing?'Ⅱ':'▶';play.setAttribute('aria-label',playing?L.pause:L.play);seek.value=String(step);state.textContent=`${L.status} ${step}/${final}`;}
    function drawBase(title,labels){
      plot.replaceChildren();plot.append(el('rect',{x:0,y:0,width:700,height:328,rx:14,fill:'#101d32'}));
      plot.append(el('text',{x:28,y:36,fill:'#edf4ff','font-size':17,'font-weight':700},title));
      plot.append(el('line',{x1:40,y1:178,x2:660,y2:178,stroke:'#5c7089','stroke-width':1.5}));
      const xs=labels.length===3?[155,350,545]:[112,270,430,588];
      xs.forEach((x,i)=>plot.append(el('text',{x,y:301,fill:'#c9d6e5','font-size':16,'text-anchor':'middle','font-weight':650},labels[i])));
      return xs;
    }
    function bar(x,amount,scale,color,label,muted){
      const h=Math.abs(amount)*scale,pos=amount>=0,y=pos?178-h:178;
      plot.append(el('rect',{x:x-36,y,width:72,height:h,rx:5,fill:color,opacity:muted?.25:.96}));
      plot.append(el('text',{x,y:pos?y-11:158,fill:muted?'#8c9db5':'#f9fbff','font-size':15,'text-anchor':'middle','font-weight':650},label));
    }
    function render(){
      if(type==='reinforce'){
        const rewards=[r0,r1,reward], gs=M.returns(rewards,gamma), adv=gs.map(v=>v-base);
        const labels=['a₀','a₁','a₂'];const phase=[words.en.initial,words.en.returns,words.en.weights][step];const xs=drawBase(`REINFORCE · ${phase}`,labels);
        const values=step===0?rewards:step===1?gs:adv;const scale=M.scale(values);
        plot.dataset.values=JSON.stringify(values);plot.dataset.scale=String(scale);
        plot.append(el('text',{x:660,y:322,fill:'#8aa2c0','font-size':12,'text-anchor':'end'},`104 px = ${fmt(104/scale)} units`));
        xs.forEach((x,i)=>bar(x,values[i],scale,step===2?(adv[i]>=0?'#2ac5a4':'#ef8a6e'):'#60aaf4',fmt(values[i]),false));
        plot.append(el('text',{x:42,y:322,fill:'#8aa2c0','font-size':12},step===0?'r = [r₀, r₁, r₂]':step===1?'Gₜ = rₜ + γGₜ₊₁':'Centred return: Gₜ − b'));
        read.textContent=`γ=${fmt(gamma)} · G=[${gs.map(fmt).join(', ')}] · G−b=[${adv.map(fmt).join(', ')}]`;
      } else {
        const rewards=allEqual?[3,3,3,3]:[ra,rb,rc,rd];
        const {mean,sigma,centered,advantages:adv}=M.group(rewards);
        const phase=[words.en.group,words.en.group,words.en.centered,words.en.normalized][step];const xs=drawBase(`GRPO · ${phase}`,['A','B','C','D']);
        const values=step<=1?rewards:step===2?centered:adv;const scale=M.scale(values);
        if(step===1)plot.append(el('line',{x1:48,x2:652,y1:178-mean*scale,y2:178-mean*scale,stroke:'#f1be66','stroke-width':2,'stroke-dasharray':'8 6'}));
        plot.dataset.values=JSON.stringify(values);plot.dataset.scale=String(scale);
        plot.append(el('text',{x:660,y:322,fill:'#8aa2c0','font-size':12,'text-anchor':'end'},`104 px = ${fmt(104/scale)} units`));
        xs.forEach((x,i)=>bar(x,values[i],scale,step>=2?(values[i]>=0?'#2ac5a4':'#ef8a6e'):'#60aaf4',fmt(values[i]),false));
        plot.append(el('text',{x:42,y:322,fill:'#8aa2c0','font-size':12},step===2?'rᵢ − μ':step===3?'(rᵢ − μ)/σ':(allEqual?'r = [3, 3, 3, 3]':'r = [A, B, C, D]')));
        read.textContent=`μ=${fmt(mean)} · σ=${fmt(sigma)} · A=[${adv.map(fmt).join(', ')}]${sigma===0?' · '+L.zero:''}`;
      }
      updateButtons();
    }
    const onReduce=()=>{if(reduce.matches)stop();else updateButtons();};
    const onVisibility=()=>{if(document.hidden)stop();};
    reduce.addEventListener('change',onReduce);
    document.addEventListener('visibilitychange',onVisibility);
    active.set(host,()=>{stop();reduce.removeEventListener('change',onReduce);document.removeEventListener('visibilitychange',onVisibility);delete host.dataset.ready;});
    render();
  }
  function scan(){for(const [host,cleanup] of active){if(!host.isConnected){cleanup();active.delete(host);}}document.querySelectorAll('[data-policy-lab]').forEach(init);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
  if(typeof document$!=='undefined'&&document$.subscribe)document$.subscribe(scan);
})();