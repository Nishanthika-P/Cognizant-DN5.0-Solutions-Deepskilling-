import { Routes, Route } from "react-router-dom";
import Header from "./components/Header.jsx";
import HomePage from "./pages/HomePage.jsx";
import CoursesPage from "./pages/CoursesPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";

function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </main>
      <footer className="site-footer">
        <p>&copy; 2026 Student Portal. Digital Nurture 5.0.</p>
      </footer>
    </>
  );
}

export default App;
