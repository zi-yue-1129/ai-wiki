/* Optional same-origin SMIL timeline controls for reviewed teaching diagrams.
 * Markdown and no-script readers retain the original image; no third-party SVG is fetched.
 */
(() => {
  'use strict';
  const sequences = {
    'gpipe-fill-drain': { duration: 12, steps: [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 11.9] },
    'gpipe-gradient-accumulation': { duration: 14, steps: [0, 2, 4, 6, 8, 10, 12, 13.5] },
    'fsdp-gather-scatter': { duration: 10, steps: [0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5] },
    'fsdp-parameter-residency': { duration: 10, steps: [0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5] },
    'zero-state-sharding': { duration: 12, steps: [0, 2, 4, 5.5, 7.5, 9.8, 11.5] },
    'megatron-column-row': { duration: 10, steps: [0, 2, 4, 6, 8, 9.5] },
    // Co-design: one step per checkpoint-spacing choice; the timeline also
    // lets readers inspect intermediate forward replay within each segment.
    'checkpoint-spacing': { duration: 12, steps: [0, 2.45, 4.85, 7.25, 9.65] },
    // FP16: semantic boundaries in both the ascending and descending sweep.
    // Seeking continuously still exposes all 27 exact power-of-two states.
    'fp16-scaling-window': { duration: 12, steps: [0, 0.95, 1.42, 4.66, 5.12, 5.59, 6.05, 6.52, 9.75, 10.21, 11.15] },
    // Each two-second interval is a complete synthetic GradScaler check.
    'gradscaler-feedback': { duration: 12, steps: [0, 2.05, 4.05, 6.05, 8.05, 10.05] },
  };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function enhance() {
    if (reduced.matches) return;
    for (const host of document.querySelectorAll('.concept-motion-player')) {
      if (host.dataset.distributedTimeline === 'yes') continue;
      const img = host.querySelector('img[src*="concept-animations/"]');
      if (!img) continue;
      const src = img.dataset.motionSrc || img.getAttribute('src') || '';
      const match = src.match(/(?:^|\/)([a-z0-9-]+)-motion\.svg(?:[?#]|$)/);
      if (!match || !Object.hasOwn(sequences, match[1])) continue;
      const config = sequences[match[1]];
      // In the co-design chapter the outer Markdown region is already the
      // keyboard-focusable scroll container. Avoid a second nested scroller.
      if (/^(checkpoint-spacing|fp16-scaling-window|gradscaler-feedback)$/.test(match[1])) {
        host.classList.add('co-design-motion-timeline');
      }
      const zh = /[\u3400-\u9fff]/.test(img.alt || '');
      const label = (en, tw) => zh ? tw : en;
      const previousControls = host.querySelector('.concept-motion-controls');
      const frame = document.createElement('object');
      frame.className = 'distributed-motion-frame';
      frame.type = 'image/svg+xml';
      frame.data = src;
      frame.setAttribute('aria-label', img.alt || match[1]);
      // An <object> fallback duplicated the original image's alt text in the
      // DOM, even while the fallback was visually inactive.  Built-page
      // accessibility checks rightly expect exactly one source image per
      // description. The object is labelled above; its nested fallback is
      // decorative, while the original image remains the no-script fallback.
      const fallback = img.cloneNode(true);
      fallback.alt = '';
      fallback.setAttribute('aria-hidden', 'true');
      fallback.setAttribute('role', 'presentation');
      frame.append(fallback);
      frame.style.visibility = 'hidden';
      frame.style.position = 'absolute';
      frame.style.width = '1px';
      frame.style.height = '1px';
      img.after(frame);
      host.dataset.distributedTimeline = 'yes';
      let svg = null, time = 0, playing = false, speed = 1, raf = 0, last = 0;
      const bar = document.createElement('div');
      bar.className = 'distributed-motion-controls';
      bar.hidden = true;
      const makeButton = (en, tw) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'concept-motion-toggle';
        b.textContent = label(en, tw);
        bar.append(b);
        return b;
      };
      const prev = makeButton('← Step', '← 上一步');
      const play = makeButton('▶ Play', '▶ 播放');
      const next = makeButton('Step →', '下一步 →');
      // Return directly to the initial model state, rather than repeatedly
      // stepping backwards through several semantic milestones.
      const restart = host.classList.contains('co-design-motion-timeline')
        ? makeButton('↺ Restart', '↺ 重新開始') : null;
      // Pin a synthetic state A and compare it with the live state B. This
      // emphasizes trade-offs and decision changes without copying SVG assets.
      const pin = host.classList.contains('co-design-motion-timeline')
        ? document.createElement('button') : null;
      const clearPin = pin ? document.createElement('button') : null;
      const comparison = pin ? document.createElement('section') : null;
      let pinnedTime = null;
      let pinA = null, pinB = null, comparisonDelta = null;
      if (pin) {
        pin.type = clearPin.type = 'button';
        pin.className = 'distributed-motion-pin';
        clearPin.className = 'distributed-motion-clear';
        pin.textContent = label('Pin A', '釘選 A');
        pin.disabled = true; // An actual SVG time must be available first.
        clearPin.textContent = label('Clear A', '清除 A');
        clearPin.hidden = true;
        bar.append(pin, clearPin);
        comparison.className = 'distributed-motion-comparison';
        comparison.hidden = true;
        comparison.setAttribute('role', 'group');
        comparison.setAttribute('aria-label', label('Pinned versus current example state', '釘選與目前示意狀態比較'));
        pinA = document.createElement('p');
        pinB = document.createElement('p');
        comparisonDelta = document.createElement('p');
        pinA.className = 'distributed-motion-compare-a';
        pinB.className = 'distributed-motion-compare-b';
        comparisonDelta.className = 'distributed-motion-compare-delta';
        comparison.append(pinA, pinB, comparisonDelta);
      }
      const seek = document.createElement('input');
      seek.type = 'range'; seek.min = '0'; seek.max = '1000'; seek.step = '1'; seek.value = '0';
      seek.className = 'distributed-motion-seek';
      seek.setAttribute('aria-label', label('Animation timeline', '動畫時間軸'));
      bar.append(seek);
      const readout = document.createElement('output');
      readout.className = 'distributed-motion-time';
      readout.setAttribute('aria-live', 'off');
      bar.append(readout);
      const rate = document.createElement('select');
      rate.className = 'distributed-motion-rate';
      rate.setAttribute('aria-label', label('Playback speed', '播放速度'));
      for (const n of [0.5, 1, 2]) {
        const opt = document.createElement('option');
        opt.value = String(n); opt.textContent = String(n) + '×';
        if (n === 1) opt.selected = true;
        rate.append(opt);
      }
      bar.append(rate);
      const status = document.createElement('span');
      status.className = 'concept-motion-status';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      bar.append(status);
      // A live *visual* state explanation accompanies the underlying SVG.
      // It is not an aria-live region: requestAnimationFrame must not flood
      // screen readers. Only explicit step/seek actions announce its content.
      const interpretation = document.createElement('p');
      interpretation.className = 'distributed-motion-interpretation';
      interpretation.setAttribute('aria-live', 'off');
      if (host.classList.contains('co-design-motion-timeline')) {
        bar.append(interpretation);
        bar.append(comparison);
      }
      // Keep controls outside the horizontally scrolled 640px figure on
      // narrow co-design pages. This makes every control reachable without
      // panning the figure and retains the original focusable figure region.
      const coDesignRegion = host.classList.contains('co-design-motion-timeline')
        ? host.closest('.concept-motion-scroll') : null;
      if (coDesignRegion) {
        bar.classList.add('co-design-motion-controls');
        coDesignRegion.after(bar);
      } else host.append(bar);

      function teachingState(t) {
        // All values are derived from the same synthetic schedules used by
        // the reviewed SVGs; none are measured GPU/optimizer observations.
        if (match[1] === 'checkpoint-spacing') {
          const phase = Math.min(4, Math.floor(t / 2.4));
          const spacing = [1, 2, 4, 8, 16][phase];
          const keep = 16 / spacing + 1, scratch = spacing - 1;
          const totalRebuilt = 16 - 16 / spacing;
          const within = Math.max(0, (t - phase * 2.4) / 2.4);
          const replayed = spacing === 1 ? 0 : Math.min(scratch, Math.floor(within * spacing / 0.9));
          return label(
            `s=${spacing} · KEEP ${keep} + REBUILD ${scratch} = PEAK ${keep + scratch} · TOTAL REBUILT ${totalRebuilt} (all segments) · active replay ${replayed}/${scratch} (last segment; example slots)`,
            `s=${spacing} · 保留 ${keep} + 重算暫存 ${scratch} = 峰值 ${keep + scratch} · 全區段重建總數 ${totalRebuilt} · 末段重算進度 ${replayed}/${scratch}（示意槽位）`
          );
        }
        if (match[1] === 'fp16-scaling-window') {
          // 27 equal discrete SMIL frames: 0..12, 12..0, final 0.
          const frame = Math.min(26, Math.floor(t / config.duration * 26 + 1e-6));
          const exponent = frame <= 12 ? frame : frame <= 25 ? 25 - frame : 0;
          const scale = 2 ** exponent;
          const low = exponent <= 2 ? '0' : 'finite';
          const high = exponent >= 11 ? 'Inf' : 'finite';
          return label(
            `S=2^${exponent} (${scale}) · LOW ${low}${low === '0' ? ' (silent underflow)' : ''} · HIGH ${high} · ${exponent >= 11 ? 'SKIP' : 'STEP ELIGIBLE'} (example)`,
            `S=2^${exponent}（${scale}）· 小梯度${low === '0' ? '歸零（仍為有限值）' : '非零有限'} · 大梯度${high === 'Inf' ? '溢位' : '有限'} · ${exponent >= 11 ? '跳過更新' : '符合更新條件'}（示意）`
          );
        }
        if (match[1] === 'gradscaler-feedback') {
          const i = Math.min(5, Math.floor(t / 2));
          const current = [1024, 1024, 2048, 1024, 1024, 2048][i];
          const following = [1024, 2048, 1024, 1024, 2048, 1024][i];
          const check = i === 2 || i === 5 ? 'Inf' : 'finite';
          const streak = [1, 2, 0, 1, 2, 0][i];
          return label(
            `t${i + 1} · S ${current} → NEXT ${following} · ${check} · ${check === 'Inf' ? 'SKIP / reset' : 'STEP ELIGIBLE'} · ${check === 'Inf' ? 'backoff' : streak === 2 ? 'grow after 2/2' : 'streak 1/2'} (example)`,
            `t${i + 1} · 當次 ${current} → 下次 ${following} · ${check === 'Inf' ? '溢位、跳過並重設' : '通過非有限值檢查、符合更新條件'} · ${check === 'Inf' ? '縮小係數' : streak === 2 ? '連續通過 2/2，放大' : '連續通過 1/2'}（示意）`
          );
        }
        return '';
      }
      function conciseState(t) {
        if (match[1] === 'checkpoint-spacing') {
          const spacing = [1, 2, 4, 8, 16][Math.min(4, Math.floor(t / 2.4))];
          const peak = 16 / spacing + spacing;
          const total = 16 - 16 / spacing;
          return label(`s=${spacing} · PEAK ${peak} · TOTAL REBUILT ${total}`,
                       `s=${spacing} · 峰值 ${peak} · 全區段重建 ${total}`);
        }
        if (match[1] === 'fp16-scaling-window') {
          const frame = Math.min(26, Math.floor(t / config.duration * 26 + 1e-6));
          const k = frame <= 12 ? frame : frame <= 25 ? 25 - frame : 0;
          return label(`S=${2 ** k} · LOW ${k <= 2 ? '0' : 'finite'} · HIGH ${k >= 11 ? 'Inf' : 'finite'} · ${k >= 11 ? 'SKIP' : 'ELIGIBLE'}`,
                       `S=${2 ** k} · 小梯度${k <= 2 ? '歸零' : '有限'} · 大梯度${k >= 11 ? '溢位' : '有限'} · ${k >= 11 ? '跳過' : '符合更新條件'}`);
        }
        const i = Math.min(5, Math.floor(t / 2));
        const s = [1024, 1024, 2048, 1024, 1024, 2048][i];
        const next = [1024, 2048, 1024, 1024, 2048, 1024][i];
        const skip = i === 2 || i === 5;
        return label(`t${i + 1} · S ${s} → ${next} · ${skip ? 'SKIP' : 'ELIGIBLE'}`,
                     `t${i + 1} · 縮放 ${s} → ${next} · ${skip ? '跳過' : '符合更新條件'}`);
      }
      function compareChange(a, b) {
        if (match[1] === 'checkpoint-spacing') {
          const get = t => {
            const s = [1, 2, 4, 8, 16][Math.min(4, Math.floor(t / 2.4))];
            return [16 / s + s, 16 - 16 / s];
          };
          const [peakA, totalA] = get(a), [peakB, totalB] = get(b);
          const signed = n => (n > 0 ? '+' : '') + n;
          return label(`B − A: Δ PEAK ${signed(peakB - peakA)} slots · Δ TOTAL REBUILT ${signed(totalB - totalA)}`,
                       `B − A：峰值 ${signed(peakB - peakA)} 槽 · 全區段重建 ${signed(totalB - totalA)}`);
        }
        if (match[1] === 'fp16-scaling-window') {
          const exp = t => {
            const n = Math.min(26, Math.floor(t / config.duration * 26 + 1e-6));
            return n <= 12 ? n : n <= 25 ? 25 - n : 0;
          };
          const x = exp(a), y = exp(b);
          const result = k => k >= 11 ? 'SKIP' : 'ELIGIBLE';
          return label(`Outcome: ${result(x)} → ${result(y)} · scale exponent ${x} → ${y}`,
                       `更新資格：${result(x) === 'SKIP' ? '跳過' : '符合'} → ${result(y) === 'SKIP' ? '跳過' : '符合'} · 指數 ${x} → ${y}`);
        }
        const skipped = t => [2, 5].includes(Math.min(5, Math.floor(t / 2)));
        return label(`Finite check: ${skipped(a) ? 'SKIP' : 'ELIGIBLE'} → ${skipped(b) ? 'SKIP' : 'ELIGIBLE'}`,
                     `有限值檢查：${skipped(a) ? '跳過' : '符合更新條件'} → ${skipped(b) ? '跳過' : '符合更新條件'}`);
      }
      function updateComparison() {
        if (pinnedTime === null || !comparison) return;
        pinA.textContent = label('A · pinned: ', 'A · 已釘選：') + conciseState(pinnedTime);
        pinB.textContent = label('B · current: ', 'B · 目前：') + conciseState(time);
        comparisonDelta.textContent = compareChange(pinnedTime, time) +
          label(' · synthetic, not measured', ' · 人工示意，非實測');
      }
      function draw() {
        if (!svg) return;
        svg.setCurrentTime(Math.min(time, config.duration - 0.001));
        seek.value = String(Math.round(time / config.duration * 1000));
        readout.textContent = time.toFixed(1) + ' / ' + config.duration + 's';
        if (interpretation.isConnected) interpretation.textContent = teachingState(time);
        updateComparison();
        play.textContent = playing ? label('Ⅱ Pause', 'Ⅱ 暫停') : label('▶ Play', '▶ 播放');
        play.setAttribute('aria-label', playing ? label('Pause animation', '暫停動畫') : label('Play animation', '播放動畫'));
      }
      function stop() {
        playing = false;
        if (raf) cancelAnimationFrame(raf);
        raf = 0; last = 0;
        draw();
      }
      function setTime(t) {
        time = Math.max(0, Math.min(config.duration - 0.001, t));
        draw();
      }
      function tick(now) {
        if (!playing || !svg) return;
        if (last) time += (now - last) / 1000 * speed;
        last = now;
        if (time >= config.duration) time %= config.duration;
        draw();
        raf = requestAnimationFrame(tick);
      }
      play.addEventListener('click', () => {
        if (!svg) return;
        if (playing) stop();
        else { playing = true; last = 0; draw(); raf = requestAnimationFrame(tick); }
        status.textContent = playing ? label('Animation playing', '動畫播放中') : label('Animation paused', '動畫已暫停');
      });
      function step(direction) {
        stop();
        const ordered = config.steps;
        const candidate = direction > 0
          ? ordered.find(t => t > time + 0.05)
          : [...ordered].reverse().find(t => t < time - 0.05);
        setTime(candidate ?? (direction > 0 ? config.duration - 0.001 : 0));
        status.textContent = interpretation.isConnected ? interpretation.textContent
          : label('Animation at ', '動畫時間 ') + time.toFixed(1) + 's';
      }
      prev.addEventListener('click', () => step(-1));
      next.addEventListener('click', () => step(1));
      restart?.addEventListener('click', () => {
        stop(); setTime(0);
        status.textContent = interpretation.isConnected ? interpretation.textContent
          : label('Animation reset to start', '動畫已重設到起點');
      });
      pin?.addEventListener('click', () => {
        if (!svg) return;
        stop();
        pinnedTime = time;
        comparison.hidden = false;
        clearPin.hidden = false;
        pin.textContent = label('Replace A', '更新 A');
        updateComparison();
        status.textContent = label('Pinned state A. Move the timeline to compare B.',
                                   '已釘選 A，移動時間軸即可比較 B。');
      });
      clearPin?.addEventListener('click', () => {
        pinnedTime = null;
        comparison.hidden = true;
        clearPin.hidden = true;
        pin.textContent = label('Pin A', '釘選 A');
        status.textContent = label('Pinned comparison cleared', '已清除釘選比較');
      });
      seek.addEventListener('input', () => {
        const selected = Number(seek.value);
        stop(); setTime(selected / 1000 * config.duration);
        status.textContent = interpretation.isConnected ? interpretation.textContent
          : label('Animation at ', '動畫時間 ') + time.toFixed(1) + 's';
      });
      rate.addEventListener('change', () => { speed = Number(rate.value); last = 0; });
      const onReduce = event => {
        stop();
        if (event.matches) {
          frame.hidden = true; bar.hidden = true;
          img.hidden = false;
          if (previousControls) previousControls.hidden = false;
          img.src = img.dataset.stillSrc || src.replace(/-motion\.svg(?=$|[?#])/, '-still.svg');
        } else if (svg) {
          img.src = src;
          img.hidden = true;
          frame.hidden = false; frame.style.visibility = '';
          frame.style.position = ''; frame.style.width = ''; frame.style.height = '';
          bar.hidden = false;
          if (previousControls) previousControls.hidden = true;
          setTime(time);
        }
      };
      reduced.addEventListener('change', onReduce);
      // Do not silently fast-forward when the reader returns to an inactive tab.
      // requestAnimationFrame may be throttled while hidden; pausing prevents a
      // large elapsed-time jump on resume and avoids unwanted background motion.
      const onVisibility = () => {
        if (document.hidden && playing) {
          stop();
          status.textContent = label('Animation paused while tab is hidden', '分頁隱藏，動畫已暫停');
        }
      };
      document.addEventListener('visibilitychange', onVisibility);
      frame.addEventListener('load', () => {
        try {
          const root = frame.contentDocument?.documentElement;
          if (!root || typeof root.pauseAnimations !== 'function' || typeof root.setCurrentTime !== 'function') return;
          svg = root;
          svg.pauseAnimations();
          setTime(0);
          if (pin) pin.disabled = false;
          // Also capture a load that finishes while reduced motion is active:
          // otherwise turning motion back on can leave this player stranded.
          if (reduced.matches) return;
          img.hidden = true;
          frame.hidden = false;
          frame.style.visibility = '';
          frame.style.position = ''; frame.style.width = ''; frame.style.height = '';
          bar.hidden = false;
          if (previousControls) previousControls.hidden = true;
        } catch (_) { /* Unsupported or cross-origin object: preserve original image and controls. */ }
      });
      const observer = new MutationObserver(() => {
        if (host.isConnected) return;
        stop(); observer.disconnect(); reduced.removeEventListener('change', onReduce);
        document.removeEventListener('visibilitychange', onVisibility);
        if (coDesignRegion) bar.remove();
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  if (window.document$?.subscribe) window.document$.subscribe(enhance);
  // A page loaded with reduced motion can opt into richer controls later.
  reduced.addEventListener('change', () => { if (!reduced.matches) enhance(); });
})();
