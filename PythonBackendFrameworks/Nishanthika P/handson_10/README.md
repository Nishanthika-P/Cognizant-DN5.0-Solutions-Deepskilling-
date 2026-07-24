# Hands-On 10 — Microservices Architecture: Concepts & Decomposition

## Service Decomposition (Task 1, step 96-97)

| Service Name          | Responsibility                              | Endpoints it owns                          | Database it owns        |
|-----------------------|----------------------------------------------|---------------------------------------------|--------------------------|
| **Course Service**    | Department + Course CRUD                      | `/api/courses/*`                             | `course_service.db`      |
| **Student Service**   | Student CRUD, enrollment                       | `/api/students/*`, `/api/students/{id}/enroll` | `student_service.db`     |
| Auth Service (future) | Registration, login, token validation          | `/api/v1/auth/*`                             | (shares or owns `users`) |
| Notification Service (future) | Email confirmations                    | internal only (no public endpoints)          | none - stateless         |



## Test the full flow through the gateway
```bash
# Create a course directly on Course Service (or via the gateway)
curl -X POST http://127.0.0.1:5000/api/courses/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4}'

# Create a student
curl -X POST http://127.0.0.1:5000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Asha","last_name":"Menon","email":"asha@college.edu"}'

# Enroll student 1 in course 1 - Student Service calls Course Service to verify
curl -X POST http://127.0.0.1:5000/api/students/1/enroll \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1}'

# Stop Course Service (Ctrl+C in Terminal 1), then retry enroll -> 503
```

## Synchronous (HTTP) vs Asynchronous (message queue) trade-offs (Task 2, step 104)
**Synchronous HTTP** (used here - Student Service calls Course Service
directly and waits): simple to reason about and debug, but creates tight
coupling - if Course Service is slow or down, the enrollment request
fails or hangs. Good for calls where the caller genuinely needs an
immediate answer (e.g. "does this course exist right now?").

**Asynchronous messaging** (e.g. RabbitMQ, Kafka): Student Service would
publish an "EnrollmentRequested" event and continue immediately; Course
Service (or a dedicated worker) consumes it whenever it's available and
publishes an "EnrollmentConfirmed"/"EnrollmentRejected" event back. This
decouples the services - Course Service being briefly down no longer
blocks the caller - at the cost of eventual consistency (the requester
doesn't get an instant yes/no) and added operational complexity (broker
to run, message schemas to version, ordering/retry to handle). Reach for
a queue when the two steps don't need to be atomic from the user's point
of view, or when you need to fan out one event to many consumers
(e.g. billing + notifications + analytics all reacting to one enrollment).

## Files
- `course_service/app.py` — Flask app, port 5001, `Department`/`Course`
  models, its own `course_service.db`
- `student_service/app.py` — Flask app, port 5002, `Student`/`Enrollment`
  models, its own `student_service.db`; `/enroll` calls Course Service
  over HTTP and returns 503 on `ConnectionError`
- `gateway/app.py` — Flask app, port 5000, proxies `/api/courses/*` and
  `/api/students/*` to the right backend service using `requests.request()`

## Expected Outcome
All three Flask apps run independently on separate ports with separate
SQLite databases. `POST /api/students/1/enroll` through the gateway
successfully routes Student Service → Course Service. Stopping Course
Service causes the enrollment endpoint to return 503.
