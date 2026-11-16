#!/usr/bin/env node
'use strict';
// Dependency-free lifecycle regression; CI separately checks real rendered MathJax.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('docs/javascripts/mathjax.js', 'utf8');
const formula = (rendered = false) => ({
  rendered,
  querySelector(selector) {
    assert.equal(selector, 'mjx-container');
    return this.rendered ? {} : null;
  },
});
const article = (...formulas) => ({
  isConnected: true,
  formulas,
  querySelectorAll(selector) {
    assert.equal(selector, '.arithmatex');
    return this.formulas;
  },
});

function setup(initial) {
  let current = initial;
  let subscribed;
  let finishStartup;
  const calls = {clear: [], typeset: [], resets: 0};
  const window = {};
  const document = {querySelector: selector => {
    assert.equal(selector, '.md-content__inner');
    return current;
  }};
  const document$ = {subscribe(callback) {
    subscribed = callback;
    callback(); // Material's current-document replay.
  }};
  vm.runInNewContext(source, {window, document, document$, console});
  const math = window.MathJax;
  const configuredReady = math.startup.ready;
  math.startup.defaultReady = () => {
    math.startup.promise = new Promise(resolve => { finishStartup = resolve; });
    math.typesetClear = roots => calls.clear.push(Array.from(roots));
    math.texReset = () => calls.resets++;
    math.typesetPromise = async nodes => {
      assert(nodes.length > 0);
      assert(nodes.every(node => !node.rendered), 'must not rescan rendered assistive MathML');
      calls.typeset.push(Array.from(nodes));
      nodes.forEach(node => { node.rendered = true; });
    };
  };
  configuredReady();
  return {math, calls,
    finish: () => finishStartup(),
    emit: next => { current = next; return subscribed(); },
    settle: () => math.startup.promise};
}

(async () => {
  // Replayed initial document waits for automatic startup rendering, then keeps
  // those MathItems tracked rather than globally clearing/rescanning their output.
  const firstFormula = formula();
  const first = article(firstFormula);
  const env = setup(first);
  await Promise.resolve();
  assert.equal(env.calls.typeset.length, 0);
  firstFormula.rendered = true;
  env.finish();
  await env.settle();
  assert.deepEqual(env.calls, {clear: [], typeset: [], resets: 0});

  // Repeated emissions of the same article do not create nested MathJax output.
  env.emit(first);
  env.emit(first);
  await env.settle();
  assert.equal(env.calls.typeset.length, 0);
  assert.equal(env.calls.clear.length, 0);

  // A replacement article clears only the removed article's tracked MathItems
  // and typesets only source formulas, preserving already rendered/accessibility output.
  first.isConnected = false;
  const raw = formula();
  const alreadyRendered = formula(true);
  const second = article(raw, alreadyRendered);
  env.emit(second);
  env.emit(second);
  await env.settle();
  assert.deepEqual(env.calls.clear, [[first]]);
  assert.deepEqual(env.calls.typeset, [[raw]]);
  assert.equal(env.calls.resets, 1);

  // Rapid navigation skips a queued article that was detached before its turn.
  const stale = article(formula());
  env.emit(stale);
  stale.isConnected = false;
  second.isConnected = false;
  const latest = article(formula());
  env.emit(latest);
  await env.settle();
  assert.equal(stale.formulas[0].rendered, false);
  assert.deepEqual(env.calls.clear, [[first], [second]]);
  assert.deepEqual(env.calls.typeset, [[raw], [latest.formulas[0]]]);

  // Math-free and absent articles are safe without inventing typeset work.
  latest.isConnected = false;
  env.emit(article());
  await env.settle();
  env.emit(null);
  await env.settle();
  assert.deepEqual(env.calls.clear, [[first], [second], [latest]]);
  assert.equal(env.calls.typeset.length, 2);

  // If startup did not render a source formula, the first replay handles it once.
  const unrendered = formula();
  const fallback = setup(article(unrendered));
  fallback.finish();
  await fallback.settle();
  assert.deepEqual(fallback.calls.typeset, [[unrendered]]);
  assert.equal(fallback.calls.clear.length, 0);
  console.log('PASS: 6 MathJax startup/navigation lifecycle scenarios; no browser run');
})().catch(error => { console.error(error); process.exitCode = 1; });
