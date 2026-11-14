/* Original, deterministic teaching labs: no model inference, network requests or external assets. */
(() => {
  'use strict';
  const translations = {
    en: {
      previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset',
      speed: 'Speed', step: 'Step', signal: 'Signal retention', factor: 'Downsampling factor',
      clean: 'Clean video', noisy: 'Noised video', latent: 'Latent state', source: 'Input',
      output: 'Decoded', waiting: 'Pending', mse: 'Reconstruction MSE',
      energy: 'Noise RMS', sample: 'Latent cells', ratio: 'Spatial cell ratio',
      noteVideo: 'Artificial video and fixed noise; this is the forward noising equation, not a learned reverse sampler.',
      noteLatent: 'Block averaging and toy latent interpolation, not a trained autoencoder or denoiser. Decode only at the final stage.',
      videoLabel: 'Four synthetic video frames, clean and forward-noised with the same signal-retention parameter.',
      latentLabel: 'Synthetic image, compressed latent-grid interpolation and end-only decoding.',
      statusVideo: (step, a, rms) => `Step ${step + 1} of 10. Signal retention ${a.toFixed(2)}. Injected noise RMS ${rms.toFixed(3)}.`,
      statusLatent: (step, f, mse) => `Step ${step + 1} of 9. Downsampling factor ${f}. ${step === 8 ? `Decoded reconstruction MSE ${mse.toFixed(4)}.` : 'Decoder has not run.'}`
    },
    'zh-TW': {
      previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設',
      speed: '播放速度', step: '步驟', signal: '訊號保留率', factor: '空間降採樣倍數',
      clean: '乾淨影片', noisy: '加雜訊影片', latent: '潛在狀態', source: '輸入',
      output: '解碼後', waiting: '尚未解碼', mse: '重建均方誤差',
      energy: '雜訊 RMS', sample: '潛在格數', ratio: '空間格數比',
      noteVideo: '固定人造影片與雜訊；此處計算前向加雜訊公式，不代表訓練後模型的反向採樣。',
      noteLatent: '使用區塊平均與人工潛在插值，而非訓練過的自編碼器或去噪器；只在最後階段執行解碼。',
      videoLabel: '四個人造影片影格：乾淨版本以及共用同一訊號保留參數的前向加雜訊版本。',
      latentLabel: '人造影像、壓縮潛在網格插值及最後階段的解碼結果。',
      statusVideo: (step, a, rms) => `第 ${step + 1}/10 步，訊號保留率 ${a.toFixed(2)}，加入雜訊的 RMS 為 ${rms.toFixed(3)}。`,
      statusLatent: (step, f, mse) => `第 ${step + 1}/9 步，降採樣倍數 ${f}，${step === 8 ? `重建均方誤差 ${mse.toFixed(4)}。` : '尚未執行解碼。'}`
    }
  };
  const alphas = [.05,.15,.25,.35,.45,.55,.65,.75,.9,1];
  const palette = value => {
    const v = Math.max(0, Math.min(1, (value + .6)/1.7));
    const r = Math.round(24 + 210*v), g=Math.round(43+143*v), b=Math.round(83+70*(1-v));
    return `rgb(${r},${g},${b})`;
  };
  const clamp = (v, low, high) => Math.max(low, Math.min(high, v));
  const seededNoise = (i) => {
    // Fixed Box–Muller Gaussian values, no stochastic trial is claimed.
    let u = ((Math.sin((i + 1)*12.9898)*43758.5453)%1 + 1)%1;
    let v = ((Math.sin((i + 13)*78.233)*24634.6345)%1 + 1)%1;
    return Math.sqrt(-2*Math.log(Math.max(u,1e-8)))*Math.cos(2*Math.PI*v)*.46;
  };
  const cleanVideo = Array.from({length:4}, (_,f) => Array.from({length:96},(_,j) => {
    const x=j%12, y=Math.floor(j/12);
    return .08+.74*Math.exp(-((x-(2+2.35*f))**2+(y-3.7)**2)/3.8)+.08*Math.sin(x*.6+y*.8);
  }));
  const videoNoise = Array.from({length:4},(_,f)=>Array.from({length:96},(_,j)=>seededNoise(f*97+j)));
  const source = Array.from({length:256}, (_,i)=>{
    const x=i%16,y=Math.floor(i/16);
    const a=.65*Math.exp(-((x-5)**2+(y-5)**2)/25);
    const b=.88*Math.exp(-((x-11)**2+(y-10)**2)/14);
    return .12+a+b+.05*Math.sin(x*.6);
  });
  const el = (tag,attrs={},value='')=>{const node=document.createElement(tag);for(const [name,val] of Object.entries(attrs))node.setAttribute(name,String(val));node.textContent=value;return node;};
  const esc = value => String(value).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function grid(vals, cols, x, y, w, h, opacity=1) {
    const rows=vals.length/cols, cw=w/cols,ch=h/rows;
    return `<g opacity="${opacity}">${vals.map((v,i)=>`<rect x="${(x+(i%cols)*cw).toFixed(2)}" y="${(y+Math.floor(i/cols)*ch).toFixed(2)}" width="${(cw+.035).toFixed(2)}" height="${(ch+.035).toFixed(2)}" fill="${palette(v)}"/>`).join('')}</g>`;
  }
  const background = `<rect width="760" height="288" rx="14" fill="#f5f8fc"/><path d="M20 44 H740" stroke="#d8e2ee"/>`;
  function videoRender(svg, step, tr, metrics) {
    const alpha=alphas[step];
    let rms=0,n=0;
    let picture=background+`<text class="dpl-title" x="22" y="29">Video · x<tspan baseline-shift="sub" font-size="11">t</tspan></text><text class="dpl-small" x="604" y="29">ᾱ = ${alpha.toFixed(2)}</text>`;
    picture+=`<text class="dpl-caption" x="24" y="65">x₀ · Clean</text><text class="dpl-caption" x="24" y="169">xₜ · Noisy</text>`;
    for (let f=0;f<4;f++) {
      const x=126+f*153;
      const noisy=cleanVideo[f].map((z,j)=>{
        const injected=Math.sqrt(1-alpha)*videoNoise[f][j]; rms+=injected*injected;n++;
        return Math.sqrt(alpha)*z+injected;
      });
      picture+=`<g><rect x="${x-4}" y="74" width="130" height="86" rx="6" fill="#d5e1eb"/>${grid(cleanVideo[f],12,x,78,122,78)}<rect x="${x-4}" y="180" width="130" height="86" rx="6" fill="#d5e1eb"/>${grid(noisy,12,x,184,122,78)}<text x="${x+59}" y="281" text-anchor="middle" class="dpl-small">F${f+1}</text></g>`;
    }
    rms=Math.sqrt(rms/n);
    svg.innerHTML=picture;
    metrics.innerHTML=`<span>ᾱ <strong>${alpha.toFixed(2)}</strong></span><span>${esc(tr.energy)} <strong>${rms.toFixed(3)}</strong></span><span>4 × 12 × 8</span>`;
    return {a:alpha,rms};
  }
  const compress = f => {
    let z=[];
    for(let y=0;y<16;y+=f)for(let x=0;x<16;x+=f){
      let sum=0;
      for(let yy=0;yy<f;yy++)for(let xx=0;xx<f;xx++)sum+=source[(y+yy)*16+x+xx];
      z.push(sum/(f*f));
    }
    return z;
  };
  const decode = (z, f) => Array.from({length:256}, (_,i)=>z[Math.floor(i/16/f)*(16/f)+Math.floor(i%16/f)]);
  function latentRender(svg,step,f,tr,metrics) {
    const z=compress(f),cols=16/f, p=step/8;
    const zNoise=z.map((x,i)=>p*x+(1-p)*seededNoise(i+913));
    const decoded=decode(z,f);
    const mse=decoded.reduce((s,v,i)=>s+(v-source[i])**2,0)/256;
    let picture=background+`<text class="dpl-title" x="22" y="29">Latent · z<tspan baseline-shift="sub" font-size="11">t</tspan></text><text class="dpl-small" x="613" y="29">f = ${f} · ${step}/8</text>`;
    picture+=`<text class="dpl-caption" x="46" y="69">x</text><text class="dpl-caption" x="337" y="69">zₜ</text><text class="dpl-caption" x="638" y="69">D(z₀)</text>`;
    picture+=grid(source,16,22,82,176,176);
    picture+=`<path d="M211 171 H267 M257 163 L267 171 L257 179" stroke="#7a8ea5" stroke-width="2.7" fill="none"/>`;
    picture+=`<rect x="298" y="82" width="176" height="176" rx="4" fill="#e4edf5"/>${grid(zNoise,cols,298,82,176,176)}`;
    picture+=`<path d="M485 171 H541 M531 163 L541 171 L531 179" stroke="#7a8ea5" stroke-width="2.7" fill="none"/>`;
    picture+=`<rect x="554" y="82" width="176" height="176" rx="4" fill="#e4edf5"/>`;
    if (step===8) picture+=grid(decoded,16,554,82,176,176);
    else picture+=`<text x="642" y="178" text-anchor="middle" class="dpl-wait">Pending</text>`;
    svg.innerHTML=picture;
    metrics.innerHTML=`<span>${esc(tr.sample)} <strong>${z.length}</strong></span><span>${esc(tr.ratio)} <strong>${f*f}:1</strong></span><span>${esc(tr.mse)} <strong>${step===8?mse.toFixed(4):'—'}</strong></span>`;
    return {mse};
  }
  function enhance(root) {
    if(root.dataset.dplReady) return;
    const kind=root.getAttribute('data-diffusion-lab');
    if (!['video','latent'].includes(kind))return;
    const tr=translations[root.getAttribute('data-lang')]||translations.en;
    const max=kind==='video'?9:8;
    const state={step:0,f:4,speed:1,timer:null};
    root.dataset.dplReady='yes';
    root.classList.add('dpl');
    root.innerHTML=`<div class="dpl-toolbar"><button type="button" data-action="previous">${tr.previous}</button><button type="button" data-action="toggle">${tr.play}</button><button type="button" data-action="next">${tr.next}</button><label>${tr.step} <input type="range" data-role="seek" min="0" max="${max}" step="1" value="0"><output data-role="step-out">0/${max}</output></label><label>${tr.speed} <select data-role="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-action="reset">${tr.reset}</button></div>
    <div class="dpl-params">${kind==='video'?`<label>${tr.signal} ᾱ <input type="range" data-role="alpha" min="0" max="9" step="1" value="0"><output data-role="alpha-out">0.05</output></label>`:`<label>${tr.factor} f <select data-role="factor"><option value="1">1</option><option value="2">2</option><option value="4" selected>4</option><option value="8">8</option></select></label>`}</div>
    <div class="dpl-canvas" tabindex="0" role="region" aria-label="${esc(kind==='video'?tr.videoLabel:tr.latentLabel)}"><svg data-role="svg" viewBox="0 0 760 288" role="img" aria-label="${esc(kind==='video'?tr.videoLabel:tr.latentLabel)}"></svg></div><div class="dpl-metrics" data-role="metrics"></div><p class="dpl-note">${kind==='video'?tr.noteVideo:tr.noteLatent}</p><p class="dpl-live" data-role="status" role="status" aria-live="polite" aria-atomic="true"></p>`;
    const find=sel=>root.querySelector(sel);
    const button=name=>find(`[data-action="${name}"]`);
    const seek=find('[data-role="seek"]');
    const stop=()=>{if(state.timer!==null)window.clearInterval(state.timer);state.timer=null;button('toggle').textContent=tr.play;};
    const render=()=>{
      seek.value=String(state.step);
      find('[data-role="step-out"]').textContent=`${state.step}/${max}`;
      const result = kind === 'video'
        ? videoRender(find('[data-role="svg"]'), state.step, tr, find('[data-role="metrics"]'))
        : latentRender(find('[data-role="svg"]'), state.step, state.f, tr, find('[data-role="metrics"]'));
      if (kind==='video'){find('[data-role="alpha"]').value=String(state.step);find('[data-role="alpha-out"]').textContent=result.a.toFixed(2);}
      find('[data-role="status"]').textContent=kind==='video'?tr.statusVideo(state.step,result.a,result.rms):tr.statusLatent(state.step,state.f,result.mse);
      if(state.step===max&&state.timer!==null)stop();
    };
    const move=delta=>{state.step=clamp(state.step+delta,0,max);render();};
    button('previous').addEventListener('click',()=>{stop();move(-1);});
    button('next').addEventListener('click',()=>{stop();move(1);});
    button('reset').addEventListener('click',()=>{stop();state.step=0;state.f=4;state.speed=1;find('[data-role="speed"]').value='1';if(kind==='latent')find('[data-role="factor"]').value='4';render();});
    button('toggle').addEventListener('click',()=>{
      if(state.timer!==null){stop();return;}
      if(state.step===max)state.step=0;
      if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){render();return;}
      button('toggle').textContent=tr.pause;
      state.timer=window.setInterval(()=>move(1),Math.round(1000/state.speed));
      render();
    });
    seek.addEventListener('input',()=>{stop();state.step=Number(seek.value);render();});
    find('[data-role="speed"]').addEventListener('change',e=>{
      const running=state.timer!==null;
      if(running)stop();state.speed=Number(e.target.value);
      if(running)button('toggle').click();
    });
    if(kind==='video')find('[data-role="alpha"]').addEventListener('input',e=>{stop();state.step=Number(e.target.value);render();});
    else find('[data-role="factor"]').addEventListener('change',e=>{stop();state.f=Number(e.target.value);render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener?.('change',e=>{if(e.matches)stop();});
    render();
  }
  const init=()=>document.querySelectorAll('[data-diffusion-lab]').forEach(enhance);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
  if(window.document$?.subscribe)window.document$.subscribe(init);
})();