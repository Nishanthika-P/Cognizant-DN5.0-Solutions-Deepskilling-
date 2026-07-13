import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useEnrollmentStore = defineStore("enrollment", () => {
  const enrolledCourses = ref([]);

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0)
  );

  function enroll(course) {
    const alreadyEnrolled = enrolledCourses.value.some(
      (c) => c.id === course.id
    );
    if (!alreadyEnrolled) {
      enrolledCourses.value.push(course);
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(
      (c) => c.id !== courseId
    );
  }

  // Task 3 advanced pattern: fetch a course by id and enroll in one action.
  async function fetchAndEnroll(courseId) {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/posts/${courseId}`
    );
    if (!response.ok) {
      throw new Error(`Could not fetch course ${courseId}`);
    }
    const post = await response.json();
    enroll({
      id: post.id,
      name: post.title.slice(0, 24),
      code: `CS${100 + Number(courseId)}`,
      credits: 3 + (Number(courseId) % 2),
    });
  }

  function $reset() {
    enrolledCourses.value = [];
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll,
    fetchAndEnroll,
    $reset,
  };
});
