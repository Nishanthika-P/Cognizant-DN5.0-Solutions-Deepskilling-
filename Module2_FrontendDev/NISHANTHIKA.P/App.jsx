import { useEffect, useState } from "react";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import CourseCard from "./components/CourseCard.jsx";
import StudentProfile from "./components/StudentProfile.jsx";

function App() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Task 3: fetch course-like data from JSONPlaceholder on mount
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
          grade: "-",
        }));
        if (isMounted) setCourses(mapped);
      } catch (err) {
        if (isMounted) setError(err.message);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadCourses();
    return () => {
      isMounted = false;
    };
  }, []); // empty dependency array: runs once after mount, like componentDidMount

  // Logs whenever the courses list changes. A missing dependency array
  // here would re-run the effect after every render, and since this
  // effect does not itself update `courses`, it stays safe — but if it
  // did, an incorrect dependency array could trigger an infinite loop.
  useEffect(() => {
    console.log("Courses updated");
  }, [courses]);

  function handleEnroll(course) {
    setEnrolledCourses((prev) => {
      if (prev.some((c) => c.id === course.id)) return prev;
      return [...prev, course];
    });
  }

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main>
        <section className="courses-section">
          <h2>Courses</h2>
          <input
            type="text"
            placeholder="Search courses..."
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />

          {loading && <p role="status">Loading courses...</p>}
          {error && <p className="error-message">Failed to load courses: {error}</p>}

          {!loading && !error && (
            <div className="course-grid">
              {filteredCourses.map((course) => (
                <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
              ))}
            </div>
          )}
        </section>

        <StudentProfile />
      </main>

      <Footer />
    </>
  );
}

export default App;
