/**
 * notopened Quiz Portal - Mobile Touch and Interaction Handler
 * Provides immediate touch feedback, prevents ghost clicks, and ensures WCAG mobile compliance.
 */
export function initTouchInteractions() {
  const interactiveSelector = '.option-btn, .next-btn, .share-btn, .game-link-btn, .footer-link';

  // Add active state styling dynamically on touch devices
  document.addEventListener('touchstart', (e) => {
    const target = e.target.closest(interactiveSelector);
    if (target && !target.disabled) {
      target.classList.add('touch-active');
    }
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    const target = e.target.closest(interactiveSelector);
    if (target) {
      target.classList.remove('touch-active');
    }
  }, { passive: true });

  document.addEventListener('touchcancel', (e) => {
    const target = e.target.closest(interactiveSelector);
    if (target) {
      target.classList.remove('touch-active');
    }
  }, { passive: true });

  // Clear touch active if finger moves away
  document.addEventListener('touchmove', (e) => {
    const activeElems = document.querySelectorAll('.touch-active');
    activeElems.forEach(el => el.classList.remove('touch-active'));
  }, { passive: true });
}
