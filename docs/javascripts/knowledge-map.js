// Knowledge map: zoom, pan, full screen, drill-down and search for the explorer that
// hooks/knowledge_map.py writes into a page. The layout arrives as JSON; this script only draws it.
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var LABEL_ZOOM = 1.6; // topic labels appear once the map is zoomed this far past "fit"
  var MIN_ZOOM = 0.5; // relative to "fit"
  var MAX_ZOOM = 8;

  function element(tag, attrs, parent) {
    var node = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach(function (name) {
      node.setAttribute(name, attrs[name]);
    });
    if (parent) parent.appendChild(node);
    return node;
  }

  function clamp(value, low, high) {
    return Math.min(high, Math.max(low, value));
  }

  function Explorer(root) {
    var data = JSON.parse(root.querySelector(".km-data").textContent);
    var text = data.text;
    var crumbs = root.querySelector(".km-crumbs");
    var input = root.querySelector(".km-search-input");
    var results = root.querySelector(".km-results");
    var stage = root.querySelector(".km-stage");
    var info = root.querySelector(".km-info");
    var fullButton = root.querySelector(".km-full");

    var svg = element("svg", { "class": "km-svg", role: "group", "aria-label": text.aria });
    var world = element("g", {}, svg);
    var edgeLayer = element("g", {}, world);
    var clusterLayer = element("g", {}, world);
    var nodeLayer = element("g", {}, world);
    stage.appendChild(svg);

    var viewKey = "";
    var view = null;
    var edgeEls = [];
    var nodeEls = [];
    var neighbours = [];
    var selected = -1;
    var hovered = -1;
    var k = 1;
    var fitK = 1;
    var tx = 0;
    var ty = 0;
    var pointers = {};
    var drag = null;
    var lastDistance = null;
    var moved = false;
    var lastWidth = 0;

    function local(ev) {
      var box = svg.getBoundingClientRect();
      return { x: ev.clientX - box.left, y: ev.clientY - box.top };
    }

    function size() {
      var box = svg.getBoundingClientRect();
      return { w: box.width, h: box.height };
    }

    function apply() {
      world.setAttribute("transform", "translate(" + tx + " " + ty + ") scale(" + k + ")");
      svg.style.setProperty("--km-k", k);
      svg.classList.toggle("km-zoomed", k >= fitK * LABEL_ZOOM);
    }

    function fit() {
      var box = size();
      var w = box.w;
      var h = box.h;
      if (!view || !w || !h) return;
      lastWidth = w;
      fitK = Math.min(w / view.w, h / view.h) * 0.96;
      k = fitK;
      tx = (w - view.w * k) / 2;
      ty = (h - view.h * k) / 2;
      apply();
    }

    function zoomAt(x, y, factor) {
      var next = clamp(k * factor, fitK * MIN_ZOOM, fitK * MAX_ZOOM);
      var ratio = next / k;
      tx = x - (x - tx) * ratio;
      ty = y - (y - ty) * ratio;
      k = next;
      apply();
    }

    function zoomCentre(factor) {
      var box = size();
      zoomAt(box.w / 2, box.h / 2, factor);
    }

    function focusNode(i) {
      var n = view.nodes[i];
      var box = size();
      k = clamp(fitK * 2.4, fitK, fitK * MAX_ZOOM);
      tx = box.w / 2 - n.x * k;
      ty = box.h / 2 - n.y * k;
      apply();
    }

    function highlight() {
      var focus = hovered >= 0 ? hovered : selected;
      var hot = {};
      if (focus >= 0) {
        hot[focus] = true;
        neighbours[focus].forEach(function (pair) {
          hot[pair.to] = true;
        });
      }
      svg.classList.toggle("km-focus", focus >= 0);
      nodeEls.forEach(function (g, j) {
        g.classList.toggle("km-hot", !!hot[j]);
        g.classList.toggle("km-on", j === focus);
      });
      edgeEls.forEach(function (line, n) {
        var edge = view.edges[n];
        line.classList.toggle("km-hot", focus >= 0 && (edge.a === focus || edge.b === focus));
      });
    }

    function showInfo() {
      info.textContent = "";
      info.hidden = selected < 0;
      if (selected < 0) return;
      var n = view.nodes[selected];
      var strong = document.createElement("strong");
      strong.textContent = n.title;
      var meta = document.createElement("span");
      meta.className = "km-meta";
      meta.textContent = [data.titles[n.section], n.status ? text[n.status] : null].filter(Boolean).join(" · ");
      info.append(strong, meta);
      if (n.href) {
        var link = document.createElement("a");
        link.href = n.href;
        link.textContent = text.open + " →";
        info.append(link);
      }
      var clear = document.createElement("button");
      clear.type = "button";
      clear.className = "km-clear";
      clear.textContent = "×";
      clear.setAttribute("aria-label", text.clear);
      clear.addEventListener("click", function () {
        select(-1);
      });
      info.append(clear);
    }

    function select(i) {
      selected = i;
      highlight();
      showInfo();
    }

    function renderCrumbs() {
      crumbs.textContent = "";
      var chain = [];
      for (var key = viewKey; key !== null; key = data.views[key].parent) {
        chain.unshift(key);
      }
      chain.forEach(function (key, n) {
        if (n > 0) {
          var sep = document.createElement("span");
          sep.className = "km-sep";
          sep.textContent = "›";
          crumbs.append(sep);
        }
        var title = key === "" ? text.all : data.views[key].title;
        var item = document.createElement(key === viewKey ? "span" : "button");
        item.textContent = title;
        if (key === viewKey) {
          item.setAttribute("aria-current", "page");
        } else {
          item.type = "button";
          item.addEventListener("click", function () {
            show(key, null);
          });
        }
        crumbs.append(item);
      });
      if (view.href) {
        var open = document.createElement("a");
        open.href = view.href;
        open.className = "km-open";
        open.textContent = text.open + " →";
        crumbs.append(open);
      }
    }

    function activate(i) {
      var n = view.nodes[i];
      if (n.view !== null && n.view !== undefined) {
        show(n.view, null);
      } else {
        select(i);
      }
    }

    function show(key, focus) {
      viewKey = key;
      view = data.views[key];
      edgeLayer.textContent = "";
      clusterLayer.textContent = "";
      nodeLayer.textContent = "";
      edgeEls = [];
      nodeEls = [];
      neighbours = view.nodes.map(function () {
        return [];
      });
      selected = -1;
      hovered = -1;

      view.edges.forEach(function (edge, n) {
        neighbours[edge.a].push({ to: edge.b });
        neighbours[edge.b].push({ to: edge.a });
        var a = view.nodes[edge.a];
        var b = view.nodes[edge.b];
        edgeEls.push(element("line", {
          "class": "km-edge",
          x1: a.x, y1: a.y, x2: b.x, y2: b.y,
          "stroke-width": 0.9 + Math.min(edge.w, 8) * 0.45
        }, edgeLayer));
      });

      view.clusters.forEach(function (c) {
        var label = element("text", { "class": "km-cluster", x: c.x, y: c.y, "text-anchor": "middle" }, clusterLayer);
        label.textContent = c.text;
      });

      view.nodes.forEach(function (n, i) {
        var classes = "km-node km-" + n.kind + (n.status === "draft" ? " km-draft" : "");
        var g = element("g", {
          "class": classes,
          tabindex: "0",
          role: "button",
          "aria-label": n.title
        }, nodeLayer);
        var disc = { cx: n.x, cy: n.y, r: n.r, fill: n.fill };
        if (n.status === "draft") disc.stroke = n.fill;
        element("circle", disc, g);
        var label = element("text", { "class": "km-label", x: n.x, y: n.y + n.r + 4 }, g);
        n.lines.forEach(function (line, j) {
          var span = element("tspan", { x: n.x, dy: j === 0 ? "1em" : "1.2em" }, label);
          span.textContent = line;
        });
        g.addEventListener("click", function () {
          if (!moved) activate(i);
        });
        g.addEventListener("keydown", function (ev) {
          if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            activate(i);
          }
        });
        g.addEventListener("pointerenter", function (ev) {
          if (ev.pointerType === "mouse") {
            hovered = i;
            highlight();
          }
        });
        g.addEventListener("pointerleave", function () {
          hovered = -1;
          highlight();
        });
        nodeEls.push(g);
      });

      fit();
      renderCrumbs();
      if (focus !== null && focus !== undefined) {
        select(focus);
        focusNode(focus);
      } else {
        showInfo();
        highlight();
      }
    }

    // Pan and pinch: pointer events cover mouse, pen and touch alike.
    svg.addEventListener("pointerdown", function (ev) {
      var p = local(ev);
      pointers[ev.pointerId] = { x: p.x, y: p.y, cx: ev.clientX, cy: ev.clientY };
      if (Object.keys(pointers).length === 1) {
        drag = { x: ev.clientX, y: ev.clientY, tx: tx, ty: ty };
        moved = false;
      }
    });

    window.addEventListener("pointermove", function (ev) {
      var pointer = pointers[ev.pointerId];
      if (!pointer) return;
      var p = local(ev);
      pointer.x = p.x;
      pointer.y = p.y;
      pointer.cx = ev.clientX;
      pointer.cy = ev.clientY;
      var ids = Object.keys(pointers);
      if (ids.length === 1 && drag) {
        var dx = ev.clientX - drag.x;
        var dy = ev.clientY - drag.y;
        if (Math.hypot(dx, dy) > 4) moved = true;
        if (moved) {
          tx = drag.tx + dx;
          ty = drag.ty + dy;
          apply();
        }
      } else if (ids.length === 2) {
        var a = pointers[ids[0]];
        var b = pointers[ids[1]];
        var distance = Math.hypot(a.x - b.x, a.y - b.y);
        if (lastDistance) {
          moved = true;
          zoomAt((a.x + b.x) / 2, (a.y + b.y) / 2, distance / lastDistance);
        }
        lastDistance = distance;
      }
    });

    function release(ev) {
      if (!pointers[ev.pointerId]) return;
      delete pointers[ev.pointerId];
      lastDistance = null;
      var ids = Object.keys(pointers);
      if (ids.length === 1) {
        var left = pointers[ids[0]];
        drag = { x: left.cx, y: left.cy, tx: tx, ty: ty };
      } else {
        drag = null;
      }
    }
    window.addEventListener("pointerup", release);
    window.addEventListener("pointercancel", release);

    svg.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var p = local(ev);
      zoomAt(p.x, p.y, Math.exp(-ev.deltaY * 0.0015));
    }, { passive: false });

    // Search: a result opens the view that holds its circle, then zooms to it.
    function renderResults() {
      var query = input.value.trim().toLowerCase();
      results.textContent = "";
      results.hidden = query === "";
      if (!query) return;
      var hits = data.search.filter(function (entry) {
        return entry.t.toLowerCase().indexOf(query) !== -1;
      }).slice(0, 8);
      if (!hits.length) {
        var none = document.createElement("li");
        none.textContent = text.no_match;
        results.append(none);
        return;
      }
      hits.forEach(function (entry) {
        var item = document.createElement("li");
        var button = document.createElement("button");
        button.type = "button";
        button.textContent = entry.t;
        var small = document.createElement("small");
        small.textContent = data.titles[entry.s] || "";
        button.append(small);
        button.addEventListener("click", function () {
          choose(entry);
        });
        item.append(button);
        results.append(item);
      });
    }

    function choose(entry) {
      input.value = "";
      results.hidden = true;
      show(entry.v, entry.i);
    }

    input.addEventListener("input", renderResults);
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        ev.preventDefault();
        var first = data.search.find(function (entry) {
          return entry.t.toLowerCase().indexOf(input.value.trim().toLowerCase()) !== -1;
        });
        if (first) choose(first);
      } else if (ev.key === "Escape") {
        input.value = "";
        results.hidden = true;
      }
    });

    root.querySelector(".km-zoom-in").addEventListener("click", function () {
      zoomCentre(1.4);
    });
    root.querySelector(".km-zoom-out").addEventListener("click", function () {
      zoomCentre(1 / 1.4);
    });
    root.querySelector(".km-fit").addEventListener("click", fit);

    function setFullscreen(on) {
      root.classList.toggle("km-fullscreen", on);
      document.body.classList.toggle("km-lock", on);
      fullButton.setAttribute("aria-pressed", String(on));
      fullButton.setAttribute("aria-label", on ? text.exit : text.full);
      fullButton.title = on ? text.exit : text.full;
      requestAnimationFrame(fit);
    }
    fullButton.addEventListener("click", function () {
      setFullscreen(!root.classList.contains("km-fullscreen"));
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && root.classList.contains("km-fullscreen")) setFullscreen(false);
    });

    window.addEventListener("resize", function () {
      var box = size();
      if (box.w && box.w !== lastWidth) fit();
    });

    // The page is ready: show the map.
    root.classList.add("km-ready");
    show("", null);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".km-explorer").forEach(function (root) {
      Explorer(root);
    });
  });
})();
