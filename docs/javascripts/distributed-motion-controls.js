/* Optional same-origin SMIL timeline controls for six distributed-training diagrams.
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
      const zh = /[\u3400-\u9fff]/.test(img.alt || '');
      const label = (en, tw) => zh ? tw : en;
      const previousControls = host.querySelector('.concept-motion-controls');
      const frame = document.createElement('object');
      frame.className = 'distributed-motion-frame';
      frame.type = 'image/svg+xml';
      frame.data = src;
      frame.setAttribute('aria-label', img.alt || match[1]);
      frame.append(img.cloneNode(true));
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
      host.append(bar);

      function draw() {
        if (!svg) return;
        svg.setCurrentTime(Math.min(time, config.duration - 0.001));
        seek.value = String(Math.round(time / config.duration * 1000));
        readout.textContent = time.toFixed(1) + ' / ' + config.duration + 's';
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
        status.textContent = label('Animation at ', '動畫時間 ') + time.toFixed(1) + 's';
      }
      prev.addEventListener('click', () => step(-1));
      next.addEventListener('click', () => step(1));
      seek.addEventListener('input', () => { const selected = Number(seek.value); stop(); setTime(selected / 1000 * config.duration); });
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
      frame.addEventListener('load', () => {
        if (reduced.matches) return;
        try {
          const root = frame.contentDocument?.documentElement;
          if (!root || typeof root.pauseAnimations !== 'function' || typeof root.setCurrentTime !== 'function') return;
          svg = root;
          svg.pauseAnimations();
          setTime(0);
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
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  if (window.document$?.subscribe) window.document$.subscribe(enhance);
})();
