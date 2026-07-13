import { configureStore } from "@reduxjs/toolkit";
import coursesReducer from "./coursesSlice.js";
import enrollmentReducer from "./enrollmentSlice.js";

export const store = configureStore({
  reducer: {
    courses: coursesReducer,
    enrollment: enrollmentReducer,
  },
});
