/* Seekable, accessible playback for continuous MAE and DINOv2 process diagrams.
 * Keep the normal <img> as a GitHub/no-JavaScript fallback. Only the two
 * reviewed, same-origin SVG assets are parsed into inline SVG for seeking.
 */
(() => {
  'use strict';
  const timelines = {
    'mae-visible-patch-reconstruction-motion.svg': 14,
    'dinov2-dual-objective-ema-motion.svg': 14,
  };
  // Semantic checkpoints guide readers through a continuous timeline. They do
  // not quantise the SVG into slides: seeking between checkpoints is optional.
  const chapters = {
    'mae-visible-patch-reconstruction-motion.svg': [
      [0, 'Mask', '遮罩', 'Hide twelve of sixteen image patches; four remain visible.', '十六個區塊遮住十二個，只保留四個可見區塊。'],
      [2.8, 'Encode', '編碼', 'Only visible tokens travel into the encoder; no mask tokens are encoded.', '只有可見 token 進入編碼器；遮罩 token 不參與編碼。'],
      [5.6, 'Decode', '解碼', 'Encoded tokens and twelve new mask tokens meet in the decoder.', '編碼後的表徵與十二個新加入的遮罩 token 在解碼器結合。'],
      [8.4, 'Reconstruct', '重建', 'The decoder predicts all sixteen patches, including visible positions.', '解碼器預測全部十六個位置，包含原本可見的區塊。'],
      [11.6, 'Masked loss', '遮罩損失', 'Only the twelve originally hidden patches contribute to reconstruction MSE.', '重建均方誤差只計算原本被遮住的十二個區塊。'],
    ],
    'dinov2-dual-objective-ema-motion.svg': [
      [0, 'Views', '不同視角', 'Student and teacher process augmented views of an image.', '學生與教師分別處理影像的增強視角。'],
      [2.8, 'CLS target', 'CLS 目標', 'Cross-view image-level self-distillation compares class-token outputs.', '跨視角的影像層級自蒸餾比較類別 token 輸出。'],
      [5.6, 'Patch target', '區塊目標', 'Masked student patches match unmasked teacher patch targets.', '學生的遮罩區塊對齊教師未遮罩的區塊目標。'],
      [8.4, 'Student gradient', '學生梯度', 'Both losses backpropagate only through the student, not the teacher.', '兩種損失只對學生反向傳播，不更新教師梯度。'],
      [11.2, 'Teacher EMA', '教師 EMA', 'The teacher follows the updated student via an exponential moving average.', '教師權重透過指數移動平均跟隨更新後的學生權重。'],
    ],
  };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const forbidden = new Set(['script', 'foreignObject', 'iframe', 'image', 'use']);

  function enhance(root = document) {
    for (const img of root.querySelectorAll('img[src*="concept-animations/"]')) {
      if (img.dataset.conceptMotionEnhanced) continue;
      const source = img.getAttribute('src') || '';
      const filename = source.split(/[?#]/, 1)[0].split('/').pop();
      const duration = timelines[filename];
      if (!duration) continue;
      const chapterList = chapters[filename];
      const still = source.replace(/-motion\.svg(?=$|[?#])/, '-still.svg');
      const zh = /[\u3400-\u9fff]/.test(img.alt || '');
      const labels = zh
        ? ['播放', '暫停', '前進 0.7 秒', '進度', '速度', '開啟原尺寸', '動畫載入失敗，顯示靜態圖', '已暫停']
        : ['Play', 'Pause', 'Step +0.7 s', 'Timeline', 'Speed', 'Open full size', 'Animation unavailable; showing still image', 'Paused'];
      img.dataset.conceptMotionEnhanced = 'yes';
      const host = document.createElement('span');
      host.className = 'concept-motion-player concept-motion-detailed';
      img.before(host);
      host.append(img);
      const controls = document.createElement('span');
      controls.className = 'concept-motion-controls';
      const toggle = document.createElement('button');
      const step = document.createElement('button');
      for (const b of [toggle, step]) { b.type = 'button'; b.className = 'concept-motion-toggle'; controls.append(b); }
      step.textContent = labels[2];
      const rangeLabel = document.createElement('label');
      rangeLabel.className = 'concept-motion-field';
      rangeLabel.textContent = labels[3];
      const slider = document.createElement('input');
      slider.type = 'range'; slider.min = '0'; slider.max = String(duration * 10); slider.step = '1'; slider.value = '0';
      slider.setAttribute('aria-label', labels[3]);
      rangeLabel.append(slider); controls.append(rangeLabel);
      const speedLabel = document.createElement('label');
      speedLabel.className = 'concept-motion-field'; speedLabel.textContent = labels[4];
      const speed = document.createElement('select');
      speed.setAttribute('aria-label', labels[4]);
      for (const value of [0.5, 1, 2]) {
        const option = document.createElement('option'); option.value = String(value); option.textContent = `${value}×`;
        if (value === 1) option.selected = true;
        speed.append(option);
      }
      speedLabel.append(speed); controls.append(speedLabel);
      const zoom = document.createElement('a');
      zoom.href = source; zoom.target = '_blank'; zoom.rel = 'noopener noreferrer'; zoom.className = 'concept-motion-zoom';
      zoom.textContent = labels[5]; controls.append(zoom);
      const chapterNav = document.createElement('span');
      chapterNav.className = 'concept-motion-chapter-nav';
      const previousChapter = document.createElement('button');
      const nextChapter = document.createElement('button');
      for (const button of [previousChapter, nextChapter]) {
        button.type = 'button'; button.className = 'concept-motion-chapter-button';
        chapterNav.append(button);
      }
      previousChapter.textContent = zh ? '上一段' : 'Previous phase';
      nextChapter.textContent = zh ? '下一段' : 'Next phase';
      controls.append(chapterNav);
      const chapterNote = document.createElement('span');
      chapterNote.className = 'concept-motion-chapter-note';
      chapterNote.setAttribute('aria-live', 'polite');
      chapterNote.setAttribute('aria-atomic', 'true');
      const status = document.createElement('span');
      status.className = 'concept-motion-status'; status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
      host.append(controls, chapterNote, status);

      let svg = null, current = 0, rate = 1, playing = false, frame = 0, previous = null;
      let pending = null, overridden = false, activeChapter = -1;
      const chapterAt = () => {
        let index = 0;
        for (let i = 1; i < chapterList.length; i++) {
          if (current >= chapterList[i][0]) index = i;
        }
        return index;
      };
      const renderChapter = () => {
        const index = chapterAt();
        if (index !== activeChapter) {
          const entry = chapterList[index];
          const title = zh ? entry[2] : entry[1];
          const detail = zh ? entry[4] : entry[3];
          chapterNote.textContent = `${index + 1}/${chapterList.length} · ${title}: ${detail}`;
          activeChapter = index;
        }
        previousChapter.disabled = index === 0 && current < 0.25;
        nextChapter.disabled = index === chapterList.length - 1;
      };
      const renderTime = () => {
        renderChapter();
        if (svg) { svg.pauseAnimations(); svg.setCurrentTime(current); }
        slider.value = String(Math.round(current * 10));
        slider.setAttribute('aria-valuetext', `${current.toFixed(1)} / ${duration} s`);
      };
      const updateToggle = () => {
        toggle.textContent = playing ? `Ⅱ ${labels[1]}` : `▶ ${labels[0]}`;
        toggle.setAttribute('aria-label', playing ? labels[1] : labels[0]);
      };
      const pause = () => {
        playing = false; previous = null; cancelAnimationFrame(frame); updateToggle();
      };
      const tick = now => {
        if (!playing) return;
        if (previous !== null) current = (current + (now - previous) * rate / 1000) % duration;
        previous = now; renderTime(); frame = requestAnimationFrame(tick);
      };
      const validate = element => {
        if (element.localName !== 'svg') throw Error('Invalid SVG root');
        for (const node of [element, ...element.querySelectorAll('*')]) {
          if (forbidden.has(node.localName)) throw Error('Disallowed SVG element');
          for (const attr of node.attributes) {
            if (/^on/i.test(attr.name) || /href$/i.test(attr.name)) throw Error('Disallowed SVG attribute');
          }
        }
      };
      const load = async () => {
        if (svg) { if (overridden) svg.classList.add('allow-motion'); svg.hidden = false; img.hidden = true; return true; }
        if (pending) return pending;
        pending = (async () => {
          try {
            const response = await fetch(source, { credentials: 'same-origin' });
            if (!response.ok) throw Error('Fetch failed');
            const parsed = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
            const element = parsed.documentElement;
            validate(element);
            svg = document.importNode(element, true);
            svg.classList.add('concept-motion-inline');
            if (overridden) svg.classList.add('allow-motion');
            svg.setAttribute('aria-label', img.alt);
            host.insertBefore(svg, img); img.hidden = true;
            renderTime(); return true;
          } catch (_) {
            img.src = still; img.hidden = false; status.textContent = labels[6];
            toggle.disabled = step.disabled = slider.disabled = speed.disabled = true;
            return false;
          }
        })();
        return pending;
      };
      const play = async () => {
        if (!(await load())) return;
        if (playing) return;
        playing = true; previous = null; updateToggle(); frame = requestAnimationFrame(tick);
      };
      toggle.addEventListener('click', () => {
        overridden = true;
        if (playing) { pause(); status.textContent = labels[7]; }
        else void play();
      });
      step.addEventListener('click', async () => {
        overridden = true; pause(); if (!(await load())) return;
        current = (current + 0.7) % duration; renderTime(); status.textContent = `${current.toFixed(1)} / ${duration} s`;
      });
      slider.addEventListener('input', async () => {
        overridden = true; pause(); current = Number(slider.value) / 10;
        if (!(await load())) return;
        renderTime(); status.textContent = `${current.toFixed(1)} / ${duration} s`;
      });
      const jumpChapter = async direction => {
        overridden = true; pause();
        if (!(await load())) return;
        const index = chapterAt();
        const target = direction < 0
          ? (current > chapterList[index][0] + 0.25 ? index : Math.max(0, index - 1))
          : Math.min(chapterList.length - 1, index + 1);
        current = chapterList[target][0];
        renderTime();
        status.textContent = `${current.toFixed(1)} / ${duration} s`;
      };
      previousChapter.addEventListener('click', () => { void jumpChapter(-1); });
      nextChapter.addEventListener('click', () => { void jumpChapter(1); });
      speed.addEventListener('change', () => { rate = Number(speed.value); previous = null; });
      reduced.addEventListener?.('change', event => {
        if (overridden) return;
        if (event.matches) { pause(); if (svg) svg.hidden = true; img.src = still; img.hidden = false; }
        else void play();
      });
      if (reduced.matches) img.src = still;
      else void play();
      updateToggle(); renderTime();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => enhance());
  else enhance();
  if (typeof window.document$ !== 'undefined' && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(() => enhance());
  }
})();
