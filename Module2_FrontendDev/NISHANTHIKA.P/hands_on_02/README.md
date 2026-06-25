# Hands-On 2 — CSS Flexbox, Grid & Responsive Design

**Program:** Digital Nurture 5.0 — Python Full Stack Engineer Track  
**Module:** Module 2 — Frontend Development  


---

## Topics Covered
- CSS Flexbox
- CSS Grid
- Mobile-First Design
- Media Queries
- Viewport Units & Fluid Layouts

---

## Files
```
hands_on_02/
├── index.html      
├── styles.css     
└── README.md       
```

---

## Task Breakdown

### Task 1 — Flexbox Navigation & Header Layout
| Step | What was done |
|------|--------------|
| 14 | Revisited `<header>` from Hands-On 1 |
| 15 | Applied `display: flex`, `align-items: center`, `justify-content: space-between` on header |
| 16 | Styled `<nav>` as a flex container with `gap` between links, vertically centred |
| 17 | Hero section uses `flex-direction: column` + `align-items: center` to stack heading, paragraph, and button vertically |
| 18 | Added a stats bar below the hero with 3 stat items (Courses Enrolled, GPA, Semester) laid out with `justify-content: space-around` and `flex: 1` on each item |

**Key concept — `flex: 1`:**  
Makes each stat item grow equally to fill all available horizontal space, creating perfectly even columns without fixed widths.

**Key concept — `gap`:**  
Works in both Flexbox and Grid. Cleaner than using `margin` on individual children.

---

### Task 2 — CSS Grid Course Card Layout
| Step | What was done |
|------|--------------|
| 19 | Wrapped all course `<article>` elements in `<div class="course-grid">` |
| 20 | Applied `display: grid` on `.course-grid` with `gap: 1.25rem` |
| 21 | Each `.course-card` uses `align-self: stretch` so all cards in a row share the same height |
| 22 | Added 2 more course cards (total 5) — grid places them automatically |
| 23 | Used `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` — grid reflows columns automatically as viewport narrows |

**Key concept — `auto-fit` + `minmax`:**  
- Each column is at least `280px` wide
- Columns grow equally (`1fr`) to fill remaining space  
- No extra media queries needed for column reflow — the grid handles it automatically

**CSS Grid vs Flexbox:**  
| | Flexbox | Grid |
|--|---------|------|
| Best for | 1D layout (row OR column) | 2D layout (rows AND columns) |
| Used here for | Header, nav, stats bar, hero | Course card layout |

---

### Task 3 — Responsive Design with Media Queries
| Step | What was done |
|------|--------------|
| 24 | Rewrote CSS as **mobile-first**: single-column default, enhanced with `min-width` breakpoints |
| 25 | `@media (min-width: 768px)`: shows full nav links (hides hamburger placeholder), grid adjusts |
| 26 | `@media (min-width: 1024px)`: explicitly sets 3-column grid, increases hero padding |
| 27 | Used `min-height: 40vh` on hero; fluid typography with `clamp(1.1rem, 3vw, 1.4rem)` on site title |
| 28 | Tested at 375px (mobile), 768px (tablet), 1280px (desktop) in DevTools device toolbar |

**Key concept — Mobile-First:**  
Write base styles for the smallest screen first, then use `min-width` media queries to add complexity for wider screens. This is the opposite of `max-width` (desktop-first).

**Key concept — `clamp(min, preferred, max)`:**  
Font sizes scale fluidly between breakpoints. `clamp(1.1rem, 3vw, 1.4rem)` means:  
- Never smaller than `1.1rem`  
- Grows with viewport at `3vw`  
- Never larger than `1.4rem`

---

## Expected Output
- Header with site name and nav aligned using Flexbox
- Stats bar showing 3 items evenly spaced
- 5 course cards in a responsive grid that reflows without JavaScript
- Layout adapts correctly at all three tested breakpoints
