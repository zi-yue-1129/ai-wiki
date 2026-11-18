// Test-only DOM selection for the exact selector used by concept-motion.js.
const assert = require('node:assert/strict');
module.exports = (selector, images) => {
  assert.equal(selector, 'img[src*="concept-animations/"]', 'Review changed production selector explicitly');
  return images.filter(image => String(image.getAttribute('src') || '').includes('concept-animations/'));
};
