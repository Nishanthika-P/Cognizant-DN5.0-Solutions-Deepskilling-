// ================================================
// HANDS-ON 3 — app.js
// ES6+ syntax, DOM manipulation, event listeners
// Loaded as:  <script type="module" src="app.js">
// ================================================

import { courses } from './data.js';


/* ================================================
   TASK 1 — ES6+ SYNTAX PRACTICE
   ================================================ */

// --- Destructuring in a loop ---
console.group('Task 1 — ES6+ Syntax');

for (const course of courses) {
  // Destructure name and credits directly from each object
  const { name, credits } = course;
  console.log(`Destructured → ${name}: ${credits} credits`);
}

// --- Array.map(): format each course as a readable string ---
const courseStrings = courses.map(
  ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);
console.log('\nFormatted course strings (Array.map):');
console.log(courseStrings);

// --- Array.filter(): only courses with 4+ credits ---
const heavyCourses = courses.filter(course => course.credits >= 4);
console.log(`\nCourses with ≥4 credits (Array.filter): ${heavyCourses.length}`);

// --- Array.reduce(): sum of all credits ---
// The accumulator starts at 0 and adds each course's credits
const totalCredits = courses.reduce((acc, course) => acc + course.credits, 0);
console.log(`\nTotal credits enrolled (Array.reduce): ${totalCredits}`);

console.groupEnd();


/* ================================================
   TASK 2 — DOM SELECTION & DYNAMIC RENDERING
   ================================================ */

// Keep a mutable working copy for sort/filter operations
let displayCourses = [...courses];

const courseGrid     = document.querySelector('.course-grid');
const totalCreditsEl = document.querySelector('#total-credits');
const selectedEl     = document.querySelector('#selected-course');

/**
 * createCourseCard(course)
 * ─────────────────────────
 * Creates and returns a single <article> DOM node
 * from a course data object.
 *
 * We use innerHTML with a template literal here because
 * the data comes from our own controlled array (no user
 * input), so XSS is not a concern.
 */
function createCourseCard(course) {
  const article = document.createElement('article');
  article.className = 'course-card';
  // Store the course id as a data attribute for event delegation
  article.dataset.courseId = course.id;

  // Template literal builds the card's inner HTML
  article.innerHTML = `
    <h3>${course.name}</h3>
    <p>Course Code: <strong>${course.code}</strong></p>
    <span class="credits">${course.credits} Credits</span>
    <span class="grade">Grade: ${course.grade}</span>
  `;
  return article;
}

/**
 * renderCourses(courseList)
 * ──────────────────────────
 * Clears the grid and re-renders cards for each
 * course in the provided array.
 *
 * We use a DocumentFragment to batch all DOM insertions
 * into a single reflow — more efficient than calling
 * appendChild() once per card.
 */
function renderCourses(courseList) {
  courseGrid.innerHTML = '';           // clear existing cards

  const fragment = document.createDocumentFragment();
  courseList.forEach(course => {
    fragment.appendChild(createCourseCard(course));
  });
  courseGrid.appendChild(fragment);   // single DOM update

  // Update total credits paragraph dynamically
  const shownTotal = courseList.reduce((acc, c) => acc + c.credits, 0);
  totalCreditsEl.textContent = `Total Credits: ${shownTotal}`;
}

// Initial render on page load
renderCourses(displayCourses);


/* ================================================
   TASK 3 — EVENT LISTENERS & INTERACTIVITY
   ================================================ */

// ── Search input ─────────────────────────────────
const searchInput = document.querySelector('#search-courses');

searchInput.addEventListener('input', () => {
  const term = searchInput.value.toLowerCase().trim();

  // Filter the master courses array (not displayCourses) so
  // the full list is always the starting point for searches
  const filtered = courses.filter(course =>
    course.name.toLowerCase().includes(term)
  );

  displayCourses = filtered;
  renderCourses(displayCourses);
});


// ── Sort by Credits button ────────────────────────
const sortBtn = document.querySelector('#sort-btn');

sortBtn.addEventListener('click', () => {
  // Sort descending (highest credits first).
  // We spread into a new array to avoid mutating the
  // original courses array — then re-assign displayCourses.
  displayCourses = [...displayCourses].sort(
    (a, b) => b.credits - a.credits
  );
  renderCourses(displayCourses);
});


// ── Event Delegation — card click ────────────────
// Attach ONE listener to the parent grid instead of
// one per card. When a card (or its child) is clicked,
// event.target.closest('.course-card') walks up the DOM
// to find the nearest ancestor article.course-card.

courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (!card) return;   // click was outside any card

  // Find the matching course using the data attribute we set
  const courseId = Number(card.dataset.courseId);
  const course   = courses.find(c => c.id === courseId);

  if (course) {
    // Update the selected-course display element (no alert needed)
    selectedEl.textContent =
      `Selected: ${course.name} (${course.code}) — Grade: ${course.grade}`;
  }
});
