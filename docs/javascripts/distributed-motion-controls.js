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
    'fp16-scaling-window': { duration: 12, steps: [0, 0.95, 1.42, 4.66, 5.12, 5.59, 6.05, 6.52, 6.98, 9.75, 10.21, 10.67, 11.15] },
    // Each two-second interval is a complete synthetic GradScaler check.
    'gradscaler-feedback': { duration: 12, steps: [0, 2.05, 4.05, 6.05, 8.05, 10.05] },
  };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function enhance() {
    // Install listeners even when motion starts disabled so a later
    // preference change activates the same reviewed teaching timeline.
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
      let frame = document.createElement('object');
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
      const comparePrevious = pin ? document.createElement('button') : null;
      const clearPin = pin ? document.createElement('button') : null;
      const swapPin = pin ? document.createElement('button') : null;
      const sweepPin = pin ? document.createElement('button') : null;
      const comparison = pin ? document.createElement('section') : null;
      let pinnedTime = null;
      // A→B is a directed *parameter/iteration scan*, not a simulated model run.
      let sweepTarget = null, sweepRate = 0;
      let pinA = null, pinB = null, comparisonDelta = null;
      // Paired gauges make the memory/recomputation, representability and
      // GradScaler feedback trade-offs perceptible without replacing the
      // precise, screen-reader-accessible numeric comparison above them.
      const checkpointSpacing = t => [1, 2, 4, 8, 16][Math.min(4, Math.floor(t / 2.4))];
      // A discrete FP16 state occupies an entire 12/26-second cell. Reuse
      // this frame index for labels, comparisons and the transition rail:
      // a time-distance highlight would disappear halfway through a state.
      const fp16Frame = t => Math.min(26, Math.floor(t / config.duration * 26 + 1e-6));
      const scaleExponent = t => {
        const frame = fp16Frame(t);
        return frame <= 12 ? frame : frame <= 25 ? 25 - frame : 0;
      };
      const feedbackIndex = t => Math.min(5, Math.floor(t / 2));
      const gauges = match[1] === 'checkpoint-spacing' ? [
        { id: 'peak', en: 'PEAK', tw: '峰值槽位', max: 17, at: t => 16 / checkpointSpacing(t) + checkpointSpacing(t) },
        { id: 'rebuilt', en: 'TOTAL REBUILT', tw: '總重算量', max: 15, at: t => 16 - 16 / checkpointSpacing(t) },
      ] : match[1] === 'fp16-scaling-window' ? [
        { id: 'exponent', en: 'EXPONENT', tw: '縮放指數', max: 12, at: scaleExponent },
        { id: 'low', en: 'LOW RETAINED', tw: '小梯度保留', max: 1, at: t => Number(scaleExponent(t) > 2) },
        { id: 'high', en: 'HIGH FINITE', tw: '大梯度有限', max: 1, at: t => Number(scaleExponent(t) < 11) },
      ] : match[1] === 'gradscaler-feedback' ? [
        { id: 'streak', en: 'FINITE STREAK', tw: '連續通過', max: 2, at: t => [1, 2, 0, 1, 2, 0][feedbackIndex(t)] },
        { id: 'next', en: 'NEXT S', tw: '下次縮放', max: 2048, at: t => [1024, 2048, 1024, 1024, 2048, 1024][feedbackIndex(t)] },
      ] : [];
      // Reproducible, hand-checked contrasts.  The times fall inside the
      // corresponding discrete SVG states, away from SMIL keyframe boundaries.
      // These are instructional examples, never measured experiments.
      const guidedCases = match[1] === 'checkpoint-spacing' ? [
        { en: 's=1 → s=4 · memory/replay trade-off', tw: 's=1 → s=4 · 記憶體與重算取捨', a: 0, b: 4.85 },
        { en: 's=8 → s=4 · dominated choice', tw: 's=8 → s=4 · 支配關係', a: 7.25, b: 4.85 },
      ] : match[1] === 'fp16-scaling-window' ? [
        { en: 'S=4 → 8 · recover LOW', tw: 'S=4 → 8 · 小梯度恢復', a: 0.95, b: 1.42 },
        { en: 'S=1024 → 2048 · HIGH overflow', tw: 'S=1024 → 2048 · 大梯度溢位', a: 4.66, b: 5.12 },
      ] : match[1] === 'gradscaler-feedback' ? [
        { en: 't1 → t5 · finite-history effect', tw: 't1 → t5 · 歷史計數效應', a: 0, b: 8.05 },
        { en: 't2 → t3 · overflow backoff', tw: 't2 → t3 · 溢位回退', a: 2.05, b: 4.05 },
      ] : [];
      // Semantic transition navigator: jump directly to state boundaries,
      // including the distinct upward/downward crossings in the FP16 sweep.
      // Each button seeks the *existing* animated SVG; no new synthetic
      // computation or duplicate visual asset is introduced.
      const landmarks = match[1] === 'checkpoint-spacing' ? [
        { t: 0, en: 's=1', tw: 's=1', hintEn: 'Checkpoint spacing 1: peak 17, rebuilt 0', hintTw: '間距 1：峰值 17、重算 0' },
        { t: 2.45, en: 's=2', tw: 's=2', hintEn: 'Checkpoint spacing 2: peak 10, rebuilt 8', hintTw: '間距 2：峰值 10、重算 8' },
        { t: 4.85, en: 's=4', tw: 's=4', hintEn: 'Checkpoint spacing 4: peak 8, rebuilt 12', hintTw: '間距 4：峰值 8、重算 12' },
        { t: 7.25, en: 's=8', tw: 's=8', hintEn: 'Checkpoint spacing 8: peak 10, rebuilt 14', hintTw: '間距 8：峰值 10、重算 14' },
        { t: 9.65, en: 's=16', tw: 's=16', hintEn: 'Checkpoint spacing 16: peak 17, rebuilt 15', hintTw: '間距 16：峰值 17、重算 15' },
      ] : match[1] === 'fp16-scaling-window' ? [
        { t: 1.42, en: 'LOW +', tw: '小值保留', hintEn: 'Ascending scale 8: small gradient first survives rounding', hintTw: '上升至縮放 8：小梯度首次不再歸零' },
        { t: 5.12, en: 'HIGH Inf', tw: '大值溢位', hintEn: 'Ascending scale 2048: large gradient overflows to infinity', hintTw: '上升至縮放 2048：大梯度溢位成無限值' },
        { t: 6.98, en: 'HIGH finite', tw: '大值恢復', hintEn: 'Descending scale 1024: large gradient becomes finite again', hintTw: '下降至縮放 1024：大梯度重新成為有限值' },
        { t: 10.67, en: 'LOW 0', tw: '小值歸零', hintEn: 'Descending scale 4: small gradient rounds to zero again', hintTw: '下降至縮放 4：小梯度再次捨入為零' },
      ] : match[1] === 'gradscaler-feedback' ? [
        { t: 0, en: 't1 · hold', tw: 't1 · 維持', hintEn: 'Iteration 1: finite, hold scale', hintTw: '第 1 次：有限值，維持縮放' },
        { t: 2.05, en: 't2 · grow', tw: 't2 · 放大', hintEn: 'Iteration 2: second finite check grows the scale', hintTw: '第 2 次：連續第兩次有限值，放大縮放' },
        { t: 4.05, en: 't3 · backoff', tw: 't3 · 縮小', hintEn: 'Iteration 3: infinity causes backoff and step skip', hintTw: '第 3 次：出現無限值，縮小並跳過更新' },
        { t: 6.05, en: 't4 · hold', tw: 't4 · 維持', hintEn: 'Iteration 4: finite after reset, hold scale', hintTw: '第 4 次：重設後首次有限值，維持縮放' },
        { t: 8.05, en: 't5 · grow', tw: 't5 · 放大', hintEn: 'Iteration 5: second finite check grows scale again', hintTw: '第 5 次：連續第二次有限值，再次放大' },
        { t: 10.05, en: 't6 · backoff', tw: 't6 · 縮小', hintEn: 'Iteration 6: infinity causes another backoff', hintTw: '第 6 次：出現無限值，再次縮小' },
      ] : [];
      const landmarkRail = landmarks.length ? document.createElement('div') : null;
      const landmarkButtons = [];
      if (landmarkRail) {
        landmarkRail.className = 'distributed-motion-landmarks';
        landmarkRail.setAttribute('role', 'group');
        landmarkRail.setAttribute('aria-label', label('Jump to key transitions', '跳至關鍵轉換狀態'));
        for (const event of landmarks) {
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'distributed-motion-landmark';
          button.textContent = label(event.en, event.tw);
          button.title = label(event.hintEn, event.hintTw);
          button.setAttribute('aria-label', label(event.hintEn, event.hintTw));
          button.disabled = true;
          button.addEventListener('click', () => {
            if (!svg) return;
            stop(false); setTime(event.t);
            status.textContent = label('Key transition: ', '關鍵狀態：') + label(event.hintEn, event.hintTw);
          });
          landmarkRail.append(button);
          landmarkButtons.push({ button, event });
        }
      }
      const gaugeFills = [];
      if (pin) {
        pin.type = comparePrevious.type = clearPin.type = swapPin.type = sweepPin.type = 'button';
        pin.className = 'distributed-motion-pin';
        comparePrevious.className = 'distributed-motion-previous';
        comparePrevious.textContent = label('Compare previous', '比較前一步');
        comparePrevious.disabled = true;
        clearPin.className = 'distributed-motion-clear';
        swapPin.className = 'distributed-motion-swap';
        sweepPin.className = 'distributed-motion-sweep';
        sweepPin.textContent = label('▶ Sweep A→B', '▶ 掃描 A→B');
        sweepPin.hidden = true;
        swapPin.textContent = label('Swap A/B', '交換 A／B');
        swapPin.hidden = true;
        sweepPin.hidden = true;
        pin.textContent = label('Pin A', '釘選 A');
        pin.disabled = true; // An actual SVG time must be available first.
        clearPin.textContent = label('Clear A', '清除 A');
        clearPin.hidden = true;
        bar.append(pin, comparePrevious, swapPin, sweepPin, clearPin);
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
        const visual = document.createElement('div');
        visual.className = 'distributed-motion-compare-visual';
        visual.setAttribute('aria-hidden', 'true'); // numerical text above is authoritative
        for (const metric of gauges) {
          const row = document.createElement('div');
          row.className = 'distributed-motion-visual-row';
          row.dataset.metric = metric.id;
          const heading = document.createElement('strong');
          heading.className = 'distributed-motion-visual-heading';
          heading.textContent = label(metric.en, metric.tw);
          row.append(heading);
          const fills = [];
          for (const side of ['A', 'B']) {
            const lane = document.createElement('div');
            lane.className = 'distributed-motion-visual-lane';
            const sideLabel = document.createElement('span');
            sideLabel.textContent = side;
            const track = document.createElement('span');
            track.className = 'distributed-motion-visual-track';
            const fill = document.createElement('span');
            fill.className = 'distributed-motion-visual-fill distributed-motion-visual-' + side.toLowerCase();
            track.append(fill); lane.append(sideLabel, track); row.append(lane);
            fills.push(fill);
          }
          gaugeFills.push({ metric, a: fills[0], b: fills[1] });
          visual.append(row);
        }
        comparison.append(pinA, pinB, comparisonDelta, visual);
      }
      // Native select makes the two most useful causal contrasts discoverable
      // without dozens of precise slider/Pin interactions.  It retains
      // native keyboard navigation and does not auto-play a selection.
      const guided = pin ? document.createElement('select') : null;
      if (guided) {
        guided.className = 'distributed-motion-scenario';
        guided.setAttribute('aria-label', label('Guided A/B comparisons', '引導式 A/B 比較'));
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = label('Try a worked comparison…', '選擇示範比較…');
        guided.append(placeholder);
        guidedCases.forEach((example, index) => {
          const option = document.createElement('option');
          option.value = String(index);
          option.textContent = label(example.en, example.tw);
          guided.append(option);
        });
        guided.disabled = true;
        bar.append(guided);
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
      if (landmarkRail) bar.append(landmarkRail);
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
      // Keep recovery outside the 640px figure scroller; retain the still.
      const retry = document.createElement('button');
      retry.type = 'button';
      retry.className = 'distributed-motion-retry';
      retry.textContent = label('Animation unavailable · Retry', '動畫無法載入 · 重試');
      retry.hidden = true;
      if (coDesignRegion) bar.after(retry);
      else host.append(retry);
      let retrying = false, retryCount = 0;
      // Once a request has timed out or failed, a late load must never
      // reactivate controls over the reviewed still. Only an explicit retry
      // (or a fresh navigation after reduced motion) accepts new events.
      let acceptingFrameLoad = true;
      // An <object> request can stall indefinitely without firing load/error.
      // Restore the existing reviewed still and offer a keyboard retry rather
      // than leaving the teaching diagram in a permanent loading state.
      const SVG_LOAD_TIMEOUT_MS = 15000;
      let loadTimer = null;
      const clearLoadTimer = () => {
        if (loadTimer !== null) window.clearTimeout(loadTimer);
        loadTimer = null;
      };
      const armLoadTimer = () => {
        clearLoadTimer();
        if (reduced.matches) return;
        loadTimer = window.setTimeout(() => {
          loadTimer = null;
          showStaticFallback();
        }, SVG_LOAD_TIMEOUT_MS);
      };

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
          const exponent = scaleExponent(t);
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
          const k = scaleExponent(t);
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
        // Signed changes distinguish scale/exponent shifts from the absolute
        // states. In GradScaler, next-scale depends on finite-check history.
        const signed = n => (n > 0 ? '+' : '') + n;
        if (match[1] === 'checkpoint-spacing') {
          const get = t => {
            const s = [1, 2, 4, 8, 16][Math.min(4, Math.floor(t / 2.4))];
            return [16 / s + s, 16 - 16 / s];
          };
          const [peakA, totalA] = get(a), [peakB, totalB] = get(b);
          return label(`B − A: Δ PEAK ${signed(peakB - peakA)} slots · Δ TOTAL REBUILT ${signed(totalB - totalA)}`,
                       `B − A：峰值 ${signed(peakB - peakA)} 槽 · 全區段重建 ${signed(totalB - totalA)}`);
        }
        if (match[1] === 'fp16-scaling-window') {
          const x = scaleExponent(a), y = scaleExponent(b);
          const result = k => k >= 11 ? 'SKIP' : 'ELIGIBLE';
          const low = k => k <= 2 ? '0' : 'finite';
          const high = k => k >= 11 ? 'Inf' : 'finite';
          // A rounded zero is finite: it loses information but does not
          // trigger the nonfinite step gate. Compare both rounded inputs.
          return label(`Outcome: ${result(x)} → ${result(y)} · LOW ${low(x)} → ${low(y)} · HIGH ${high(x)} → ${high(y)} · scale exponent ${x} → ${y} (Δ ${signed(y - x)})`,
                       `更新資格：${result(x) === 'SKIP' ? '跳過' : '符合'} → ${result(y) === 'SKIP' ? '跳過' : '符合'} · 小梯度 ${low(x)} → ${low(y)} · 大梯度 ${high(x)} → ${high(y)} · 指數 ${x} → ${y}（Δ ${signed(y - x)}）`);
        }
        const index = t => Math.min(5, Math.floor(t / 2));
        const skipped = i => i === 2 || i === 5;
        // Decision-time counts: a 2/2 check triggers growth then resets.
        // Inf also resets the tracker; these are not post-update counts.
        const streak = [1, 2, 0, 1, 2, 0];
        const nextScale = [1024, 2048, 1024, 1024, 2048, 1024];
        const ia = index(a), ib = index(b);
        return label(`Finite check: ${skipped(ia) ? 'SKIP' : 'ELIGIBLE'} → ${skipped(ib) ? 'SKIP' : 'ELIGIBLE'} · streak ${streak[ia]}/2 → ${streak[ib]}/2 · NEXT S ${nextScale[ia]} → ${nextScale[ib]} (Δ ${signed(nextScale[ib] - nextScale[ia])})`,
                     `有限值檢查：${skipped(ia) ? '跳過' : '符合更新條件'} → ${skipped(ib) ? '跳過' : '符合更新條件'} · 連續通過 ${streak[ia]}/2 → ${streak[ib]}/2 · 下次縮放 ${nextScale[ia]} → ${nextScale[ib]}（Δ ${signed(nextScale[ib] - nextScale[ia])}）`);
      }
      function comparisonInsight(a, b) {
        // Interpret the paired *synthetic* states, not only their numbers.
        // A smaller checkpoint peak and smaller cumulative replay are both
        // desirable in this deliberately limited two-metric toy model.
        if (match[1] === 'checkpoint-spacing') {
          const sa = checkpointSpacing(a), sb = checkpointSpacing(b);
          const dPeak = (16 / sb + sb) - (16 / sa + sa);
          const dReplay = (16 - 16 / sb) - (16 - 16 / sa);
          if (!dPeak && !dReplay) return label('Same aggregate costs.', '總體成本相同。');
          if (dPeak <= 0 && dReplay <= 0) {
            return label('B dominates A on both schematic costs.', 'B 在兩項示意成本上皆不劣於 A。');
          }
          if (dPeak >= 0 && dReplay >= 0) {
            return label('A dominates B on both schematic costs.', 'A 在兩項示意成本上皆不劣於 B。');
          }
          return label('Memory–recomputation trade-off.', '記憶體與重算量存在取捨。');
        }
        if (match[1] === 'fp16-scaling-window') {
          const regime = k => k <= 2
            ? label('LOW ZERO', '小梯度歸零')
            : k >= 11 ? label('HIGH INF', '大梯度溢位')
              : label('BOTH FINITE NONZERO', '兩筆皆為有限非零');
          return label('Rounded regime: ', '捨入狀態：') + regime(scaleExponent(a)) + ' → ' + regime(scaleExponent(b)) +
            label(' (illustrative binary16 only).', '（僅限本例 binary16）。');
        }
        const decision = t => {
          const i = feedbackIndex(t);
          return [label('hold', '維持'), label('grow', '放大'), label('backoff', '縮小'),
                  label('hold', '維持'), label('grow', '放大'), label('backoff', '縮小')][i];
        };
        return label('Next-scale action: ', '下一次縮放動作：') + decision(a) + ' → ' + decision(b) +
          label(' (depends on finite-check history).', '（取決於歷次有限值檢查）。');
      }
      // Offer a local state-to-state comparison without requiring precise
      // slider movement and manual Pin A. The *previous time cell*, rather
      // than the previous distinct numerical value, is essential for FP16:
      // its upward and downward crossings have different causal contexts.
      function previousStateTime(t) {
        if (match[1] === 'checkpoint-spacing') {
          const i = Math.min(4, Math.floor(t / 2.4));
          return i ? config.steps[i - 1] : null;
        }
        if (match[1] === 'fp16-scaling-window') {
          const i = fp16Frame(t);
          if (!i) return null;
          const before = i - 1;
          return before ? (before + 0.12) * config.duration / 26 : 0;
        }
        const i = feedbackIndex(t);
        return i ? config.steps[i - 1] : null;
      }
      function updateComparison() {
        if (pinnedTime === null || !comparison) return;
        pinA.textContent = label('A · pinned: ', 'A · 已釘選：') + conciseState(pinnedTime);
        pinB.textContent = label('B · current: ', 'B · 目前：') + conciseState(time);
        comparisonDelta.textContent = compareChange(pinnedTime, time) +
          ' · ' + comparisonInsight(pinnedTime, time) +
          label(' · synthetic, not measured', ' · 人工示意，非實測');
        for (const { metric, a, b } of gaugeFills) {
          // All domains are fixed by the six reviewed teaching schedules;
          // do not rescale A and B separately or imply empirical magnitudes.
          a.style.width = (100 * metric.at(pinnedTime) / metric.max) + '%';
          b.style.width = (100 * metric.at(time) / metric.max) + '%';
        }
      }
      function draw() {
        if (!svg) return;
        svg.setCurrentTime(Math.min(time, config.duration - 0.001));
        seek.value = String(Math.round(time / config.duration * 1000));
        // Expose the actual schematic computation rather than an opaque
        // 0–1000 position when a screen-reader user operates the timeline.
        // This is not an aria-live announcement on every animation frame.
        if (host.classList.contains('co-design-motion-timeline')) {
          seek.setAttribute('aria-valuetext', conciseState(time));
        }
        readout.textContent = time.toFixed(1) + ' / ' + config.duration + 's';
        if (interpretation.isConnected) interpretation.textContent = teachingState(time);
        updateComparison();
        if (comparePrevious) comparePrevious.disabled = previousStateTime(time) === null;
        for (const { button, event } of landmarkButtons) {
          // Highlight an actual discrete teaching state, never an arbitrary
          // nearest event that might be several numerical steps away.
          const active = match[1] === 'checkpoint-spacing'
            ? checkpointSpacing(time) === checkpointSpacing(event.t)
            : match[1] === 'gradscaler-feedback'
              ? feedbackIndex(time) === feedbackIndex(event.t)
              : fp16Frame(time) === fp16Frame(event.t);
          button.classList.toggle('is-current', active);
          if (active) button.setAttribute('aria-current', 'step');
          else button.removeAttribute('aria-current');
        }
        play.textContent = playing ? label('Ⅱ Pause', 'Ⅱ 暫停') : label('▶ Play', '▶ 播放');
        play.setAttribute('aria-label', playing ? label('Pause animation', '暫停動畫') : label('Play animation', '播放動畫'));
      }
      function stop(redraw = true) {
        playing = false;
        sweepTarget = null;
        if (raf) cancelAnimationFrame(raf);
        raf = 0; last = 0;
        // A seek/semantic jump draws its new state once after stopping.
        // Pausing without a new state still redraws the pause control.
        if (redraw) draw();
      }
      function setTime(t) {
        time = Math.max(0, Math.min(config.duration - 0.001, t));
        draw();
      }
      function tick(now) {
        if (!playing || !svg) return;
        if (last) {
          const elapsed = (now - last) / 1000 * speed;
          if (sweepTarget !== null) {
            const remaining = sweepTarget - time;
            const travel = elapsed * sweepRate;
            if (Math.abs(remaining) <= travel + 1e-6) {
              time = sweepTarget;
              stop(); // Leave B selected; unlike regular Play, never wrap.
              status.textContent = label('A→B illustrative scan complete; B selected.',
                                         'A→B 示意掃描完成，停留在 B。');
              return;
            }
            time += Math.sign(remaining) * travel;
          } else time += elapsed;
        }
        last = now;
        if (sweepTarget === null && time >= config.duration) time %= config.duration;
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
        stop(false);
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
        stop(false); setTime(0);
        status.textContent = interpretation.isConnected ? interpretation.textContent
          : label('Animation reset to start', '動畫已重設到起點');
      });
      pin?.addEventListener('click', () => {
        if (!svg) return;
        stop();
        pinnedTime = time;
        comparison.hidden = false;
        clearPin.hidden = false;
        swapPin.hidden = false;
        sweepPin.hidden = false;
        pin.textContent = label('Replace A', '更新 A');
        updateComparison();
        status.textContent = label('Pinned state A. Move the timeline to compare B.',
                                   '已釘選 A，移動時間軸即可比較 B。');
      });
      comparePrevious?.addEventListener('click', () => {
        if (!svg) return;
        const earlier = previousStateTime(time);
        if (earlier === null) return;
        stop();
        pinnedTime = earlier;
        comparison.hidden = false;
        clearPin.hidden = false;
        swapPin.hidden = false;
        sweepPin.hidden = false;
        pin.textContent = label('Replace A', '更新 A');
        updateComparison();
        status.textContent = label('Comparing the previous synthetic state A to current B.',
                                   '已比較前一個人工示意狀態 A 與目前狀態 B。');
      });
      // Reversing the comparison must reverse the signed B − A delta as
      // well as the displayed A/B positions, not just exchange text labels.
      swapPin?.addEventListener('click', () => {
        if (!svg || pinnedTime === null) return;
        stop();
        const previousA = pinnedTime;
        pinnedTime = time;
        setTime(previousA);
        status.textContent = label('Swapped A and B; signed differences now use the reversed order.',
                                   '已交換 A 與 B，差值方向也已反轉。');
      });
      // Show the trajectory between the pinned A and the currently selected B.
      // This is a UI sweep over fixed examples, not actual optimisation time.
      sweepPin?.addEventListener('click', () => {
        if (!svg || pinnedTime === null) return;
        const target = time;
        stop();
        if (Math.abs(target - pinnedTime) < 0.02) {
          status.textContent = label('A and B are identical; choose a different B to scan.',
                                     'A 與 B 相同，請先選擇其他 B。');
          return;
        }
        sweepTarget = target;
        sweepRate = Math.abs(target - pinnedTime) / 3; // 3s at 1×, both directions.
        time = pinnedTime;
        playing = true; last = 0;
        draw();
        status.textContent = label('Scanning illustrative states from A to B; Pause stops the scan.',
                                   '正在從 A 掃描示意狀態至 B；按暫停可停止掃描。');
        raf = requestAnimationFrame(tick);
      });
      guided?.addEventListener('change', () => {
        if (!svg || guided.value === '') return;
        const example = guidedCases[Number(guided.value)];
        if (!example) return;
        stop();
        pinnedTime = example.a;
        comparison.hidden = false;
        clearPin.hidden = false;
        swapPin.hidden = false;
        sweepPin.hidden = false;
        pin.textContent = label('Replace A', '更新 A');
        setTime(example.b);
        status.textContent = label('Loaded illustrative A/B comparison: ', '已選取人工 A/B 比較：') +
          label(example.en, example.tw) + '. ' + comparisonInsight(example.a, example.b);
        // Reset to placeholder so the same case can be selected again.
        guided.value = '';
      });
      clearPin?.addEventListener('click', () => {
        pinnedTime = null;
        comparison.hidden = true;
        clearPin.hidden = true;
        swapPin.hidden = true;
        sweepPin.hidden = true;
        pin.textContent = label('Pin A', '釘選 A');
        status.textContent = label('Pinned comparison cleared', '已清除釘選比較');
      });
      // Native range sliders advance 1/1000 of the 12-second animation per
      // Arrow press, effectively trapping keyboard readers inside one unchanged
      // numerical state. On the co-design figures, ordinary Left/Right instead
      // traverses the *next discrete mathematical state*. Shift+Left/Right
      // keeps native fine seeking, while Home/End retain native endpoints.
      if (host.classList.contains('co-design-motion-timeline')) {
        seek.addEventListener('keydown', event => {
          if (!svg || event.shiftKey || event.altKey || event.ctrlKey || event.metaKey ||
              !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
          event.preventDefault();
          const direction = event.key === 'ArrowRight' ? 1 : -1;
          let target;
          if (match[1] === 'fp16-scaling-window') {
            // There are 26 nonzero-width SMIL cells for 27 boundary samples;
            // seek just inside the cell to avoid a rounding boundary race.
            const index = Math.max(0, Math.min(25, fp16Frame(time) + direction));
            target = index === 0 ? 0 : (index + 0.12) * config.duration / 26;
          } else {
            const index = match[1] === 'checkpoint-spacing'
              ? Math.min(4, Math.floor(time / 2.4)) : feedbackIndex(time);
            target = config.steps[Math.max(0, Math.min(config.steps.length - 1, index + direction))];
          }
          stop(false); setTime(target);
          // aria-valuetext is synchronised by draw(); do not create a new
          // aria-live utterance for every repeated keypress.
        });
      }
      seek.addEventListener('input', () => {
        // A touch drag can emit dozens of input events each second. Keep the
        // SVG, aria-valuetext and text interpretation in sync immediately,
        // but do not flood the polite live region while the thumb is moving.
        const selected = Number(seek.value);
        stop(false); setTime(selected / 1000 * config.duration);
      });
      seek.addEventListener('change', () => {
        // Announce the selected mathematical state once the user commits the
        // seek (pointer release or a completed keyboard adjustment).
        if (!svg) return;
        status.textContent = interpretation.isConnected ? interpretation.textContent
          : label('Animation at ', '動畫時間 ') + time.toFixed(1) + 's';
      });
      rate.addEventListener('change', () => { speed = Number(rate.value); last = 0; });
      const onReduce = event => {
        stop();
        if (event.matches) {
          clearLoadTimer();
          retry.hidden = true;
          frame.hidden = true; bar.hidden = true;
          img.hidden = false;
          if (previousControls) previousControls.hidden = false;
          img.src = img.dataset.stillSrc || src.replace(/-motion\.svg(?=$|[?#])/, '-still.svg');
        } else if (svg) {
          retry.hidden = true;
          frame.removeAttribute('aria-hidden');
          img.src = src;
          img.hidden = true;
          frame.hidden = false; frame.style.visibility = '';
          frame.style.position = ''; frame.style.width = ''; frame.style.height = '';
          bar.hidden = false;
          if (previousControls) previousControls.hidden = true;
          setTime(time);
        } else if (!svg) {
          retry.hidden = true;
          // Keep the reviewed still visible until the SVG timeline is validated.
          // Switching out of reduced motion must not briefly expose an
          // unpausable animated <img> while the <object> request is pending.
          img.src = img.dataset.stillSrc || src.replace(/-motion\.svg(?=$|[?#])/, '-still.svg');
          img.hidden = false;
          frame.hidden = false;
          // Retry a deferred object navigation: its fallback HTML document
          // may have loaded while display:none, not the intended SVG.
          acceptingFrameLoad = true;
          frame.removeAttribute('data');
          frame.data = src;
          armLoadTimer();
          if (previousControls) previousControls.hidden = false;
        }
      };
      reduced.addEventListener('change', onReduce);
      // Initial reduced motion needs the same static fallback as a change.
      if (reduced.matches) onReduce({ matches: true });
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
      // Pause a timeline that is entirely outside the viewport. Co-design
      // controls sit BELOW their horizontal SVG scroller; both must leave
      // view before pausing, or a reader using controls on a phone would
      // accidentally stop the diagram while its controls remain visible.
      const viewportTargets = coDesignRegion ? [coDesignRegion, bar] : [host];
      const viewportVisible = new Map(viewportTargets.map(target => [target, true]));
      const viewportObserver = typeof IntersectionObserver === 'function'
        ? new IntersectionObserver(entries => {
            for (const entry of entries) viewportVisible.set(entry.target, entry.isIntersecting);
            if (playing && [...viewportVisible.values()].every(visible => !visible)) {
              stop();
              status.textContent = label('Animation paused while out of view',
                                         '動畫離開畫面，已暫停');
            }
          }, { threshold: 0 }) : null;
      for (const target of viewportTargets) viewportObserver?.observe(target);
      // A failed or invalid SVG <object> must never leave a blank diagram
      // alongside controls that appear to operate a nonexistent timeline.
      const showStaticFallback = () => {
        acceptingFrameLoad = false;
        clearLoadTimer();
        stop(false);
        retrying = false;
        retry.removeAttribute('aria-disabled');
        retry.textContent = label('Animation unavailable · Retry', '動畫無法載入 · 重試');
        retry.hidden = reduced.matches;
        svg = null;
        img.src = img.dataset.stillSrc || src.replace(/-motion\.svg(?=$|[?#])/, '-still.svg');
        img.hidden = false;
        // display:none may defer a subsequent object navigation.
        frame.hidden = reduced.matches;
        frame.setAttribute('aria-hidden', 'true');
        frame.style.visibility = 'hidden';
        frame.style.position = 'absolute';
        frame.style.width = '1px';
        frame.style.height = '1px';
        bar.hidden = true;
        if (previousControls) previousControls.hidden = false;
      };
      retry.addEventListener('click', () => {
        if (retrying || reduced.matches) return;
        retrying = true;
        acceptingFrameLoad = true;
        retry.textContent = label('Loading animation…', '動畫載入中…');
        retry.setAttribute('aria-disabled', 'true');
        frame.hidden = false;
        frame.style.visibility = 'hidden';
        frame.style.position = 'absolute';
        frame.style.width = '1px';
        frame.style.height = '1px';
        // Fetch the same reviewed asset, bypassing any cached transient error.
        const url = new URL(src, document.baseURI);
        url.searchParams.set('_motion_retry', String(++retryCount));
        // Chromium can stop navigating an <object> after a failed request.
        // A fresh host also isolates late events from the abandoned navigation.
        const abandoned = frame;
        frame = abandoned.cloneNode(true);
        bindFrameEvents(frame);
        frame.data = url.href;
        abandoned.replaceWith(frame);
        armLoadTimer();
      });
      const onFrameLoad = () => {
        if (!acceptingFrameLoad) return;
        clearLoadTimer();
        try {
          const root = frame.contentDocument?.documentElement;
          // A valid SVG can still be the *wrong* asset (e.g. a cached still).
          // Only co-design players require SMIL timeline elements; otherwise
          // interactive controls would claim to scrub a motionless document.
          const hasTeachingTimeline = !coDesignRegion || !!root?.querySelector(
            'animate, animateTransform, animateMotion, set');
          if (!root || root.namespaceURI !== 'http://www.w3.org/2000/svg' ||
              typeof root.pauseAnimations !== 'function' ||
              typeof root.setCurrentTime !== 'function' || !hasTeachingTimeline) {
            showStaticFallback();
            return;
          }
          svg = root;
          retrying = false;
          retry.removeAttribute('aria-disabled');
          const retryFocused = document.activeElement === retry;
          retry.hidden = true;
          retry.textContent = label('Animation unavailable · Retry', '動畫無法載入 · 重試');
          svg.pauseAnimations();
          // SVG <object> can reload after a reduced-motion toggle or document
          // navigation. Restore the reader's position and pinned A/B context;
          // restarting at zero silently changes the synthetic comparison.
          setTime(time);
          if (pin) pin.disabled = false;
          if (guided) guided.disabled = false;
          landmarkButtons.forEach(({ button }) => { button.disabled = false; });
          // Also capture a load that finishes while reduced motion is active:
          // otherwise turning motion back on can leave this player stranded.
          if (reduced.matches) return;
          img.hidden = true;
          frame.hidden = false;
          frame.style.visibility = '';
          frame.removeAttribute('aria-hidden');
          frame.style.position = ''; frame.style.width = ''; frame.style.height = '';
          bar.hidden = false;
          if (previousControls) previousControls.hidden = true;
          if (retryFocused) play.focus();
        } catch (_) { showStaticFallback(); }
      };
      const bindFrameEvents = candidate => {
        candidate.addEventListener('load', () => {
          if (candidate === frame && acceptingFrameLoad) onFrameLoad();
        });
        candidate.addEventListener('error', () => {
          if (candidate === frame && acceptingFrameLoad) showStaticFallback();
        });
      };
      bindFrameEvents(frame);
      if (!reduced.matches) armLoadTimer();
      const observer = new MutationObserver(() => {
        if (host.isConnected) return;
        clearLoadTimer();
        stop(); observer.disconnect(); reduced.removeEventListener('change', onReduce);
        document.removeEventListener('visibilitychange', onVisibility);
        viewportObserver?.disconnect();
        if (coDesignRegion) bar.remove();
        retry.remove();
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
