# Hands-On 9: Web Accessibility (a11y) & Cross-Browser Compatibility


- **Task 1 — Audit & semantic fixes**: a comment block at the top of
  `index.html` records the baseline Lighthouse score and the five issues
  found (missing labels, a skipped heading level, no keyboard support on
  cards, low-contrast button, an unnamed `<nav>`), each with a matching
  fix elsewhere in the file. Every `<input>` has an associated `<label>`;
  headings run `h1 -> h2 -> h3` with no skipped levels.
  
- **Task 2 — ARIA & keyboard navigation**: `aria-label="Main navigation"`
  on `<nav>`, `aria-current="page"` tracked automatically as the user
  scrolls (via `IntersectionObserver` in `app.js`), course cards are
  `tabindex="0"` with a `keydown` handler so Enter/Space activates them
  the same as a click, the results count is `role="status"
  aria-live="polite"` so screen readers announce updates, and the mobile
  menu button toggles `aria-expanded` between `true`/`false`.
  
- **Task 3 — Colour contrast & cross-browser**: `styles.css` opens with a
  documented before/after contrast check (hex values and ratios) for the
  hero button and body text, both now passing the WCAG AA 4.5:1 minimum.
  A caniuse summary for CSS Grid, `clamp()`, and flex `gap` is included
  as a comment, along with a `css-vars-ponyfill` CDN script as a fallback
  for browsers without native CSS custom property support.


## Notes
- No emojis are used anywhere in the UI text.
