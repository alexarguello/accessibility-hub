/**
 * Makes wide markdown tables reachable by keyboard (WCAG 2.1.1).
 *
 * Docusaurus renders tables with overflow: auto, so a table wider than the page
 * scrolls sideways. Keyboard users can only scroll it if it can take focus.
 * This adds tabindex="0" to tables that actually overflow, and removes it when
 * they don't, so narrow tables don't become extra Tab stops.
 */
function updateScrollableTables() {
  document.querySelectorAll('.markdown table').forEach((table) => {
    const overflows = table.scrollWidth > table.clientWidth + 1;
    if (overflows && !table.hasAttribute('tabindex')) {
      table.setAttribute('tabindex', '0');
      table.dataset.scrollFocus = 'true';
    } else if (!overflows && table.dataset.scrollFocus === 'true') {
      table.removeAttribute('tabindex');
      delete table.dataset.scrollFocus;
    }
  });
}

if (typeof window !== 'undefined') {
  window.addEventListener('resize', updateScrollableTables);
}

export function onRouteDidUpdate() {
  // Wait one frame so the new page's tables are in the DOM and laid out.
  window.requestAnimationFrame(updateScrollableTables);
}
