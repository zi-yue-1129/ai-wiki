#!/usr/bin/env node
'use strict';
// Exercises the exact browser discovery JavaScript against a minimal DOM.
// This does not simulate native keyboard scrolling: the Chromium suite does that.
const assert = require('node:assert/strict');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const path = require('node:path');

class Element {
  constructor(name, parent = null, options = {}) {
    this.name = name;
    this.parentElement = parent;
    this.children = [];
    if (parent) parent.children.push(this);
    this.clientWidth = options.clientWidth ?? 358;
    this.scrollWidth = options.scrollWidth ?? this.clientWidth;
    this.style = {overflowX: options.overflowX ?? 'visible', display:'block', visibility:'visible'};
    this.attrs = {...options.attrs};
    this.tabIndex = this.attrs.tabindex === undefined ? -1 : Number(this.attrs.tabindex);
    this.dataset = {};
    this.tagName = (options.tagName ?? 'DIV').toUpperCase();
    this.isConnected = true;
  }
  getAttribute(name) { return this.attrs[name] ?? null; }
  hasAttribute(name) { return name in this.attrs; }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  removeAttribute(name) { delete this.attrs[name]; }
  getBoundingClientRect() { return {x:0,y:0,width:this.clientWidth,height:360}; }
  getClientRects() { return [this.getBoundingClientRect()]; }
  contains(el) { return el === this || this.children.some(child => child.contains(el)); }
}

const harness = path.join(__dirname, 'test_built_motion_browser.py');
const extract = `import ast,sys
module=ast.parse(open(sys.argv[1],encoding='utf-8').read())
for n in module.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MOTION_SCROLL_DISCOVERY_JS' for t in n.targets):
  print(ast.literal_eval(n.value));break
else: raise SystemExit('Missing actual MOTION_SCROLL_DISCOVERY_JS')`;
const actualJS = execFileSync('python', ['-c', extract, harness], {encoding:'utf8'});
function fixture() {
  const body = new Element('body');
  const article = new Element('article', body);
  const images = [];
  article.querySelectorAll = selector => {
    assert.equal(selector, 'img[data-concept-motion-enhanced="yes"]');
    return images;
  };
  const document = {querySelector(selector) {
    assert.equal(selector, '.md-content__inner'); return article;
  }};
  const discover = vm.runInNewContext(`(${actualJS})`, {
    document, getComputedStyle: node => node.style, Set,
  });
  return {body, article, images, discover,
    image(parent) { const img = new Element('image', parent, {tagName:'IMG'}); images.push(img);return img; }};
}
function identities(actual, expected) {
  assert.equal(actual.length, expected.length);
  expected.forEach(el => assert.ok(actual.includes(el), `Missing actual element: ${el.name}`));
}
let passed = 0;
function test(name, run) {run();passed++;console.log(`PASS ${name}`);}
const scrolling = {overflowX:'auto',clientWidth:358,scrollWidth:640,attrs:{tabindex:'0'}};
test('classless focusable inline-style wrapper is discovered', () => {
  const f=fixture(), outer=new Element('classless',f.article,scrolling);
  f.image(new Element('fixed inner',outer,{clientWidth:640}));
  identities(f.discover(),[outer]);
});
test('two images sharing one ancestor yield one actual element', () => {
  const f=fixture(), outer=new Element('shared',f.article,scrolling);
  f.image(outer);f.image(new Element('inner',outer));
  identities(f.discover(),[outer]);
});
test('nested scrollable ancestors are all covered and deduplicated', () => {
  const f=fixture(), outer=new Element('outer',f.article,scrolling);
  const inner=new Element('inner',outer,{...scrolling,overflowX:'scroll'});
  f.image(inner);f.image(inner);f.image(outer);
  identities(f.discover(),[inner,outer]);
});
test('fitting wrapper, visible overflow, and hidden overflow are not scrollers', () => {
  const f=fixture();
  for(const options of [{...scrolling,scrollWidth:358},{...scrolling,scrollWidth:360},
    {...scrolling,overflowX:'visible'},{...scrolling,overflowX:'hidden'}]) {
    f.image(new Element('not scrollable',f.article,options));
  }
  identities(f.discover(),[]);
});
test('missing and negative tabindex remain visible to mandatory focus validation', () => {
  const f=fixture(), absent=new Element('missing tabindex',f.article,{...scrolling,attrs:{}});
  const negative=new Element('negative tabindex',f.article,{...scrolling,attrs:{tabindex:'-1'}});
  f.image(absent);f.image(negative);
  identities(f.discover(),[absent,negative]);
  assert.equal(absent.getAttribute('tabindex'),null);
  assert.equal(negative.tabIndex,-1);
});
test('article itself may scroll but ancestors outside article are excluded', () => {
  const f=fixture();
  for(const el of [f.body,f.article]) {el.style.overflowX='auto';el.scrollWidth=640;}
  f.image(new Element('inner',f.article));
  identities(f.discover(),[f.article]);
});
test('separate scrollers with same dimensions retain separate identities', () => {
  const f=fixture(), a=new Element('a',f.article,scrolling),b=new Element('b',f.article,scrolling);
  f.image(a);f.image(b);identities(f.discover(),[a,b]);
});
test('empty article does not manufacture scroll targets', () => {
  const f=fixture();identities(f.discover(),[]);
});
console.log(`${passed} actual-JS scroll discovery tests passed; native key behavior remains a browser check.`);
