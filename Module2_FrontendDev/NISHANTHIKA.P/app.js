import { courses } from "./data.js";

const JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com";

/* -----------------------------------------------------------
   TASK 1: Promises and async/await
   ----------------------------------------------------------- */

// 45. fetchUser with .then() chaining
function fetchUserWithThen(id) {
  return fetch(`${JSONPLACEHOLDER_BASE}/users/${id}`)
    .then((response) => response.json())
    .then((user) => {
      console.log("[.then] User name:", user.name);
      return user;
    });
}

// 46. Same function rewritten with async/await + try/catch
async function fetchUser(id) {
  try {
    const response = await fetch(`${JSONPLACEHOLDER_BASE}/users/${id}`);
    const user = await response.json();
    console.log("[async/await] User name:", user.name);
    return user;
  } catch (error) {
    console.error("fetchUser failed:", error.message);
    throw error;
  }
}

// 47. Simulated network delay returning local course data
function fetchAllCourses() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(courses), 1000);
  });
}

// 49. Promise.all demo — fetch two users simultaneously
async function fetchTwoUsersTogether() {
  const resultEl = document.getElementById("users-result");
  resultEl.textContent = "Loading users 1 and 2...";
  try {
    const [userOne, userTwo] = await Promise.all([
      fetchUser(1),
      fetchUser(2),
    ]);
    resultEl.textContent = `Loaded together: ${userOne.name} and ${userTwo.name}`;
  } catch (error) {
    resultEl.textContent = "Failed to load users.";
  }
}

/* -----------------------------------------------------------
   TASK 2: Fetch API with error handling
   ----------------------------------------------------------- */

// 50. Reusable fetch wrapper that throws on non-OK responses
async function apiFetch(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed (${response.status}): ${url}`);
  }
  return response.json();
}

let lastNotificationsUrl = `${JSONPLACEHOLDER_BASE}/posts?_limit=5`;

async function loadNotifications(url) {
  lastNotificationsUrl = url;
  const statusEl = document.getElementById("notifications-status");
  const listEl = document.getElementById("notifications-list");
  const retryBtn = document.getElementById("retry-btn");

  retryBtn.classList.add("hidden");
  statusEl.textContent = "Loading notifications...";
  statusEl.classList.remove("error-message");
  listEl.innerHTML = "";

  try {
    const posts = await apiFetch(url);
    statusEl.textContent = `${posts.length} notifications loaded.`;
    listEl.innerHTML = posts
      .map(
        (post) => `
          <article class="notification-card">
            <strong>${post.title}</strong>
            <p>${post.body}</p>
          </article>
        `
      )
      .join("");
  } catch (error) {
    statusEl.textContent = `Could not load notifications: ${error.message}`;
    statusEl.classList.add("error-message");
    retryBtn.classList.remove("hidden");
  }
}

/* -----------------------------------------------------------
   TASK 3: Introduction to Axios
   ----------------------------------------------------------- */

// 56. apiFetch rewritten using axios.get — Axios auto-parses JSON
//     and rejects automatically on non-2xx responses.
async function axiosFetch(url, config = {}) {
  const response = await axios.get(url, config);
  return response.data;
}

// 58. Request interceptor logging every outgoing request
axios.interceptors.request.use((config) => {
  console.log(`API call started: ${config.url}`);
  return config;
});

// 57. axios.get with params to fetch posts belonging to user 1
async function loadUserOnePosts() {
  const resultEl = document.getElementById("axios-result");
  resultEl.innerHTML = "<li>Loading...</li>";
  try {
    const posts = await axiosFetch(`${JSONPLACEHOLDER_BASE}/posts`, {
      params: { userId: 1 },
    });
    resultEl.innerHTML = posts
      .map((post) => `<li class="notification-card">${post.title}</li>`)
      .join("");
  } catch (error) {
    resultEl.innerHTML = `<li class="error-message">Failed to load posts.</li>`;
  }
}

/*
 * 59. Fetch vs Axios — three differences observed in this file:
 * 1. Fetch only rejects on network failure; a 404/500 still resolves
 *    with response.ok === false, so we must check it manually in
 *    apiFetch(). Axios rejects automatically on any non-2xx status.
 * 2. Fetch requires an explicit response.json() call to parse the
 *    body. Axios parses JSON automatically and exposes it on
 *    response.data.
 * 3. Axios supports request/response interceptors (used above to log
 *    every call) and config shortcuts like `params` and `timeout`
 *    out of the box; Fetch needs this to be hand-rolled.
 */

/* -----------------------------------------------------------
   Rendering helpers for course cards
   ----------------------------------------------------------- */

function renderCourses(list) {
  const grid = document.getElementById("course-grid");
  grid.innerHTML = "";
  list.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    grid.appendChild(article);
  });
}

/* -----------------------------------------------------------
   Wiring everything up on page load
   ----------------------------------------------------------- */

async function init() {
  const coursesStatus = document.getElementById("courses-status");

  // Task 1 usage: show loading state while the simulated fetch resolves
  const loadedCourses = await fetchAllCourses();
  coursesStatus.textContent = `${loadedCourses.length} courses loaded.`;
  renderCourses(loadedCourses);

  // Task 2 usage: load live notifications from JSONPlaceholder
  await loadNotifications(lastNotificationsUrl);

  // Wire up buttons
  document
    .getElementById("load-notifications-btn")
    .addEventListener("click", () =>
      loadNotifications(`${JSONPLACEHOLDER_BASE}/posts?_limit=5`)
    );

  document
    .getElementById("load-bad-url-btn")
    .addEventListener("click", () =>
      loadNotifications(`${JSONPLACEHOLDER_BASE}/nonexistent`)
    );

  document
    .getElementById("retry-btn")
    .addEventListener("click", () => loadNotifications(lastNotificationsUrl));

  document
    .getElementById("load-users-btn")
    .addEventListener("click", fetchTwoUsersTogether);

  document
    .getElementById("axios-posts-btn")
    .addEventListener("click", loadUserOnePosts);
}

init();
