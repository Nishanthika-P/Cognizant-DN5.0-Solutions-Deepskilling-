"""
Digital Nurture 5.0 | Module 3 | Hands-On 4 — Task 3
=====================================================
N+1 Query Problem: Identification and Fix

The N+1 problem:
  - 1 query fetches N rows from a primary table
  - Then N additional queries are issued (one per row) to fetch related data
  - Total = N+1 queries instead of 1

This script demonstrates both the BROKEN and FIXED approaches,
measures round-trips, and times the difference.

Requirements: pip install psycopg2-binary
"""

import time
import psycopg2

# ------------------------------------------------------------------
# DATABASE CONNECTION — update credentials as needed
# ------------------------------------------------------------------
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "college_db",
    "user":     "postgres",
    "password": "your_password",   # <-- change this
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ==================================================================
# VERSION 1 — THE N+1 PROBLEM (BAD APPROACH)
# ==================================================================
def fetch_enrollments_n_plus_1():
    """
    56: Simulate the N+1 problem.
      Query 1  : SELECT all enrollments (1 query)
      Queries 2…N+1 : For EACH enrollment row, fire a separate SELECT
                      to get the student's name.

    With 12 enrollments in sample data → 1 + 12 = 13 queries total.
    With 10,000 enrollments → 10,001 queries total (see Step 59 comment).
    """
    conn = get_connection()
    cursor = conn.cursor()
    query_count = 0

    start = time.perf_counter()

    # ---- Query 1: fetch all enrollments ----
    cursor.execute("SELECT enrollment_id, student_id, course_id, grade FROM enrollments")
    query_count += 1
    enrollments = cursor.fetchall()

    results = []
    for enrollment_id, student_id, course_id, grade in enrollments:
        # ---- Query 2…N+1: one round-trip PER enrollment row ----
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s",
            (student_id,)
        )
        query_count += 1
        row = cursor.fetchone()
        student_name = f"{row[0]} {row[1]}" if row else "Unknown"
        results.append((enrollment_id, student_name, course_id, grade))

    elapsed = time.perf_counter() - start
    cursor.close()
    conn.close()

    return results, query_count, elapsed


# ==================================================================
# VERSION 2 — FIXED WITH A SINGLE JOIN QUERY (GOOD APPROACH)
# ==================================================================
def fetch_enrollments_with_join():
    """
    57: Fix with a single JOIN query.
    One SQL statement retrieves enrollments + student names in one round-trip.
    No matter how many rows exist, it is always exactly 1 query.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query_count = 0

    start = time.perf_counter()

    # ---- Single query: JOIN fetches everything at once ----
    cursor.execute("""
        SELECT
            e.enrollment_id,
            s.first_name || ' ' || s.last_name  AS student_name,
            e.course_id,
            e.grade
        FROM enrollments e
        JOIN students s ON s.student_id = e.student_id
        ORDER BY e.enrollment_id
    """)
    query_count += 1
    results = cursor.fetchall()

    elapsed = time.perf_counter() - start
    cursor.close()
    conn.close()

    return results, query_count, elapsed


# ==================================================================
# COMPARISON & OUTPUT
# ==================================================================
def main():
    print("=" * 60)
    print("  Hands-On 4 | Task 3 — N+1 Query Problem Demo")
    print("=" * 60)

    # --- Run N+1 version ---
    results_v1, queries_v1, time_v1 = fetch_enrollments_n_plus_1()
    print(f"\n[VERSION 1 — N+1 Approach]")
    print(f"  Total queries executed : {queries_v1}")
    print(f"  Time taken             : {time_v1 * 1000:.3f} ms")
    print(f"  Sample rows returned   : {len(results_v1)}")

    # --- Run JOIN version ---
    results_v2, queries_v2, time_v2 = fetch_enrollments_with_join()
    print(f"\n[VERSION 2 — Single JOIN Approach]")
    print(f"  Total queries executed : {queries_v2}")
    print(f"  Time taken             : {time_v2 * 1000:.3f} ms")
    print(f"  Sample rows returned   : {len(results_v2)}")

    # --- Step 58: Compare round-trips ---
    print(f"\n[COMPARISON — Step 58]")
    print(f"  Queries saved          : {queries_v1 - queries_v2}")
    if time_v2 > 0:
        speedup = time_v1 / time_v2
        print(f"  Speed improvement      : {speedup:.1f}x faster")

    # --- Verify both return identical data ---
    v1_set = set(results_v1)
    v2_set = set(results_v2)
    print(f"  Data identical         : {v1_set == v2_set}")

    # --- Step 59: Extrapolation to 10,000 enrollments ---
    print(f"\n[STEP 59 — Extrapolation to 10,000 enrollments]")
    print(f"  N+1 version would issue : 10,001 queries")
    print(f"  JOIN version would issue:     1 query")
    print(f"  Extra unnecessary queries: 10,000")
    print(f"  At 1 ms avg network latency → 10,001 ms ≈ 10 seconds extra per request!")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()


# ==================================================================
"""
59 — DOCUMENTATION COMMENT
=================================
In a real application with 10,000 enrollments:

  N+1 Version:
    - Query 1   : SELECT * FROM enrollments            → 1 query
    - Queries 2…10001 : SELECT student name per row    → 10,000 queries
    - TOTAL     : 10,001 queries

  JOIN Version:
    - Query 1   : SELECT e.*, s.name FROM enrollments JOIN students → 1 query
    - TOTAL     : 1 query

  Impact:
    - Each network round-trip to the database averages ~1-5 ms even on localhost.
    - 10,000 extra round-trips = 10–50 seconds of wasted latency per request.
    - In production (DB on separate server), this can be 100 ms+ per round-trip
      → 10,000 * 100ms = 1,000 seconds = completely unusable application.

  Root Cause:
    - This pattern is introduced most often by ORM LAZY LOADING.
    - When you access enrollment.student inside a loop, the ORM silently issues
      a new SELECT for each access unless configured otherwise.

  Fix Options:
    1. Raw SQL   : Write an explicit JOIN (as done in Version 2).
    2. SQLAlchemy: Use joinedload() or selectinload() on the query.
    3. Django ORM: Use select_related('student') on the queryset.
    All three reduce N+1 queries down to 1 (or at most 2-3 with subquery loading).
"""
# ==================================================================
