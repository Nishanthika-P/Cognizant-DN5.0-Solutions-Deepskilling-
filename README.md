# Cognizant-DN5.0-Solutions-Deepskilling-

# What This Exercise Covers
- Designing a relational database schema from scratch
- Writing DDL statements (CREATE, ALTER, DROP)
- Enforcing constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK)
- Normalisation analysis — 1NF, 2NF, 3NF
- Safe schema modifications using ALTER TABLE


## Tables Created

| Table | Description |
|---|---|
| `departments` | Stores department info and budget |
| `students` | Student details linked to a department |
| `courses` | Course details linked to a department |
| `enrollments` | Links students to courses with grade |
| `professors` | Professor details linked to a department |

---

## Tasks Completed

### Task 1 — Create Database and Tables
- Created `college_db` database
- Wrote `CREATE TABLE` statements for all 5 tables
- Added `NOT NULL`, `UNIQUE`, `PRIMARY KEY` constraints
- Defined all `FOREIGN KEY` relationships

### Task 2 — Normalisation Analysis
- **1NF:** All columns hold atomic values. No multi-valued fields.
- **2NF:** All non-key columns in `enrollments` are fully dependent on the composite key `(student_id, course_id)`.
- **3NF:** No transitive dependencies. `dept_name` is stored in `departments`, not in `students`.
- Analysis documented as SQL comments inside the file.

### Task 3 — Alter and Extend Schema
- Added `phone_number VARCHAR(15)` to `students`
- Added `max_seats INT DEFAULT 60` to `courses`
- Added `CHECK` constraint on `grade` column in `enrollments`
- Renamed `hod_name` to `head_of_dept` in `departments`
- Dropped `phone_number` (schema rollback simulation)

---

## File Structure
```
Module3_DatabaseIntegration/
└── Nishanthika P/
    └── hands_on_1.sql
```
