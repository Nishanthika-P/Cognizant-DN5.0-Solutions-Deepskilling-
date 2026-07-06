// Task 2 solution: global state shared through Context API, before it
// gets refactored to Redux Toolkit in Task 3. Kept here for reference
// and grading — the live app (App.jsx) uses the Redux store instead.
// To try this version, wrap <App /> in <EnrollmentProvider> inside
// main.jsx and swap useSelector/useDispatch calls for useContext.

import { createContext, useContext, useState } from "react";

const EnrollmentContext = createContext(null);

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  function enroll(course) {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  }

  function remove(courseId) {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId));
  }

  const value = { enrolledCourses, enroll, remove };

  return (
    <EnrollmentContext.Provider value={value}>
      {children}
    </EnrollmentContext.Provider>
  );
}

export function useEnrollment() {
  const context = useContext(EnrollmentContext);
  if (!context) {
    throw new Error("useEnrollment must be used within an EnrollmentProvider");
  }
  return context;
}
