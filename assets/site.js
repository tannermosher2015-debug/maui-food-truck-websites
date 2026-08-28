/* Shared behaviour for every page: mobile nav, header state, scroll reveals.
   Page-specific behaviour (the Today card, the intake form) stays on its page. */
document.documentElement.classList.remove("no-js");
(function () {
  "use strict";
  var reduce = matchMedia("(prefers-reduced-motion:reduce)").matches;

  /* ---- mobile nav ---- */
  var nav = document.getElementById("nav"), navBtn = document.getElementById("navBtn");
  if (nav && navBtn) {
    navBtn.addEventListener("click", function () {
      navBtn.setAttribute("aria-expanded", nav.classList.toggle("open"));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); navBtn.setAttribute("aria-expanded", "false"); }
    });
  }

  /* ---- header goes solid once the hero is behind it.
          Pages with no hero ship .stuck in the markup and are left alone. ---- */
  var head = document.getElementById("head"), hero = document.querySelector(".hero");
  if (head && hero) {
    addEventListener("scroll", function () {
      head.classList.toggle("stuck", scrollY > innerHeight * 0.82);
    }, { passive: true });
  }

  /* ---- scroll reveals. Transform and opacity only, with a safety net. ---- */
  var risers = document.querySelectorAll(".rise");
  function showAll() { for (var i = 0; i < risers.length; i++) risers[i].classList.add("in"); }
  if (reduce || !("IntersectionObserver" in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    for (var i = 0; i < risers.length; i++) io.observe(risers[i]);
    /* An instant jump (anchor link, restored scroll) skips the observer entirely. */
    setTimeout(showAll, 2900);
  }
})();
