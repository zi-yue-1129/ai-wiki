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
  // Three illustrative predictor updates on a repeatable next-state feature.
  // The target is unchanged; only the forecast moves before the stochastic probe.
  const predictable = [[260,165],[289,145],[310,130]];
  const errors=outcomes.map(([x,y])=>(x-mean[0])**2+(y-mean[1])**2);
  const expectation=errors.reduce((a,b)=>a+b,0)/3;
  // A hypothetical distribution: p2=1/3 while p1 and p3 trade mass.
  // All three remain possible for skew in [-60,60].
  function distribution(skew) {
    const weights=[(100+skew)/300,1/3,(100-skew)/300];
    const center=[0,0];
    outcomes.forEach(([x,y],i)=>{center[0]+=weights[i]*x;center[1]+=weights[i]*y;});
    const variance=outcomes.reduce((sum,[x,y],i)=>sum+weights[i]*((x-center[0])**2+(y-center[1])**2),0);
    return {weights,center,variance};
  }
  const words={
    en:{prev:'Previous step',next:'Next step',play:'Play',pause:'Pause',seek:'Timeline',speed:'Speed',step:'Step',
      rnd:['Observe A','Train A','Train A','A familiar','Switch to B','Train B','Train B','B familiar'],
      icm:['Before update','Train forward','Predictable fitted','Sample 1','Sample 2','Sample 3'],
      rndNote:'RND measures predictor error, not a visit count. After A training, a never-seen B can have low error through generalisation. The Transfer slider compares hypothetical B predictions without any parameter update. Coordinates and bonuses are schematic, not measured.',
      icmNote:'For the repeatable outcome, the toy forward prediction fits its fixed target; then three initially equally likely outcomes illustrate residual sample error. Reweight the possible outcomes to move the conditional mean, or shift the prediction away from it to increase expected squared error. Not measured data.',
      sampleTitle:'Sample outcomes',drawOne:'Draw 1',drawMany:'Draw 20',clearSamples:'Reset samples',sampleMean:'Running mean',sampleCount:'Draws',sampleHint:'Independent toy draws: the running mean need not approach the expectation monotonically. The shaded ±1 SE reference is computed from the exact three-outcome loss distribution (not fitted from draws); it shrinks as 1/√n. It is not a 95% confidence interval and does not contain every sample mean. The trace and shade use a fixed y-range for each slider setting, unlike the separate 0–16 marker strip.',sampleNone:'No samples yet',sampleRecent:'Most recent outcomes',sampleCurve:'Running-mean trace',sampleAxis:'Draws',sampleSE:'Analytic SE',
      shift:'Prediction shift',center:'Reset to mean',balance:'Outcome balance',resetBalance:'Equal weights',weights:'P(1/2/3)',expected:'Expected',biasSquared:'Bias²',variance:'Variance',transfer:'Transfer to B',noTransfer:'Reset transfer',bonus:'Squared gap'},
    zh:{prev:'上一步',next:'下一步',play:'播放',pause:'暫停',seek:'進度',speed:'速度',step:'步驟',
      rnd:['觀測 A','訓練 A','訓練 A','熟悉 A','切換到 B','訓練 B','訓練 B','熟悉 B'],
      icm:['更新前','訓練前向模型','已擬合可預測結果','取樣 1','取樣 2','取樣 3'],
      rndNote:'RND 衡量預測誤差，而非造訪次數。訓練 A 後，即使未曾看過 B，泛化也可能使 B 的誤差很低。遷移滑桿比較假設性的 B 預測，不會執行參數更新；座標與獎勵均非實測。',
      icmNote:'可重複轉移的固定目標與前向預測會逐步接近；三個初始等機率結果呈現殘餘樣本誤差。調整結果權重可移動條件平均值；再偏移預測點，可觀察期望平方誤差如何增加。非模型實測。',
      sampleTitle:'重複抽樣',drawOne:'抽取 1 次',drawMany:'抽取 20 次',clearSamples:'重設樣本',sampleMean:'樣本平均',sampleCount:'抽樣次數',sampleHint:'從選定條件分布獨立進行示意抽樣；樣本平均不保證單調接近期望值。淡紫色 ±1 SE 區域是用三種結果的精確損失分布計算的理論標準誤範圍，會依 1/√n 收縮，並非從抽樣估計、95% 信賴區間或每次樣本平均都必須落入的範圍。軌跡與區域的縱軸依滑桿設定固定，與上方 0–16 標記帶不同。',sampleNone:'尚未抽樣',sampleRecent:'最近抽到的結果',sampleCurve:'累積樣本平均軌跡',sampleAxis:'抽樣次數',sampleSE:'解析標準誤',
      shift:'預測位置偏移',center:'回到條件平均值',balance:'結果機率偏重',resetBalance:'恢復等機率',weights:'P(1/2/3)',expected:'期望值',biasSquared:'偏差平方',variance:'變異數',transfer:'對 B 的泛化程度',noTransfer:'重設泛化',bonus:'平方誤差'}
  };
  const fmt=v=>(v/1000).toFixed(2);
  const fmtTerm=v=>(v/1000).toFixed(3);
  function svg(kind,n,zh,bias=0,transfer=0,skew=0) {
    const isRnd=kind==='rnd', row=rnd[n], stochastic=!isRnd&&n>=3;
    const sampled=stochastic?outcomes[n-3]:mean;
    const dist=distribution(skew);
    const tx=isRnd?row[1]:mean[0],ty=isRnd?row[2]:mean[1];
    // Counterfactual predictors after training on A, evaluated on a never-seen B.
    // A stays untouched; B's target is fixed, while a hypothetical predictor
    // can already generalise to B before any B-specific update.
    const factor=isRnd&&n>=4?1-transfer/100:1;
    const px=isRnd?tx+(row[3]-tx)*factor:(stochastic?dist.center[0]+bias:predictable[n][0]);
    const py=isRnd?ty+(row[4]-ty)*factor:(stochastic?dist.center[1]:predictable[n][1]);
    const ox=isRnd?tx:sampled[0],oy=isRnd?ty:sampled[1];
    // Keep the ICM sample and expected-error bar on one fixed scale;
    // 16000 exceeds the largest schematic outcome gap (14700.24) across the
    // allowed probability/forecast sliders, avoiding hidden saturation.
    const err=(ox-px)**2+(oy-py)**2, unit=isRnd?21000:16000;
    const width=Math.min(244,244*err/unit);
    // E[||Y-p||²] = ||E[Y]-p||² + E[||Y-E[Y]||²] for fixed Y distribution.
    // For a deterministic next feature, the conditional variance is zero:
    // expected squared error equals the current sample error before *and* after fitting.
    const conditionalMse=stochastic?dist.variance+bias*bias:err;
    const tick=128+Math.min(244,244*conditionalMse/unit);
    const tag=isRnd?'Obs '+row[0]:stochastic?'Stochastic':'Predictable';
    // Match each outcome, geometric gap and weighted error contribution.
    const outcomeColours=['#267f9f','#319d91','#8672b4'];
    const rays=!isRnd&&stochastic?outcomes.map(([x,y],i)=>
      `<line data-outcome-ray="${i+1}" x1="${x}" y1="${y}" x2="${dist.center[0].toFixed(2)}" y2="${dist.center[1].toFixed(2)}" stroke="${outcomeColours[i]}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="5 5"/>`).join(''):'';
    const dots=!isRnd&&stochastic?outcomes.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="16" fill="none" stroke="${outcomeColours[i]}" stroke-width="${(1+4*dist.weights[i]).toFixed(2)}" stroke-dasharray="3 5" opacity="${i===n-3?'1':'.65'}"/><text x="${x+(i===0?15:-20)}" y="${y-18}" font-size="13" fill="${outcomeColours[i]}">${i+1}</text>`).join(''):'';
    const badge=isRnd&&row[0]==='B'?'#fff0db':'#e4f1fa';
    // Each coloured contribution is p_i * ||Y_i - prediction||². Their
    // sum is the violet expected-error tick, not an average of three
    // equally weighted samples after Outcome balance has been changed.
    const terms=stochastic?outcomes.map(([x,y],i)=>dist.weights[i]*((x-px)**2+(y-py)**2)):[];
    const termScale=344/6000;
    const termBars=stochastic?terms.map((term,i)=>{
      const left=28+terms.slice(0,i).reduce((a,v)=>a+v,0)*termScale;
      return `<rect data-contribution="${i+1}" x="${left.toFixed(2)}" y="370" width="${(term*termScale).toFixed(2)}" height="16" fill="${outcomeColours[i]}"/>`;
    }).join(''):'';
    const termLabels=stochastic?terms.map((term,i)=>`<rect x="${28+i*121}" y="399" width="11" height="11" rx="2" fill="${outcomeColours[i]}"/><text x="${44+i*121}" y="409" font-size="13" fill="#344a5d">${i+1}: ${fmtTerm(term)}</text>`).join(''):'';
    const decompositionScale=344/6000;
    const varianceBar=stochastic?dist.variance*decompositionScale:0;
    const biasBar=stochastic?bias*bias*decompositionScale:0;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 410 ${stochastic?505:340}" role="img" aria-label="${zh ? `特徵空間示意：${tag}，比較平方預測誤差` : `${tag}: schematic feature-space squared-error comparison`}">
      <title>${isRnd?'RND fixed target and trained predictor':'ICM sample error and conditional expected error'}</title>
      <desc>${zh ? "示意座標，非訓練實測結果。" : "Illustrative coordinates; not measured training results."}</desc>
      <rect x="1" y="1" width="408" height="${stochastic?503:338}" rx="16" fill="#f7fafc" stroke="#bed0dc"/>
      <rect x="18" y="15" width="150" height="39" rx="11" fill="${badge}"/>
      <text x="31" y="40" font-size="20" font-weight="700" fill="#223d52">${tag}</text>
      <text x="295" y="39" font-size="17" fill="#537084">Feature space</text>
      <path d="M28 70H382M28 70V246" fill="none" stroke="#d3e0e7" stroke-width="1.5"/>
      ${rays}
      ${dots}
      ${stochastic?`<circle cx="${dist.center[0].toFixed(2)}" cy="${dist.center[1].toFixed(2)}" r="17" fill="none" stroke="#775fb0" stroke-width="2" stroke-dasharray="3 4"/>`: ''}
      ${stochastic?`<line data-bias-vector="true" x1="${dist.center[0].toFixed(2)}" y1="${dist.center[1].toFixed(2)}" x2="${px.toFixed(2)}" y2="${py.toFixed(2)}" stroke="#775fb0" stroke-width="4" stroke-linecap="round"/>`:''}
      <path d="M${px} ${py}L${ox} ${oy}" stroke="#b87932" stroke-dasharray="6 5" stroke-width="3"/>
      <circle cx="${px}" cy="${py}" r="10" fill="#e19748" stroke="#fff" stroke-width="3"/>
      ${isRnd&&n>=4&&transfer===100?`<circle cx="${px}" cy="${py}" r="16" fill="none" stroke="#e19748" stroke-width="3"/>`:""}
      <circle cx="${ox}" cy="${oy}" r="10" fill="#27926e" stroke="#fff" stroke-width="3"/>
      <text x="28" y="263" font-size="16" fill="#9c6b36">● Prediction</text>
      <text x="178" y="263" font-size="16" fill="#167359">● ${isRnd?'Target':'Actual'}</text>
      <text x="28" y="287" font-size="16" fill="#344a5d">Squared gap</text>
      <rect x="128" y="275" width="244" height="12" rx="6" fill="#e0eaf0"/>
      <rect x="128" y="275" width="${width.toFixed(2)}" height="12" rx="6" fill="#d28a3e"/>
      ${isRnd?'':`<path d="M${tick} 270v23" stroke="#775fb0" stroke-width="3"/><text x="28" y="316" font-size="16" fill="#7357a2">Expected</text><text x="112" y="316" font-size="15" fill="#7357a2">${fmt(conditionalMse)}</text>`}
      <text x="326" y="316" font-size="17" font-weight="700" fill="#8a551c">${fmt(err)}</text>
      ${stochastic?`<path d="M28 333H382" stroke="#d3e0e7" stroke-width="1.5"/>
      <text x="28" y="355" font-size="15" font-weight="600" fill="#344a5d">Weighted p × gap²</text>
      <text x="327" y="355" font-size="15" font-weight="700" fill="#7357a2">Σ ${fmtTerm(conditionalMse)}</text>
      <rect x="28" y="370" width="344" height="16" rx="3" fill="#e0eaf0"/>
      ${termBars}
      ${termLabels}
      <path d="M28 422H382" stroke="#d3e0e7" stroke-width="1.5"/>
      <text x="28" y="445" font-size="15" font-weight="600" fill="#344a5d">Variance + Bias²</text>
      <text x="327" y="445" font-size="15" font-weight="700" fill="#7357a2">${fmtTerm(conditionalMse)}</text>
      <rect x="28" y="457" width="344" height="16" rx="3" fill="#e0eaf0"/>
      <rect data-mse-variance="true" x="28" y="457" width="${varianceBar.toFixed(2)}" height="16" fill="#775fb0"/>
      <rect data-mse-bias="true" x="${(28+varianceBar).toFixed(2)}" y="457" width="${biasBar.toFixed(2)}" height="16" fill="#e19748"/>
      <text x="28" y="493" font-size="13" fill="#7357a2">Variance ${fmtTerm(dist.variance)}</text>
      <text x="217" y="493" font-size="13" fill="#a66323">Bias² ${fmtTerm(bias*bias)}</text>`:''}
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
      let index=0,timer=0,bias=0,transfer=0,skew=0;
      let sampleSeed=314159,sampleCount=0,sampleSum=0,sampleRecent=[],sampleTrace=[];
      const plot=document.createElement('div');plot.className='curiosity-lab-plot';
      const controls=document.createElement('div');controls.className='curiosity-lab-toolbar';
      const button=(text,cb)=>{const el=document.createElement('button');el.type='button';el.setAttribute('aria-label',text);el.addEventListener('click',cb);return el;};
      const prev=button(L.prev,()=>{stop();set(index-1);});
      const play=button(L.play,()=>{if(timer){stop();return;}if(reduced.matches)return;if(index===last)set(0);start();});
      const next=button(L.next,()=>{stop();set(index+1);});
      const seek=document.createElement('input');Object.assign(seek,{type:'range',min:'0',max:String(last),step:'1',value:'0'});seek.setAttribute('aria-label',L.seek);seek.dataset.timeline='true';
      const speed=document.createElement('select');speed.setAttribute('aria-label',L.speed);
      for(const v of [.5,1,2]){const o=document.createElement('option');o.value=String(v);o.textContent=v+'×';if(v===1)o.selected=true;speed.append(o);}
      const status=document.createElement('output');status.className='curiosity-lab-status';status.setAttribute('aria-live','polite');
      const note=document.createElement('p');note.className='curiosity-lab-note';note.textContent=L[kind+'Note'];
      const biasRow=document.createElement('div');biasRow.className='curiosity-lab-bias';biasRow.hidden=true;
      const biasLabel=document.createElement('label');biasLabel.textContent=L.shift;
      const biasInput=document.createElement('input');Object.assign(biasInput,{type:'range',min:'-40',max:'40',step:'10',value:'0'});
      biasInput.dataset.bias='true';biasInput.setAttribute('aria-label',L.shift);
      biasLabel.append(biasInput);
      const biasValue=document.createElement('output');biasValue.className='curiosity-lab-bias-value';
      const reset=button(L.center,()=>{stop();bias=0;biasInput.value='0';resetSamples();set(index);});reset.textContent=L.center;
      const metrics=document.createElement('output');metrics.className='curiosity-lab-metrics';metrics.setAttribute('aria-live','polite');
      biasRow.append(biasLabel,biasValue,reset,metrics);
      const skewRow=document.createElement('div');skewRow.className='curiosity-lab-bias curiosity-lab-skew';skewRow.hidden=true;
      const skewLabel=document.createElement('label');skewLabel.textContent=L.balance;
      const skewInput=document.createElement('input');Object.assign(skewInput,{type:'range',min:'-60',max:'60',step:'20',value:'0'});
      skewInput.dataset.skew='true';skewInput.setAttribute('aria-label',L.balance);skewLabel.append(skewInput);
      const skewValue=document.createElement('output');skewValue.className='curiosity-lab-bias-value';
      const skewReset=button(L.resetBalance,()=>{stop();skew=0;skewInput.value='0';resetSamples();set(index);});skewReset.textContent=L.resetBalance;
      const skewMetrics=document.createElement('output');skewMetrics.className='curiosity-lab-metrics';skewMetrics.setAttribute('aria-live','polite');
      skewRow.append(skewLabel,skewValue,skewReset,skewMetrics);
      const transferRow=document.createElement('div');transferRow.className='curiosity-lab-bias curiosity-lab-transfer';transferRow.hidden=true;
      const transferLabel=document.createElement('label');transferLabel.textContent=L.transfer;
      const transferInput=document.createElement('input');Object.assign(transferInput,{type:'range',min:'0',max:'100',step:'25',value:'0'});
      transferInput.dataset.transfer='true';transferInput.setAttribute('aria-label',L.transfer);
      transferLabel.append(transferInput);
      const transferValue=document.createElement('output');transferValue.className='curiosity-lab-bias-value';
      const transferReset=button(L.noTransfer,()=>{transfer=0;transferInput.value='0';set(index);});transferReset.textContent=L.noTransfer;
      const transferMetrics=document.createElement('output');transferMetrics.className='curiosity-lab-metrics';transferMetrics.setAttribute('aria-live','polite');
      transferRow.append(transferLabel,transferValue,transferReset,transferMetrics);
      // Monte Carlo probe: independently draw next features from the current
      // hypothetical conditional distribution. Its analytical expectation is
      // not estimated by the sampler; only the orange running mean is sampled.
      const sampleRow=document.createElement('section');sampleRow.className='curiosity-lab-samples';sampleRow.hidden=true;
      sampleRow.setAttribute('role','group');sampleRow.setAttribute('aria-label',L.sampleTitle);
      const sampleTitle=document.createElement('strong');sampleTitle.textContent=L.sampleTitle;
      const sampleActions=document.createElement('div');sampleActions.className='curiosity-lab-sample-actions';
      const drawOne=button(L.drawOne,()=>{stop();drawSamples(1);});drawOne.textContent=L.drawOne;
      const drawMany=button(L.drawMany,()=>{stop();drawSamples(20);});drawMany.textContent=L.drawMany;
      const clear=button(L.clearSamples,()=>{stop();resetSamples();renderSamples();});clear.textContent=L.clearSamples;
      sampleActions.append(drawOne,drawMany,clear);
      const sampleStats=document.createElement('output');sampleStats.className='curiosity-lab-sample-stats';sampleStats.setAttribute('aria-live','polite');
      const sampleTrack=document.createElement('div');sampleTrack.className='curiosity-lab-sample-track';sampleTrack.setAttribute('role','img');
      const expectedMarker=document.createElement('span');expectedMarker.className='curiosity-lab-sample-expected';
      const observedMarker=document.createElement('span');observedMarker.className='curiosity-lab-sample-observed';
      sampleTrack.append(expectedMarker,observedMarker);
      const sampleLegend=document.createElement('div');sampleLegend.className='curiosity-lab-sample-legend';
      sampleLegend.textContent=`${L.expected} · ${L.sampleMean}  |  0 — 16.00`;
      const trajectory=document.createElement('div');trajectory.className='curiosity-lab-sample-trajectory';trajectory.hidden=true;
      const sampleHistory=document.createElement('div');sampleHistory.className='curiosity-lab-sample-history';sampleHistory.setAttribute('aria-label',L.sampleRecent);
      const sampleHint=document.createElement('p');sampleHint.className='curiosity-lab-sample-hint';sampleHint.textContent=L.sampleHint;
      sampleRow.append(sampleTitle,sampleActions,sampleStats,sampleTrack,sampleLegend,trajectory,sampleHistory,sampleHint);
      controls.append(prev,play,next,seek,status,speed);host.replaceChildren(plot,controls,biasRow,skewRow,transferRow,sampleRow,note);
      transferInput.addEventListener('input',()=>{stop();transfer=Number(transferInput.value);set(index);});
      biasInput.addEventListener('input',()=>{stop();bias=Number(biasInput.value);resetSamples();set(index);});
      skewInput.addEventListener('input',()=>{stop();skew=Number(skewInput.value);resetSamples();set(index);});
      function resetSamples(){sampleSeed=314159;sampleCount=0;sampleSum=0;sampleRecent=[];sampleTrace=[];}
      function drawSamples(count){
        if(kind!=='icm'||index<3)return;
        const dist=distribution(skew),prediction=[dist.center[0]+bias,dist.center[1]];
        for(let n=0;n<count;n++){
          // Seeded synthetic draws keep this demonstration reproducible.
          sampleSeed=(Math.imul(1664525,sampleSeed)+1013904223)>>>0;
          const u=sampleSeed/4294967296;
          const outcome=u<dist.weights[0]?0:u<dist.weights[0]+dist.weights[1]?1:2;
          const point=outcomes[outcome];
          sampleSum+=(point[0]-prediction[0])**2+(point[1]-prediction[1])**2;
          sampleCount++;
          sampleRecent.push(outcome+1);
          // Retain only the latest 120 cumulative means to bound DOM and memory.
          sampleTrace.push(sampleSum/(1000*sampleCount));
          if(sampleTrace.length>120)sampleTrace.shift();
          if(sampleRecent.length>12)sampleRecent.shift();
        }
        renderSamples();
      }
      function renderTrajectory(expected){
        trajectory.hidden=sampleCount===0;
        if(!sampleCount){trajectory.replaceChildren();return;}
        // Every point is a *prefix mean*, not an individual sample loss or
        // a parameter-update trajectory. The y-axis bounds depend only on
        // the *possible* losses under this fixed counterfactual setting,
        // never on the observed draws, so successive draws cannot rescale it.
        const dist=distribution(skew),px=dist.center[0]+bias,py=dist.center[1];
        const possible=outcomes.map(([x,y])=>((x-px)**2+(y-py)**2)/1000);
        // Exact SD of *sample loss* under fixed categorical probabilities;
        // the mean of n i.i.d. losses has theoretical SE = SD / sqrt(n).
        // This is a one-SE reference, NOT a confidence interval for ICM.
        const lossSD=Math.sqrt(possible.reduce((sum,loss,i)=>sum+dist.weights[i]*(loss-expected)**2,0));
        const minY=Math.max(0,Math.floor(Math.min(...possible,expected-lossSD)-.4));
        const maxY=Math.max(minY+2,Math.ceil(Math.max(...possible,expected+lossSD)+.4));
        const x0=44,x1=394,y0=122,ySpan=90;
        const xx=i=>x0+(sampleTrace.length>1?i/(sampleTrace.length-1):0)*(x1-x0);
        const yy=v=>y0-(v-minY)/(maxY-minY)*ySpan;
        const points=sampleTrace.map((v,i)=>`${xx(i).toFixed(2)},${yy(v).toFixed(2)}`);
        const expectedY=yy(expected).toFixed(2);
        const latest=points[points.length-1].split(',');
        const start=sampleCount-sampleTrace.length+1;
        const upper=sampleTrace.map((_,i)=>`${xx(i).toFixed(2)},${yy(expected+lossSD/Math.sqrt(start+i)).toFixed(2)}`);
        const lower=sampleTrace.map((_,i)=>`${xx(i).toFixed(2)},${yy(expected-lossSD/Math.sqrt(start+i)).toFixed(2)}`).reverse();
        const oneSE=lossSD/Math.sqrt(sampleCount);
        // Controlled numeric inputs only; no user-supplied markup enters this SVG.
        trajectory.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 410 154" role="img" aria-label="${L.sampleCurve}: ${sampleCount} ${L.sampleAxis}; ${L.sampleMean} ${(sampleSum/(1000*sampleCount)).toFixed(3)}; ${L.expected} ${expected.toFixed(3)}; ${L.sampleSE} ${oneSE.toFixed(3)}">
          <rect x="1" y="1" width="408" height="152" rx="9" fill="#f7fafc" stroke="#ccdae5"/>
          <path d="M44 32H394 M44 77H394 M44 122H394" stroke="#dce7ed" stroke-width="1"/>
          <path d="M44 32V122H394" stroke="#91a9b8" stroke-width="1.4" fill="none"/>
          <text x="34" y="36" text-anchor="end" font-size="12" fill="#496174">${maxY}</text>
          <text x="34" y="81" text-anchor="end" font-size="12" fill="#496174">${Number(((maxY+minY)/2).toFixed(1))}</text>
          <text x="34" y="126" text-anchor="end" font-size="12" fill="#496174">${minY}</text>
          ${sampleTrace.length>1?`<polygon data-sample-se-band="true" points="${upper.concat(lower).join(' ')}" fill="#b8a5da" fill-opacity=".4"/>`:`<line data-sample-se-band="true" x1="44" x2="44" y1="${yy(expected+lossSD).toFixed(2)}" y2="${yy(expected-lossSD).toFixed(2)}" stroke="#b8a5da" stroke-width="7"/>`}
          <line x1="44" y1="${expectedY}" x2="394" y2="${expectedY}" stroke="#775fb0" stroke-width="2" stroke-dasharray="6 4"/>
          <polyline data-sample-means="true" points="${points.join(' ')}" stroke="#b36b25" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" fill="none"/>
          <circle data-sample-latest="true" cx="${latest[0]}" cy="${latest[1]}" r="4.3" fill="#b36b25" stroke="white" stroke-width="1.5"/>
          <line x1="80" y1="15" x2="100" y2="15" stroke="#b36b25" stroke-width="3"/>
          <text x="106" y="19" font-size="13" fill="#7b4818">Mean</text>
          <rect x="155" y="10" width="14" height="10" rx="2" fill="#b8a5da" fill-opacity=".65"/>
          <text x="173" y="19" font-size="12" fill="#654e8d">±1 SE</text>
          <line x1="232" y1="15" x2="252" y2="15" stroke="#775fb0" stroke-dasharray="5 3" stroke-width="2.4"/>
          <text x="258" y="19" font-size="13" fill="#5d448d">Expected</text>
          <text x="44" y="141" font-size="12" fill="#496174" text-anchor="middle">${start}</text>
          ${sampleCount>start?`<text x="394" y="141" font-size="12" fill="#496174" text-anchor="middle">${sampleCount}</text>`:''}
        </svg>`;
        trajectory.dataset.standardError=String(oneSE);
        trajectory.dataset.yMin=String(minY);
        trajectory.dataset.yMax=String(maxY);
        trajectory.dataset.windowStart=String(start);
        trajectory.dataset.totalDraws=String(sampleCount);
      }
      function renderSamples(){
        if(sampleRow.hidden)return;
        const dist=distribution(skew),expected=(dist.variance+bias*bias)/1000;
        const observed=sampleCount?sampleSum/(1000*sampleCount):0;
        expectedMarker.style.left=`${Math.min(100,100*expected/16).toFixed(2)}%`;
        observedMarker.hidden=sampleCount===0;
        if(sampleCount)observedMarker.style.left=`${Math.min(100,100*observed/16).toFixed(2)}%`;
        sampleTrack.setAttribute('aria-label',`${L.expected}: ${expected.toFixed(3)}; ${L.sampleMean}: ${sampleCount?observed.toFixed(3):L.sampleNone}`);
        const losses=outcomes.map(([x,y])=>((x-dist.center[0]-bias)**2+(y-dist.center[1])**2)/1000);
        const lossSD=Math.sqrt(losses.reduce((sum,v,i)=>sum+dist.weights[i]*(v-expected)**2,0));
        sampleStats.textContent=`${L.sampleCount}: ${sampleCount} · ${L.sampleMean}: ${sampleCount?observed.toFixed(3):'—'} · ${L.expected}: ${expected.toFixed(3)} · ${L.sampleSE}: ${sampleCount?(lossSD/Math.sqrt(sampleCount)).toFixed(3):'—'}`;
        clear.disabled=sampleCount===0;
        renderTrajectory(expected);
        sampleHistory.replaceChildren(...sampleRecent.map(i=>{
          const el=document.createElement('span');el.className=`curiosity-lab-sample-chip curiosity-lab-sample-chip-${i}`;
          el.textContent=String(i);return el;
        }));
      }
      function sync(){prev.textContent='←';next.textContent='→';play.textContent=timer?'Ⅱ':'▶';play.setAttribute('aria-label',timer?L.pause:L.play);play.disabled=reduced.matches;prev.disabled=index===0;next.disabled=index===last;seek.value=String(index);status.textContent=`${L.step} ${index+1}/${last+1} · ${L[kind][index]}`;}
      function set(n){
        index=Math.min(last,Math.max(0,n));
        plot.innerHTML=svg(kind,index,host.dataset.locale==='zh-TW',bias,transfer,skew);
        biasRow.hidden=kind!=='icm'||index<3;
        if(!biasRow.hidden){
          biasValue.textContent=`Δx ${bias>0?'+':''}${bias}`;
          reset.disabled=bias===0;
          const d=distribution(skew);
          metrics.textContent=`${L.expected} ${fmt(d.variance+bias*bias)} = ${L.biasSquared} ${fmt(bias*bias)} + ${L.variance} ${fmt(d.variance)}`;
        }
        skewRow.hidden=kind!=='icm'||index<3;
        if(!skewRow.hidden){
          const d=distribution(skew);
          skewValue.textContent=`${skew>0?'+':''}${skew}`;
          skewReset.disabled=skew===0;
          skewMetrics.textContent=`${L.weights}: ${d.weights.map(p=>(p*100).toFixed(1)+'%').join(' / ')}`;
        }
        sampleRow.hidden=kind!=='icm'||index<3;
        if(sampleRow.hidden&&sampleCount)resetSamples();
        if(!sampleRow.hidden)renderSamples();
        transferRow.hidden=kind!=='rnd'||index<4;
        if(!transferRow.hidden){
          transferValue.textContent=`${transfer}%`;
          transferReset.disabled=transfer===0;
          const row=rnd[index], baseError=(row[1]-row[3])**2+(row[2]-row[4])**2;
          transferMetrics.textContent=`${L.bonus}: ${fmt(baseError*(1-transfer/100)**2)}`;
        }
        sync();
      }
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
