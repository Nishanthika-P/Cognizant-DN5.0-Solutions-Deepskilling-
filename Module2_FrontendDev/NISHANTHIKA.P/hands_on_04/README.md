# Hands-On 4: Async JavaScript, Fetch API & API Integration

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

