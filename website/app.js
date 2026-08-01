document.addEventListener('DOMContentLoaded', () => {
  const reduceMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  if (reduceMotionQuery.matches) {
    document.documentElement.style.scrollBehavior = 'auto';
    const orbitEls = document.querySelectorAll('.orbit');
    orbitEls.forEach((el) => {
      el.style.animation = 'none';
    });
  }
});
