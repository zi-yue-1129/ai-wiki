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
        ['All accepted', 'Correct 6/8 · positive coverage 4/4 · negative coverage 4/4'],
        ['Selective', 'Correct 5/5 · positive coverage 1/4 · negative coverage 4/4'],
      ],
      zh: [
        ['全部接受', '正確 6/8 · 正類別覆蓋 4/4 · 負類別覆蓋 4/4'],
        ['選擇性接受', '正確 5/5 · 正類別覆蓋 1/4 · 負類別覆蓋 4/4'],
      ],
    },
  };
  const blocked = new Set(['script', 'foreignObject', 'iframe', 'image', 'use']);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

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
      note.className = 'concept-motion-chapter-note'; note.setAttribute('aria-live', 'polite');
      const calculation = document.createElement('span');
      calculation.className = 'concept-motion-calculation'; calculation.setAttribute('aria-live', 'off');
      const status = document.createElement('span');
      status.className = 'concept-motion-status'; status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      host.append(controls, note, calculation, status);

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
        sync(); status.textContent = lang[stopIndex()][0];
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
