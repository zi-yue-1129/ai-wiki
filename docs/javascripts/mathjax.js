/* Preserve MathJax's initial rendering and only typeset new article content. */
(() => {
  let previousArticle = null;

  function typesetArticle() {
    const article = document.querySelector('.md-content__inner');
    const math = window.MathJax;
    // MathJax 3 calls must be serialized with its automatic initial typeset.
    // Clearing and rescanning that output would typeset its assistive MathML
    // again, nesting mjx-container nodes and widening hidden inline formulas.
    math.startup.promise = math.startup.promise.then(async () => {
      if (!article || !article.isConnected || article === previousArticle) return;
      if (previousArticle) math.typesetClear([previousArticle]);
      const pending = Array.from(article.querySelectorAll('.arithmatex'))
        .filter(node => !node.querySelector('mjx-container'));
      if (pending.length) {
        math.texReset();
        await math.typesetPromise(pending);
      }
      previousArticle = article;
    });
    return math.startup.promise;
  }

  window.MathJax = {
    tex: {
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      ignoreHtmlClass: ".*|",
      processHtmlClass: "arithmatex"
    },
    startup: {
      ready() {
        window.MathJax.startup.defaultReady();
        // Material replays its current document when subscribing, then emits
        // new documents if instant navigation is enabled in the future.
        document$.subscribe(typesetArticle);
      }
    }
  };
})();
