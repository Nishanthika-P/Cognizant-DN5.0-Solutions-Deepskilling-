import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getAllCourses } from "../api/courseApi.js";

// Async thunk: components dispatch this and never touch the API layer
// directly. The three lifecycle actions (pending/fulfilled/rejected) are
// generated automatically.
export const fetchAllCourses = createAsyncThunk(
  "courses/fetchAll",
  async () => {
    return await getAllCourses();
  }
);

const coursesSlice = createSlice({
  name: "courses",
  initialState: {
    items: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllCourses.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAllCourses.fulfilled, (state, action) => {
        state.items = action.payload;
        state.loading = false;
      })
      .addCase(fetchAllCourses.rejected, (state, action) => {
        state.error = action.error.message || "Failed to load courses";
        state.loading = false;
      });
  },
});

// Selectors: components read state through these, never through
// state.courses.items directly. If the state shape ever changes, only
// these functions need to be updated.
export const selectCourses = (state) => state.courses.items;
export const selectCoursesLoading = (state) => state.courses.loading;
export const selectCoursesError = (state) => state.courses.error;

export default coursesSlice.reducer;
