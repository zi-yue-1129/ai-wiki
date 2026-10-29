#!/usr/bin/env node
'use strict';
// Dependency-free behaviour tests; not a substitute for rendered browser review.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('docs/javascripts/concept-motion-detailed.js', 'utf8');
function setup(filename, zh, reduced, fail = false) {
  const created = [];
  class Element {
    constructor(tag) {
      this.localName = tag; this.dataset = {}; this.attrs = {}; this.children = [];
      this.events = {}; this.disabled = false; this.hidden = false;
      this.value = ''; this.textContent = ''; this.classList = { add() {} };
      created.push(this);
    }
    append(...nodes) { this.children.push(...nodes); }
    before(node) { this.beforeNode = node; }
    insertBefore(node) { this.children.unshift(node); }
    setAttribute(key, value) { this.attrs[key] = value; }
    getAttribute(key) { return this.attrs[key] ?? null; }
    addEventListener(name, callback) { this.events[name] = callback; }
    querySelectorAll() { return []; }
  }
  const img = new Element('img');
  img.attrs.src = `/assets/concept-animations/${filename}`;
  img.alt = zh ? '遮罩動畫' : 'Masked animation';
  const document = {
    readyState: 'complete', querySelectorAll: () => [img],
    createElement: tag => new Element(tag),
    importNode: () => {
      const svg = new Element('svg');
      svg.pauseAnimations = () => {};
      svg.setCurrentTime = t => { svg.currentTime = t; };
      return svg;
    },
  };
  const window = { matchMedia: () => ({ matches: reduced, addEventListener() {} }) };
  const fetch = async () => {
    if (fail) throw Error('simulated network failure');
    return { ok: true, text: async () => '<svg></svg>' };
  };
  class DOMParser {
    parseFromString() {
      return { documentElement: { localName: 'svg', querySelectorAll: () => [], attributes: [] } };
    }
  }
  vm.runInNewContext(source, {
    window, document, fetch, DOMParser,
    requestAnimationFrame: () => 1, cancelAnimationFrame: () => {},
  });
  return {
    img,
    find: (tag, label) => created.find(el => el.localName === tag && el.textContent === label),
    note: () => created.find(el => el.className === 'concept-motion-chapter-note'),
    slider: () => created.find(el => el.localName === 'input'),
  };
}
const settle = async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); };
async function main() {
  let scenarios = 0;
  for (const filename of [
    'mae-visible-patch-reconstruction-motion.svg',
    'dinov2-dual-objective-ema-motion.svg',
  ]) {
    for (const zh of [false, true]) {
      for (const reduced of [false, true]) {
        const h = setup(filename, zh, reduced);
        const next = h.find('button', zh ? '下一段' : 'Next phase');
        const prev = h.find('button', zh ? '上一段' : 'Previous phase');
        assert.ok(next && prev, 'bilingual chapter buttons exist');
        assert.match(h.note().textContent, /^1\/5 · /);
        next.events.click(); await settle();
        assert.match(h.note().textContent, /^2\/5 · /);
        assert.equal(h.slider().value, '28');
        prev.events.click(); await settle();
        assert.match(h.note().textContent, /^1\/5 · /);
        assert.equal(h.slider().value, '0');
        h.slider().value = '125'; h.slider().events.input(); await settle();
        assert.match(h.note().textContent, /^5\/5 · /);
        assert.equal(next.disabled, true);
        scenarios++;
      }
    }
  }
  const h = setup('mae-visible-patch-reconstruction-motion.svg', false, true, true);
  h.find('button', 'Next phase').events.click(); await settle();
  assert.equal(h.find('button', 'Next phase').disabled, true);
  assert.equal(h.find('button', 'Previous phase').disabled, true);
  assert.match(h.img.src, /-still\.svg$/);
  console.log(`PASS: ${scenarios} bilingual/reduced-motion scenarios, chapter navigation, scrub, and fetch-failure fallback`);
}
main().catch(err => { console.error(err); process.exitCode = 1; });
