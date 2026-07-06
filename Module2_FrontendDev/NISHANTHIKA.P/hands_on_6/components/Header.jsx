import { Link, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectEnrolledCount } from "../store/enrollmentSlice.js";

function Header({ siteName }) {
  const enrolledCount = useSelector(selectEnrolledCount);
  const location = useLocation();

  const links = [
    { to: "/", label: "Home" },
    { to: "/courses", label: "Courses" },
    { to: "/profile", label: "Profile" },
  ];

  return (
    <header className="site-header">
      <div className="site-title">{siteName}</div>
      <nav aria-label="Main navigation">
        <ul>
          {links.map((link) => (
            <li key={link.to}>
              <Link
                to={link.to}
                aria-current={location.pathname === link.to ? "page" : undefined}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <span className="enrolled-badge">Enrolled: {enrolledCount}</span>
    </header>
  );
}

export default Header;
