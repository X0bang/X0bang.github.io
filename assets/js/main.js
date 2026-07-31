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

  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {}
    });
  }

  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  var onScheme = function (e) {
    var stored = null;
    try {
      stored = localStorage.getItem("theme");
    } catch (err) {}
    if (!stored) root.setAttribute("data-theme", e.matches ? "dark" : "light");
  };
  if (mq.addEventListener) mq.addEventListener("change", onScheme);
  else if (mq.addListener) mq.addListener(onScheme);

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
     into view. Only the active Projects view can intersect — the other two
     are display:none — so a handful of clips animate rather than every copy
     of every card. Reduced motion leaves the still in place. */

  function playAnimatedThumb(img) {
    var anim = img.getAttribute("data-anim");
    if (anim && img.getAttribute("src") !== anim) img.src = anim;
  }

  var animThumbs = document.querySelectorAll(".pub-thumb img[data-anim]");
  if (!reduced && animThumbs.length && "IntersectionObserver" in window) {
    var animIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            playAnimatedThumb(entry.target);
            animIO.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "150px 0px", threshold: 0.01 }
    );
    Array.prototype.forEach.call(animThumbs, function (img) {
      animIO.observe(img);
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

      var more = card.querySelector(".pub-more");
      if (more) {
        more.addEventListener("click", function (e) {
          e.preventDefault();
          card.classList.toggle("open");
        });
      }
    }
  );
})();
