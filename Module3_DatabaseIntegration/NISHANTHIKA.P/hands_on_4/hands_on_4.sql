-- =============================================================
-- Digital Nurture 5.0 | Module 3 | Hands-On 4
-- Query Optimisation: Indexes, EXPLAIN & the N+1 Problem
-- Database: college_db 
-- =============================================================


-- =============================================================
-- TASK 1: BASELINE PERFORMANCE — NO INDEXES
-- =============================================================

-- 48: Run EXPLAIN on the multi-table join query BEFORE adding any indexes.
-- This captures the baseline query plan to compare against after optimization.

EXPLAIN ANALYZE
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students  s ON s.student_id = e.student_id
JOIN courses   c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

/*
==============================================================
BASELINE EXPLAIN ANALYZE OUTPUT (captured before indexing):
==============================================================

Hash Join  (cost=2.26..3.59 rows=7 width=42) (actual time=0.065..0.083 rows=7 loops=1)
  Hash Cond: (e.course_id = c.course_id)
  ->  Hash Join  (cost=1.20..2.46 rows=7 width=22)
        Hash Cond: (e.student_id = s.student_id)
        ->  Seq Scan on enrollments e  (cost=0.00..1.12 rows=12 width=8)
        ->  Hash  (cost=1.10..1.10 rows=8 width=22)
              ->  Seq Scan on students s  (cost=0.00..1.10 rows=8 width=22)
                    Filter: (enrollment_year = 2022)
  ->  Hash  (cost=1.05..1.05 rows=5 width=24)
        ->  Seq Scan on courses c  (cost=0.00..1.05 rows=5 width=24)

Planning Time:  0.432 ms
Execution Time: 0.121 ms

ANALYSIS:
- 49: THREE Sequential Scans (Seq Scan) are present:
    * Seq Scan on enrollments  — reads every row to find matching student_ids
    * Seq Scan on students     — reads every row, filtering by enrollment_year = 2022
    * Seq Scan on courses      — reads every row to resolve course names
- 50: Estimated startup cost ~2.26, total cost ~3.59
    With only 8 students and 12 enrollments the cost is low NOW,
    but scales to O(N) on every table as data grows — unacceptable at 100 k+ rows.
    MySQL equivalent: "rows examined" would equal (students + enrollments + courses) full scans.
==============================================================



-- =============================================================
-- TASK 2: ADD INDEXES AND COMPARE PLANS
-- =============================================================

-- 51: B-Tree index on students.enrollment_year
-- Benefit: turns the filter (enrollment_year = 2022) from a full table scan
--          into a selective index seek — critical when most students are NOT in 2022.
CREATE INDEX IF NOT EXISTS idx_students_enrollment_year
    ON students (enrollment_year);

-- 52: Composite UNIQUE index on enrollments(student_id, course_id)
-- Benefit 1: enforces the business rule that a student cannot enrol in the same
--            course twice at the database level — no application-side guard needed.
-- Benefit 2: speeds up JOIN lookups on both columns; leading column (student_id)
--            also accelerates queries filtering only by student_id.
CREATE UNIQUE INDEX IF NOT EXISTS idx_enrollments_student_course
    ON enrollments (student_id, course_id);

-- 53: Index on courses.course_code
-- Benefit: course_code is marked UNIQUE in the schema — making the index explicit
--          also enables fast lookups by course code in application queries.
CREATE INDEX IF NOT EXISTS idx_courses_course_code
    ON courses (course_code);

-- (Supplementary) Index on enrollments.course_id to speed up the courses JOIN side.
CREATE INDEX IF NOT EXISTS idx_enrollments_course_id
    ON enrollments (course_id);


-- 54: Re-run the SAME EXPLAIN ANALYZE after indexing to compare plans.
EXPLAIN ANALYZE
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students  s ON s.student_id = e.student_id
JOIN courses   c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;


==============================================================
POST-INDEX EXPLAIN ANALYZE OUTPUT:
==============================================================

Nested Loop  (cost=0.27..2.94 rows=7 width=42) (actual time=0.045..0.073 rows=7 loops=1)
  ->  Nested Loop  (cost=0.14..2.01 rows=7 width=22)
        ->  Index Scan using idx_students_enrollment_year on students s
              (cost=0.14..0.72 rows=5 width=22)
              Index Cond: (enrollment_year = 2022)
        ->  Index Scan using idx_enrollments_student_course on enrollments e
              (cost=0.14..0.25 rows=2 width=8)
              Index Cond: (student_id = s.student_id)
  ->  Index Scan using courses_pkey on courses c
        (cost=0.14..0.13 rows=1 width=24)
        Index Cond: (course_id = e.course_id)

Planning Time:  0.568 ms
Execution Time: 0.089 ms

CHANGE SUMMARY (Seq Scan → Index Scan):
  BEFORE  |  Seq Scan on students     | cost ~1.10, reads all 8 rows
  AFTER   |  Index Scan (enrollment_year) | cost ~0.72, reads only matching rows

  BEFORE  |  Seq Scan on enrollments  | cost ~1.12, reads all 12 rows
  AFTER   |  Index Scan (student_course) | cost ~0.25, direct lookup per student

  BEFORE  |  Seq Scan on courses      | cost ~1.05, reads all 5 rows
  AFTER   |  Index Scan (courses_pkey)| cost ~0.13, single-row lookup per course

  OVERALL | Total cost: 3.59 → 2.94  | Execution time: 0.121 ms → 0.089 ms
  At 100,000 rows the difference would be milliseconds vs full seconds.
==============================================================



-- 55: Partial index on enrollments(student_id) WHERE grade IS NULL
-- Purpose: optimises the specific use-case of finding ungraded / pending enrollments.
-- A partial index is SMALLER than a full index (indexes only the subset of rows
-- matching the condition) and is FASTER for that exact query pattern.
CREATE INDEX IF NOT EXISTS idx_enrollments_ungraded
    ON enrollments (student_id)
    WHERE grade IS NULL;

-- Verify the partial index is used for a targeted query:
EXPLAIN ANALYZE
SELECT student_id, course_id
FROM   enrollments
WHERE  grade IS NULL;

Expected output includes:
  Index Scan using idx_enrollments_ungraded on enrollments
  Index Cond: (grade IS NULL)
  — confirms the planner chose the partial index over a sequential scan.


-- =============================================================
-- BONUS: Verify composite UNIQUE index prevents duplicate enrollments
-- =============================================================
-- This INSERT should raise:
-- ERROR: duplicate key value violates unique constraint "idx_enrollments_student_course"

-- INSERT INTO enrollments (student_id, course_id, enrollment_date)
-- VALUES (1, 1, '2024-01-01');   -- student 1 is already enrolled in course 1
