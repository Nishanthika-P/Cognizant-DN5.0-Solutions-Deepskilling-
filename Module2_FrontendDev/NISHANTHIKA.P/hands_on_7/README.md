# Hands-On 7: Angular — Components, Services, DI, Routing & Forms

Built with standalone Angular components (Angular 17 style), which is what
`ng new --routing` scaffolds by default today. `provideHttpClient()` and
`provideRouter()` are wired up in `src/main.ts` instead of an `AppModule`.

- **Task 1 — Components & data binding**: `HeaderComponent`,
  `CourseListComponent`, `CourseCardComponent`, and
  `StudentProfileComponent`. `CourseCardComponent` declares `@Input()`
  properties (`name`, `code`, `credits`, `grade`) rendered with `{{ }}`
  interpolation. `CourseListComponent` renders cards with `*ngFor`, binds
  a search box with `[(ngModel)]` (via `FormsModule`), and shows a
  "No courses found" message with `*ngIf` when the filtered list is empty.
  
- **Task 2 — Services & DI**: `src/app/services/course.service.ts` injects
- 
  `HttpClient` and exposes `getCourses()` as an `Observable`.
  `CourseListComponent` injects the service through its constructor,
  subscribes in `ngOnInit()`, and shows a loading message via `*ngIf`
  while `loading` is true.
  
- **Task 3 — Routing & Reactive Forms**: `src/app/app.routes.ts` defines
- 
  `''` → `CourseListComponent` and `'profile'` → `StudentProfileComponent`.
  `<router-outlet>` sits in `app.component.html`; the header uses
  `routerLink` / `routerLinkActive`. `StudentProfileComponent` builds a
  `FormGroup` with `FormBuilder` (name required, email required + email
  validator, semester required with min/max), shows inline error messages,
  and disables Submit until the form is valid.
