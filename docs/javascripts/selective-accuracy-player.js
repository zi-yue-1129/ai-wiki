/* Two source-reviewed classification lessons: seek, step and inspect one discrete
 * acceptance mask at a time. The untouched <img> remains the GitHub/no-JS fallback.
 * Loaded before the generic concept-motion enhancer to avoid double controls.
 */
(() => {
  'use strict';
  const lessons = {
    'accuracy-selective-coverage-motion.svg': {
      duration: 12,
      stops: [0, 4, 8],
      en: [
        ['Top 2', 'Accepted 2/6 · correct 2/2 · selective risk 0/2'],
        ['Top 4', 'Accepted 4/6 · correct 3/4 · selective risk 1/4'],
        ['Top 6', 'Accepted 6/6 · correct 4/6 · selective risk 2/6'],
      ],
      zh: [
        ['前 2 筆', '接受 2/6 · 正確 2/2 · 選擇性風險 0/2'],
        ['前 4 筆', '接受 4/6 · 正確 3/4 · 選擇性風險 1/4'],
        ['前 6 筆', '接受 6/6 · 正確 4/6 · 選擇性風險 2/6'],
      ],
    },
    'accuracy-selective-class-coverage-motion.svg': {
      duration: 8,
      stops: [0, 4],
      en: [
        ['All accepted', 'Accepted 8/8 · Correct 6/8 · positive coverage 4/4 · negative coverage 4/4'],
        ['Selective', 'Accepted 5/8 · Correct 5/5 · positive coverage 1/4 · negative coverage 4/4'],
      ],
      zh: [
        ['全部接受', '接受 8/8 · 正確 6/8 · 正類別覆蓋 4/4 · 負類別覆蓋 4/4'],
        ['選擇性接受', '接受 5/8 · 正確 5/5 · 正類別覆蓋 1/4 · 負類別覆蓋 4/4'],
      ],
    },
  };
  const blocked = new Set(['script', 'foreignObject', 'iframe', 'image', 'use']);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  // Linked plots are computed from the schematic examples shown in the main SVG.
  // They highlight the same semantic state, never measured model performance.
  function makeLinkedPlot(filename, zh, chooseStage) {
    const ns = 'http://www.w3.org/2000/svg';
    const node = (tag, attrs = {}, label = '') => {
      const el = document.createElementNS(ns, tag);
      for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
      if (label) el.textContent = label;
      return el;
    };
    const plot = node('svg', {viewBox:'0 0 640 168',
      role:filename === 'accuracy-selective-coverage-motion.svg' ? 'group' : 'img',
      class:'selective-linked-plot'});
    plot.style.cssText = 'display:block;width:100%;max-width:640px;height:auto;margin:10px 0';
    plot.append(node('rect', {x:1,y:1,width:638,height:166,rx:12,
      fill:'#f8fafc',stroke:'#d4deec'}));
    const write = (x,y,label,attrs={}) => plot.append(node('text',
      {x,y,fill:'#526783','font-family':'Arial, sans-serif',
        'font-size':13,...attrs}, label));
    let update;
    if (filename === 'accuracy-selective-coverage-motion.svg') {
      const accepted = [2,4,6], incorrect = [0,1,2];
      const risks = accepted.map((count,i) => incorrect[i] / count);
      const xs = accepted.map(count => 80 + 480 * count / 6);
      const ys = risks.map(risk => 119 - 200 * risk);
      write(24,25,'RISK',{'font-weight':700});
      plot.append(node('path',{d:'M 84 34 V 120 H 588',fill:'none',
        stroke:'#9aacc1','stroke-width':1.5}));
      plot.append(node('polyline',{
        points:xs.map((x,i)=>String(x)+','+String(ys[i])).join(' '),
        fill:'none',stroke:'#087e85','stroke-width':3,
        'stroke-linecap':'round','stroke-linejoin':'round'}));
      const labels = risks.map(risk => String(Math.round(100 * risk)) + '%');
      const coverages = accepted.map(count => String(count) + '/6');
      const stageSelectors = [];
      for (let i=0;i<3;i++) {
        plot.append(node('circle',{cx:xs[i],cy:ys[i],r:5,
          fill:'#087e85'}));
        write(xs[i],ys[i]-20,labels[i],{'text-anchor':'middle',
          'font-size':12,'font-weight':600});
        write(xs[i],144,coverages[i],{'text-anchor':'middle','font-size':12});
        // Invisible pointer targets also support keyboard navigation without
        // altering the original synthetic chart or its fallback image.
        const hit = node('circle', {cx:xs[i],cy:ys[i],r:16,fill:'transparent',
          stroke:'none','stroke-width':3,cursor:'pointer',
          style:'outline:none',
          'data-acceptance-stage':i});
        hit.setAttribute('role', 'button');
        hit.setAttribute('tabindex', '0');
        hit.setAttribute('aria-label', zh
          ? '選擇接受 ' + coverages[i] + '，風險 ' + labels[i]
          : 'Select ' + coverages[i] + ' accepted, risk ' + labels[i]);
        hit.addEventListener('click', () => chooseStage(i));
        hit.addEventListener('keydown', event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault(); chooseStage(i);
          }
        });
        hit.addEventListener('focus', () => hit.setAttribute('stroke', '#193e69'));
        hit.addEventListener('blur', () => hit.setAttribute('stroke', 'none'));
        stageSelectors.push(hit);
        plot.append(hit);
      }
      const cursor = node('circle',{cx:xs[0],cy:ys[0],r:11,
        fill:'none',stroke:'#dc743b','stroke-width':3});
      plot.append(cursor);
      write(476,160,'COVERAGE →',{'font-weight':700,'font-size':12});
      update = index => {
        cursor.setAttribute('cx',xs[index]); cursor.setAttribute('cy',ys[index]);
        stageSelectors.forEach((hit,i) =>
          hit.setAttribute('aria-pressed',String(i===index)));
        plot.setAttribute('aria-label',zh
          ? '風險覆蓋率對照：接受 ' + coverages[index] + '，風險 ' + labels[index] + '，橘色圈標示目前狀態。'
          : 'Risk–coverage comparison: ' + coverages[index] + ' accepted, ' + labels[index] + ' risk. Orange ring marks the current state.');
      };
    } else {
      write(24,26,'CLASS COVERAGE',{'font-weight':700});
      const bars=[];
      for (const [i,label,y] of [[0,'POS',60],[1,'NEG',108]]) {
        write(35,y+18,label,{'font-weight':700,'font-size':14});
        plot.append(node('rect',{x:116,y,width:415,height:24,rx:7,
          fill:'#e5ebf2'}));
        const fill=node('rect',{x:116,y,width:415,height:24,rx:7,
          fill:i===0?'#087e85':'#3c719d'});
        plot.append(fill);
        const value=node('text',{x:545,y:y+18,fill:'#172b4d',
          'font-family':'Arial, sans-serif','font-size':15,
          'font-weight':700},'4/4');
        plot.append(value);
        bars.push({fill,value});
      }
      update = index => {
        const positive=index===0?4:1;
        bars[0].fill.setAttribute('width',String(415*positive/4));
        bars[0].value.textContent=String(positive)+'/4';
        bars[1].fill.setAttribute('width','415');
        bars[1].value.textContent='4/4';
        plot.setAttribute('aria-label',zh
          ? '類別覆蓋率：整體接受 ' + (index===0?'8/8':'5/8') + '，正類別 ' + positive + '/4，負類別 4/4。兩條橫條代表保留比例。'
          : 'Class coverage: ' + (index===0?'8/8':'5/8') + ' accepted, positive ' + positive + '/4, negative 4/4. Two bars show acceptance rates.');
      };
    }
    return {element:plot, update:index => {
      update(index); plot.setAttribute('data-active-stage',String(index));
    }};
  }

  function enhance(root = document) {
    for (const img of root.querySelectorAll('img[data-motion-src]')) {
      if (img.dataset.conceptMotionEnhanced) continue;
      const source = img.dataset.motionSrc;
      const filename = source.split(/[?#]/, 1)[0].split('/').pop();
      const lesson = lessons[filename];
      if (!lesson) continue;
      const url = new URL(source, document.baseURI);
      if (url.origin !== location.origin || !url.pathname.includes('/assets/concept-animations/')) continue;
      const still = img.dataset.stillSrc || img.getAttribute('src');
      const zh = /[\u3400-\u9fff]/.test(img.alt || '');
      const lang = zh ? lesson.zh : lesson.en;
      const label = zh
        ? {play:'播放', pause:'暫停', prev:'上一步', next:'下一步', time:'進度', speed:'速度', loading:'載入動畫中', error:'動畫無法載入，保留靜態比較圖'}
        : {play:'Play', pause:'Pause', prev:'Previous step', next:'Next step', time:'Timeline', speed:'Speed', loading:'Loading animation', error:'Animation unavailable; static comparison retained'};

      const host = document.createElement('span');
      host.className = 'concept-motion-player concept-motion-detailed selective-motion-player';
      img.before(host);
      host.append(img);
      img.dataset.conceptMotionEnhanced = 'yes';
      const controls = document.createElement('span');
      controls.className = 'concept-motion-controls';
      const button = text => {
        const el = document.createElement('button');
        el.type = 'button'; el.className = 'concept-motion-toggle'; el.textContent = text;
        controls.append(el); return el;
      };
      const toggle = button('▶ ' + label.play);
      const prev = button(label.prev);
      const next = button(label.next);
      const timeLabel = document.createElement('label');
      timeLabel.className = 'concept-motion-field';
      timeLabel.textContent = label.time;
      const slider = document.createElement('input');
      slider.type = 'range'; slider.min = '0'; slider.max = String(lesson.duration * 10 - 1);
      slider.step = '1'; slider.value = '0';
      slider.setAttribute('aria-label', label.time);
      timeLabel.append(slider); controls.append(timeLabel);
      const speedLabel = document.createElement('label');
      speedLabel.className = 'concept-motion-field'; speedLabel.textContent = label.speed;
      const speed = document.createElement('select');
      speed.setAttribute('aria-label', label.speed);
      for (const rate of [0.5, 1, 2]) {
        const option = document.createElement('option');
        option.value = String(rate); option.textContent = String(rate) + '×';
        if (rate === 1) option.selected = true;
        speed.append(option);
      }
      speedLabel.append(speed); controls.append(speedLabel);
      const note = document.createElement('span');
      // Announce the arithmetic, not just a generic stage title. Only one
      // live region changes per semantic transition; visual frames stay silent.
      note.className = 'concept-motion-chapter-note'; note.setAttribute('aria-live', 'off');
      const calculation = document.createElement('span');
      calculation.className = 'concept-motion-calculation';
      calculation.setAttribute('aria-live', 'polite');
      calculation.setAttribute('aria-atomic', 'true');
      const status = document.createElement('span');
      status.className = 'concept-motion-status'; status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      host.append(controls, note, calculation, status);

      let linkedPlot = null, plottedIndex = -1;
      let svg = null, current = reduced.matches ? lesson.stops[1] : 0;
      let playing = false, frame = 0, previous = null, pending = null;
      // Pending loads may have several competing handlers; only the last user intent wins.
      let intentVersion = 0;
      const stopIndex = () => {
        let index = 0;
        for (let i = 1; i < lesson.stops.length; i++) if (current >= lesson.stops[i]) index = i;
        return index;
      };
      let announcedIndex = -1;
      const sync = () => {
        const index = stopIndex();
        // Seek the SVG every frame, but announce only actual acceptance changes.
        // Rewriting an aria-live node at 60 Hz floods assistive technology.
        if (index !== announcedIndex) {
          note.textContent = String(index + 1) + '/' + lang.length + ' · ' + lang[index][0];
          calculation.textContent = lang[index][1];
          announcedIndex = index;
        }
        if (linkedPlot && index !== plottedIndex) {
          linkedPlot.update(index); plottedIndex = index;
        }
        slider.value = String(Math.round(current * 10));
        slider.setAttribute('aria-valuetext', lang[index][0] + ', ' + current.toFixed(1) + ' / ' + lesson.duration + ' s');
        prev.disabled = index === 0 && current === 0;
        next.disabled = index === lesson.stops.length - 1;
        toggle.textContent = (playing ? 'Ⅱ ' + label.pause : '▶ ' + label.play);
        toggle.setAttribute('aria-label', playing ? label.pause : label.play);
        if (svg) { svg.pauseAnimations(); svg.setCurrentTime(current); }
      };
      const pause = () => {
        playing = false; previous = null; cancelAnimationFrame(frame); sync();
      };
      // The selected point and the time slider are views of the same state.
      // Invalidate older Play promises before applying the new cutoff.
      const chooseStage = index => {
        ++intentVersion; pause();
        current = lesson.stops[index]; sync();
      };
      const validate = parsed => {
        if (parsed.localName !== 'svg') throw Error('Invalid SVG document');
        for (const node of [parsed, ...parsed.querySelectorAll('*')]) {
          if (blocked.has(node.localName)) throw Error('Unsafe SVG element');
          for (const attr of node.attributes) {
            if (/^on/i.test(attr.name) || /href$/i.test(attr.name)) throw Error('Unsafe SVG attribute');
          }
          if (node.localName === 'style' && /@import|url\s*\(/i.test(node.textContent)) throw Error('External CSS');
        }
      };
      const load = async () => {
        if (svg) return true;
        if (pending) return pending;
        status.textContent = label.loading;
        pending = (async () => {
          try {
            const response = await fetch(url.href, {credentials:'same-origin'});
            if (!response.ok) throw Error('SVG unavailable');
            const doc = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
            if (doc.querySelector('parsererror')) throw Error('Invalid SVG XML');
            validate(doc.documentElement);
            // Source CSS freezes a scene under reduced motion. For this explicit,
            // paused-by-default player, manual seeking must still work.
            for (const node of doc.querySelectorAll('style')) node.remove();
            svg = document.importNode(doc.documentElement, true);
            svg.classList.add('concept-motion-inline');
            svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', img.alt);
            host.insertBefore(svg, img); img.hidden = true;
            linkedPlot = makeLinkedPlot(filename, zh, chooseStage);
            host.insertBefore(linkedPlot.element, controls);
            sync(); status.textContent = '';
            return true;
          } catch (_) {
            img.src = still; img.hidden = false;
            status.textContent = label.error;
            for (const el of [toggle, prev, next, slider, speed]) el.disabled = true;
            return false;
          }
        })();
        return pending;
      };
      const tick = now => {
        if (!playing) return;
        if (!host.isConnected) { pause(); return; }
        if (previous !== null) current = (current + (now - previous) / 1000 * Number(speed.value)) % lesson.duration;
        previous = now; sync(); frame = requestAnimationFrame(tick);
      };
      toggle.addEventListener('click', async () => {
        if (playing) { ++intentVersion; pause(); return; }
        const intent = ++intentVersion;
        if (!(await load()) || intent !== intentVersion) return;
        playing = true; previous = null; sync(); frame = requestAnimationFrame(tick);
      });
      const jump = async delta => {
        const intent = ++intentVersion;
        pause(); if (!(await load()) || intent !== intentVersion) return;
        current = lesson.stops[Math.max(0, Math.min(lesson.stops.length - 1, stopIndex() + delta))];
        // The localized chapter note already announces the accepted set.
        // Keep the role=status region for load/error feedback only, avoiding
        // duplicate (and later stale) screen-reader announcements on stepping.
        sync();
      };
      prev.addEventListener('click', () => { void jump(-1); });
      next.addEventListener('click', () => { void jump(1); });
      slider.addEventListener('input', async () => {
        const target = Number(slider.value) / 10;
        const intent = ++intentVersion;
        pause(); current = target;
        if (!(await load()) || intent !== intentVersion) return;
        sync();
      });
      reduced.addEventListener?.('change', event => {
        if (event.matches) { ++intentVersion; pause(); current = lesson.stops[1]; sync(); }
      });
      sync();
      // Show the same starting acceptance state as the localised trace.
      // No-JavaScript and failed fetch still retain the reviewed comparison image.
      void load();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => enhance());
  else enhance();
  if (typeof window.document$ !== 'undefined' && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => enhance());
  }
})();
