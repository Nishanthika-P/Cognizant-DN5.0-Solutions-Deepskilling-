import { createSlice } from "@reduxjs/toolkit";

const enrollmentSlice = createSlice({
  name: "enrollment",
  initialState: {
    enrolledCourses: [],
  },
  reducers: {
    enroll(state, action) {
      const course = action.payload;
      const alreadyEnrolled = state.enrolledCourses.some(
        (c) => c.id === course.id
      );
      if (!alreadyEnrolled) {
        state.enrolledCourses.push(course);
      }
    },
    unenroll(state, action) {
      const courseId = action.payload;
      state.enrolledCourses = state.enrolledCourses.filter(
        (c) => c.id !== courseId
      );
    },
  },
});

export const { enroll, unenroll } = enrollmentSlice.actions;

export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses;
export const selectEnrolledCount = (state) => state.enrollment.enrolledCourses.length;

export default enrollmentSlice.reducer;
