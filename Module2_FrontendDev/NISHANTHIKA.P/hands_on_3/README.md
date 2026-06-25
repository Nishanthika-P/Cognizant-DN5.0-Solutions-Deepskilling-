# Hands-On 3 — JavaScript ES6+ & DOM Manipulation

**Program:** Digital Nurture 5.0 — Python Full Stack Engineer Track  
**Module:** Module 2 — Frontend Development  
---

## Topics Covered
- `let` / `const` / `var`
- Arrow Functions & Template Literals
- Array Methods (`map`, `filter`, `reduce`)
- DOM Selection & Modification
- Event Listeners
- ES6 Modules (`import` / `export`)

---

## Files
```
hands_on_03/
├── index.html      
├── styles.css      
├── data.js         
├── app.js         
└── README.md     
```



## Task Breakdown

### Task 1 — ES6+ Syntax Practice
| Step | What was done |
|------|--------------|
| 29 | Created `data.js` with `export const courses` — array of 5 course objects (`id`, `name`, `code`, `credits`, `grade`) |
| 30 | In `app.js`, imported using `import { courses } from './data.js'`; used destructuring `const { name, credits } = course` in a loop |
| 31 | Used `Array.map()` to create formatted strings: `"CS101 — Data Structures (4 credits)"` |
| 32 | Used `Array.filter()` to get courses with `credits >= 4`; logged the count |
| 33 | Used `Array.reduce()` to calculate total credits enrolled |
| 34 | Rewrote loops as arrow functions; used template literals for string interpolation |

**Key concept — `const` vs immutability:**  
`const` prevents the variable binding from being reassigned, but does NOT make arrays/objects immutable. You can still `.push()` to a `const` array.

**Key concept — Destructuring:**  
```js
const { name, credits } = course;
// cleaner than: course.name, course.credits
```

---

### Task 2 — DOM Selection & Dynamic Rendering
| Step | What was done |
|------|--------------|
| 35 | `index.html` has an empty `<div class="course-grid">` — no hardcoded articles |
| 36 | Selected the grid with `document.querySelector('.course-grid')` |
| 37 | Created each `<article>` using `document.createElement()`, set `className` and `innerHTML` via template literal |
| 38 | Used `DocumentFragment` to batch-append all cards in a single DOM update (better performance than repeated `appendChild`) |
| 39 | Updated `<p id="total-credits">` dynamically after rendering using `textContent` |


---

### Task 3 — Event Listeners & Interactivity
| Step | What was done |
|------|--------------|
| 40 | Added `<input id="search-courses">` above the course grid |
| 41 | Attached `'input'` event listener — filters the courses array on every keystroke (case-insensitive) and re-renders matching cards |
| 42 | Added `Sort by Credits` button — on click, sorts `displayCourses` descending by credits and re-renders |
| 43 | Clicking a card updates `<p id="selected-course">` with that course's name and grade |
| 44 | Used **event delegation**: single `'click'` listener on `.course-grid`; detects which card was clicked via `event.target.closest('.course-card')` |


**Key concept — Re-rendering safely:**  
Always clear the container before re-rendering to avoid duplicate cards:
```js
courseGrid.innerHTML = '';  // clear first
// then append new cards
```




---

## Expected Output
- Console logs: formatted course strings, filtered count (`3`), total credits (`18`)
- Page: 5 course cards rendered dynamically from `data.js`
- Search box filters cards in real time
- Sort button reorders cards by credits (descending)
- Clicking a card shows its name and grade below the grid
