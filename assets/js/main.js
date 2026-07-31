/* Site behaviour: theme toggle, mobile nav, scroll progress, list expanders
   and the Projects "By Year / By Topic" switch. No framework, no dependencies. */

(function () {
  "use strict";

  var root = document.documentElement;

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

  // Follow the OS while the visitor has not made an explicit choice.
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  var onSchemeChange = function (e) {
    var stored = null;
    try {
      stored = localStorage.getItem("theme");
    } catch (err) {}
    if (!stored) root.setAttribute("data-theme", e.matches ? "dark" : "light");
  };
  if (mq.addEventListener) mq.addEventListener("change", onSchemeChange);
  else if (mq.addListener) mq.addListener(onSchemeChange);

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
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    var height =
      document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (bar) bar.style.width = (height > 0 ? (scrolled / height) * 100 : 0) + "%";
    if (backToTop) backToTop.classList.toggle("is-visible", scrolled > 400);
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

  /* ---- "Show all" / "Show less" ------------------------------------- */

  Array.prototype.forEach.call(
    document.querySelectorAll(".list-toggle"),
    function (btn) {
      btn.addEventListener("click", function () {
        var section = btn.closest(".section");
        if (!section) return;
        var expanded = section.classList.toggle("is-expanded");
        btn.setAttribute("aria-expanded", expanded ? "true" : "false");
      });
    }
  );

  /* ---- Projects: By Year / By Topic --------------------------------- */

  var switches = document.querySelectorAll(".section-switch .switch-btn");
  Array.prototype.forEach.call(switches, function (btn) {
    btn.addEventListener("click", function () {
      var view = btn.getAttribute("data-view");

      Array.prototype.forEach.call(switches, function (other) {
        var active = other === btn;
        other.classList.toggle("is-active", active);
        other.setAttribute("aria-pressed", active ? "true" : "false");
      });

      var byYear = document.getElementById("projects-by-year");
      var byTopic = document.getElementById("projects-by-topic");
      if (byYear) byYear.classList.toggle("is-active", view === "by-year");
      if (byTopic) byTopic.classList.toggle("is-active", view === "by-topic");
    });
  });
})();
