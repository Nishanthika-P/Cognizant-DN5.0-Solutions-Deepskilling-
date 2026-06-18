-- ============================================================
-- HANDS-ON 1: Schema Design & Core SQL — DDL and Normalisation
-- Database: MySQL | college_db
-- ============================================================

-- Task 1: Create the Database and Tables
-- -------------------------------------------------------

CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- Create departments first (referenced by other tables)
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name     VARCHAR(100) NOT NULL,
    hod_name      VARCHAR(100),
    budget        DECIMAL(12,2)
);

CREATE TABLE students (
    student_id      INT PRIMARY KEY AUTO_INCREMENT,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,
    CONSTRAINT fk_student_dept FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id     INT PRIMARY KEY AUTO_INCREMENT,
    course_name   VARCHAR(150) NOT NULL,
    course_code   VARCHAR(20)  UNIQUE,
    credits       INT,
    department_id INT,
    CONSTRAINT fk_course_dept FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(2),
    CONSTRAINT fk_enroll_student FOREIGN KEY (student_id)
        REFERENCES students(student_id),
    CONSTRAINT fk_enroll_course FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id  INT PRIMARY KEY AUTO_INCREMENT,
    prof_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE,
    department_id INT,
    salary        DECIMAL(10,2),
    CONSTRAINT fk_prof_dept FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- -------------------------------------------------------
-- Task 2: Verify Normalisation (Analysis Comments)
-- -------------------------------------------------------

-- 1NF Analysis:
-- All columns hold atomic (single, indivisible) values.
-- No column stores multiple values (e.g., tags or phone lists).
-- Every table has a single-column primary key. Schema is in 1NF.

-- 2NF Analysis:
-- enrollments has a composite candidate key: (student_id, course_id).
-- Non-key columns: enrollment_date and grade.
-- enrollment_date depends on BOTH student_id AND course_id (when a
--   specific student enrolled in a specific course) — fully dependent.
-- grade also depends on both (a student's grade in a specific course).
-- No partial dependency exists. Schema is in 2NF.

-- 3NF Analysis:
-- A transitive dependency would exist if we stored dept_name inside
--   the students table: student_id → department_id → dept_name.
-- dept_name would depend on department_id, not directly on student_id.
-- We correctly store only department_id (FK) in students, and keep
--   dept_name in the departments table. No transitive dependencies.
-- Schema is in 3NF.

-- -------------------------------------------------------
-- Task 3: Alter and Extend the Schema
-- -------------------------------------------------------

-- Add phone_number to students
ALTER TABLE students
    ADD COLUMN phone_number VARCHAR(15);

-- Add max_seats to courses
ALTER TABLE courses
    ADD COLUMN max_seats INT DEFAULT 60;

-- Add CHECK constraint on grade
-- (MySQL 8+ enforces CHECK constraints)
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade
        CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Rename hod_name to head_of_dept
ALTER TABLE departments
    CHANGE hod_name head_of_dept VARCHAR(100);

-- Drop phone_number (schema rollback)
ALTER TABLE students
    DROP COLUMN phone_number;



