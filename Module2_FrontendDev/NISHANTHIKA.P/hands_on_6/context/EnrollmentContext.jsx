// Task 2 solution: global state shared through Context API 

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
