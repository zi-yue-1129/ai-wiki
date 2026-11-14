/* Original CC BY-SA 4.0 instructional calculations: NT-Xent and additive-alignment context. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const labels = {
    en: {previous:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',step:'Step',temperature:'Temperature τ',positive:'Positive similarity',loss:'NT-Xent loss',probability:'Positive softmax weight',target:'Target step',source:'Biased source',bias:'Score bias',context:'Context vector',sum:'Weight sum',note:'Synthetic arithmetic, not trained embeddings, translation, or measurements.',sim:'NT-Xent candidate probabilities',att:'Alignment weights and context',share:'Softmax share',weight:'Weight',frame:'Decoder step'},
    'zh-TW': {previous:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',step:'步驟',temperature:'溫度 τ',positive:'正樣本相似度',loss:'NT-Xent 損失',probability:'正樣本 Softmax 權重',target:'解碼步驟',source:'加權偏置來源',bias:'分數偏置',context:'脈絡向量',sum:'權重總和',note:'人工算例，非訓練嵌入、真實翻譯或實測結果。',sim:'NT-Xent 候選樣本機率',att:'對齊權重與脈絡向量',share:'Softmax 比例',weight:'權重',frame:'解碼步驟'}
  };
  const baseAlignment = [[.65,.20,.10,.05],[.08,.72,.12,.08],[.05,.15,.20,.60]];
  const annotations = [[.3,.8],[.9,.2],[.2,-.4],[-.7,.5]];
  const temperatures = [1.2,1,.8,.6,.4,.2];
  const colors = ['#0b878e','#df8b59','#597aa8','#8b7db8','#a0aab3'];
  const fix = x => Number(x).toFixed(3);
  const node = (name, attributes={}, content='') => {
    const el = document.createElementNS(NS,name);
    Object.entries(attributes).forEach(([k,v])=>el.setAttribute(k,String(v)));
    if (content!==undefined) el.textContent=String(content);
    return el;
  };
  const svgText=(svg,x,y,value,opts={})=>svg.append(node('text',{x,y,'font-size':13,'font-family':'system-ui, sans-serif',fill:'#2b3d50',...opts},value));
  const div = (className,text='')=>{const e=document.createElement('div');e.className=className;if(text)e.textContent=text;return e;};
  const softmax = scores => {const m=Math.max(...scores);const e=scores.map(v=>Math.exp(v-m));const z=e.reduce((a,b)=>a+b,0);return e.map(v=>v/z);};
  function makeLab(host){
    if(host.dataset.labReady==='true')return;
    const kind=host.dataset.conceptLab;
    if(!['simclr','bahdanau'].includes(kind))return;
    host.dataset.labReady='true';
    const lang=host.dataset.lang==='zh-TW'?'zh-TW':'en', t=labels[lang];
    host.replaceChildren();
    const state={step:0,speed:1,playing:false,timer:null,pos:.8,source:1,bias:0};
    const total=kind==='simclr'?temperatures.length:3;
    const settings=div('cal-inputs'), toolbar=div('cal-toolbar'), output=div('cal-readout');
    const scroll=div('cal-scroll');scroll.tabIndex=0;scroll.setAttribute('role','region');scroll.setAttribute('aria-label',kind==='simclr'?t.sim:t.att);
    const svg=node('svg',{xmlns:NS,viewBox:'0 0 640 300',width:640,height:300,role:'img','aria-label':kind==='simclr'?t.sim:t.att});scroll.append(svg);
    function range(label,min,max,step,value,onChange){
      const wrap=document.createElement('label');wrap.className='cal-field';wrap.append(document.createTextNode(label));
      const input=document.createElement('input');input.type='range';input.min=min;input.max=max;input.step=step;input.value=value;
      input.setAttribute('aria-label',label);
      const val=document.createElement('output');val.textContent=String(value);
      input.addEventListener('input',()=>{val.textContent=input.value;onChange(Number(input.value));render();});
      wrap.append(input,val);settings.append(wrap);return {input,val};
    }
    const btn=(word,fn)=>{const b=document.createElement('button');b.type='button';b.textContent=word;b.addEventListener('click',fn);toolbar.append(b);return b;};
    const seek=range(t.step,0,total-1,1,0,v=>{state.step=v;pause();});
    let secondary;
    if(kind==='simclr')secondary=range(t.positive,-1,1,.05,.8,v=>state.pos=v);
    else {
      const select=document.createElement('select');select.setAttribute('aria-label',t.source);
      for(let i=0;i<4;i++){const option=document.createElement('option');option.value=i;option.textContent='h'+(i+1);select.append(option);}select.value=1;
      const wrap=document.createElement('label');wrap.className='cal-field';wrap.append(t.source,select);settings.append(wrap);
      select.addEventListener('change',()=>{state.source=Number(select.value);render();});
      secondary=range(t.bias,-2,2,.25,0,v=>state.bias=v);
      secondary.select=select;
    }
    const prev=btn(t.previous,()=>{pause();state.step=Math.max(0,state.step-1);render();});
    const next=btn(t.next,()=>{pause();state.step=Math.min(total-1,state.step+1);render();});
    let play;
    const pause=()=>{if(state.timer!==null)window.clearInterval(state.timer);state.timer=null;state.playing=false;if(play)play.textContent=t.play;};
    const tick=()=>{state.step=(state.step+1)%total;render();};
    const start=()=>{pause();state.playing=true;play.textContent=t.pause;state.timer=window.setInterval(tick,Math.round(1050/state.speed));};
    play=btn(t.play,()=>state.playing?pause():start());
    const speeds=document.createElement('select');speeds.setAttribute('aria-label',t.speed);
    for(const n of [.5,1,2]){const opt=document.createElement('option');opt.value=n;opt.textContent=n+'×';speeds.append(opt);}speeds.value='1';speeds.addEventListener('change',()=>{state.speed=Number(speeds.value);if(state.playing)start();});
    const speedWrap=document.createElement('label');speedWrap.className='cal-speed';speedWrap.append(t.speed,speeds);toolbar.append(speedWrap);
    btn(t.reset,()=>{pause();state.step=0;state.pos=.8;state.source=1;state.bias=0;state.speed=1;seek.input.value=0;secondary.input.value=kind==='simclr'?.8:0;secondary.val.textContent=secondary.input.value;if(secondary.select)secondary.select.value='1';speeds.value='1';render();});
    output.setAttribute('aria-live','polite');output.setAttribute('aria-atomic','true');
    const note=div('cal-note',t.note);
    host.append(settings,toolbar,scroll,output,note);
    const clear=title=>{svg.replaceChildren();svg.append(node('title',{},title),node('rect',{x:0,y:0,width:640,height:300,rx:12,fill:'#f8fafc'}));};
    function drawSimclr(){
      const tau=temperatures[state.step],scores=[state.pos,.4,.1,-.2,-.4];
      const probs=softmax(scores.map(v=>v/tau));const loss=-Math.log(probs[0]);
      clear(t.sim);svgText(svg,22,34,`τ = ${tau.toFixed(2)}    p(+) = ${fix(probs[0])}    L = ${fix(loss)}`,{'font-size':17,'font-weight':700});
      const base=softmax(scores);
      probs.forEach((v,i)=>{
        const x=42+i*116,y=240,h=160*v,baseH=160*base[i];
        svg.append(node('rect',{x,y:y-baseH,width:66,height:baseH,rx:3,fill:'none',stroke:'#a8b7c9','stroke-width':1.5,'stroke-dasharray':'4 4'}));
        svg.append(node('rect',{x,y:y-h,width:66,height:h,rx:3,fill:colors[i]}));
        svgText(svg,x+33,265,i===0?'POS':'N'+i,{'text-anchor':'middle','font-weight':700});
        svgText(svg,x+33,Math.max(59,y-h-9),fix(v),{'text-anchor':'middle','font-size':12});
      });
      output.textContent=`${t.temperature}: ${tau.toFixed(2)} · ${t.probability}: ${fix(probs[0])} · ${t.loss}: ${fix(loss)} · Σp = ${fix(probs.reduce((a,b)=>a+b,0))}`;
    }
    function drawBahdanau(){
      const raw=baseAlignment[state.step].map((v,i)=>Math.log(v)+(i===state.source?state.bias:0));
      const p=softmax(raw),ctx=[0,1].map(k=>p.reduce((sum,v,i)=>sum+v*annotations[i][k],0));
      clear(t.att);svgText(svg,22,32,`${t.frame} ${state.step+1}  ·  c = (${fix(ctx[0])}, ${fix(ctx[1])})`,{'font-size':17,'font-weight':700});
      p.forEach((v,i)=>{
        const y=58+i*45;
        svgText(svg,28,y+17,`h${i+1}`);
        svg.append(node('rect',{x:79,y,width:410,height:23,rx:3,fill:'#e3ebf0'}));
        svg.append(node('rect',{x:79,y,width:410*v,height:23,rx:3,fill:i===state.source?'#dc895f':'#0e868c'}));
        svgText(svg,512,y+17,fix(v),{'font-size':13});
      });
      svg.append(node('line',{x1:30,y1:258,x2:606,y2:258,stroke:'#b9cad4','stroke-width':1.5}));
      svgText(svg,40,281,`Σα = ${fix(p.reduce((a,b)=>a+b,0))}`);
      svgText(svg,290,281,`c₁ = ${fix(ctx[0])}    c₂ = ${fix(ctx[1])}`);
      output.textContent=`${t.frame}: ${state.step+1} · ${t.sum}: ${fix(p.reduce((a,b)=>a+b,0))} · ${t.context}: (${fix(ctx[0])}, ${fix(ctx[1])}) · α = (${p.map(fix).join(', ')})`;
    }
    function render(){seek.input.value=state.step;seek.val.textContent=String(state.step);prev.disabled=state.step===0;next.disabled=state.step===total-1;kind==='simclr'?drawSimclr():drawBahdanau();}
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    host.addEventListener('keydown',e=>{if(e.key==='Escape')pause();});
    render();
  }
  function initialise(){document.querySelectorAll('[data-concept-lab]').forEach(makeLab);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialise,{once:true});else initialise();
  if(window.document$&&typeof window.document$.subscribe==='function')window.document$.subscribe(initialise);
})();
