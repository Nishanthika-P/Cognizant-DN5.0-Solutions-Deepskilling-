# Cognizant-DN5.0-Solutions-Deepskilling-

##  About This Module

This module covers end-to-end database integration for a **Student Course Registration System** — a realistic college scenario used across all 7 hands-on exercises. The work progresses from schema design to advanced ORM and migrations.

---

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

### Hands-On 1 — Schema Design & Core SQL (DDL + Normalisation)
**Difficulty:** Beginner | **File:** `hands_on_1.sql`

**What I did:**
- Created `college_db` database with 5 tables: `departments`, `students`, `courses`, `enrollments`, `professors`
- Applied all constraints: `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`
- Verified normalisation: documented 1NF, 2NF, 3NF analysis as SQL comments
- Extended schema using `ALTER TABLE`: added columns, renamed columns, dropped columns

**Key Concepts:** DDL, Referential Integrity, Normalisation, Schema Design

---

###  Hands-On 2 — SQL Queries, Joins & Aggregations
**Difficulty:** Beginner | **File:** `hands_on_2.sql`

**What I did:**
- Inserted all sample data using `INSERT` statements
- Performed `UPDATE` and `DELETE` operations with verification
- Wrote single-table queries using `WHERE`, `ORDER BY`, `LIKE`, `BETWEEN`
- Wrote multi-table `INNER JOIN` and `LEFT JOIN` queries across 3–4 tables
- Used aggregate functions: `COUNT`, `AVG`, `SUM`, `ROUND`
- Used `GROUP BY` and `HAVING` for summary reports

**Key Concepts:** DML, JOINs, Aggregations, Filtering

---

### Hands-On 3 — Advanced SQL: Subqueries, Views & Transactions
**Difficulty:** Intermediate | **File:** `hands_on_3.sql`

**What I did:**
- Wrote correlated and non-correlated subqueries
- Used derived tables in `FROM` clause
- Created views `vw_student_enrollment_summary` and `vw_course_stats` with GPA calculation
- Analysed why multi-table views are not updatable
- Created views with `WITH CHECK OPTION`
- Wrote stored procedure `sp_enroll_student` with duplicate check
- Wrote stored procedure `sp_transfer_student` with full transaction, `COMMIT`, `ROLLBACK`
- Demonstrated `SAVEPOINT` for partial rollback

**Key Concepts:** Subqueries, Views, Stored Procedures, Transactions, SAVEPOINT

---

###  Hands-On 4 — Query Optimisation: Indexes & N+1 Problem
**Difficulty:** Intermediate | **Files:** `hands_on_4.sql`, `hands_on_4_n_plus_one.py`

**What I did:**
- Ran `EXPLAIN FORMAT=JSON` to capture baseline query plan (Full Table Scan identified)
- Created B-Tree index on `students.enrollment_year`
- Created composite UNIQUE index on `enrollments(student_id, course_id)`
- Created index on `courses.course_code`
- Created partial index on `enrollments` for `grade IS NULL`
- Re-ran `EXPLAIN` and confirmed Index Scan replaced Full Table Scan
- Simulated N+1 problem in Python: 11 queries for 10 enrollments
- Fixed with single JOIN query: 1 query for same data
- Benchmarked time difference using Python's `time` module

**Key Concepts:** Indexes, EXPLAIN, Query Plans, N+1 Problem, Eager Loading

---

###  Hands-On 5 — MongoDB: Document Modelling, CRUD & Aggregation
**Difficulty:** Intermediate | **File:** `hands_on_5.mongodb.js`

**What I did:**
- Created `college_nosql` database with `feedback` collection
- Inserted 10+ feedback documents with varying ratings, tags, semesters
- Included a document without `attachments` field (schema-less flexibility)
- Performed all CRUD operations: find with filters, projection, updateMany, push to array, deleteMany
- Built aggregation pipeline: filter → group → sort → project with `$round`
- Built tag frequency leaderboard using `$unwind` and `$group`
- Created index on `course_code` and verified `IXSCAN` using `explain()`

**Key Concepts:** MongoDB, BSON, CRUD, Aggregation Pipeline, $unwind, Indexes

---

### Hands-On 6 — ORM Integration: SQLAlchemy
**Difficulty:** Advanced | **Files:** `models.py`, `crud.py`

**What I did:**
- Defined 5 SQLAlchemy ORM models: `Department`, `Student`, `Course`, `Enrollment`, `Professor`
- Set up bidirectional relationships using `relationship()` and `back_populates`
- Used `Base.metadata.create_all()` to auto-create tables in `college_db_orm`
- Performed full CRUD via SQLAlchemy session API
- Identified N+1 problem using `echo=True` (13 queries for 10 enrollments)
- Fixed with `joinedload()` — reduced to 1 query
- Documented query count comparison in comments

**Key Concepts:** SQLAlchemy ORM, Sessions, Relationships, joinedload, N+1 Fix

---

### Hands-On 7 — Migrations & Versioning: Alembic
**Difficulty:** Advanced | **File:** `hands_on_7_notes.py`

**What I did:**
- Initialised Alembic with `alembic init migrations`
- Configured `alembic.ini` and `env.py` to link SQLAlchemy models
- Generated baseline migration with `--autogenerate`
- Inspected `upgrade()` and `downgrade()` functions
- Applied migration with `alembic upgrade head`
- Added `is_active` column to `Student` model → generated and applied incremental migration
- Added new `CourseSchedule` table → generated and applied migration
- Practised rollback: `alembic downgrade -1` and `alembic downgrade base`
- Re-applied all migrations with `alembic upgrade head`

**Key Concepts:** Alembic, Migration Versioning, upgrade/downgrade, Schema Evolution

---


## File Structure
```
Module3_DatabaseIntegration/
└── NISHANTHIKA.P/
    ├── hands_on_1.sql
    ├── hands_on_2.sql
    ├── hands_on_3.sql
    ├── hands_on_4.sql
    ├── hands_on_4_n_plus_one.py
    ├── hands_on_5.mongodb.js
    ├── hands_on_6.py
    └── hands_on_7_notes.py
```
