import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectEnrolledCount } from "../store/enrollmentSlice.js";

function Header() {
  const enrolledCount = useSelector(selectEnrolledCount);

  return (
    <header className="site-header">
      <div className="site-title">Student Portal</div>
      <nav aria-label="Main navigation">
        <Link to="/">Home</Link>
        <Link to="/courses">Courses</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <span className="enrolled-badge">Enrolled: {enrolledCount}</span>
    </header>
  );
}

export default Header;
