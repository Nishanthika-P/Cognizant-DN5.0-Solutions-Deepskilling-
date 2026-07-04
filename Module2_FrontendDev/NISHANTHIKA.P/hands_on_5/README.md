# Hands-On 5: React Fundamentals — Components, Props, State & Hooks

## What's inside
- `src/components/Header.jsx` — receives `siteName` and `enrolledCount` as props.
- `src/components/Footer.jsx` — simple copyright line.
- `src/components/CourseCard.jsx` — receives course fields as props and an
  optional `onEnroll` handler.
- `src/components/StudentProfile.jsx` — a form with local `useState` bound
  to each input via `onChange`.
- `src/data/courses.js` — starter course data (used as a visual reference;
  the live list is fetched from an API, see below).
- `src/App.jsx`:
  - **Task 1**: renders `Header`, `Footer`, and `CourseCard`.
  - **Task 2**: `useState` for `courses`, `searchTerm`, and
    `enrolledCourses`. Enrollment state is lifted up to `App` and passed
    down as `onEnroll`; the enrolled count is passed to `Header`.
  - **Task 3**: a `useEffect` (empty dependency array) fetches 5 posts from
    JSONPlaceholder on mount and maps them into course-like objects, with
    `loading` and `error` state. A second `useEffect` logs "Courses updated"
    whenever `courses` changes — see the code comment explaining why the
    dependency array matters.
