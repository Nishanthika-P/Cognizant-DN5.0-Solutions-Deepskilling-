# Hands-On 4: Async JavaScript, Fetch API & API Integration

## How to run
Just open `index.html` directly in a browser (Chrome or Firefox). No build step
or npm install needed. Axios is loaded from a CDN in `index.html`.

## What's inside
- `index.html` — page structure: Courses section, Notifications section,
  a Promise.all demo section, and an Axios demo section.
- `styles.css` — styling for cards, buttons, loading and error states.
- `data.js` — local course data used by `fetchAllCourses()`.
- `app.js` — all three tasks:
  - **Task 1**: `fetchUserWithThen`, `fetchUser` (async/await), `fetchAllCourses`
    (simulated 1s delay), and a `Promise.all` demo that fetches two users at once.
  - **Task 2**: `apiFetch()` — a reusable fetch wrapper that checks `response.ok`
    and throws a descriptive error. Used to load notifications from
    JSONPlaceholder `/posts`, with a loading indicator, a friendly error
    message, and a Retry button (triggered by a bad URL button).
  - **Task 3**: the same request rewritten with Axios, including a request
    interceptor that logs every outgoing call, a `params` example, and a
    code comment listing three fetch vs. axios differences.

## Notes
- All network calls hit the public JSONPlaceholder API — no auth needed.
- Open the browser console to see the logged output from Task 1 and the
  Axios interceptor from Task 3.
