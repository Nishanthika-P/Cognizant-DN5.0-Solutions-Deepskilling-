-- ============================================================
-- HANDS-ON 3: Advanced SQL — Subqueries, Views & Transactions
-- Database: MySQL | college_db
-- ============================================================

USE college_db;

-- -------------------------------------------------------
-- Task 1: Subqueries
-- -------------------------------------------------------

-- Students enrolled in more courses than the average
-- Non-correlated subquery calculates the average first
SELECT s.student_id, CONCAT(s.first_name,' ',s.last_name) AS full_name,
       COUNT(e.course_id) AS enrolled_courses
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    SELECT AVG(course_count)
    FROM (
        SELECT student_id, COUNT(course_id) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
);

-- Courses where ALL enrolled students got an 'A'
-- Using NOT EXISTS to exclude courses with any non-A grade
SELECT c.course_name, c.course_code
FROM courses c
WHERE EXISTS (
    SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
    AND (e.grade != 'A' OR e.grade IS NULL)
);

-- Professor with highest salary in each department (correlated subquery)
SELECT p.prof_name, p.salary, d.dept_name
FROM professors p
JOIN departments d ON p.department_id = d.department_id
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Departments where average professor salary exceeds 85,000 (derived table)
SELECT dept_name, avg_salary
FROM (
    SELECT d.dept_name, AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_avg
WHERE avg_salary > 85000;

-- -------------------------------------------------------
-- Task 2: Creating and Using Views
-- -------------------------------------------------------

-- View — student enrollment summary with GPA
CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
JOIN departments d  ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- View — course stats
CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

--  Query view for students with GPA above 3.0
SELECT * FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

--  Attempt to UPDATE through multi-table view
-- UPDATE vw_student_enrollment_summary SET dept_name = 'IT' WHERE student_id = 1;
-- RESULT: ERROR — MySQL does not allow UPDATE on views built from multiple tables
--         or that use GROUP BY / aggregate functions.
-- WHY: A view is updatable only if it maps directly to a single base table,
--      has no GROUP BY, DISTINCT, aggregate functions, or JOINs.
--      vw_student_enrollment_summary uses JOIN + GROUP BY → not updatable.

-- Drop and recreate with WITH CHECK OPTION (single-table view)
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Simple single-table view with CHECK OPTION
CREATE VIEW vw_cs_students AS
SELECT * FROM students
WHERE department_id = 1
WITH CHECK OPTION;
-- WITH CHECK OPTION: any INSERT/UPDATE through this view must satisfy
-- WHERE department_id = 1 — prevents adding non-CS students via the view.

-- Recreate the summary views
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
JOIN departments d  ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * FROM vw_course_stats;  -- should return 5 rows

-- -------------------------------------------------------
-- Task 3: Stored Procedures and Transactions
-- -------------------------------------------------------

-- Stored procedure to enroll a student (with duplicate check)
DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id     INT,
    IN p_course_id      INT,
    IN p_enroll_date    DATE
)
BEGIN
    -- Check for duplicate enrollment
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enroll_date);
        SELECT 'Enrollment successful.' AS message;
    END IF;
END$$

DELIMITER ;

-- Test: CALL sp_enroll_student(1, 3, '2022-07-01');  new enrollment
-- Test: CALL sp_enroll_student(1, 1, '2022-07-01');  duplicate → error

-- Create log table and transfer procedure with transaction
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id        INT PRIMARY KEY AUTO_INCREMENT,
    student_id    INT,
    old_dept_id   INT,
    new_dept_id   INT,
    transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id   INT,
    IN p_new_dept_id  INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Transfer failed — transaction rolled back.';
    END;

    START TRANSACTION;

    -- Get old department
    SELECT department_id INTO v_old_dept_id
    FROM students WHERE student_id = p_student_id;

    -- Update student department
    UPDATE students
    SET department_id = p_new_dept_id
    WHERE student_id = p_student_id;

    -- Log the transfer
    INSERT INTO department_transfer_log (student_id, old_dept_id, new_dept_id)
    VALUES (p_student_id, v_old_dept_id, p_new_dept_id);

    COMMIT;
    SELECT 'Transfer successful.' AS message;
END$$

DELIMITER ;

-- Test valid transfer:   CALL sp_transfer_student(1, 2);
-- Test invalid dept FK:  CALL sp_transfer_student(1, 999); -- triggers rollback

-- SAVEPOINT demonstration
START TRANSACTION;

-- First enrollment insert
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (2, 4, '2022-07-01', 'B');

SAVEPOINT after_first_insert;

-- Second insert (intentionally failing — duplicate enrollment if already exists)
-- To simulate failure: insert a duplicate key
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (2, 4, '2022-07-01', 'A');  -- This will fail due to any UNIQUE constraint

-- If above fails, roll back only to the savepoint
ROLLBACK TO SAVEPOINT after_first_insert;

COMMIT;  -- saves only the first insert

-- Verify: first insert is saved, second is not
SELECT * FROM enrollments WHERE student_id = 2 AND course_id = 4;
