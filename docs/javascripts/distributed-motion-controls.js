/* Optional same-origin SMIL timeline controls for reviewed teaching diagrams.
 * Markdown and no-script readers retain the original image; no third-party SVG is fetched.
 */
(() => {
  'use strict';
  const sequences = {
    'gpipe-1f1b-schedule': { duration: 14, steps: [0, 1.02, 2.02, 3.02, 4.02, 5.02, 6.02, 7.02, 8.02, 9.02, 10.02, 11.02, 12.02] },
    'gpipe-activation-liveness': { duration: 14, steps: [0, 1.02, 2.02, 3.02, 4.02, 5.02, 6.02, 7.02, 8.02, 9.02, 10.02, 11.02, 12.02] },
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
      // The new GPipe diagrams retain native-width labels on narrow screens.
      // Their actual overflow owner must be keyboard-focusable in either motion mode.
      if (/^gpipe-(1f1b-schedule|activation-liveness)$/.test(match[1])) {
        host.classList.add('gpipe-comparison-timeline');
        host.tabIndex = 0;
        host.setAttribute('role', 'region');
        host.setAttribute('aria-label', zh ? '可水平捲動的管線排程圖，使用左右方向鍵' : 'Scrollable pipeline diagram; use Left and Right arrow keys');
      }
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
      // Independent of the Inf/NaN skip gate: both sampled gradients must
      // remain nonzero and finite in the idealized binary16 path.
      const pairWindow = k => k >= 3 && k <= 10;
      // Counterfactual FTZ at the binary16 gradient-storage boundary.
      // Even the largest sampled S=4096 leaves LOW at 2^-15 (< 2^-14,
      // the smallest normal). LOW needs S>=8192 to be normal, but HIGH
      // already overflows at S>=2048. No single scale preserves both
      // values when these subnormal outputs are flushed to zero.
      // Idealized binary16 rounding of S*g_low, followed by *FP32* division
      // by S. All example powers of two that survive rounding recover 2^-27
      // exactly; a skipped optimizer step is a separate condition.
      const unscaledLow = k => k <= 2 ? '0' : '2^-27';
      // A growth decision shows 2/2 at evaluation time, but resets the
      // counter *after* committing the scale update for the next iteration.
      const postDecisionStreak = [1, 0, 0, 1, 0, 0];
      // Running count of toy *eligible* steps; do not imply that an
      // optimizer ran or weights changed in this illustrative sequence.
      const eligibleSoFar = [1, 2, 2, 3, 4, 4];
      // Rendering only: accessible counts remain in interpretation and slider.
      const retentionTraceCells = [];
      const retentionTraceButtons = []; // Native navigation, synchronized to SVG.
      const policyWindowCells = [];
      let policyWindowDirection = null, policyScaleSelect = null, policySweepSelect = null;
      const paretoMapDots = [];
      // Fixed synthetic choices; peak-cap feasibility is not a GPU measurement.
      const checkpointChoices = [1, 2, 4, 8, 16].map(spacing => ({
        spacing, peak: 16 / spacing + spacing, rebuilt: 16 - 16 / spacing
      }));
      let paretoBudgetSelect = null, paretoBudgetLine = null, paretoBudgetReadout = null;
      let paretoReplaySelect = null, paretoReplayLine = null; // Independent replay-cost cap, same five sampled points.
      let paretoBudgetCompareButton = null; // Constrained, keyboard-operable A/B action.
      let paretoWitness = null; // Rendered only for a dominated sampled spacing.
      let paretoABPath = null; // Curved dotted link between pinned A and current B (not a trajectory).
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
        { en: 's=2 → s=8 · equal peak, more replay', tw: 's=2 → s=8 · 峰值相同、重算較多', a: 2.45, b: 7.25 },
        { en: 's=1 → s=16 · equal peak, extra replay', tw: 's=1 → s=16 · 峰值相同、重算增加', a: 0, b: 9.65 },
      ] : match[1] === 'fp16-scaling-window' ? [
        { en: 'S=4 → 8 · recover LOW', tw: 'S=4 → 8 · 小梯度恢復', a: 0.95, b: 1.42 },
        { en: 'S=1024 → 2048 · HIGH overflow', tw: 'S=1024 → 2048 · 大梯度溢位', a: 4.66, b: 5.12 },
        { en: 'S=2048 → 1024 · descending recovery', tw: 'S=2048 → 1024 · 下降時恢復有限', a: 6.52, b: 6.98 },
        { en: 'S=8 → 4 · descending underflow', tw: 'S=8 → 4 · 下降時再次歸零', a: 10.21, b: 10.67 },
      ] : match[1] === 'gradscaler-feedback' ? [
        { en: 't1 → t5 · finite-history effect', tw: 't1 → t5 · 歷史計數效應', a: 0, b: 8.05 },
        { en: 't2 → t3 · overflow backoff', tw: 't2 → t3 · 溢位回退', a: 2.05, b: 4.05 },
        { en: 't1 → t2 · finite streak grows', tw: 't1 → t2 · 連續通過後放大', a: 0, b: 2.05 },
        { en: 't3 → t4 · finite recovery holds', tw: 't3 → t4 · 恢復有限後維持', a: 4.05, b: 6.05 },
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
        { t: 1.42, en: 'LOW +', tw: '小值保留', hintEn: 'Ascending scale 8: small gradient first survives as a subnormal', hintTw: '上升至縮放 8：小梯度首次成為非零次正規數' },
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
        if (match[1] === 'gradscaler-feedback') {
          // Two hypothetical storage policies follow the same six checks;
          // colours do NOT represent measurements of a particular GPU.
          const trace = document.createElement('div');
          trace.className = 'distributed-motion-retention-trace';
          trace.setAttribute('role', 'group');
          trace.setAttribute('aria-label', label(
            'GradScaler iterations: ideal IEEE versus hypothetical FTZ low-gradient retention',
            'GradScaler 迭代：理想 IEEE 與假設 FTZ 的小梯度保留比較'));
          const header = document.createElement('div');
          header.className = 'distributed-motion-retention-row';
          header.append(document.createElement('span'));
          for (let i = 1; i <= 6; i++) {
            const step = document.createElement('button');
            step.type = 'button';
            step.className = 'distributed-motion-retention-step';
            step.textContent = 't' + i;
            step.disabled = true;
            const skipped = i === 3 || i === 6;
            step.setAttribute('aria-label', label(
              `Iteration ${i}, scale ${skipped ? 2048 : 1024}: ${skipped ? 'Inf check; optimizer step skipped' : 'eligible finite check; IEEE LOW retained, hypothetical FTZ LOW zero'}`,
              `第 ${i} 次迭代，縮放 ${skipped ? 2048 : 1024}：${skipped ? '偵測到 Inf，跳過最佳化器更新' : '通過有限值檢查；IEEE 保留小梯度，FTZ 假設使小梯度歸零'}`));
            step.addEventListener('click', () => {
              if (!svg) return;
              stop(false);
              setTime((i - 1) * 2 + 0.05);
              status.textContent = teachingState(time);
            });
            header.append(step);
            retentionTraceButtons.push(step);
          }
          trace.append(header);
          for (const policy of ['IEEE', 'FTZ']) {
            const lane = document.createElement('div');
            lane.className = 'distributed-motion-retention-row';
            lane.setAttribute('aria-hidden', 'true');
            const heading = document.createElement('strong');
            heading.className = 'distributed-motion-retention-label';
            heading.textContent = policy;
            lane.append(heading);
            const cells = [];
            for (let i = 0; i < 6; i++) {
              const cell = document.createElement('span');
              cell.className = 'distributed-motion-retention-cell';
              cell.dataset.state = 'future';
              lane.append(cell);
              cells.push(cell);
            }
            retentionTraceCells.push(cells);
            trace.append(lane);
          }
          const traceLegend = document.createElement('div');
          traceLegend.className = 'distributed-motion-retention-legend';
          traceLegend.setAttribute('aria-hidden', 'true');
          for (const [state, caption] of [
            ['retained', 'LOW +'], ['lost', 'LOW 0'], ['skipped', 'SKIP'],
            ['current', 'Selected B'], ['pinned', 'Pinned A']
          ]) {
            const item = document.createElement('span');
            item.className = 'distributed-motion-retention-legend-item';
            const swatch = document.createElement('span');
            swatch.className = 'distributed-motion-retention-legend-swatch';
            swatch.dataset.state = state;
            item.append(swatch, document.createTextNode(caption));
            traceLegend.append(item);
          }
          trace.append(traceLegend);
          bar.append(trace);
        }
        if (match[1] === 'fp16-scaling-window') {
          // Two native selectors let readers inspect any of the 13 scales in
          // either sweep direction without 26 fine-grained slider key presses.
          // Both navigate the original SVG time axis, not a duplicate model.
          const selector = document.createElement('div');
          selector.className = 'distributed-motion-policy-jump';
          const scaleLabel = document.createElement('label');
          scaleLabel.textContent = label('Scale', '縮放係數');
          policyScaleSelect = document.createElement('select');
          policyScaleSelect.className = 'distributed-motion-policy-scale';
          policyScaleSelect.disabled = true;
          for (let k = 0; k <= 12; k++) {
            const option = document.createElement('option');
            option.value = String(k);
            option.textContent = 'S=' + (2 ** k);
            policyScaleSelect.append(option);
          }
          scaleLabel.append(policyScaleSelect);
          const sweepLabel = document.createElement('label');
          sweepLabel.textContent = label('Sweep', '掃描方向');
          policySweepSelect = document.createElement('select');
          policySweepSelect.className = 'distributed-motion-policy-sweep';
          policySweepSelect.disabled = true;
          for (const [value, en, tw] of [
            ['up', 'Ascending ↑', '上升 ↑'],
            ['down', 'Descending ↓', '下降 ↓']
          ]) {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = label(en, tw);
            policySweepSelect.append(option);
          }
          sweepLabel.append(policySweepSelect);
          selector.append(scaleLabel, sweepLabel);
          // Hypothetical binary16 storage FTZ versus ideal IEEE subnormals;
          // the SVG and all controls still share one timeline.
          const panel = document.createElement('section');
          panel.className = 'distributed-motion-policy-window';
          panel.setAttribute('aria-hidden', 'true');
          const heading = document.createElement('div');
          heading.className = 'distributed-motion-policy-heading';
          const textLabel = document.createElement('span');
          textLabel.textContent = 'FP16 PAIR · IEEE / FTZ';
          policyWindowDirection = document.createElement('span');
          policyWindowDirection.className = 'distributed-motion-policy-direction';
          heading.append(textLabel, policyWindowDirection);
          panel.append(heading);
          const ticks = document.createElement('div');
          ticks.className = 'distributed-motion-policy-row';
          const kLabel = document.createElement('strong');
          kLabel.className = 'distributed-motion-policy-label';
          kLabel.textContent = '2^k';
          ticks.append(kLabel);
          for (let k = 0; k <= 12; k++) {
            const tick = document.createElement('span');
            tick.className = 'distributed-motion-policy-tick';
            tick.textContent = [0, 3, 6, 10, 12].includes(k) ? String(k) : '';
            ticks.append(tick);
          }
          panel.append(ticks);
          for (const policy of ['IEEE', 'FTZ']) {
            const row = document.createElement('div');
            row.className = 'distributed-motion-policy-row';
            const policyLabel = document.createElement('strong');
            policyLabel.className = 'distributed-motion-policy-label';
            policyLabel.textContent = policy;
            row.append(policyLabel);
            const cells = [];
            for (let k = 0; k <= 12; k++) {
              const cell = document.createElement('span');
              cell.className = 'distributed-motion-policy-cell';
              cell.dataset.exponent = String(k);
              cell.dataset.state = k >= 11 ? 'overflow'
                : policy === 'IEEE' && pairWindow(k) ? 'valid' : 'underflow';
              row.append(cell);
              cells.push(cell);
            }
            policyWindowCells.push(cells);
            panel.append(row);
          }
          // A small in-panel key explains texture and the current outline
          // without forcing a reader to scroll to the bilingual prose.
          // The entire visual panel remains aria-hidden: the localized slider
          // value and interpretation are the authoritative accessible reading.
          const legend = document.createElement('div');
          legend.className = 'distributed-motion-policy-legend';
          for (const [state, caption] of [
            ['underflow', 'LOW 0'],
            ['valid', 'PAIR nonzero'],
            ['overflow', 'HIGH Inf'],
            ['current', 'Selected'],
            ['pinned', 'Pinned A'],
          ]) {
            const item = document.createElement('span');
            item.className = 'distributed-motion-policy-legend-item';
            const swatch = document.createElement('span');
            swatch.className = 'distributed-motion-policy-legend-swatch';
            swatch.dataset.state = state;
            item.append(swatch, document.createTextNode(caption));
            legend.append(item);
          }
          panel.append(legend);
          bar.append(selector, panel);
        }
        if (match[1] === 'checkpoint-spacing') {
          // A second, synchronised view exposes the sampled Pareto frontier:
          // x = peak *simultaneously live* activation slots, y = total
          // reconstructed activations. It is not a benchmark or GPU profile.
          const map = document.createElement('section');
          map.className = 'distributed-motion-pareto';
          map.setAttribute('role', 'group');
          map.setAttribute('aria-label', label('Five-choice checkpoint memory and recomputation map',
                                             '五種檢查點配置的記憶體與重算量地圖'));
          const heading = document.createElement('p');
          heading.className = 'distributed-motion-pareto-title';
          heading.textContent = label('Peak storage × total replay (schematic)',
                                      '峰值儲存 × 總重建量（示意）');
          const plot = document.createElement('div');
          plot.className = 'distributed-motion-pareto-plot';
          const curve = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
          curve.classList.add('distributed-motion-pareto-line');
          curve.setAttribute('viewBox', '0 0 100 100');
          curve.setAttribute('preserveAspectRatio', 'none');
          curve.setAttribute('aria-hidden', 'true');
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
          const choices = checkpointChoices.map((choice, i) => ({ ...choice, i }));
          line.setAttribute('points', choices.slice(0, 3).map(choice =>
            (10 + 80 * choice.peak / 17).toFixed(3) + ',' +
            (90 - 80 * choice.rebuilt / 15).toFixed(3)).join(' '));
          paretoBudgetLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          paretoBudgetLine.classList.add('distributed-motion-pareto-budget-line');
          paretoBudgetLine.setAttribute('y1', '10');
          paretoBudgetLine.setAttribute('y2', '90');
          paretoReplayLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          paretoReplayLine.classList.add('distributed-motion-pareto-replay-line');
          paretoReplayLine.setAttribute('x1', '10');
          paretoReplayLine.setAttribute('x2', '90');
          // A state-dependent witness is distinct from the sampled frontier:
          // s=2 dominates s=8 at equal PEAK and also dominates s=16 in
          // both modelled costs. The diagram does not draw an optimiser path.
          const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
          const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
          const markerId = 'co-design-witness-' +
            (document.querySelectorAll('.distributed-motion-pareto').length + 1);
          marker.setAttribute('id', markerId);
          marker.setAttribute('markerWidth', '7');
          marker.setAttribute('markerHeight', '7');
          marker.setAttribute('refX', '5');
          marker.setAttribute('refY', '3');
          marker.setAttribute('orient', 'auto');
          const arrowHead = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          arrowHead.setAttribute('d', 'M0 0 6 3 0 6');
          arrowHead.setAttribute('fill', 'none');
          arrowHead.setAttribute('stroke', '#ac6731');
          arrowHead.setAttribute('stroke-width', '1.7');
          marker.append(arrowHead); defs.append(marker);
          paretoWitness = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          paretoWitness.classList.add('distributed-motion-pareto-witness');
          paretoWitness.setAttribute('marker-end', 'url(#' + markerId + ')');
          paretoWitness.style.display = 'none';
          paretoABPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          paretoABPath.classList.add('distributed-motion-pareto-ab');
          paretoABPath.style.display = 'none';
          // Draw behind the dominance witness; never imply an optimisation direction.
          curve.append(defs, paretoBudgetLine, paretoReplayLine, line, paretoABPath, paretoWitness);
          plot.append(curve);
          const budgetLabel = document.createElement('label');
          budgetLabel.className = 'distributed-motion-budget-control';
          budgetLabel.append(document.createTextNode(label('Memory cap (slots)', '記憶體上限（槽）')));
          paretoBudgetSelect = document.createElement('input');
          paretoBudgetSelect.type = 'range';
          paretoBudgetSelect.min = '8';
          paretoBudgetSelect.max = '17';
          paretoBudgetSelect.step = '1';
          paretoBudgetSelect.value = '10';
          paretoBudgetSelect.disabled = true; // enable only after SVG verification
          budgetLabel.append(paretoBudgetSelect);
          const replayLabel = document.createElement('label');
          replayLabel.className = 'distributed-motion-budget-control distributed-motion-replay-control';
          replayLabel.append(document.createTextNode(label('Replay cap (rebuilt)', '重建上限（個）')));
          paretoReplaySelect = document.createElement('input');
          paretoReplaySelect.type = 'range';
          paretoReplaySelect.min = '0';
          paretoReplaySelect.max = '15';
          paretoReplaySelect.step = '1';
          paretoReplaySelect.value = '15'; // Default keeps the prior memory-only lesson intact.
          paretoReplaySelect.disabled = true;
          replayLabel.append(paretoReplaySelect);
          // Compare the selected state A with the least-replay feasible B,
          // without introducing another animation timeline.
          const budgetActions = document.createElement('div');
          budgetActions.className = 'distributed-motion-budget-actions';
          paretoBudgetCompareButton = document.createElement('button');
          paretoBudgetCompareButton.type = 'button';
          paretoBudgetCompareButton.className = 'distributed-motion-budget-compare';
          paretoBudgetCompareButton.textContent = label('Compare current → best feasible',
                                                       '比較目前 → 最佳可行');
          paretoBudgetCompareButton.disabled = true;
          budgetActions.append(paretoBudgetCompareButton);
          paretoBudgetReadout = document.createElement('p');
          paretoBudgetReadout.className = 'distributed-motion-budget-readout';
          paretoBudgetReadout.setAttribute('aria-live', 'off');
          for (const choice of choices) {
            const dot = document.createElement('button');
            dot.type = 'button';
            dot.className = 'distributed-motion-pareto-dot';
            dot.dataset.spacing = String(choice.spacing);
            dot.dataset.frontier = String(choice.i < 3);
            dot.style.left = (10 + 80 * choice.peak / 17) + '%';
            dot.style.bottom = (10 + 80 * choice.rebuilt / 15) + '%';
            dot.textContent = String(choice.spacing);
            dot.disabled = true; // never advertise seeking before SVG verification
            dot.setAttribute('aria-label', label(
              'Select spacing ' + choice.spacing + ': peak ' + choice.peak +
              ' slots, rebuilt ' + choice.rebuilt + '; ' +
              (choice.i < 3 ? 'Pareto frontier' : 'dominated'),
              '選取間距 ' + choice.spacing + '：峰值 ' + choice.peak +
              ' 槽、重建 ' + choice.rebuilt + '；' +
              (choice.i < 3 ? '非支配解' : '被其他設定支配')));
            dot.addEventListener('click', () => {
              if (!svg) return;
              stop(false);
              setTime(config.steps[choice.i]);
              status.textContent = interpretation.textContent;
            });
            paretoMapDots.push({ button: dot, spacing: choice.spacing });
            plot.append(dot);
          }
          const x = document.createElement('span'), y = document.createElement('span');
          x.className = 'distributed-motion-pareto-axis-x';
          y.className = 'distributed-motion-pareto-axis-y';
          x.textContent = 'PEAK →';
          y.textContent = 'REBUILT ↑';
          plot.append(x, y);
          const legend = document.createElement('div');
          legend.className = 'distributed-motion-pareto-legend';
          legend.textContent = label('Solid: frontier · Dashed: dominated · Ring: selected · Amber: pinned A · Violet curve: A/B · Violet vertical/blue horizontal: caps · Arrow: dominance',
                                     '實線點：非支配 · 虛線點：被支配 · 外框：目前 · 琥珀框：釘選 A · 紫色弧線：A/B · 紫色直線／藍色橫線：雙上限 · 箭頭：支配見證');
          map.append(heading, budgetLabel, replayLabel, budgetActions, plot, legend, paretoBudgetReadout);
          bar.append(map);
        }
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
          const witnessEn = spacing === 8 ? ' · s=2 witness: PEAK 10=10; REBUILT 8<14'
            : spacing === 16 ? ' · s=2 witness: PEAK 10<17; REBUILT 8<15' : '';
          const witnessTw = spacing === 8 ? ' · s=2 支配此設定：峰值同為 10、重建量 8<14'
            : spacing === 16 ? ' · s=2 支配此設定：峰值 10<17、重建量 8<15' : '';
          return label(
            `s=${spacing} · KEEP ${keep} + REBUILD ${scratch} = PEAK ${keep + scratch} · TOTAL REBUILT ${totalRebuilt} (all segments) · FWD LAYER EVALS ${16 + totalRebuilt} (initial + replay) · active replay ${replayed}/${scratch} (last segment; example slots) · ${spacing <= 4 ? 'PARETO FRONTIER' : 'DOMINATED'} (five choices)${witnessEn}`,
            `s=${spacing} · 保留 ${keep} + 重算暫存 ${scratch} = 峰值 ${keep + scratch} · 全區段重建總數 ${totalRebuilt} · 前向層計算 ${16 + totalRebuilt}（初次加重算）· 末段重算進度 ${replayed}/${scratch}（示意槽位）· ${spacing <= 4 ? '非支配解' : '被其他設定支配'}（限五種選項）${witnessTw}`
          );
        }
        if (match[1] === 'fp16-scaling-window') {
          // 27 equal discrete SMIL frames: 0..12, 12..0, final 0.
          const exponent = scaleExponent(t);
          const scale = 2 ** exponent;
          const low = exponent <= 2 ? '0' : 'subnormal';
          const high = exponent >= 11 ? 'Inf' : 'finite';
          return label(
            `S=2^${exponent} (${scale}) · LOW ${low}${low === '0' ? ' (silent underflow)' : ''} · HIGH ${high} · ${exponent >= 11 ? 'SKIP' : 'STEP ELIGIBLE'} · PAIR WINDOW ${pairWindow(exponent) ? 'YES' : 'NO'} · FTZ LOW 0 · FTZ PAIR NO · IEEE/FTZ MISMATCH ${pairWindow(exponent) ? 'YES' : 'NO'} · LOW AFTER FP32 UNSCALE ${unscaledLow(exponent)}${exponent >= 11 ? ' (step skipped)' : ''} (example)`,
            `S=2^${exponent}（${scale}）· 小梯度${low === '0' ? '歸零（仍為有限值）' : '非零次正規'} · 大梯度${high === 'Inf' ? '溢位' : '有限'} · ${exponent >= 11 ? '跳過更新' : '符合更新條件'} · 兩筆均非零有限：${pairWindow(exponent) ? '是' : '否'} · 沖零假設：小梯度 0、兩筆非零有限 否 · IEEE／沖零判斷相異：${pairWindow(exponent) ? '是' : '否'} · FP32 還原小梯度 ${unscaledLow(exponent)}${exponent >= 11 ? '（跳過更新）' : ''}（示意）`
          );
        }
        if (match[1] === 'gradscaler-feedback') {
          const i = Math.min(5, Math.floor(t / 2));
          const current = [1024, 1024, 2048, 1024, 1024, 2048][i];
          const following = [1024, 2048, 1024, 1024, 2048, 1024][i];
          const check = i === 2 || i === 5 ? 'Inf' : 'finite';
          const streak = [1, 2, 0, 1, 2, 0][i];
          return label(
            `t${i + 1} · S ${current} → NEXT ${following} · ${check} · ${check === 'Inf' ? 'SKIP / reset' : 'STEP ELIGIBLE'} · ${check === 'Inf' ? 'backoff' : streak === 2 ? 'grow after 2/2; counter resets to 0' : 'streak 1/2'} · POST-DECISION STREAK ${postDecisionStreak[i]}/2 · ELIGIBLE SO FAR ${eligibleSoFar[i]} (example) · ELIGIBLE LOW KEPT: IEEE ${eligibleSoFar[i]} / FTZ 0 (hypothetical storage)`,
            `t${i + 1} · 當次 ${current} → 下次 ${following} · ${check === 'Inf' ? '溢位、跳過並重設' : '通過非有限值檢查、符合更新條件'} · ${check === 'Inf' ? '縮小係數' : streak === 2 ? '連續通過 2/2，放大後計數歸零' : '連續通過 1/2'} · 決策後計數 ${postDecisionStreak[i]}/2 · 累計符合更新條件 ${eligibleSoFar[i]} 次（示意）· 符合條件且小梯度非零累計：IEEE ${eligibleSoFar[i]}／沖零假設 0`
          );
        }
        return '';
      }
      function conciseState(t) {
        if (match[1] === 'checkpoint-spacing') {
          const spacing = [1, 2, 4, 8, 16][Math.min(4, Math.floor(t / 2.4))];
          const peak = 16 / spacing + spacing;
          const total = 16 - 16 / spacing;
          return label(`s=${spacing} · PEAK ${peak} · TOTAL REBUILT ${total} · FWD EVALS ${16 + total} · ${spacing <= 4 ? 'FRONTIER' : 'DOMINATED'}`,
                       `s=${spacing} · 峰值 ${peak} · 全區段重建 ${total} · 前向層計算 ${16 + total} · ${spacing <= 4 ? '非支配' : '被支配'}`);
        }
        if (match[1] === 'fp16-scaling-window') {
          const k = scaleExponent(t);
          return label(`S=${2 ** k} · LOW ${k <= 2 ? '0' : 'subnormal'} · HIGH ${k >= 11 ? 'Inf' : 'finite'} · ${k >= 11 ? 'SKIP' : 'ELIGIBLE'} · PAIR WINDOW ${pairWindow(k) ? 'YES' : 'NO'} · FTZ PAIR NO · IEEE/FTZ MISMATCH ${pairWindow(k) ? 'YES' : 'NO'} · LOW UNSCALED ${unscaledLow(k)}`,
                       `S=${2 ** k} · 小梯度${k <= 2 ? '歸零' : '次正規'} · 大梯度${k >= 11 ? '溢位' : '有限'} · ${k >= 11 ? '跳過' : '符合更新條件'} · 兩筆非零有限 ${pairWindow(k) ? '是' : '否'} · 沖零假設兩筆非零 否 · IEEE／沖零判斷相異 ${pairWindow(k) ? '是' : '否'} · 還原小梯度 ${unscaledLow(k)}`);
        }
        const i = Math.min(5, Math.floor(t / 2));
        const s = [1024, 1024, 2048, 1024, 1024, 2048][i];
        const next = [1024, 2048, 1024, 1024, 2048, 1024][i];
        const skip = i === 2 || i === 5;
        return label(`t${i + 1} · S ${s} → ${next} · ${skip ? 'SKIP' : 'ELIGIBLE'} · ELIGIBLE SO FAR ${eligibleSoFar[i]} · ELIGIBLE LOW KEPT IEEE/FTZ ${eligibleSoFar[i]}/0`,
                     `t${i + 1} · 縮放 ${s} → ${next} · ${skip ? '跳過' : '符合更新條件'} · 累計符合更新條件 ${eligibleSoFar[i]} 次 · 符合條件且保留小梯度 IEEE／沖零 ${eligibleSoFar[i]}／0`);
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
          return label(`B − A: Δ PEAK ${signed(peakB - peakA)} slots · Δ TOTAL REBUILT ${signed(totalB - totalA)} · Δ FWD EVALS ${signed(totalB - totalA)}`,
                       `B − A：峰值 ${signed(peakB - peakA)} 槽 · 全區段重建 ${signed(totalB - totalA)} · 前向層計算 Δ ${signed(totalB - totalA)}`);
        }
        if (match[1] === 'fp16-scaling-window') {
          const x = scaleExponent(a), y = scaleExponent(b);
          const result = k => k >= 11 ? 'SKIP' : 'ELIGIBLE';
          const low = k => k <= 2 ? '0' : 'subnormal';
          const high = k => k >= 11 ? 'Inf' : 'finite';
          // A rounded zero is finite: it loses information but does not
          // trigger the nonfinite step gate. Compare both rounded inputs.
          return label(`Outcome: ${result(x)} → ${result(y)} · LOW ${low(x)} → ${low(y)} · HIGH ${high(x)} → ${high(y)} · scale exponent ${x} → ${y} (Δ ${signed(y - x)}) · PAIR WINDOW ${pairWindow(x) ? 'YES' : 'NO'} → ${pairWindow(y) ? 'YES' : 'NO'} · IEEE/FTZ MISMATCH ${pairWindow(x) ? 'YES' : 'NO'} → ${pairWindow(y) ? 'YES' : 'NO'} · FTZ PAIR NO → NO · LOW AFTER UNSCALE ${unscaledLow(x)} → ${unscaledLow(y)}`,
                       `更新資格：${result(x) === 'SKIP' ? '跳過' : '符合'} → ${result(y) === 'SKIP' ? '跳過' : '符合'} · 小梯度 ${low(x)} → ${low(y)} · 大梯度 ${high(x)} → ${high(y)} · 指數 ${x} → ${y}（Δ ${signed(y - x)}）· 兩筆均非零有限 ${pairWindow(x) ? '是' : '否'} → ${pairWindow(y) ? '是' : '否'} · IEEE／沖零判斷相異 ${pairWindow(x) ? '是' : '否'} → ${pairWindow(y) ? '是' : '否'} · 沖零假設兩筆非零 否 → 否 · 還原小梯度 ${unscaledLow(x)} → ${unscaledLow(y)}`);
        }
        const index = t => Math.min(5, Math.floor(t / 2));
        const skipped = i => i === 2 || i === 5;
        // Decision-time counts: a 2/2 check triggers growth then resets.
        // Inf also resets the tracker; these are not post-update counts.
        const streak = [1, 2, 0, 1, 2, 0];
        const nextScale = [1024, 2048, 1024, 1024, 2048, 1024];
        const ia = index(a), ib = index(b);
        return label(`Finite check: ${skipped(ia) ? 'SKIP' : 'ELIGIBLE'} → ${skipped(ib) ? 'SKIP' : 'ELIGIBLE'} · streak ${streak[ia]}/2 → ${streak[ib]}/2 · NEXT S ${nextScale[ia]} → ${nextScale[ib]} (Δ ${signed(nextScale[ib] - nextScale[ia])}) · POST-DECISION ${postDecisionStreak[ia]}/2 → ${postDecisionStreak[ib]}/2 · ELIGIBLE SO FAR ${eligibleSoFar[ia]} → ${eligibleSoFar[ib]} (Δ ${signed(eligibleSoFar[ib] - eligibleSoFar[ia])}) · ELIGIBLE LOW KEPT IEEE ${eligibleSoFar[ia]} → ${eligibleSoFar[ib]} / FTZ 0 → 0`,
                     `有限值檢查：${skipped(ia) ? '跳過' : '符合更新條件'} → ${skipped(ib) ? '跳過' : '符合更新條件'} · 連續通過 ${streak[ia]}/2 → ${streak[ib]}/2 · 下次縮放 ${nextScale[ia]} → ${nextScale[ib]}（Δ ${signed(nextScale[ib] - nextScale[ia])}）· 決策後 ${postDecisionStreak[ia]}/2 → ${postDecisionStreak[ib]}/2 · 累計符合更新條件 ${eligibleSoFar[ia]} → ${eligibleSoFar[ib]}（Δ ${signed(eligibleSoFar[ib] - eligibleSoFar[ia])}）· 符合條件且小梯度保留 IEEE ${eligibleSoFar[ia]} → ${eligibleSoFar[ib]}／沖零假設 0 → 0`);
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
            return label('B Pareto-dominates A (no worse on either cost).', 'B 在雙成本上 Pareto 支配 A（皆不劣且至少一項更好）。');
          }
          if (dPeak >= 0 && dReplay >= 0) {
            return label('A Pareto-dominates B (no worse on either cost).', 'A 在雙成本上 Pareto 支配 B（皆不劣且至少一項更好）。');
          }
          return label('Memory–recomputation trade-off.', '記憶體與重算量存在取捨。');
        }
        if (match[1] === 'fp16-scaling-window') {
          const regime = k => k <= 2
            ? label('LOW ZERO', '小梯度歸零')
            : k >= 11 ? label('HIGH INF', '大梯度溢位')
              : label('LOW SUBNORMAL, HIGH FINITE', '小梯度次正規、大梯度有限');
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
        for (const { button, spacing } of paretoMapDots) {
          button.classList.toggle('is-pinned', pinnedTime !== null && checkpointSpacing(pinnedTime) === spacing);
        }
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
        if (paretoBudgetLine && paretoBudgetSelect && paretoReplayLine &&
            paretoReplaySelect && paretoBudgetReadout) {
          const cap = Number(paretoBudgetSelect.value);
          const replayCap = Number(paretoReplaySelect.value);
          const feasible = checkpointChoices.filter(choice =>
            choice.peak <= cap && choice.rebuilt <= replayCap
          ).sort((a, b) => a.rebuilt - b.rebuilt);
          // Two independent upper bounds may have an empty intersection.
          const best = feasible[0] || null;
          const cutoff = (10 + 80 * cap / 17).toFixed(3);
          const replayCutoff = (90 - 80 * replayCap / 15).toFixed(3);
          paretoBudgetLine.setAttribute('x1', cutoff);
          paretoBudgetLine.setAttribute('x2', cutoff);
          paretoReplayLine.setAttribute('y1', replayCutoff);
          paretoReplayLine.setAttribute('y2', replayCutoff);
          for (const { button, spacing } of paretoMapDots) {
            const choice = checkpointChoices.find(candidate => candidate.spacing === spacing);
            button.dataset.feasible = String(choice.peak <= cap && choice.rebuilt <= replayCap);
            button.dataset.best = String(Boolean(best) && spacing === best.spacing);
          }
          const result = best ? label(
            'least replay s=' + best.spacing + ' (' + best.peak +
              ' peak, ' + best.rebuilt + ' rebuilt).',
            '重建最少為 s=' + best.spacing + '（峰值 ' +
              best.peak + '、重建 ' + best.rebuilt + '）。'
          ) : label('no feasible sampled choice satisfies both caps.',
                    '沒有取樣配置同時符合兩項上限。');
          paretoBudgetReadout.textContent = label(
            'Caps ' + cap + ' slots / ' + replayCap + ' rebuilt: ' +
              feasible.length + '/5 feasible; ',
            '上限 ' + cap + ' 槽／' + replayCap + ' 個重建：5 種中有 ' +
              feasible.length + ' 種可行；'
          ) + result;
          const accessibleResult = best ? label('best feasible s=' + best.spacing,
            '可行配置中重建最少 s=' + best.spacing) :
            label('no feasible sampled choice', '沒有可行的取樣配置');
          paretoBudgetSelect.setAttribute('aria-valuetext', label(cap + ' slots', cap + ' 槽') +
            '; ' + accessibleResult);
          paretoReplaySelect.setAttribute('aria-valuetext',
            label(replayCap + ' rebuilt maximum', '最多重建 ' + replayCap + ' 個') +
            '; ' + accessibleResult);
          if (paretoBudgetCompareButton) {
            const current = checkpointSpacing(time);
            paretoBudgetCompareButton.disabled = !best || current === best.spacing;
            paretoBudgetCompareButton.setAttribute('aria-label', best ? label(
              'Pin current s=' + current + ' as A; compare to best feasible s=' +
                best.spacing + ' under both caps',
              '將目前 s=' + current + ' 釘選為 A，與兩項上限下最佳可行 s=' +
                best.spacing + ' 比較'
            ) : label('No sampled choice satisfies both caps; comparison unavailable',
                      '沒有同時符合兩項上限的取樣配置，無法比較'));
          }
        }
        for (const { button, spacing } of paretoMapDots) {
          const active = checkpointSpacing(time) === spacing;
          button.classList.toggle('is-current', active);
          if (active) button.setAttribute('aria-current', 'true');
          else button.removeAttribute('aria-current');
        }
        if (paretoWitness) {
          const selected = checkpointSpacing(time);
          if (selected === 8 || selected === 16) {
            // Coordinates match the sampled points; shorten the shaft to
            // keep the arrowhead outside the s=2 button even at phone width.
            const point = s => ({
              x: 10 + 80 * (16 / s + s) / 17,
              y: 90 - 80 * (16 - 16 / s) / 15
            });
            const from = point(selected), to = point(2);
            for (const [attribute, value] of [
              ['x1', from.x + .15 * (to.x - from.x)],
              ['y1', from.y + .15 * (to.y - from.y)],
              ['x2', from.x + .78 * (to.x - from.x)],
              ['y2', from.y + .78 * (to.y - from.y)]
            ]) paretoWitness.setAttribute(attribute, value.toFixed(3));
            paretoWitness.style.display = '';
          } else paretoWitness.style.display = 'none';
        }
        if (paretoABPath) {
          const spacingA = pinnedTime === null ? null : checkpointSpacing(pinnedTime);
          const spacingB = checkpointSpacing(time);
          if (spacingA !== null && spacingA !== spacingB) {
            const position = s => ({
              x: 10 + 80 * (16 / s + s) / 17,
              y: 90 - 80 * (16 - 16 / s) / 15
            });
            const a = position(spacingA), b = position(spacingB);
            const dx = b.x - a.x, dy = b.y - a.y;
            const distance = Math.hypot(dx, dy) || 1;
            // The small perpendicular bend keeps A/B distinguishable from
            // the straight amber dominance witness at equal PEAK; it is only
            // a UI connector, not a cost function or time/optimisation path.
            const midX = (a.x + b.x) / 2 - 8 * dy / distance;
            const midY = (a.y + b.y) / 2 + 8 * dx / distance;
            paretoABPath.setAttribute('d',
              `M ${a.x.toFixed(3)} ${a.y.toFixed(3)} Q ${midX.toFixed(3)} ${midY.toFixed(3)} ${b.x.toFixed(3)} ${b.y.toFixed(3)}`);
            paretoABPath.style.display = '';
          } else {
            paretoABPath.removeAttribute('d');
            paretoABPath.style.display = 'none';
          }
        }
        if (policyWindowCells.length) {
          const exponent = scaleExponent(time);
          const exponentA = pinnedTime === null ? null : scaleExponent(pinnedTime);
          const sweepDirection = fp16Frame(time) <= 12 ? 'up' : 'down';
          policyWindowDirection.textContent = 'S=2^' + exponent +
            (sweepDirection === 'up' ? ' ↑' : ' ↓');
          // Playback, seek and Pin A/B all share this state.
          policyScaleSelect.value = String(exponent);
          policySweepSelect.value = sweepDirection;
          for (const cells of policyWindowCells) {
            cells.forEach((cell, k) => {
              if (k === exponent) cell.dataset.current = 'true';
              else delete cell.dataset.current;
              if (k === exponentA) cell.dataset.pinned = 'true';
              else delete cell.dataset.pinned;
            });
          }
        }
        if (retentionTraceCells.length) {
          const current = feedbackIndex(time);
          const pinned = pinnedTime === null ? null : feedbackIndex(pinnedTime);
          retentionTraceButtons.forEach((button, i) => {
            const active = i === current;
            button.classList.toggle('is-current', active);
            button.classList.toggle('is-pinned', i === pinned);
            if (active) button.setAttribute('aria-current', 'step');
            else button.removeAttribute('aria-current');
          });
          retentionTraceCells.forEach((cells, policy) => {
            cells.forEach((cell, i) => {
              // Cyan: nonzero IEEE low; hatched amber: FTZ silently lost low.
              // A skipped nonfinite check appears in BOTH policy lanes.
              cell.dataset.state = i > current ? 'future'
                : (i === 2 || i === 5) ? 'skipped'
                  : policy === 0 ? 'retained' : 'lost';
              if (i === current) cell.dataset.current = 'true';
              else delete cell.dataset.current;
              if (i === pinned) cell.dataset.pinned = 'true';
              else delete cell.dataset.pinned;
            });
          });
        }
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
        else {
          // A click dispatched while the player is offscreen or the tab is
          // hidden must not restart an otherwise paused SMIL timeline.
          if (!canStartMotion()) {
            status.textContent = label('Scroll the diagram or controls into view to play.',
                                       '請先捲動至動畫或控制列，再開始播放。');
            return;
          }
          playing = true; last = 0; draw(); raf = requestAnimationFrame(tick);
        }
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
        draw(); // The plotted baseline markers must appear immediately on Pin A.
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
        draw(); // Previous-state baseline is also a visual state.
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
        // The A→B scan is motion too; it must obey exactly the same
        // visibility and reduced-motion policy as ordinary playback.
        if (!canStartMotion()) {
          status.textContent = label('Scroll the diagram or controls into view to scan A→B.',
                                     '請先捲動至動畫或控制列，再進行 A→B 掃描。');
          return;
        }
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
        updateComparison();
        draw(); // Remove A/B link and pinned FTZ/IEEE markers on Clear A.
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
      const jumpToPolicyChoice = () => {
        if (!svg || !policyScaleSelect || !policySweepSelect) return;
        const exponent = Number(policyScaleSelect.value);
        // Frames 0..12 ascend; 13..25 descend from 12 to 0.
        // The small offset lands inside a discrete SMIL state.
        const index = policySweepSelect.value === 'up' ? exponent : 25 - exponent;
        stop(false);
        setTime(index === 0 ? 0 : (index + 0.12) * config.duration / 26);
        status.textContent = teachingState(time);
      };
      policyScaleSelect?.addEventListener('change', jumpToPolicyChoice);
      policySweepSelect?.addEventListener('change', jumpToPolicyChoice);
      paretoBudgetSelect?.addEventListener('input', () => {
        // Reuse the same sampled points; no second animation clock.
        draw();
      });
      paretoBudgetSelect?.addEventListener('change', () => {
        status.textContent = paretoBudgetReadout?.textContent || '';
      });
      paretoReplaySelect?.addEventListener('input', () => draw());
      paretoReplaySelect?.addEventListener('change', () => {
        status.textContent = paretoBudgetReadout?.textContent || '';
      });
      paretoBudgetCompareButton?.addEventListener('click', () => {
        if (!svg || !paretoBudgetSelect || !paretoReplaySelect) return;
        const cap = Number(paretoBudgetSelect.value);
        const replayCap = Number(paretoReplaySelect.value);
        const feasible = checkpointChoices.filter(choice =>
          choice.peak <= cap && choice.rebuilt <= replayCap
        ).sort((a, b) => a.rebuilt - b.rebuilt);
        const best = feasible[0];
        if (!best) return; // An empty feasible intersection cannot be compared.
        const before = checkpointSpacing(time);
        if (before === best.spacing) return;
        const target = landmarks.find(event => event.en === 's=' + best.spacing);
        if (!target) return;
        stop(false);
        pinnedTime = time; // A is the original reader-selected spacing
        comparison.hidden = false;
        clearPin.hidden = false;
        swapPin.hidden = false;
        sweepPin.hidden = false;
        pin.textContent = label('Replace A', '更新 A');
        setTime(target.t); // B redraws existing SMIL, A/B gauges and map
        status.textContent = label(
          'Caps ' + cap + ' slots / ' + replayCap + ' rebuilt: pinned s=' + before + ' as A; selected best feasible s=' +
            best.spacing + ' as B. ' + compareChange(pinnedTime, time),
          '上限 ' + cap + ' 槽／' + replayCap + ' 個重建：釘選 s=' + before + ' 為 A；選取最佳可行 s=' +
            best.spacing + ' 為 B。' + compareChange(pinnedTime, time)
        );
      });
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
      // IntersectionObserver delivers updates asynchronously, so its last
      // cached state is not enough to gate a new Play/Scan request. Inspect
      // actual current geometry as well as tab and motion preferences.
      const canStartMotion = () => !document.hidden && !reduced.matches &&
        viewportTargets.some(target => {
          if (!target.isConnected) return false;
          const rect = target.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0 && rect.bottom > 0 &&
            rect.right > 0 && rect.top < window.innerHeight &&
            rect.left < window.innerWidth;
        });
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
          paretoMapDots.forEach(({ button }) => { button.disabled = false; });
          if (paretoBudgetSelect) paretoBudgetSelect.disabled = false;
          if (paretoReplaySelect) paretoReplaySelect.disabled = false;
          retentionTraceButtons.forEach(button => { button.disabled = false; });
          if (policyScaleSelect) policyScaleSelect.disabled = false;
          if (policySweepSelect) policySweepSelect.disabled = false;
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
          if (candidate !== frame) return;
          if (acceptingFrameLoad) {
            onFrameLoad();
          } else {
            // A timed-out request may still finish as a valid SMIL SVG. Keep
            // its reviewed still visible AND stop its hidden animation clock:
            // ignoring the late event alone leaves animation work running.
            try { candidate.contentDocument?.documentElement?.pauseAnimations?.(); }
            catch (_) { /* Cross-origin or unavailable document: retain still. */ }
          }
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
