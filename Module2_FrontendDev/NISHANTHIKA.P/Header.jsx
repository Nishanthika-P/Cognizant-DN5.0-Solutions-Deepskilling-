function Header({ siteName, enrolledCount }) {
  return (
    <header className="site-header">
      <div className="site-title">{siteName}</div>
      <nav aria-label="Main navigation">
        <ul>
          <li>Home</li>
          <li>Courses</li>
          <li>Profile</li>
        </ul>
      </nav>
      <span className="enrolled-badge">Enrolled: {enrolledCount}</span>
    </header>
  );
}

export default Header;
