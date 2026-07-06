import { configureStore } from "@reduxjs/toolkit";
import enrollmentReducer from "./enrollmentSlice.js";

export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
});
