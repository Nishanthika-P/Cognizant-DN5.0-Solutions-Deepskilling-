# Hands-On 8: Vue.js — Composition API, Vue Router & Pinia



- **Task 1 — Components & reactive data**: `Header.vue` and `CourseCard.vue`
  are single-file components using `<script setup>`. `CourseCard.vue`
  declares props with `defineProps` and emits an `enroll` event.
  `CoursesView.vue` holds a reactive `courses` ref populated `onMounted`,
  renders cards with `v-for`/`:key`, and filters them through a `computed`
  property (`filteredCourses`) bound to a `searchTerm` ref via `v-model`.
  
- **Task 2 — Vue Router**: `src/router/index.js` defines `/`, `/courses`,
  `/courses/:id`, and `/profile`, plus a `router.beforeEach` navigation
  guard that logs each navigation. `App.vue` renders `<RouterView />` with
  `<RouterLink>` nav items in the header. `CourseDetailView.vue` reads the
  `:id` param with `useRoute()` and redirects to `/profile` after
  enrolling with `useRouter().push(...)`.
  
- **Task 3 — Pinia**: `src/stores/enrollment.js` is a setup-style store
  (`defineStore('enrollment', () => {...})`) with `enrolledCourses`,
  a `totalCredits` computed, `enroll`/`unenroll` actions, an advanced
  `fetchAndEnroll(courseId)` action that fetches and enrolls in one call,
  and a `$reset()` helper. `ProfileView.vue` reads state through
  `storeToRefs(store)` to keep reactivity intact after destructuring.
