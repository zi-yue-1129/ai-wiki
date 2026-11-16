/* Original, synthetic sharpness-geometry labs. The SVG and values are calculated together. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  const lang = {
    en: {
      radius: 'Perturbation radius ρ', scale: 'Coordinate scale a', offset: 'Coordinate displacement Δu',
      step: 'Next step', reset: 'Reset', play: 'Play', pause: 'Pause', speed: 'Speed',
      scroll: 'Computed loss geometry. Focus this diagram and scroll horizontally on narrow screens.',
      radiusAria: 'Two quadratic losses and their different rises at the same perturbation radius',
      reparamAria: 'The same objective drawn in original and rescaled coordinates',
      note: 'Constructed quadratic examples; not empirical model accuracy or measured landscape.',
      radiusDetail: 'Common radius', reparamDetail: 'Equal coordinate offsets do not imply equal physical displacements.',
      reduce: 'Reduced motion: autoplay disabled; sliders and step remain available.'
    },
    zh: {
      radius: '共同擾動半徑 ρ', scale: '座標縮放 a', offset: '新座標位移 Δu',
      step: '下一步', reset: '重設', play: '播放', pause: '暫停', speed: '速度',
      scroll: '依公式計算的損失地形；可聚焦此圖，窄螢幕請水平捲動。',
      radiusAria: '相同擾動半徑下，兩個二次損失函數的增量對照',
      reparamAria: '相同目標函數在原始與重新縮放的座標下呈現不同曲率',
      note: '人工解析式示例，非模型實測準確率或地形量測。',
      radiusDetail: '共同半徑', reparamDetail: '相同座標位移不代表相同的實際參數擾動。',
      reduce: '已啟用減少動態效果：停用自動播放，滑桿與單步操作仍可使用。'
    }
  };
  const html = (tag, cls, value) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (value !== undefined) e.textContent = value;
    return e;
  };
  const svg = (tag, attrs={}, value) => {
    const e = document.createElementNS(NS, tag);
    for (const [k,v] of Object.entries(attrs)) e.setAttribute(k, String(v));
    if (value !== undefined) e.textContent = value;
    return e;
  };
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const fmt = n => n.toFixed(3);
  function init(host) {
    const kind = host.dataset.sharpnessLab;
    if (host.dataset.sharpnessReady || !['radius','reparam'].includes(kind)) return;
    host.dataset.sharpnessReady = '1';
    const L = lang[host.dataset.lang === 'zh' ? 'zh' : 'en'];
    const range = kind === 'radius' ? [.1,1,.05] : [.6,1.6,.05];
    let val = kind === 'radius' ? .6 : 1.0;
    let playing = false, raf = 0, last = 0, direction = 1;
    const root = html('section','sgl-panel');
    const controlRow = html('div','sgl-controls');
    const label = html('label','sgl-label',kind === 'radius' ? L.radius : L.scale);
    const slider = html('input','sgl-range');
    slider.type = 'range'; slider.min = String(range[0]);slider.max = String(range[1]);slider.step = String(range[2]);slider.value = String(val);
    slider.setAttribute('aria-label',kind === 'radius' ? L.radius : L.scale);
    const number = html('output','sgl-number'); label.append(slider,number);
    const speed = html('select','sgl-select');speed.setAttribute('aria-label',L.speed);
    [.5,1,2].forEach(n => {const o=html('option','',`${n}×`);o.value=String(n);speed.append(o);});speed.value='1';
    const makeButton=(title,glyph,fn) => { const b=html('button','sgl-btn',glyph);b.type='button';b.setAttribute('aria-label',title);b.addEventListener('click',fn);return b; };
    const play=makeButton(L.play,'▶',()=>{if(playing){stop();return;}if(mq.matches)return;playing=true;last=0;raf=requestAnimationFrame(tick);sync();});
    const step=makeButton(L.step,'→',()=>{stop();set(val+range[2]>range[1]?range[0]:val+range[2]);});
    const reset=makeButton(L.reset,'↺',()=>{stop();direction=1;speed.value='1';set(kind==='radius'?.6:1);});
    controlRow.append(label,play,step,reset,speed);
    const frame=html('div','sgl-scroll');frame.setAttribute('role','region');frame.setAttribute('tabindex','0');frame.setAttribute('aria-label',L.scroll);
    const chart=svg('svg',{viewBox:'0 0 640 300',role:'img','aria-label':kind==='radius'?L.radiusAria:L.reparamAria});frame.append(chart);
    const detail=html('output','sgl-detail');detail.setAttribute('aria-live','polite');
    const notice=html('p','sgl-note',L.note+(mq.matches?' '+L.reduce:''));
    root.append(controlRow,frame,detail,notice);host.append(root);
    const line=(x1,y1,x2,y2,color,width=1.5,dash) => chart.append(svg('line',{x1,y1,x2,y2,stroke:color,'stroke-width':width,...(dash?{'stroke-dasharray':dash}:{})}));
    const rect=(x,y,w,h,fill,rx=8) => chart.append(svg('rect',{x,y,width:w,height:h,fill,rx}));
    const text=(x,y,content,color='#24405a',size=15,anchor='start') => chart.append(svg('text',{x,y,'font-size':size,'text-anchor':anchor,'font-family':'Arial,Helvetica,sans-serif',fill:color},content));
    const curve=(x0,y0,sx,sy,k,domain,color) => {
      let d='';for(let i=0;i<=80;i++){const u=-domain+2*domain*i/80;
        const x=x0+sx*u,y=y0-sy*k*u*u;
        d+=(i===0?'M':'L')+x.toFixed(2)+','+y.toFixed(2)+' ';}
      chart.append(svg('path',{d,fill:'none',stroke:color,'stroke-width':3.2,'stroke-linecap':'round'}));
    };
    function draw(){
      chart.replaceChildren();rect(0,0,640,300,'#f7fafc',12);
      number.textContent=val.toFixed(2);
      if(kind==='radius'){
        const rho=val,flat=.25*rho*rho,sharp=rho*rho;
        rect(18,18,385,262,'#fff',12);rect(415,18,207,262,'#fff',12);
        text(36,46,'Fixed radius', '#17324d',16);text(434,46,'Loss rise','#17324d',16);
        line(48,241,385,241,'#b4c7d8');line(211,70,211,250,'#bacbd8',1.2,'3 5');
        curve(211,241,102,53,.25,1.55,'#08766f');curve(211,241,102,53,1,1.55,'#aa4f2a');
        for(const [k,color] of [[.25,'#08766f'],[1,'#aa4f2a']]){
          const x=211+102*rho,y=241-53*k*rho*rho;
          line(211,241,x,241,color,2,'5 4');line(x,y,x,241,color,1.5,'4 4');
          chart.append(svg('circle',{cx:x,cy:y,r:6,fill:color,stroke:'#fff','stroke-width':2}));
        }
        text(56,266,'Flat · κ=0.5','#08766f',12);text(223,266,'Sharp · κ=2','#aa4f2a',12);
        const base=238;
        rect(441,77,55,161,'#ebf3f7',6);rect(530,77,55,161,'#f8ede7',6);
        rect(441,base-flat*132,55,flat*132,'#08766f',5);rect(530,base-sharp*132,55,sharp*132,'#aa4f2a',5);
        text(468,base-flat*132-8,fmt(flat),'#08766f',13,'middle');text(558,base-sharp*132-8,fmt(sharp),'#b6532c',13,'middle');
        text(469,257,'Flat','#08766f',13,'middle');text(558,257,'Sharp','#aa4f2a',13,'middle');
        detail.textContent=`${L.radiusDetail} ρ=${rho.toFixed(2)}; ΔLflat=${fmt(flat)}; ΔLsharp=${fmt(sharp)}; ratio=4.000`;
      } else {
        const a=val, du=.6, dw=a*du,h=2*a*a,orig=du*du,scaled=a*a*du*du;
        rect(18,18,298,262,'#fff',12);rect(325,18,297,262,'#fff',12);
        text(35,44,'Physical w', '#17324d',16);text(342,44,'Coordinate u', '#17324d',16);
        line(37,244,300,244,'#b4c7d8');line(343,244,603,244,'#b4c7d8');
        line(167,68,167,249,'#bccbd9',1.2,'3 5');line(472,68,472,249,'#bccbd9',1.2,'3 5');
        curve(167,244,94,70,1,1.12,'#08766f');curve(472,244,94,70,a*a,1.12,'#aa4f2a');
        for(const [cx,y0,k,c] of [[167,244,1,'#08766f'],[472,244,a*a,'#aa4f2a']]){
          const x=cx+94*du,y=y0-70*k*du*du;
          line(cx,y0,x,y0,c,2,'5 4');line(x,y,x,y0,c,1.4,'4 4');
          chart.append(svg('circle',{cx:x,cy:y,r:6,fill:c,stroke:'#fff','stroke-width':2}));
        }
        text(35,76,'H = 2.000','#08766f',14);text(342,76,`H = ${fmt(h)}`,'#b6532c',14);
        text(35,265,'Δw = 0.600','#08766f',13);text(342,265,'Δu = 0.600','#b6532c',13);
        detail.textContent=`a=${a.toFixed(2)}; Hessian(w)=2.000; Hessian(u)=${fmt(h)}; Δu=0.600; physical Δw=${fmt(dw)}; ΔL(u)=${fmt(scaled)}`;
      }
      sync();
    }
    function set(n){val=clamp(Number(n),range[0],range[1]);val=Math.round(val/range[2])*range[2];slider.value=String(val);draw();}
    function sync(){detail.setAttribute('aria-live',playing?'off':'polite');play.textContent=playing?'Ⅱ':'▶';play.setAttribute('aria-label',playing?L.pause:L.play);play.disabled=mq.matches;}
    function stop(){playing=false;cancelAnimationFrame(raf);raf=0;last=0;sync();}
    function tick(now){if(!playing)return;if(last){val+=direction*(now-last)*(range[1]-range[0])*Number(speed.value)/5500;
      if(val>=range[1]){val=range[1];direction=-1;}else if(val<=range[0]){val=range[0];direction=1;}
      slider.value=String(val);draw();}last=now;raf=requestAnimationFrame(tick);}
    slider.addEventListener('input',()=>{stop();set(slider.value);});
    mq.addEventListener?.('change',()=>{if(mq.matches)stop();notice.textContent=L.note+(mq.matches?' '+L.reduce:'');sync();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    draw();
  }
  const enhance=()=>document.querySelectorAll('[data-sharpness-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$ && typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
