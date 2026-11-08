/* Bilingual original curiosity probes: deterministic state transitions, not measured experiments. */
(function runCuriosityLabs() {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  // Pixel coordinates in a toy feature space; not observed training outputs.
  const rnd = [
    ['A',170,122,66,213], ['A',170,122,99,183],
    ['A',170,122,140,144], ['A',170,122,165,125],
    ['B',350,125,245,215], ['B',350,125,279,184],
    ['B',350,125,316,150], ['B',350,125,344,129]
  ];
  const outcomes = [[365,101],[310,174],[255,115]];
  const mean = [310,130];
  const errors=outcomes.map(([x,y])=>(x-mean[0])**2+(y-mean[1])**2);
  const expectation=errors.reduce((a,b)=>a+b,0)/3;
  const words={
    en:{prev:'Previous step',next:'Next step',play:'Play',pause:'Pause',seek:'Timeline',speed:'Speed',step:'Step',
      rnd:['Observe A','Train A','Train A','A familiar','Switch to B','Train B','Train B','B familiar'],
      icm:['Repeatable','Repeatable','Repeatable','Sample 1','Sample 2','Sample 3'],
      rndNote:'Illustrative feature coordinates, not measured rewards. A new observation changes both network outputs; only the predictor parameters train.',
      icmNote:'Three equally likely toy outcomes. The forecast equals their conditional mean. Sample error changes; expected MSE is fixed. Not measured data.'},
    zh:{prev:'上一步',next:'下一步',play:'播放',pause:'暫停',seek:'進度',speed:'速度',step:'步驟',
      rnd:['觀測 A','訓練 A','訓練 A','熟悉 A','切換到 B','訓練 B','訓練 B','熟悉 B'],
      icm:['可重複','可重複','可重複','取樣 1','取樣 2','取樣 3'],
      rndNote:'人工設計的特徵座標，不是實測獎勵。不同觀測使兩個網路的輸出改變，只有預測器參數接受訓練。',
      icmNote:'三個等機率示意結果，預測值等於條件平均值；樣本誤差改變，期望均方誤差不變。非模型實測。'}
  };
  const fmt=v=>(v/1000).toFixed(2);
  function svg(kind,n) {
    const isRnd=kind==='rnd', row=rnd[n], stochastic=!isRnd&&n>=3;
    const sampled=stochastic?outcomes[n-3]:mean;
    const tx=isRnd?row[1]:mean[0],ty=isRnd?row[2]:mean[1];
    const px=isRnd?row[3]:mean[0],py=isRnd?row[4]:mean[1];
    const ox=isRnd?tx:sampled[0],oy=isRnd?ty:sampled[1];
    const err=(ox-px)**2+(oy-py)**2, unit=isRnd?21000:5000;
    const width=Math.min(244,244*err/unit);
    const tick=128+Math.min(244,244*(stochastic?expectation:0)/unit);
    const tag=isRnd?'Obs '+row[0]:stochastic?'Stochastic':'Predictable';
    const dots=!isRnd&&stochastic?outcomes.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="16" fill="none" stroke="#319d7a" stroke-dasharray="3 5" opacity="${i===n-3?'.9':'.45'}"/>`).join(''):'';
    const badge=isRnd&&row[0]==='B'?'#fff0db':'#e4f1fa';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 410 340" role="img" aria-label="${tag}: schematic feature-space squared-error comparison">
      <title>${isRnd?'RND fixed target and trained predictor':'ICM sample error and conditional expected error'}</title>
      <desc>Illustrative coordinates; not measured training results.</desc>
      <rect x="1" y="1" width="408" height="338" rx="16" fill="#f7fafc" stroke="#bed0dc"/>
      <rect x="18" y="15" width="150" height="39" rx="11" fill="${badge}"/>
      <text x="31" y="40" font-size="17" font-weight="700" fill="#223d52">${tag}</text>
      <text x="295" y="39" font-size="13" fill="#537084">Feature space</text>
      <path d="M28 70H382M28 70V246" fill="none" stroke="#d3e0e7" stroke-width="1.5"/>
      ${dots}
      <path d="M${px} ${py}L${ox} ${oy}" stroke="#b87932" stroke-dasharray="6 5" stroke-width="3"/>
      <circle cx="${px}" cy="${py}" r="10" fill="#e19748" stroke="#fff" stroke-width="3"/>
      <circle cx="${ox}" cy="${oy}" r="10" fill="#27926e" stroke="#fff" stroke-width="3"/>
      <text x="28" y="263" font-size="12" fill="#9c6b36">● Prediction</text>
      <text x="178" y="263" font-size="12" fill="#167359">● ${isRnd?'Target':'Actual'}</text>
      <text x="28" y="287" font-size="13" fill="#344a5d">Squared gap</text>
      <rect x="128" y="275" width="244" height="12" rx="6" fill="#e0eaf0"/>
      <rect x="128" y="275" width="${width.toFixed(2)}" height="12" rx="6" fill="#d28a3e"/>
      ${isRnd?'':`<path d="M${tick} 270v23" stroke="#775fb0" stroke-width="3"/><text x="28" y="316" font-size="12" fill="#7357a2">Expected</text><text x="112" y="316" font-size="13" fill="#7357a2">${fmt(stochastic?expectation:0)}</text>`}
      <text x="326" y="316" font-size="15" font-weight="700" fill="#8a551c">${fmt(err)}</text>
      </svg>`;
  }
  function enhance(){
    document.querySelectorAll('[data-curiosity-lab]').forEach(host=>{
      if(host.dataset.labReady) return;
      const kind=host.dataset.curiosityLab;
      if(kind!=='rnd'&&kind!=='icm')return;
      host.dataset.labReady='yes';
      host.classList.add('curiosity-lab');
      const L=words[host.dataset.locale==='zh-TW'?'zh':'en'];
      const last=kind==='rnd'?7:5;
      let index=0,timer=0;
      const plot=document.createElement('div');plot.className='curiosity-lab-plot';
      const controls=document.createElement('div');controls.className='curiosity-lab-toolbar';
      const button=(text,cb)=>{const el=document.createElement('button');el.type='button';el.setAttribute('aria-label',text);el.addEventListener('click',cb);return el;};
      const prev=button(L.prev,()=>{stop();set(index-1);});
      const play=button(L.play,()=>{if(timer){stop();return;}if(reduced.matches)return;if(index===last)set(0);start();});
      const next=button(L.next,()=>{stop();set(index+1);});
      const seek=document.createElement('input');Object.assign(seek,{type:'range',min:'0',max:String(last),step:'1',value:'0'});seek.setAttribute('aria-label',L.seek);
      const speed=document.createElement('select');speed.setAttribute('aria-label',L.speed);
      for(const v of [.5,1,2]){const o=document.createElement('option');o.value=String(v);o.textContent=v+'×';if(v===1)o.selected=true;speed.append(o);}
      const status=document.createElement('output');status.className='curiosity-lab-status';status.setAttribute('aria-live','polite');
      const note=document.createElement('p');note.className='curiosity-lab-note';note.textContent=L[kind+'Note'];
      controls.append(prev,play,next,seek,status,speed);host.replaceChildren(plot,controls,note);
      function sync(){prev.textContent='←';next.textContent='→';play.textContent=timer?'Ⅱ':'▶';play.setAttribute('aria-label',timer?L.pause:L.play);play.disabled=reduced.matches;prev.disabled=index===0;next.disabled=index===last;seek.value=String(index);status.textContent=`${L.step} ${index+1}/${last+1} · ${L[kind][index]}`;}
      function set(n){index=Math.min(last,Math.max(0,n));plot.innerHTML=svg(kind,index);sync();}
      function stop(){if(timer){clearInterval(timer);timer=0;}sync();}
      function start(){timer=setInterval(()=>{if(index===last){stop();return;}set(index+1);},900/(+speed.value));sync();}
      seek.addEventListener('input',()=>{const n=+seek.value;stop();set(n);});
      speed.addEventListener('change',()=>{if(timer){stop();start();}});
      reduced.addEventListener?.('change',()=>{if(reduced.matches)stop();sync();});
      document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
      set(0);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();
