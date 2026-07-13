import { courses } from "./data.js";

const grid = document.getElementById("course-grid");
const searchInput = document.getElementById("search-courses");
const resultsCount = document.getElementById("results-count");
const menuToggle = document.getElementById("menu-toggle");
const primaryNav = document.getElementById("primary-nav");
const exploreBtn = document.getElementById("explore-btn");

/* -----------------------------------------------------------
   TASK 1 & 2: Semantic, accessible rendering of course cards
   ----------------------------------------------------------- */

function renderCourses(list) {
  grid.innerHTML = "";

  list.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    // Fix: cards are keyboard-focusable, not just mouse-clickable
    article.tabIndex = 0;
    article.setAttribute(
      "aria-label",
      `${course.name}, ${course.code}, ${course.credits} credits, grade ${course.grade}`
    );
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    grid.appendChild(article);
  });

  // Fix: the live region announces the updated count to screen readers
  resultsCount.textContent = `${list.length} course${
    list.length === 1 ? "" : "s"
  } found`;
}

function selectCourse(article) {
  const label = article.getAttribute("aria-label");
  // A simple, accessible way to surface the selection without relying
  // solely on a blocking alert().
  resultsCount.textContent = `Selected: ${label}`;
}

// Event delegation for both click and keyboard activation
grid.addEventListener("click", (event) => {
  const card = event.target.closest(".course-card");
  if (card) selectCourse(card);
});

grid.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") return;
  const card = event.target.closest(".course-card");
  if (!card) return;
  event.preventDefault();
  selectCourse(card);
});

/* -----------------------------------------------------------
   Search filtering
   ----------------------------------------------------------- */

searchInput.addEventListener("input", (event) => {
  const term = event.target.value.toLowerCase();
  const filtered = courses.filter((course) =>
    course.name.toLowerCase().includes(term)
  );
  renderCourses(filtered);
});

/* -----------------------------------------------------------
   TASK 2: aria-expanded hamburger toggle for the mobile nav
   ----------------------------------------------------------- */

menuToggle.addEventListener("click", () => {
  const isOpen = primaryNav.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
});

/* -----------------------------------------------------------
   Explore Courses button scrolls to and focuses the courses
   heading so keyboard/screen-reader users land in the right spot
   ----------------------------------------------------------- */

exploreBtn.addEventListener("click", () => {
  const coursesHeading = document.querySelector("#courses h2");
  coursesHeading.setAttribute("tabindex", "-1");
  coursesHeading.scrollIntoView({ behavior: "smooth" });
  coursesHeading.focus();
});

/* -----------------------------------------------------------
   Highlight the current section's nav link with aria-current
   as the user scrolls, so the "active" indicator stays accurate
   ----------------------------------------------------------- */

const navLinks = document.querySelectorAll("[data-nav-link]");
const sections = ["hero", "courses", "profile", "grades"].map((id) =>
  document.getElementById(id)
);

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => link.removeAttribute("aria-current"));
      const match = document.querySelector(
        `[data-nav-link][href="#${entry.target.id}"]`
      );
      if (match) match.setAttribute("aria-current", "page");
    });
  },
  { threshold: 0.5 }
);

sections.forEach((section) => observer.observe(section));

renderCourses(courses);
