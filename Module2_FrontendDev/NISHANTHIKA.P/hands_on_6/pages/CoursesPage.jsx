import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import CourseCard from "../components/CourseCard.jsx";
import { enroll } from "../store/enrollmentSlice.js";
import { initialCourses } from "../data/courses.js";

function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;

    async function loadCourses() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          "https://jsonplaceholder.typicode.com/posts?_limit=5"
        );
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }
        const posts = await response.json();
        const mapped = posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS${100 + index}`,
          credits: 3 + (index % 2),
        }));
        if (isMounted) setCourses(mapped);
      } catch (err) {
        // Fall back to local data so the page still works offline.
        if (isMounted) {
          setCourses(initialCourses);
          setError(err.message);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadCourses();
    return () => {
      isMounted = false;
    };
  }, []);

  function handleEnroll(course) {
    dispatch(enroll(course));
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
        <p className="error-message">
          Live data unavailable, showing offline course list.
        </p>
      )}

      {!loading && (
        <div className="course-grid">
          {filteredCourses.length === 0 && <p>No courses found.</p>}
          {filteredCourses.map((course) => (
            <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
          ))}
        </div>
      )}
    </section>
  );
}

export default CoursesPage;
