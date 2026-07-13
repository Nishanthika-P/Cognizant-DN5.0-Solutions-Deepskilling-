import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import CourseCard from "../components/CourseCard.jsx";
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from "../store/coursesSlice.js";
import { enroll } from "../store/enrollmentSlice.js";
import { enrollStudent } from "../api/courseApi.js";

function CoursesPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    // Components never call the API directly — they dispatch the thunk
    // and read the result back out through selectors.
    dispatch(fetchAllCourses());
  }, [dispatch]);

  async function handleEnroll(course) {
    dispatch(enroll(course));
    try {
      // Demonstrates the centralised courseApi module being used for a
      // write operation, going through the same interceptors as reads.
      await enrollStudent("student-1", course.id);
    } catch (err) {
      console.error("Enrollment call failed:", err.message);
    }
    navigate("/profile");
  }

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section className="courses-section">
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
      />

      {loading && <p role="status">Loading courses...</p>}
      {error && (
        <div className="error-box">
          <p className="error-message">Could not load courses: {error}</p>
          <button onClick={() => dispatch(fetchAllCourses())}>Retry</button>
        </div>
      )}

      {!loading && !error && (
        <div className="course-grid">
          {filteredCourses.map((course) => (
            <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
          ))}
        </div>
      )}
    </section>
  );
}

export default CoursesPage;
