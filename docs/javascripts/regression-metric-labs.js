/* Deterministic, synthetic regression-metric teaching labs; no external resources. */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const NS = 'http://www.w3.org/2000/svg';
  const strings = {
    en: { outlier:'Outlier magnitude d', sweep:'Prediction interpolation k', prev:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',note:'Synthetic values, not model measurements or a training trajectory.',outread:'Four absolute residuals stay at 1. The fifth is d.',rread:'The fixed targets are (1, 2, 3, 4), with mean 2.5 and TSS = 5.',scroll:'Calculated regression metric diagram; focus and scroll horizontally on small screens',reduced:'Automatic playback is disabled by your reduced-motion preference; manual controls remain available.',outaria:'Five residuals, their squared contributions, MAE and RMSE',raria:'Targets, changing predictions, total and residual sums of squares, and R squared'},
    zh: { outlier:'離群殘差 d', sweep:'預測插值參數 k',prev:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',note:'僅為人工構造的示意數值，不是模型實測或訓練軌跡。',outread:'四筆絕對殘差固定為 1，第五筆為 d。',rread:'固定目標為 (1, 2, 3, 4)，平均值為 2.5，TSS = 5。',scroll:'迴歸指標運算圖；可聚焦，窄螢幕請水平捲動',reduced:'系統已啟用減少動態效果，停用自動播放，仍可手動操作。',outaria:'五筆殘差、平方誤差貢獻以及 MAE 與 RMSE',raria:'真實值、預測值、總平方和、殘差平方和以及 R 平方'}
  };
  const elem=(tag,cls,txt)=>{const x=document.createElement(tag);if(cls)x.className=cls;if(txt!==undefined)x.textContent=txt;return x;};
  const svg=(tag,attrs={},txt)=>{const x=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))x.setAttribute(k,String(v));if(txt!==undefined)x.textContent=txt;return x;};
  const fmt=v=>(Math.abs(v)<0.0005?0:v).toFixed(3);
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  function init(host) {
    if(host.dataset.metricReady)return;
    const type=host.dataset.regressionLab;
    if(type!=='outlier'&&type!=='r2')return;
    host.dataset.metricReady='1';
    const L=strings[host.dataset.lang==='zh'?'zh':'en'];
    const min=type==='outlier'?1:0,max=type==='outlier'?6:1.5,inc=type==='outlier'?.1:.05;
    let value=min,direction=1,playing=false,frame=0,last=0;
    const panel=elem('section','rml-panel');
    const inputs=elem('div','rml-inputs'), controls=elem('div','rml-controls');
    const label=elem('label','rml-label',type==='outlier'?L.outlier:L.sweep);
    const seek=elem('input','rml-seek');seek.type='range';seek.min=String(min);seek.max=String(max);seek.step=String(inc);seek.value=String(min);seek.setAttribute('aria-label',type==='outlier'?L.outlier:L.sweep);
    const current=elem('output','rml-number');label.append(seek,current);inputs.append(label);
    const viewport=elem('div','rml-scroll');viewport.tabIndex=0;viewport.setAttribute('role','region');viewport.setAttribute('aria-label',L.scroll);
    const graph=svg('svg',{viewBox:'0 0 680 390',width:'680',height:'390',role:'img','aria-label':type==='outlier'?L.outaria:L.raria});
    viewport.append(graph);
    const detail=elem('output','rml-detail');detail.setAttribute('aria-live','polite');
    const info=elem('p','rml-note',L.note+' '+(type==='outlier'?L.outread:L.rread));
    const button=(text,short,fn)=>{const b=elem('button','rml-button',short);b.type='button';b.setAttribute('aria-label',text);b.addEventListener('click',fn);return b;};
    function stop(){playing=false;cancelAnimationFrame(frame);frame=0;last=0;refreshButtons();}
    function setValue(v){value=clamp(v,min,max);seek.value=String(Math.round(value/inc)*inc);draw();}
    const prev=button(L.prev,'←',()=>{stop();setValue(value-inc);});
    const play=button(L.play,'▶',()=>{if(playing){stop();return;}if(reduced.matches)return;playing=true;last=0;frame=requestAnimationFrame(tick);refreshButtons();});
    const next=button(L.next,'→',()=>{stop();setValue(value+inc);});
    const reset=button(L.reset,'↺',()=>{stop();direction=1;speed.value='1';setValue(min);});
    const speed=elem('select','rml-speed');speed.setAttribute('aria-label',L.speed);
    [.5,1,2].forEach(v=>{const o=elem('option','',`${v}×`);o.value=String(v);if(v===1)o.selected=true;speed.append(o);});
    controls.append(prev,play,next,reset,speed);
    seek.addEventListener('input',()=>{stop();value=Number(seek.value);draw();});
    function tick(ts){if(!playing)return;if(last){value+=direction*(ts-last)*Number(speed.value)*(max-min)/6000;
      if(value>=max){value=max;direction=-1;}else if(value<=min){value=min;direction=1;}
      draw();}last=ts;frame=requestAnimationFrame(tick);}
    function refreshButtons(){prev.disabled=value<=min;next.disabled=value>=max;play.disabled=reduced.matches;play.textContent=playing?'Ⅱ':'▶';play.setAttribute('aria-label',playing?L.pause:L.play);}
    function text(x,y,label,fill='#dce8f5',size=15,anchor='middle'){graph.append(svg('text',{x,y,fill,'font-size':size,'text-anchor':anchor,'font-family':'Arial, sans-serif'},label));}
    function rect(x,y,w,h,fill,round=5){graph.append(svg('rect',{x,y,width:w,height:Math.max(h,1),rx:round,fill}));}
    function draw(){
      // Keep the native slider (including its accessible value) in sync with playback.
      seek.value=String(Math.round(value/inc)*inc);
      graph.replaceChildren();rect(0,0,680,390,'#132238',14);
      current.textContent=Number(value).toFixed(type==='outlier'?1:2);
      if(type==='outlier'){
        const errors=[1,1,1,1,value],mae=(4+value)/5,rmse=Math.sqrt((4+value*value)/5);
        text(28,34,'MAE vs RMSE','#f4f7ff',19,'start');
        graph.append(svg('line',{x1:32,x2:400,y1:245,y2:245,stroke:'#7890ad','stroke-width':1.5}));
        errors.forEach((v,i)=>{const x=58+i*68,h=v*29;rect(x,245-h,38,h,i===4?'#f4ad70':'#65b3e8');text(x+19,266,`e${i+1}`,'#cddbea',13);text(x+19,237-h,fmt(v),'#f2f7fd',13);});
        text(474,277,'MAE','#a9ddff',16);text(589,277,'RMSE','#9be7cc',16);
        const bh=mae*55,rh=rmse*55;
        rect(453,248-bh,43,bh,'#65b3e8');rect(568,248-rh,43,rh,'#4bc2a3');
        text(474,237-bh,fmt(mae),'#dcefff',14);text(589,237-rh,fmt(rmse),'#d7ffed',14);
        // Squaring makes the outlier dominate the RMSE numerator: 4 fixed + d².
        // The common scale of 40 is the largest possible squared-error sum.
        text(30,339,'Σe²','#dce8f5',17,'start');
        rect(105,317,300,22,'#253c56',3);
        const fixedWidth=4/40*300,outlierWidth=value*value/40*300;
        rect(105,317,fixedWidth,22,'#65b3e8',2);
        rect(105+fixedWidth,317,outlierWidth,22,'#f4ad70',2);
        text(435,335,'4 + d²','#bcd4e9',16,'start');
        text(622,335,fmt(4+value*value),'#f4f7ff',16,'end');
        detail.textContent=`d=${fmt(value)} · MAE=(4+d)/5=${fmt(mae)} · RMSE=√((4+d²)/5)=${fmt(rmse)} · RMSE−MAE=${fmt(rmse-mae)}`;
      } else {
        const k=value,ys=[1,2,3,4],pred=ys.map(y=>y+k*(2.5-y)),rss=5*k*k,r2=1-k*k;
        text(28,34,'R² vs Mean','#f4f7ff',19,'start');
        const px=[82,222,362,502],coord=v=>247-(v-.5)*48;
        graph.append(svg('line',{x1:35,x2:554,y1:coord(2.5),y2:coord(2.5),stroke:'#e3b96c','stroke-dasharray':'6 5','stroke-width':2}));
        ys.forEach((y,i)=>{const x=px[i],py=coord(y),qy=coord(pred[i]);
          graph.append(svg('line',{x1:x,y1:py,x2:x,y2:qy,stroke:'#a6c5d5','stroke-width':3}));
          graph.append(svg('circle',{cx:x,cy:py,r:6,fill:'#6bbcf5'}));
          graph.append(svg('circle',{cx:x,cy:qy,r:6,fill:'#f3ad75',stroke:'#f7f5ee','stroke-width':1}));
          text(x,279,`y${i+1}`,'#d6e5f3',13);
        });
        text(575,118,'TSS','#e4c48e',15,'start');text(575,138,'5.000','#e4c48e',15,'start');
        text(575,178,'RSS','#f6b98d',15,'start');text(575,198,fmt(rss),'#f6b98d',15,'start');
        text(575,239,'R²','#a6f0d4',15,'start');text(575,259,fmt(r2),'#a6f0d4',16,'start');
        // Shared scale: equal bar lengths imply RSS=TSS and R²=0.
        const scale=350/11.25,baseX=112,thresholdX=baseX+5*scale;
        text(28,331,'TSS','#e3b96c',15,'start');
        text(28,362,'RSS','#f3ad75',15,'start');
        rect(baseX,314,350,19,'#253c56',3);
        rect(baseX,345,350,19,'#253c56',3);
        rect(baseX,314,5*scale,19,'#e3b96c',3);
        rect(baseX,345,rss*scale,19,'#f3ad75',3);
        graph.append(svg('line',{x1:thresholdX,x2:thresholdX,y1:307,y2:375,stroke:'#dce8f5','stroke-width':1.5,'stroke-dasharray':'3 3'}));
        text(510,330,'Boundary','#cddbea',14,'start');
        text(510,354,'R² = 0','#a6f0d4',14,'start');
        detail.textContent=`k=${fmt(k)} · TSS=5.000 · RSS=${fmt(rss)} · R²=1−RSS/TSS=${fmt(r2)}${r2<0?' · RSS > TSS':''}`;
      }
      refreshButtons();
    }
    panel.append(inputs,viewport,detail,controls,info);host.replaceChildren(panel);
    reduced.addEventListener('change',()=>{if(reduced.matches)stop();else refreshButtons();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    if(reduced.matches)info.append(' '+L.reduced);
    draw();
  }
  function scan(){document.querySelectorAll('[data-regression-lab]').forEach(init);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
  if(typeof document$!=='undefined'&&document$.subscribe)document$.subscribe(scan);
})();