import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { enroll } from "../store/enrollmentSlice.js";

function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!courseId) return;

    let isMounted = true;
    async function loadCourse() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `https://jsonplaceholder.typicode.com/posts/${courseId}`
        );
        if (!response.ok) {
          throw new Error(`Course ${courseId} not found`);
        }
        const post = await response.json();
        if (isMounted) {
          setCourse({
            id: post.id,
            name: post.title.slice(0, 24),
            code: `CS${100 + Number(courseId)}`,
            credits: 3 + (Number(courseId) % 2),
          });
        }
      } catch (err) {
        if (isMounted) setError(err.message);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadCourse();
    return () => {
      isMounted = false;
    };
  }, [courseId]);

  function handleEnroll() {
    if (!course) return;
    dispatch(enroll(course));
    navigate("/profile");
  }

  if (!courseId) return <p>No course selected.</p>;
  if (loading) return <p role="status">Loading course...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <section className="course-detail">
      <h2>{course.name}</h2>
      <p>{course.code}</p>
      <p>{course.credits} credits</p>
      <button onClick={handleEnroll}>Enroll</button>
    </section>
  );
}

export default CourseDetailPage;
