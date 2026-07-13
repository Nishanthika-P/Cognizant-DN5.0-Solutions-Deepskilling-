# Hands-On 10: API Integration & Advanced State Management

This exercise lets you pick one framework to implement. **React (Redux
Toolkit) is the implementation here.** The NgRx and Pinia sections below
are read-and-understand concept summaries, as the exercise allows.

## How to run
```
npm install
npm run dev
```

## What's inside

### Task 1 — Centralised API service layer
- `src/api/apiClient.js` — a single configured Axios instance with a
  `baseURL`, default headers, and a 5s timeout.
- `src/api/courseApi.js` — `getAllCourses()`, `getCourseById(id)`, and
  `enrollStudent(studentId, courseId)`, all built on that instance.
- A response interceptor unwraps `response.data` and standardises errors
  into `{ message, statusCode }`. A request interceptor attaches a mock
  `Authorization` header to every call. Components only ever see data or
  a plain error message — never raw HTTP status codes.

### Task 2 — Redux Toolkit async thunks
- `src/store/coursesSlice.js` defines `fetchAllCourses` with
  `createAsyncThunk`, and handles `pending` / `fulfilled` / `rejected` in
  `extraReducers` (setting `loading` and `error` accordingly).
- `CoursesPage.jsx` dispatches the thunk in a `useEffect` and reads
  results back only through `selectCourses` / `selectCoursesLoading` /
  `selectCoursesError` — never `state.courses.items` directly.
- To see the rejected path: temporarily change the `baseURL` in
  `apiClient.js` to something invalid, reload `/courses`, and the error
  box + Retry button will appear.

### Task 3 — Global error handling + framework comparison
- `src/components/ErrorBoundary.jsx` is a class component wrapping the
  whole app in `main.jsx`. It catches render-time errors anywhere below
  it and shows a fallback UI with a Reload button instead of a blank
  crashed page.

**NgRx concept (Angular)** — same data flow as Redux, with the names
swapped: a component dispatches an `Action` (e.g. `loadCourses`), an
`Effect` intercepts it, calls the service/API, and dispatches a
success/failure action; a pure `Reducer` updates the `Store`; a
`Selector` reads a slice of state back into the component. The
distinguishing piece is that Effects live outside reducers specifically
so reducers can stay pure (no API calls inside them).

**Pinia advanced patterns (Vue)** — see `handson_08/src/stores/enrollment.js`
for a live example: an async action (`fetchAndEnroll`) does the fetch and
the state update in one step, `$reset()` clears the store back to its
initial state, and `storeToRefs(store)` is used in components so
destructured state stays reactive (plain destructuring breaks Vue's
reactivity).

**Comparison — boilerplate, learning curve, tooling:**

| | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|---|---|---|---|
| Boilerplate | Low with RTK's `createSlice`/`createAsyncThunk` — much less than classic Redux | Highest — separate files for actions, reducers, effects, selectors per feature | Lowest — a store is just a function returning refs/computed/actions |
| Learning curve | Moderate — need to understand actions/reducers/thunks conceptually | Steepest — RxJS observables plus the full NgRx vocabulary | Gentlest — feels like plain reactive JavaScript |
| Built-in tooling | Redux DevTools (separate install), Immer built into RTK | Angular DevTools + Redux DevTools extension, strong typing via Angular CLI | Vue DevTools with a first-class Pinia tab out of the box |
| Best fit | Teams wanting predictable, inspectable state without hand-rolling Redux | Large enterprise Angular apps already committed to RxJS everywhere | Small-to-mid apps wanting global state with minimal ceremony |

## Notes
- No emojis are used anywhere in the UI text.
- Build-tested with `npm install && npm run build` — compiles cleanly.
