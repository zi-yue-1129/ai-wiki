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
        ['All accepted', 'Accepted 8/8 · Correct 6/8 · positive coverage 4/4 · negative coverage 4/4 · class gap 0 pp · rejected 0/8 (rejected-only accuracy undefined)'],
        ['Selective', 'Accepted 5/8 · Correct 5/5 · positive coverage 1/4 · negative coverage 4/4 · class gap 75 pp · rejected 3/8 (1/3 correct, 2/3 wrong)'],
      ],
      zh: [
        ['全部接受', '接受 8/8 · 正確 6/8 · 正類別覆蓋 4/4 · 負類別覆蓋 4/4 · 類別覆蓋差距 0 個百分點 · 拒答 0/8（拒答樣本正確率未定義）'],
        ['選擇性接受', '接受 5/8 · 正確 5/5 · 正類別覆蓋 1/4 · 負類別覆蓋 4/4 · 類別覆蓋差距 75 個百分點 · 拒答 3/8（1/3 正確、2/3 錯誤）'],
      ],
    },
  };
  const blocked = new Set(['script', 'foreignObject', 'iframe', 'image', 'use']);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  // Linked plots are computed from the schematic examples shown in the main SVG.
  // They highlight the same semantic state, never measured model performance.
  function makeLinkedPlot(filename, zh, chooseStage, pauseForCase) {
    const ns = 'http://www.w3.org/2000/svg';
    const node = (tag, attrs = {}, label = '') => {
      const el = document.createElementNS(ns, tag);
      for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
      if (label) el.textContent = label;
      return el;
    };
    const riskPlot = filename === 'accuracy-selective-coverage-motion.svg';
    const plot = node('svg', {viewBox:riskPlot?'0 0 640 356':'0 0 640 420',
      role:'group',
      class:'selective-linked-plot'});
    // Retain native-width labels on phones. The focusable parent figure owns
    // horizontal scrolling; scaling this 640px chart to 320px halves 12px text.
    plot.style.cssText = 'display:block;width:640px;min-width:640px;max-width:none;height:auto;margin:10px 0';
    plot.append(node('rect', {x:1,y:1,width:638,height:riskPlot?354:418,rx:12,
      fill:'#f8fafc',stroke:'#d4deec'}));
    const write = (x,y,label,attrs={}) => {
      const text = node('text',
        {x,y,fill:'#526783','font-family':'Arial, sans-serif',
          'font-size':13,...attrs}, label);
      plot.append(text);
      return text; // The OVERALL row is updated when acceptance changes.
    };
    // Arrow navigation walks discrete cases; Tab and Enter/Space remain available.
    const keyboardStage = (key, index, last) => {
      if (key === 'ArrowRight' || key === 'ArrowDown') return Math.min(last, index + 1);
      if (key === 'ArrowLeft' || key === 'ArrowUp') return Math.max(0, index - 1);
      if (key === 'Home') return 0;
      if (key === 'End') return last;
      return null;
    };
    let update;
    if (filename === 'accuracy-selective-coverage-motion.svg') {
      const accepted = [2,4,6], incorrect = [0,1,2];
      const risks = accepted.map((count,i) => incorrect[i] / count);
      const xs = accepted.map(count => 80 + 480 * count / 6);
      const ys = risks.map(risk => 119 - 200 * risk);
      // All six integer cutoffs expose non-monotonic selective risk.
      // Only the three even-k milestones map onto playable SVG scenes.
      const allAccepted = [1,2,3,4,5,6];
      const allIncorrect = [0,0,1,1,2,2];
      const allXs = allAccepted.map(count => 80 + 480 * count / 6);
      const allYs = allAccepted.map((count,i) =>
        119 - 200 * allIncorrect[i] / count);
      // The three playable scenes (even k) are a coarse summary. Inspecting
      // intermediate integer cutoffs must expose their exact error arithmetic
      // without pretending that the main SVG supports six acceptance masks.
      let activeRiskIndex = 0;
      let inspecting = null;
      const fmt = value =>
        (Math.round(value * 10) / 10).toFixed(1).replace(/\.0$/, '');
      const describe = count => {
        const errors = allIncorrect[count - 1];
        // Whether the newly admitted case is wrong determines the update.
        const newError = errors - (count > 1 ? allIncorrect[count - 2] : 0);
        const risk = errors / count;
        const previousRisk = count > 1 ?
          allIncorrect[count - 2] / (count - 1) : risk;
        const change = risk - previousRisk;
        const delta = count === 1 ? 'start' :
          (change > 1e-9 ? '↑' : change < -1e-9 ? '↓' : '=') +
          fmt(Math.abs(change) * 100) + ' pp';
        return 'k=' + count + ' · +' + (newError ? 'WRONG' : 'CORRECT') +
          ' · ' + errors + '/' + count +
          ' wrong · ' + fmt(risk * 100) + '% · ' + delta;
      };
      const inspection = write(24,190,'',{'font-size':13,
        'font-weight':700,fill:'#193e69','data-risk-inspection':'true'});
      // A one-case counterfactual compares outcomes without inventing observations.
      plot.append(node('path',{d:'M 24 202 H 616',fill:'none',
        stroke:'#d4deec','stroke-width':1}));
      const nextCase = write(24,224,'',{'font-size':12,
        'font-weight':700,fill:'#193e69','data-next-case':'true'});
      // The same 0–100% scale makes next-case conditional risks comparable.
      // Neither bar adds observations or changes the playable acceptance mask.
      const nextBars = [false,true].map((wrong,i) => {
        const y = 246 + 31*i;
        write(24,y+12,wrong?'+WRONG':'+CORRECT',{'font-size':12,
          'font-weight':700,fill:wrong?'#924624':'#0d626a'});
        plot.append(node('rect',{x:148,y,width:360,height:15,rx:6,
          fill:'#e5ebf2'}));
        const bar = node('rect',{x:148,y,width:0,height:15,rx:6,
          fill:wrong?'#de9468':'#50aca3',
          'data-next-bar':wrong?'wrong':'correct'});
        plot.append(bar);
        const value = write(522,y+12,'—',{'font-size':12,
          'font-weight':700,fill:'#193e69',
          'data-next-value':wrong?'wrong':'correct'});
        return {bar,value,wrong};
      });
      // Bracket the two hypothetical outcomes on the very same 0–100% axis.
      // Their difference is exactly 1/(k+1), not a confidence interval.
      const nextSpread = node('path', {'data-next-spread':'true',
        fill:'none',stroke:'#516a85','stroke-width':1.7,
        'stroke-linecap':'round'});
      plot.append(nextSpread);
      const nextSpreadValue = write(283,336,'',{'font-size':12,
        'font-weight':700,fill:'#193e69','text-anchor':'middle',
        'data-next-spread-value':'true'});
      // One outlined marker identifies which hypothetical branch the fixed,
      // synthetic ranked sequence actually follows; the other is arithmetic.
      const observedNext = node('circle',{
        'data-next-observed':'true',cx:148,cy:253.5,r:0,
        fill:'#f8fafc',stroke:'#193e69','stroke-width':2.5});
      plot.append(observedNext);
      const observedNote = write(407,336,'',{'font-size':11,
        'font-weight':700,fill:'#193e69',
        'data-next-observed-label':'true'});
      const nextScenario = count => {
        if (count === allAccepted.length) return {
          chart:'END OF SIX OBSERVED CASES · no next-case outcome in this example',
          aria:zh ? '六筆觀測案例已結束，無下一筆實際結果。'
            : 'End of six observed cases; no next outcome.'
        };
        const errors = allIncorrect[count - 1], n = count + 1;
        const sampleWrong = allIncorrect[count] > errors;
        const right = errors + '/' + n;
        const wrong = (errors + 1) + '/' + n;
        const rightPct = fmt(100 * errors / n) + '%';
        const wrongPct = fmt(100 * (errors + 1) / n) + '%';
        return {
          chart:'HYPOTHETICAL NEXT: +CORRECT ' + right + ' (' + rightPct +
            ') · +WRONG ' + wrong + ' (' + wrongPct + ')',
          aria:zh ? '假設下一筆正確，風險 ' + right + '（' + rightPct +
            '）；假設下一筆錯誤，風險 ' + wrong + '（' + wrongPct +
            '）；兩者相差 ' + fmt(100/n) + ' 個百分點，不是信賴區間或模型實測；本人工示例的下一筆' +
            (sampleWrong ? '錯誤' : '正確') + '，空心圈標記對應分支。'
            : 'Hypothetical next case: if correct, risk ' + right + ' (' +
              rightPct + '); if wrong, risk ' + wrong + ' (' + wrongPct +
              '). Their spread is ' + fmt(100/n) + ' percentage points, not a confidence interval or measured outcome. ' +
              'The next case in the constructed sample is ' +
              (sampleWrong ? 'wrong' : 'correct') +
              '; an outlined circle marks its branch.'
        };
      };
      // Focus is an explicit reading choice. Horizontal scrolling can produce
      // incidental mouseenter/mouseleave events below a stationary pointer;
      // these must not override a keyboard reader's currently focused cutoff.
      const focusedRiskCount = () => {
        const active = document.activeElement;
        if (!active || !plot.contains(active)) return null;
        const cutoff = active.getAttribute('data-risk-k');
        if (cutoff !== null) return Number(cutoff);
        const stage = active.getAttribute('data-acceptance-stage');
        return stage !== null ? accepted[Number(stage)] : null;
      };
      const showInspection = (count, fromHover = false) => {
        const focused = focusedRiskCount();
        if (fromHover && focused !== null && focused !== count) return;
        inspecting = count;
        inspection.textContent = describe(count);
        nextCase.textContent = nextScenario(count).chart;
        const terminal = count === allAccepted.length;
        const currentErrors = allIncorrect[count - 1], nextCount = count + 1;
        nextBars.forEach(({bar,value,wrong}) => {
          const numerator = currentErrors + Number(wrong);
          bar.setAttribute('width',String(terminal?0:360*numerator/nextCount));
          value.textContent = terminal ? '—' :
            numerator+'/'+nextCount+' '+fmt(100*numerator/nextCount)+'%';
        });
        if (terminal) {
          observedNext.setAttribute('r','0');
          observedNote.textContent = '';
        } else {
          const sampleWrong = allIncorrect[count] > currentErrors;
          observedNext.setAttribute('r','5');
          observedNext.setAttribute('cx',String(148 + 360 *
            (currentErrors + Number(sampleWrong))/nextCount));
          observedNext.setAttribute('cy',String(253.5 + 31*Number(sampleWrong)));
          observedNote.textContent = 'IN SAMPLE: +' +
            (sampleWrong ? 'WRONG' : 'CORRECT');
        }
        if (terminal) {
          nextSpread.setAttribute('d','');
          nextSpreadValue.textContent = '—';
        } else {
          const low = 148 + 360*currentErrors/nextCount;
          const high = low + 360/nextCount;
          nextSpread.setAttribute('d','M '+low+' 304V315 M '+low+
            ' 310H'+high+' M '+high+' 304V315');
          nextSpreadValue.setAttribute('x',String((low+high)/2));
          nextSpreadValue.textContent = 'Δ '+fmt(100/nextCount)+' pp';
        }
        plot.setAttribute('data-inspected-k',String(count));
      };
      const restoreInspection = () => {
        inspecting = null;
        showInspection(focusedRiskCount() ?? accepted[activeRiskIndex]);
        inspecting = null;
      };
      write(24,25,'RISK',{'font-weight':700});
      plot.append(node('path',{d:'M 84 34 V 120 H 588',fill:'none',
        stroke:'#9aacc1','stroke-width':1.5}));
      plot.append(node('polyline',{
        points:allXs.map((x,i)=>String(x)+','+String(allYs[i])).join(' '),
        fill:'none',stroke:'#087e85','stroke-width':3,
        'stroke-linecap':'round','stroke-linejoin':'round'}));
      const labels = risks.map(risk => String(Math.round(100 * risk)) + '%');
      const coverages = accepted.map(count => String(count) + '/6');
      // Small hollow dots show intermediate cutoffs, not extra controls.
      allAccepted.forEach((count,i) => {
        const milestone = count % 2 === 0;
        const dot = node('circle',{cx:allXs[i],cy:allYs[i],
          r:milestone?5:4,fill:milestone?'#087e85':'#f8fafc',
          stroke:milestone?'none':'#087e85',
          'stroke-width':milestone?0:2,'data-risk-k':count});
        if (!milestone) {
          dot.setAttribute('role','button');
          dot.setAttribute('tabindex','0');
          dot.setAttribute('cursor','help');
          const newError = allIncorrect[i] - (i > 0 ? allIncorrect[i - 1] : 0);
          const fraction = allIncorrect[i] + '/' + count;
          const riskPercent = fmt(allIncorrect[i] * 100 / count) + '%';
          const before = count === 1 ? 0 :
            allIncorrect[i - 1] / (count - 1);
          const difference = allIncorrect[i] / count - before;
          const deltaValue = fmt(Math.abs(difference) * 100);
          const deltaWords = count === 1 ?
            (zh ? '初始門檻' : 'initial cutoff') :
            (difference > 1e-9 ? (zh ? '增加 ' : 'increase ') :
              difference < -1e-9 ? (zh ? '減少 ' : 'decrease ') :
                (zh ? '不變 ' : 'unchanged ')) + deltaValue +
              (zh ? ' 個百分點' : ' percentage points');
          dot.setAttribute('aria-label',zh
            ? '檢視 k=' + count + '，新增' + (newError ? '錯誤' : '正確') +
                '案例，累積錯誤 ' + fraction + '，選擇性風險 ' +
                riskPercent + '，相對前一門檻' +
                deltaWords + '；不變更主動畫；' + nextScenario(count).aria
            : 'Inspect k=' + count + ': newly admitted ' +
                (newError ? 'incorrect' : 'correct') + ' case, ' +
                fraction + ' wrong, risk ' + riskPercent +
                ', change from prior cutoff: ' +
                deltaWords + '; main animation unchanged; ' + nextScenario(count).aria);
          dot.addEventListener('mouseenter',() => showInspection(count, true));
          dot.addEventListener('mouseleave',() => {
            if (document.activeElement !== dot) restoreInspection();
          });
          dot.addEventListener('focus',() => {
            dot.setAttribute('r','8');
            dot.setAttribute('stroke','#193e69');
            showInspection(count);
          });
          dot.addEventListener('blur',() => {
            dot.setAttribute('r','4');
            dot.setAttribute('stroke','#087e85');
            restoreInspection();
          });
          // Touch/click inspects an intermediate cutoff without seeking the main SVG.
          dot.addEventListener('click', () => showInspection(count));
          dot.addEventListener('keydown',event => {
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault();
              showInspection(count);
            }
          });
        }
        plot.append(dot);
        if (!milestone) {
          // Keep the visible 8px schematic dot; a separate 32px transparent
          // pointer target makes touch exploration practical on small screens.
          // It is hidden from the accessibility tree: the original dot owns
          // the name, Tab stop, keyboard activation and visible focus halo.
          const touchHit = node('circle', {cx:allXs[i],cy:allYs[i],r:16,
            fill:'transparent','pointer-events':'all','aria-hidden':'true',
            'data-risk-touch-k':count});
          touchHit.addEventListener('mouseenter', () => showInspection(count, true));
          touchHit.addEventListener('mouseleave', () => {
            if (document.activeElement !== dot) restoreInspection();
          });
          touchHit.addEventListener('click', () => {
            dot.focus(); showInspection(count);
          });
          plot.append(touchHit);
        }
      });
      write(24,160,'HOLLOW: k=1,3,5',{'font-size':12});
      const stageSelectors = [];
      for (let i=0;i<3;i++) {
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
          ? '選擇接受 ' + coverages[i] + '，風險 ' + labels[i] + '。' + nextScenario(accepted[i]).aria
          : 'Select ' + coverages[i] + ' accepted, risk ' + labels[i] + '. ' + nextScenario(accepted[i]).aria);
        hit.addEventListener('click', () => chooseStage(i));
        hit.addEventListener('keydown', event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault(); chooseStage(i);
            return;
          }
          const target = keyboardStage(event.key, i, 2);
          if (target !== null) {
            event.preventDefault();
            stageSelectors[target].focus();
            chooseStage(target);
          }
        });
        hit.addEventListener('mouseenter', () => showInspection(accepted[i], true));
        hit.addEventListener('mouseleave', () => {
          if (document.activeElement !== hit) restoreInspection();
        });
        hit.addEventListener('focus', () => {
          hit.setAttribute('stroke', '#193e69');
          showInspection(accepted[i]);
        });
        hit.addEventListener('blur', () => {
          hit.setAttribute('stroke', 'none');
          restoreInspection();
        });
        stageSelectors.push(hit);
        // In DOM/Tab order, place this playable cutoff after its even-k
        // marker, interleaved with the hollow k=1,3,5 inspection controls.
        // The plot still draws the active cursor last, above every marker.
        const anchor = plot.querySelector('circle[data-risk-k="' + accepted[i] + '"]');
        plot.insertBefore(hit, anchor.nextSibling);
      }
      const cursor = node('circle',{cx:xs[0],cy:ys[0],r:11,
        fill:'none',stroke:'#dc743b','stroke-width':3});
      plot.append(cursor);
      write(476,160,'COVERAGE →',{'font-weight':700,'font-size':12});
      update = index => {
        activeRiskIndex = index;
        if (inspecting === null) restoreInspection();
        cursor.setAttribute('cx',xs[index]); cursor.setAttribute('cy',ys[index]);
        stageSelectors.forEach((hit,i) =>
          hit.setAttribute('aria-pressed',String(i===index)));
        plot.setAttribute('aria-label',zh
          ? '六個離散接受門檻的風險比較；空心點為 k=1、3、5。新增正確案例可能降低風險。目前接受 ' + coverages[index] + '，風險 ' + labels[index] + '，橘色圈標示目前階段。'
          : 'Six discrete risk–coverage cutoffs; hollow dots are k=1,3,5. Adding a correct case can lower risk. Currently ' + coverages[index] + ' accepted, ' + labels[index] + ' risk; orange ring marks the stage.');
      };
    } else {
      write(24,26,'CLASS COVERAGE',{'font-weight':700});
      // Direct comparison is pedagogically different from dragging the timeline:
      // all eight cases versus the same five accepted cases. The buttons and
      // animation use one shared acceptance-stage state.
      const classChoices = [];
      for (const [index, caption, x, width] of [
        [0, 'ALL', 391, 84], [1, 'SELECTIVE', 489, 126],
      ]) {
        const control = node('g', {'data-acceptance-stage':index,
          cursor:'pointer', style:'outline:none'});
        control.setAttribute('role', 'button');
        control.setAttribute('tabindex', '0');
        control.setAttribute('aria-label', zh
          ? (index===0 ? '比較全部接受，8/8' : '比較選擇性接受，5/8')
          : (index===0 ? 'Compare all accepted, 8/8' : 'Compare selective acceptance, 5/8'));
        const surface = node('rect', {x,y:9,width,height:27,rx:8,
          fill:'#ffffff',stroke:'#adc0ce','stroke-width':1.5});
        const captionNode = node('text', {x:x+width/2,y:27,
          'text-anchor':'middle',fill:'#24516e',
          'font-family':'Arial, sans-serif','font-size':12,'font-weight':700}, caption);
        control.append(surface, captionNode);
        // Selection and keyboard focus are independent visual states. Always
        // repaint the selected fill, even while the control retains focus:
        // otherwise a clicked/keyboard-activated choice can look unselected.
        const paint = selected => {
          const focused = document.activeElement === control;
          surface.setAttribute('fill', selected ? '#e3f0ef' : '#ffffff');
          surface.setAttribute('stroke', focused ? '#193e69' :
            selected ? '#087e85' : '#adc0ce');
          surface.setAttribute('stroke-width', focused ? '3' :
            selected ? '2' : '1.5');
        };
        control.addEventListener('click', () => chooseStage(index));
        control.addEventListener('keydown', event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault(); chooseStage(index);
            return;
          }
          const target = keyboardStage(event.key, index, 1);
          if (target !== null) {
            event.preventDefault();
            classChoices[target].control.focus();
            chooseStage(target);
          }
        });
        control.addEventListener('focus', () =>
          paint(control.getAttribute('aria-pressed') === 'true'));
        control.addEventListener('blur', () => paint(control.getAttribute('aria-pressed') === 'true'));
        classChoices.push({control,paint});
        plot.append(control);
      }
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
      // Dashed ghost endpoint: flipping one case changes just its class
      // coverage numerator, not the current acceptance mask or predictions.
      const flipMarker = node('line',{x1:116,x2:116,y1:55,y2:90,
        stroke:'#b45336','stroke-width':2.5,'stroke-dasharray':'4 3',
        'aria-hidden':'true',visibility:'hidden','data-flip-marker':'true'});
      plot.append(flipMarker);
      // Visible accepted/total and correct/accepted ratios highlight why a
      // perfect accepted-only accuracy need not mean equal class coverage.
      write(35,155,'OVERALL',{'font-weight':700,'font-size':12});
      const overall = write(116,155,'8/8 accepted · 6/8 correct',{'font-size':12,
        'data-overall-metrics':'true'});
      // Absolute difference between true-class acceptance rates, measured in
      // percentage points. This is a descriptive disparity, not a fairness verdict.
      const gap = write(468,155,'GAP 0 pp',{'font-size':12,'font-weight':700,
        fill:'#193e69','data-class-gap':'true'});
      // Rejection never repairs a prediction: reveal the hidden outcomes,
      // including the undefined rejected-only rate when no case is rejected.
      write(35,184,'REJECTED',{'font-weight':700,'font-size':12});
      const rejected = write(116,184,'0/8 rejected · accuracy N/A',
        {'font-size':12,'data-rejected-metrics':'true'});
      // Rejecting predictions partitions outcomes; it never repairs them.
      // Show both conservation equations beside the live rejected-case tally.
      plot.append(node('path',{d:'M 35 199 H 605',
        stroke:'#d4deec','stroke-width':1}));
      const rightMarker = node('circle',{cx:40,cy:216,r:5,fill:'#087e85'});
      const wrongMarker = node('circle',{cx:40,cy:241,r:5,fill:'#c26646'});
      plot.append(rightMarker, wrongMarker);
      const rightBalance = write(56,221,'RIGHT 6 = 6 accepted + 0 rejected',
        {'font-size':13,'font-weight':700,fill:'#193e69',
          'data-correct-balance':'true'});
      const wrongBalance = write(56,246,'WRONG 2 = 2 accepted + 0 rejected',
        {'font-size':13,'font-weight':700,fill:'#193e69',
          'data-wrong-balance':'true'});
      // Selecting a fixed prediction reveals the exact +1 contribution to
      // RIGHT/WRONG x accepted/rejected. Keep the two conservation equations
      // visible and unchanged; do not confuse a partition with corrected errors.
      const contribution = node('g',{'data-case-contribution':'true',
        'aria-hidden':'true',visibility:'hidden'});
      const contributionBg = node('rect',{x:513,y:205,width:89,height:23,rx:11,
        fill:'#e3f0ef',stroke:'#087e85','stroke-width':1});
      const contributionText = node('text',{x:557,y:221,
        'text-anchor':'middle',fill:'#0d626a',
        'font-family':'Arial, sans-serif','font-size':12,'font-weight':700},'+1 IN');
      contribution.append(contributionBg,contributionText);
      plot.append(contribution);
      // Eight fixed case outcomes expose what selective accuracy omits.
      // Correctness never changes when an acceptance rule changes.
      plot.append(node('path',{d:'M 35 260 H 605',
        stroke:'#d4deec','stroke-width':1}));
      write(35,281,'CASE OUTCOMES',{'font-weight':700,'font-size':12});
      const caseTiles = [];
      // Inspect individual provenance without changing predictions or the
      // acceptance mask. Use the existing legend line to preserve viewBox.
      const caseInspection = write(116,368,'✓ right · × wrong',{
        'font-size':12,'font-weight':700,fill:'#193e69',
        'data-case-inspection':'true'});
      plot.append(node('path',{d:'M 35 380 H 605',
        stroke:'#d4deec','stroke-width':1}));
      write(35,401,'FLIP',{'font-weight':700,'font-size':12});
      const flipPreview = write(116,401,'FOCUS A CASE TO PREVIEW FLIP',{
        'font-size':12,'font-weight':700,fill:'#193e69',
        'data-flip-preview':'true'});
      const flipMath = entry => {
        const kept = caseTiles.filter(({tile}) =>
          tile.getAttribute('data-case-accepted') === 'true');
        const wasAccepted = entry.tile.getAttribute('data-case-accepted') === 'true';
        const direction = wasAccepted ? -1 : 1;
        const accepted = kept.length + direction;
        const correct = kept.filter(item => item.correct).length +
          (entry.correct ? direction : 0);
        const positive = kept.filter(item => item.cls === 'POS').length +
          (entry.cls === 'POS' ? direction : 0);
        const negative = kept.filter(item => item.cls === 'NEG').length +
          (entry.cls === 'NEG' ? direction : 0);
        return {accepted,correct,positive,negative,
          gap:Math.abs(positive-negative)*25};
      };
      let inspectedCase = null;
      const inspectCase = entry => {
        inspectedCase = entry;
        const selectedRight = Boolean(entry && entry.correct);
        const selectedWrong = Boolean(entry && !entry.correct);
        rightMarker.setAttribute('r',selectedRight?'8':'5');
        wrongMarker.setAttribute('r',selectedWrong?'8':'5');
        rightMarker.setAttribute('stroke',selectedRight?'#193e69':'none');
        wrongMarker.setAttribute('stroke',selectedWrong?'#193e69':'none');
        rightMarker.setAttribute('stroke-width',selectedRight?'2':'0');
        wrongMarker.setAttribute('stroke-width',selectedWrong?'2':'0');
        rightBalance.setAttribute('fill',selectedRight?'#087e85':'#193e69');
        wrongBalance.setAttribute('fill',selectedWrong?'#b45336':'#193e69');
        contribution.setAttribute('visibility',entry?'visible':'hidden');
        flipMarker.setAttribute('visibility',entry?'visible':'hidden');
        if (entry) {
          const flipped = flipMath(entry);
          const markerX = 116 + 415 *
            (entry.cls === 'POS' ? flipped.positive : flipped.negative) / 4;
          flipMarker.setAttribute('x1',String(markerX));
          flipMarker.setAttribute('x2',String(markerX));
          flipMarker.setAttribute('y1',entry.cls === 'POS' ? '55' : '103');
          flipMarker.setAttribute('y2',entry.cls === 'POS' ? '90' : '138');
          flipPreview.textContent = entry.cls[0] + (entry.i + 1) +
            ' → ' + flipped.correct + '/' + flipped.accepted +
            ' RIGHT · POS ' + flipped.positive + '/4 · NEG ' +
            flipped.negative + '/4 · GAP ' + flipped.gap + ' pp';
        } else {
          flipPreview.textContent = 'FOCUS A CASE TO PREVIEW FLIP';
        }
        if (entry) {
          const accepted = entry.tile.getAttribute('data-case-accepted') === 'true';
          contributionBg.setAttribute('y',entry.correct?'205':'230');
          contributionBg.setAttribute('fill',accepted?'#e3f0ef':'#fff0e8');
          contributionBg.setAttribute('stroke',accepted?'#087e85':'#b45336');
          contributionText.setAttribute('y',entry.correct?'221':'246');
          contributionText.setAttribute('fill',accepted?'#0d626a':'#92400e');
          contributionText.textContent = accepted ? '+1 IN' : '+1 OUT';
        }
        caseInspection.textContent = entry
          ? entry.cls[0] + (entry.i + 1) + ': ' +
            (entry.correct ? 'RIGHT' : 'WRONG') + ' · ' +
            (entry.tile.getAttribute('data-case-accepted') === 'true'
              ? 'ACCEPTED' : 'REJECTED') + ' → +1 ' +
            (entry.tile.getAttribute('data-case-accepted') === 'true'
              ? 'IN' : 'OUT')
          : '✓ right · × wrong';
        caseTiles.forEach(({tile,control}) => {
          const focused = entry && control === entry.control;
          const accepted = tile.getAttribute('data-case-accepted') === 'true';
          tile.setAttribute('stroke', focused ? '#193e69' :
            accepted ? '#087e85' : '#9aacc1');
          tile.setAttribute('stroke-width', focused ? '3' : '1.5');
        });
      };
      for (const [cls,outcomes,y] of [
        ['POS',[true,false,false,true],294],
        ['NEG',[true,true,true,true],325],
      ]) {
        write(35,y+18,cls,{'font-weight':700,'font-size':13});
        outcomes.forEach((correct,i) => {
          const x = 116 + 74*i;
          const tile = node('rect',{x,y,width:66,height:24,rx:7,
            fill:'#e3f0ef',stroke:'#087e85','stroke-width':1.5,
            'data-case-id':cls[0]+(i+1),
            'data-case-correct':String(correct),
            'data-case-accepted':'true'});
          const control = node('g', {
            role:'button',tabindex:0,cursor:'pointer',style:'outline:none',
            'data-case-control':cls[0] + (i + 1)});
          control.append(tile,
            node('text',{x:x+9,y:y+17,fill:'#193e69',
              'font-family':'Arial, sans-serif','font-size':12,
              'font-weight':700},cls[0]+(i+1)),
            node('text',{x:x+45,y:y+17,
              fill:correct?'#0d626a':'#b45336',
              'font-family':'Arial, sans-serif','font-size':15,
              'font-weight':700},correct?'✓':'×'));
          plot.append(control);
          const entry = {tile,control,cls,i,correct};
          caseTiles.push(entry);
          // Freeze the acceptance rule before inspecting a fixed prediction:
          // automatic playback must not change the mask mid-inspection.
          control.addEventListener('focus', () => {
            pauseForCase(); inspectCase(entry);
          });
          control.addEventListener('blur', () => inspectCase(null));
          control.addEventListener('click', () => {
            control.focus(); inspectCase(entry);
          });
          // Horizontal scrolling may move the pointer under keyboard focus.
          control.addEventListener('mouseenter', () => {
            if (!caseTiles.some(({control}) => control === document.activeElement))
              inspectCase(entry);
          });
          control.addEventListener('mouseleave', () => {
            if (!caseTiles.some(({control}) => control === document.activeElement))
              inspectCase(null);
          });
          control.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault(); inspectCase(entry); return;
            }
            if (event.key === 'Escape') {
              event.preventDefault(); control.blur(); return;
            }
            const next = keyboardStage(event.key,caseTiles.indexOf(entry),7);
            if (next !== null) {
              event.preventDefault(); caseTiles[next].control.focus();
            }
          });
        });
      }
      write(470,310,'TEAL accepted',{'font-size':12,
        'font-weight':700,fill:'#0d626a'});
      write(470,340,'PALE rejected',{'font-size':12,'font-weight':700});
      update = index => {
        classChoices.forEach(({control,paint},i) => {
          control.setAttribute('aria-pressed',String(i===index));
          paint(i===index);
        });
        caseTiles.forEach(({tile,control,cls,i,correct}) => {
          const accepted = index === 0 || cls === 'NEG' || i === 0;
          tile.setAttribute('fill',accepted?'#e3f0ef':'#eef2f7');
          tile.setAttribute('stroke-dasharray',accepted?'none':'4 3');
          tile.setAttribute('data-case-accepted',String(accepted));
          const id = cls[0] + (i + 1);
          control.setAttribute('aria-label',zh
            ? '個案 ' + id + '，' + (correct?'預測正確':'預測錯誤') +
              '，' + (accepted?'接受':'拒答') +
              '；此案例計入' + (correct?'正確':'錯誤') +
              (accepted?'且接受':'且拒答') + '的計數一筆；方向鍵檢視相鄰個案'
            : 'Case ' + id + ', ' + (correct?'correct':'wrong') +
              ', ' + (accepted?'accepted':'rejected') +
              '; contributes one to the ' + (correct?'right':'wrong') +
              '-' + (accepted?'accepted':'rejected') +
              ' count; use arrow keys for adjacent cases');
        });
        // Localize the one-bit counterfactual on each keyboard control.
        caseTiles.forEach(entry => {
          const flipped = flipMath(entry);
          const addition = zh
            ? '；若只反轉此個案的接受狀態，接受 ' +
              flipped.accepted + ' 筆，正確 ' + flipped.correct +
              ' 筆；正類覆蓋 ' + flipped.positive +
              '/4，負類覆蓋 ' + flipped.negative +
              '/4，差距 ' + flipped.gap + ' 個百分點'
            : '; flipping only this case would retain ' +
              flipped.accepted + ' cases with ' + flipped.correct +
              ' correct; positive coverage ' + flipped.positive +
              '/4, negative coverage ' + flipped.negative +
              '/4, gap ' + flipped.gap + ' percentage points';
          entry.control.setAttribute('aria-label',
            entry.control.getAttribute('aria-label') + addition);
        });
        inspectCase(inspectedCase);
        const positive=index===0?4:1;
        bars[0].fill.setAttribute('width',String(415*positive/4));
        bars[0].value.textContent=String(positive)+'/4';
        bars[1].fill.setAttribute('width','415');
        bars[1].value.textContent='4/4';
        overall.textContent=index===0?'8/8 accepted · 6/8 correct':
          '5/8 accepted · 5/5 correct';
        const gapPp = Math.abs(positive / 4 - 1) * 100;
        gap.textContent = 'GAP ' + gapPp + ' pp';
        const keptCorrect = index === 0 ? 6 : 5;
        const keptWrong = positive + 4 - keptCorrect;
        const rejectedCount = 8 - (positive + 4);
        const rejectedCorrect = 6 - keptCorrect;
        const rejectedWrong = rejectedCount - rejectedCorrect;
        rejected.textContent = rejectedCount === 0
          ? '0/8 rejected · accuracy N/A'
          : rejectedCount + '/8 rejected · ' + rejectedCorrect + '/' +
            rejectedCount + ' correct · ' + rejectedWrong + '/' +
            rejectedCount + ' wrong';
        rightBalance.textContent = 'RIGHT 6 = ' + keptCorrect +
          ' accepted + ' + rejectedCorrect + ' rejected';
        wrongBalance.textContent = 'WRONG 2 = ' + keptWrong +
          ' accepted + ' + rejectedWrong + ' rejected';
        plot.setAttribute('aria-label',zh
          ? '類別覆蓋率：整體接受 ' + (index===0?'8/8':'5/8') + '，正類別 ' + positive + '/4，負類別 4/4，兩類別覆蓋差距 ' + gapPp + ' 個百分點。' + (rejectedCount === 0 ? '沒有拒答樣本，拒答樣本正確率未定義。' : '拒答 ' + rejectedCount + '/8，當中正確 ' + rejectedCorrect + '/' + rejectedCount + '，錯誤 ' + rejectedWrong + '/' + rejectedCount + '。') + '正確預測總數 6、錯誤預測總數 2，在接受與拒答之間重新分配但加總不變。兩條橫條代表保留比例；八格個案的預測對錯不變，只有接受或拒答狀態改變。'
          : 'Class coverage: ' + (index===0?'8/8':'5/8') + ' accepted, positive ' + positive + '/4, negative 4/4, absolute class coverage gap ' + gapPp + ' percentage points. ' + (rejectedCount === 0 ? 'No rejected cases; rejected-only accuracy is undefined. ' : rejectedCount + '/8 rejected, with ' + rejectedCorrect + '/' + rejectedCount + ' correct and ' + rejectedWrong + '/' + rejectedCount + ' wrong. ') + 'The six correct and two wrong predictions are partitioned, not repaired. Two bars show acceptance rates. Eight case tiles retain their right/wrong outcomes while acceptance styling changes.');
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
      const fallbackDisplay = img.style.getPropertyValue('display');
      const fallbackDisplayPriority = img.style.getPropertyPriority('display');
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
            host.insertBefore(svg, img);
            // Inline display:block in Markdown can override the hidden attribute.
            // Hide the still visibly as well as semantically after SVG insertion.
            img.hidden = true; img.style.setProperty('display', 'none', 'important');
            linkedPlot = makeLinkedPlot(filename, zh, chooseStage, () => {
              // Cancel an in-flight Play promise as well as the current frame.
              ++intentVersion; pause();
            });
            host.insertBefore(linkedPlot.element, controls);
            sync(); status.textContent = '';
            return true;
          } catch (_) {
            // Never leave an incomplete interactive overlay atop the fallback.
            if (svg) { svg.remove(); svg = null; }
            if (linkedPlot) { linkedPlot.element.remove(); linkedPlot = null; }
            img.src = still; img.hidden = false;
            if (fallbackDisplay) img.style.setProperty('display', fallbackDisplay, fallbackDisplayPriority);
            else img.style.removeProperty('display');
            status.textContent = label.error;
            for (const el of [toggle, prev, next, slider, speed]) el.disabled = true;
            return false;
          }
        })();
        return pending;
      };
      // A hidden tab must never resume a stale Play command or silently skip
      // acceptance stages while requestAnimationFrame is suspended.
      const onVisibilityChange = () => {
        if (!host.isConnected) {
          document.removeEventListener('visibilitychange', onVisibilityChange);
          return;
        }
        if (document.hidden) {
          ++intentVersion;
          if (playing) pause();
        }
      };
      document.addEventListener('visibilitychange', onVisibilityChange);
      const tick = now => {
        if (!playing) return;
        if (!host.isConnected) {
          pause();
          document.removeEventListener('visibilitychange', onVisibilityChange);
          return;
        }
        // Also bound elapsed time if a device stalls without firing visibilitychange.
        // Educational frames should not leap across several accepted sets.
        if (previous !== null) {
          const elapsedSeconds = Math.min(0.1, Math.max(0, (now - previous) / 1000));
          current = (current + elapsedSeconds * Number(speed.value)) % lesson.duration;
        }
        previous = now; sync(); frame = requestAnimationFrame(tick);
      };
      toggle.addEventListener('click', async () => {
        if (playing) { ++intentVersion; pause(); return; }
        const intent = ++intentVersion;
        if (document.hidden || !(await load()) || intent !== intentVersion || document.hidden) return;
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
