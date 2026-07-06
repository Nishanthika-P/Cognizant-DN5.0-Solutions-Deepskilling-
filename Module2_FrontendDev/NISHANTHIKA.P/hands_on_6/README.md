# Hands-On 6: React Routing & State Management

This project extends Hands-On 5 with React Router, Context API, and Redux
Toolkit.

- **Task 1 — React Router**: `src/App.jsx` defines routes for `/`,
  `/courses`, `/courses/:courseId`, and `/profile`. `main.jsx` wraps the
  app in `<BrowserRouter>`. `Header.jsx` uses `<Link>` (with
  `aria-current="page"` on the active link) instead of plain `<a>` tags.
  `CourseDetailPage.jsx` reads the `:courseId` param with `useParams()`,
  and both `CoursesPage.jsx` and `CourseDetailPage.jsx` call
  `useNavigate()` to redirect to `/profile` after enrolling.
- **Task 2 — Context API**: `src/context/EnrollmentContext.jsx` contains
  the Context-based reference solution for this task (a provider holding
  `enrolledCourses` plus `enroll`/`remove` functions). It is not wired
  into the live app because Task 3 replaces it with Redux — see the
  comment at the top of that file for how to try it standalone.
- **Task 3 — Redux Toolkit**: `src/store/enrollmentSlice.js` defines the
  `enroll` and `unenroll` reducers plus `selectEnrolledCourses` /
  `selectEnrolledCount` selectors. `src/store/store.js` wires it into a
  single store via `configureStore`. `main.jsx` wraps the app in
  `<Provider store={store}>`. Components read/write state with
  `useSelector` and `useDispatch` — never by reaching into store shape
  directly. Install the Redux DevTools browser extension to watch the
  `enroll` / `unenroll` actions and state diffs live.


