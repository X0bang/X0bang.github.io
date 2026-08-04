/* Site behaviour — no framework, no dependencies.
   Theme toggle, mobile nav, scroll progress, scroll reveal, the cover's
   epigraph face, the expanders, the Projects view switch, and the card glow. */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Animations stay off until JS is running, so nothing is hidden without it.
  if (!reduced) document.body.classList.add("anim");

  /* ---- Theme -------------------------------------------------------- */

  var mq = window.matchMedia("(prefers-color-scheme: dark)");

  function stored() {
    try {
      return localStorage.getItem("theme");
    } catch (e) {
      return null;
    }
  }

  function store(v) {
    try {
      if (v) localStorage.setItem("theme", v);
      else localStorage.removeItem("theme");
    } catch (e) {}
  }

  /* A stored theme is an *override*, and an override only means anything while
     it disagrees with the system. Once the two coincide — because the system
     changed, or because the toggle was clicked back — drop it and resume
     following the system. Without this, one click on a dark evening pins the
     site to that theme permanently, which is the bug this replaces. */
  function syncTheme() {
    var sys = mq.matches ? "dark" : "light";
    if (stored() === sys) store(null);
    /* Applies the override too, rather than leaving that to the inline script
       in head.html — same result on load, but this stays correct on its own. */
    root.setAttribute("data-theme", stored() || sys);
  }

  syncTheme();

  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store(next === (mq.matches ? "dark" : "light") ? null : next);
    });
  }

  if (mq.addEventListener) mq.addEventListener("change", syncTheme);
  else if (mq.addListener) mq.addListener(syncTheme);

  /* ---- Mobile navigation -------------------------------------------- */

  var navToggle = document.getElementById("nav-toggle");
  if (navToggle) {
    navToggle.addEventListener("click", function () {
      var nav = navToggle.closest(".site-nav");
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---- Scroll progress + back to top -------------------------------- */

  var bar = document.getElementById("scroll-progress");
  var backToTop = document.querySelector(".back-to-top");
  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset || root.scrollTop;
    var h = root.scrollHeight - root.clientHeight;
    if (bar) bar.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
    if (backToTop) backToTop.classList.toggle("is-visible", y > 400);
    ticking = false;
  }

  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    },
    { passive: true }
  );
  onScroll();

  /* ---- Scroll reveal ------------------------------------------------ */

  var revealables = document.querySelectorAll(".reveal");
  if (!reduced && revealables.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    Array.prototype.forEach.call(revealables, function (el) {
      io.observe(el);
    });
  } else {
    Array.prototype.forEach.call(revealables, function (el) {
      el.classList.add("in");
    });
  }

  /* ---- Cover: swap the contact face for the epigraph ----------------- */

  var cover = document.getElementById("profile-cover");
  var avatar = document.getElementById("avatar-wrap");
  var desc = document.getElementById("my-desc");

  if (cover && avatar && desc && desc.textContent.trim() !== "") {
    var setDeep = function (on) {
      if (on) {
        // First open: attach the warm artwork. Held back until now so the
        // page does not fetch it for a state most visitors never enter.
        var twin = cover.querySelector(".cover-deep[data-src]");
        if (twin) {
          twin.style.backgroundImage = 'url("' + twin.dataset.src + '")';
          twin.removeAttribute("data-src");
        }
      }
      cover.classList.toggle("deep", on);
      avatar.setAttribute("aria-pressed", on ? "true" : "false");
    };

    // Pointer devices reveal it on hover; everything else toggles on click.
    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      avatar.addEventListener("mouseenter", function () {
        setDeep(true);
      });
      cover.addEventListener("mouseleave", function () {
        setDeep(false);
      });
    }

    avatar.addEventListener("click", function () {
      setDeep(!cover.classList.contains("deep"));
    });

    avatar.addEventListener("focus", function () {
      setDeep(true);
    });
    avatar.addEventListener("blur", function () {
      setDeep(false);
    });
    avatar.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setDeep(!cover.classList.contains("deep"));
      }
    });
  }

  /* ---- Expanders ----------------------------------------------------- */

  Array.prototype.forEach.call(
    document.querySelectorAll(".list-toggle"),
    function (btn) {
      var target = document.getElementById(btn.getAttribute("aria-controls"));
      if (!target) return;
      btn.addEventListener("click", function () {
        var open = target.classList.toggle("expanded");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
  );

  /* ---- Projects: Selected / By Year / By Topic ------------------------ */

  var segButtons = document.querySelectorAll(".segmented button[data-view]");
  var views = {
    selected: document.getElementById("projects-selected"),
    "by-year": document.getElementById("projects-by-year"),
    "by-topic": document.getElementById("projects-by-topic")
  };

  Array.prototype.forEach.call(segButtons, function (btn) {
    btn.addEventListener("click", function () {
      var view = btn.getAttribute("data-view");

      Array.prototype.forEach.call(segButtons, function (other) {
        var on = other === btn;
        other.classList.toggle("active", on);
        other.setAttribute("aria-pressed", on ? "true" : "false");
      });

      Object.keys(views).forEach(function (key) {
        if (views[key]) views[key].classList.toggle("is-active", key === view);
      });

      // Cards in a newly shown view have never intersected — reveal them.
      if (views[view]) {
        Array.prototype.forEach.call(
          views[view].querySelectorAll(".reveal"),
          function (el) {
            el.classList.add("in");
          }
        );
      }
    });
  });

  /* ---- Animated thumbnails -------------------------------------------
     They start as a still and swap to the animation once the card scrolls
     into view, and from then on they keep running — scrolling past one no
     longer stops it.

     The observer is still what starts them, and that is deliberate: only the
     active Projects view can intersect, since the other two are display:none,
     so a handful of clips load rather than every copy of every card. Autoplay
     on the element itself would fetch all five copies of both videos at load,
     which is the 7.6MB regression this replaced. */

  function playAnimatedThumb(img) {
    var anim = img.getAttribute("data-anim");
    if (anim && img.getAttribute("src") !== anim) img.src = anim;
  }

  var animThumbs = document.querySelectorAll(
    ".pub-thumb img[data-anim], .pub-thumb video, " +
      ".page-hero img[data-anim], .page-hero video"
  );
  if (!reduced && animThumbs.length && "IntersectionObserver" in window) {
    var animIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          if (el.tagName === "VIDEO") {
            var p = el.play();
            if (p && p.catch) p.catch(function () {});
          } else {
            playAnimatedThumb(el);
          }
          // Started once, left running: stop observing so nothing pauses it.
          animIO.unobserve(el);
        });
      },
      { rootMargin: "150px 0px", threshold: 0.01 }
    );
    Array.prototype.forEach.call(animThumbs, function (el) {
      animIO.observe(el);
    });
  }

  /* ---- Project cards: glow follows the cursor, click to expand -------- */

  Array.prototype.forEach.call(
    document.querySelectorAll(".pub-card"),
    function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", e.clientX - r.left + "px");
        card.style.setProperty("--my", e.clientY - r.top + "px");
      });

      // Hovering also starts it, for anything the observer below misses.
      var thumb = card.querySelector(".pub-thumb img[data-anim]");
      if (thumb && !reduced) {
        card.addEventListener("mouseenter", function () {
          playAnimatedThumb(thumb);
        });
      }

    }
  );

  /* ---- Where readers came from ---------------------------------------

     Only on /visitors/. stats.json is written by the server from its own
     access log — no analytics service, no cookie, no beacon, and nothing
     about a visitor reaches this page beyond a country and a count. */

  var visitors = document.getElementById("visitors");
  if (visitors && window.fetch) {
    // Two regional indicator letters make the flag; no image, no font.
    function flag(cc) {
      if (!/^[A-Z]{2}$/.test(cc)) return "";
      return String.fromCodePoint(
        0x1f1e6 + cc.charCodeAt(0) - 65,
        0x1f1e6 + cc.charCodeAt(1) - 65
      );
    }

    function el(tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text !== undefined) n.textContent = text;
      return n;
    }

    // The mirror keeps no log of its own — read the totals from the host that
    // does. Cross-origin there, which is why that response carries an
    // Access-Control-Allow-Origin header.
    var local =
      location.hostname === "boyuezhang.com" ||
      location.hostname === "www.boyuezhang.com" ||
      location.hostname === "localhost" ||
      location.hostname === "127.0.0.1";

    fetch(local ? "/stats.json" : "https://boyuezhang.com/stats.json", {
      cache: "no-cache",
    })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (d) {
        if (!d || !d.visits) throw new Error("empty");

        var empty = visitors.querySelector(".visitors-empty");
        if (empty) empty.remove();

        // Shade against the busiest country: with one of them at a third of
        // all traffic, sharing a scale with the total leaves the rest flat.
        // The square root keeps the small ones visible without pretending
        // they are close to the top.
        var top = d.countries[0].n;
        d.countries.forEach(function (c) {
          var t = Math.sqrt(c.n / top);
          var land = document.getElementById("c" + c.cc);
          var dot = document.getElementById("d" + c.cc);
          [land, dot].forEach(function (n) {
            if (!n) return;
            n.classList.add("is-hit");
            n.style.setProperty("--t", t.toFixed(3));
            var t2 = n.querySelector("title") || el("title");
            t2.textContent = c.name + " — " + c.n;
            n.appendChild(t2);
          });
        });

        var figures = el("div", "visitors-figures");
        [
          [d.visits, d.visits === 1 ? "visit" : "visits"],
          [d.views, d.views === 1 ? "page view" : "page views"],
          [d.countries.length, d.countries.length === 1 ? "country" : "countries"],
        ].forEach(function (pair) {
          var f = el("div", "visitors-figure");
          f.appendChild(el("span", "visitors-figure-n", String(pair[0])));
          f.appendChild(el("span", "visitors-figure-label", pair[1]));
          figures.appendChild(f);
        });
        visitors.insertBefore(figures, visitors.firstChild);

        var since = new Date(d.since * 1000).toLocaleDateString("en-GB", {
          day: "numeric",
          month: "short",
          year: "numeric",
        });

        var list = el("ul", "visitors-chips");
        d.countries.forEach(function (c) {
          var li = el("li");
          li.appendChild(el("span", "visitors-flag", flag(c.cc)));
          li.appendChild(el("span", "visitors-name", c.name));
          li.appendChild(el("span", "visitors-n", String(c.n)));
          list.appendChild(li);
        });
        visitors.appendChild(list);
        visitors.appendChild(el("p", "visitors-since", "since " + since));
      })
      .catch(function () {
        var empty = visitors.querySelector(".visitors-empty");
        if (empty) empty.textContent = "The count is not reachable from here.";
      });
  }
})();
