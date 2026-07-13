import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectEnrolledCourses, unenroll } from "../store/enrollmentSlice.js";

function ProfilePage() {
  const enrolledCourses = useSelector(selectEnrolledCourses);
  const dispatch = useDispatch();

  const [profile, setProfile] = useState({ name: "", email: "", semester: "" });

  function handleChange(event) {
    const { name, value } = event.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  }

  const totalCredits = enrolledCourses.reduce(
    (sum, course) => sum + course.credits,
    0
  );

  return (
    <section className="profile-page">
      <h2>Student Profile</h2>
      <form>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" value={profile.name} onChange={handleChange} />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={profile.email}
          onChange={handleChange}
        />

        <label htmlFor="semester">Semester</label>
        <input
          id="semester"
          name="semester"
          type="number"
          min="1"
          max="8"
          value={profile.semester}
          onChange={handleChange}
        />
      </form>

      <h3>Enrolled Courses</h3>
      {enrolledCourses.length === 0 && <p>No courses enrolled yet.</p>}
      <ul className="enrolled-list">
        {enrolledCourses.map((course) => (
          <li key={course.id}>
            {course.name} ({course.code}) - {course.credits} credits
            <button onClick={() => dispatch(unenroll(course.id))}>Remove</button>
          </li>
        ))}
      </ul>
      {enrolledCourses.length > 0 && (
        <p className="total-credits">Total credits: {totalCredits}</p>
      )}
    </section>
  );
}

export default ProfilePage;
