import { Link } from "react-router-dom";

function HomePage() {
  return (
    <section className="hero">
      <h1>Welcome to the Student Portal</h1>
      <p>Browse your courses, manage your profile, and track enrollment.</p>
      <Link to="/courses">
        <button>Explore Courses</button>
      </Link>
    </section>
  );
}

export default HomePage;
