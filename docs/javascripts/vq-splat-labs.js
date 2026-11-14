/* Original, deterministic VQ-VAE and alpha-compositing teaching experiments.
 * Values are synthetic. No inference, fitted geometry or gradient training.
 */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const CODES = [[0.20, 0.35], [0.75, 0.35], [0.48, 0.82]];
  const RGB = [[235, 93, 98], [79, 171, 223], [239, 193, 100]];
  const BG = [30, 39, 60];
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const n3 = x => x.toFixed(3);
  const nearest = (x, y) => {
    const d = CODES.map(([a, b]) => (x-a)**2 + (y-b)**2);
    const index = d.indexOf(Math.min(...d));
    return { index, d, error: Math.sqrt(d[index]) };
  };
  const composite = alphas => {
    let t = 1, weights = [];
    for (const a of alphas) { weights.push(t * a); t *= 1-a; }
    const color = BG.map((c, ch) => Math.round(clamp(weights.reduce((v,w,i)=>v+w*RGB[i][ch],0)+t*c,0,255)));
    return { weights, t, color };
  };
  const locales = {
    en: {titleV:'VQ-VAE · nearest-code transition',titleS:'3DGS · front-to-back compositing', x:'Encoder x',y:'Encoder y', alpha:'Opacity',prev:'Previous',next:'Next',play:'Play',pause:'Pause',seek:'Step',speed:'Speed',reset:'Reset',current:'Selected code',error:'Quantisation distance',rest:'Remaining T',output:'Final RGB',partial:'Visible contribution',noteV:'Synthetic 2D codebook; forward assignment only, no learned encoder or straight-through gradient.',noteS:'Synthetic pixel opacities and RGB, not measured colours. At intermediate steps, unprocessed layers are replaced by the background for the preview.', step:'Step', of:'of'},
    zh: {titleV:'VQ-VAE · 最近碼本切換',titleS:'3DGS · 由近至遠 Alpha 合成', x:'編碼器 x',y:'編碼器 y', alpha:'有效不透明度',prev:'上一步',next:'下一步',play:'播放',pause:'暫停',seek:'步驟',speed:'速度',reset:'重設',current:'選中的碼本',error:'量化距離',rest:'剩餘透射率 T',output:'最終 RGB',partial:'已處理圖層貢獻',noteV:'人工二維碼本，僅展示前向離散指派，非模型實際表徵或直通梯度。',noteS:'人工不透明度與 RGB，並非場景實測。中間步驟的預覽會把尚未處理的圖層暫時視為背景。',step:'步驟',of:'／'}
  };
  const svgEl = (tag, attrs={}, label) => {
    const e=document.createElementNS(NS,tag);
    Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,String(v)));
    if(label!==undefined)e.textContent=label;
    return e;
  };
  function setup(root) {
    if (root.dataset.vqSplatReady) return;
    root.dataset.vqSplatReady='1';
    const mode = root.dataset.vqSplatLab;
    const lang = root.dataset.lang === 'zh'?'zh':'en';
    const t = locales[lang];
    const total = mode==='vq'?5:3;
    const defaults = mode==='vq'? [0.82,0.38]:[0.50,0.60,0.80];
    const config = {values:[...defaults],step:0,speed:1,playing:false};
    const fields = defaults.map((val,i)=>{
      const label=mode==='vq'?(i===0?t.x:t.y):`${t.alpha} ${i+1}`;
      const min=mode==='vq'?'0.05':'0', max=mode==='vq'?'0.95':'1',step='0.01';
      return `<label class="vq-splat-field"><span>${label} <output data-value="${i}">${val.toFixed(2)}</output></span><input type="range" data-param="${i}" min="${min}" max="${max}" step="${step}" value="${val}" aria-label="${label}"></label>`;
    }).join('');
    root.classList.add('vq-splat-lab');
    root.innerHTML=`<h4>${mode==='vq'?t.titleV:t.titleS}</h4><div class="vq-splat-params">${fields}</div><div class="vq-splat-scroll" tabindex="0" role="region" aria-label="${mode==='vq'?'Codebook calculation':'Alpha accumulation'}"><svg viewBox="0 0 720 270" role="img" aria-label="${mode==='vq'?'Nearest neighbour and code distances':'Sorted alpha layers and transmittance'}"></svg></div><div class="vq-splat-controls"><button type="button" data-action="prev">${t.prev}</button><button type="button" data-action="play">${t.play}</button><button type="button" data-action="next">${t.next}</button><label>${t.seek} <input type="range" data-action="seek" min="0" max="${total}" value="0" step="1" aria-label="${t.seek}"></label><label>${t.speed} <select data-action="speed" aria-label="${t.speed}"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-action="reset">${t.reset}</button></div><div class="vq-splat-status" role="status" aria-live="polite"></div><p class="vq-splat-note">${mode==='vq'?t.noteV:t.noteS}</p>`;
    const svg=root.querySelector('svg');
    const status=root.querySelector('[role=status]');
    const control=a=>root.querySelector(`[data-action="${a}"]`);
    let timer=null;
    const S=(tag,attrs,label)=>{const el=svgEl(tag,attrs,label);svg.append(el);return el;};
    const txt=(x,y,value,opts={})=>S('text',{x,y,fill:'#23364e','font-size':opts.size||14,'font-family':'system-ui, sans-serif','font-weight':opts.bold?'650':'400',...opts.attr},value);
    function vqView() {
      const [toX,toY]=config.values;
      const x=0.1+(toX-0.1)*config.step/total, y=0.35+(toY-0.35)*config.step/total;
      const {index,d,error}=nearest(x,y);
      const toPoint=([a,b])=>[47+a*270,239-b*195];
      S('rect',{x:25,y:18,width:332,height:231,rx:12,fill:'#f5f8fc',stroke:'#dbe3ed'});
      for(let j=0;j<=4;j++) {const xx=47+j*270/4, yy=239-j*195/4; S('line',{x1:xx,y1:42,x2:xx,y2:239,stroke:'#dfe8ef'}); S('line',{x1:47,y1:yy,x2:317,y2:yy,stroke:'#dfe8ef'});}
      S('line',{x1:47,y1:239,x2:317,y2:239,stroke:'#8296a8'});
      txt(45,37,'Codebook', {bold:true});
      const pal=['#e56f55','#2e9cba','#9b78cc'];
      CODES.forEach((p,i)=>{const [cx,cy]=toPoint(p);S('circle',{cx,cy,r:i===index?16:12,fill:pal[i],stroke:'#fff','stroke-width':3});txt(cx-10,cy-21,`e${i+1}`,{bold:true});});
      const [cx,cy]=toPoint([x,y]),[qx,qy]=toPoint(CODES[index]);
      S('line',{x1:cx,y1:cy,x2:qx,y2:qy,stroke:'#e59c22','stroke-width':3,'stroke-dasharray':'6 5'});
      S('circle',{cx,cy,r:8,fill:'#fff',stroke:'#183b57','stroke-width':3});
      txt(49,261,`zₑ (${x.toFixed(2)}, ${y.toFixed(2)})`,{size:12});
      txt(385,37,'Squared distance', {bold:true});
      d.forEach((v,i)=>{const ypos=77+i*57;txt(385,ypos,`e${i+1}`);S('rect',{x:425,y:ypos-14,width:222,height:18,rx:5,fill:'#e8eef4'});S('rect',{x:425,y:ypos-14,width:Math.max(1,222*clamp(v/1.2,0,1)),height:18,rx:5,fill:pal[i]});txt(657,ypos,n3(v),{size:12});});
      txt(383,243,`zq = e${index+1}  ·  L2 = ${n3(error)}`,{bold:true,size:14});
      status.textContent=`${t.step} ${config.step} ${t.of} ${total} · ${t.current}: e${index+1} · ${t.error}: ${n3(error)}`;
    }
    function splatView() {
      const done=config.step;
      const alphas=config.values;
      let remain=1, w=[0,0,0];
      for(let i=0;i<done;i++){w[i]=remain*alphas[i];remain*=1-alphas[i];}
      const color=BG.map((c,ch)=>Math.round(clamp(w.reduce((s,v,i)=>s+v*RGB[i][ch],0)+remain*c,0,255)));
      txt(24,34,'Front → back', {bold:true});
      let bx=25;
      for(let i=0;i<3;i++){
        const x=25+i*225;
        S('rect',{x,y:58,width:209,height:87,rx:11,fill:i<done?'#edf7f9':'#f2f5f9',stroke:i===done?'#efaf44':'#dae5ec','stroke-width':i===done?2:1});
        S('circle',{cx:x+35,cy:91,r:16,fill:`rgb(${RGB[i].join(',')})`,opacity:i<done?1:0.32});
        txt(x+60,84,`Layer ${i+1}`,{bold:true});
        txt(x+60,112,`α = ${alphas[i].toFixed(2)}`,{size:13});
        txt(x+17,134,`w = ${n3(w[i])}`,{bold:i<done,size:13});
        if(i<2) txt(x+214,105,'→',{bold:true,size:20});
      }
      txt(25,176,'Contributions', {bold:true});
      S('rect',{x:25,y:190,width:520,height:33,rx:6,fill:'#e7ebef'});
      const pal=['#eb5d62','#4fabe0','#efc164'];
      let at=25;
      for(let i=0;i<3;i++){let ww=520*w[i];if(ww>0){S('rect',{x:at,y:190,width:ww,height:33,fill:pal[i]});at+=ww;}}
      S('rect',{x:at,y:190,width:520*remain,height:33,fill:'#26354b'});
      txt(26,245,`T = ${n3(remain)}    ·    Σw = ${n3(1-remain)}`,{size:13});
      txt(570,178,done===3?'Final RGB':'Preview*',{bold:true});
      S('rect',{x:570,y:191,width:122,height:47,rx:7,fill:`rgb(${color.join(',')})`,stroke:'#7d8b9a'});
      txt(568,256,color.join(', '),{size:12});
      status.textContent=`${t.step} ${done} ${t.of} ${total} · ${t.rest}: ${n3(remain)} · ${done===3?t.output:t.partial}: rgb(${color.join(', ')})`;
    }
    function render(){svg.replaceChildren();if(mode==='vq')vqView();else splatView();control('seek').value=String(config.step);control('play').textContent=config.playing?t.pause:t.play;control('play').setAttribute('aria-pressed',String(config.playing));}
    function stop(){if(timer!==null){clearInterval(timer);timer=null;}config.playing=false;render();}
    function setStep(v){config.step=clamp(v,0,total);render();}
    function start(){if(config.playing){stop();return;}if(config.step===total)config.step=0;config.playing=true;render();timer=setInterval(()=>{if(document.hidden){stop();return;}if(config.step===total){stop();return;}setStep(config.step+1);},Math.round(1050/config.speed));}
    for(const input of root.querySelectorAll('[data-param]')) input.addEventListener('input',()=>{const i=Number(input.dataset.param);config.values[i]=Number(input.value);root.querySelector(`[data-value="${i}"]`).textContent=config.values[i].toFixed(2);stop();render();});
    control('prev').addEventListener('click',()=>{stop();setStep(config.step-1);});
    control('next').addEventListener('click',()=>{stop();setStep(config.step+1);});
    control('seek').addEventListener('input',e=>{stop();setStep(Number(e.target.value));});
    control('play').addEventListener('click',start);
    control('speed').addEventListener('change',e=>{const was=config.playing;stop();config.speed=Number(e.target.value);if(was)start();});
    control('reset').addEventListener('click',()=>{stop();config.values=[...defaults];config.step=0;config.speed=1;control('speed').value='1';root.querySelectorAll('[data-param]').forEach((el,i)=>{el.value=String(defaults[i]);root.querySelector(`[data-value="${i}"]`).textContent=defaults[i].toFixed(2);});render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden&&config.playing)stop();});
    render();
  }
  function enhance(){document.querySelectorAll('[data-vq-splat-lab]').forEach(setup);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe) window.document$.subscribe(enhance);
  // Pure reference equations, exposed for deterministic automated regression tests.
  window.__vqSplatMath={nearest,composite};
})();