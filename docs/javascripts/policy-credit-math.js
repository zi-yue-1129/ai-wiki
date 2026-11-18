/* Pure numerical model shared by the original policy-credit teaching labs. */
(() => {
  'use strict';
  function returns(rewards, gamma) {
    const result = Array(rewards.length).fill(0);
    let next = 0;
    for (let t = rewards.length - 1; t >= 0; --t) {
      next = rewards[t] + gamma * next;
      result[t] = next;
    }
    return result;
  }
  function group(rewards) {
    const mean = rewards.reduce((a, b) => a + b, 0) / rewards.length;
    const centered = rewards.map(value => value - mean);
    const sigma = Math.sqrt(centered.reduce((a, value) => a + value * value, 0) / rewards.length);
    return {mean, centered, sigma, defined: sigma > 0,
      advantages: centered.map(value => sigma > 0 ? value / sigma : 0)};
  }
  function scale(values, pixels = 104) {
    return pixels / Math.max(1, ...values.map(Math.abs));
  }
  const api = {returns, group, scale};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else globalThis.PolicyCreditMath = api;
})();
