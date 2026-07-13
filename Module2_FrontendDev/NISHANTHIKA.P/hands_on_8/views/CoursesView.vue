<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import CourseCard from "../components/CourseCard.vue";
import { useEnrollmentStore } from "../stores/enrollment.js";

const courses = ref([]);
const searchTerm = ref("");
const loading = ref(true);
const error = ref(null);

const router = useRouter();
const store = useEnrollmentStore();

onMounted(async () => {
  try {
    const response = await fetch(
      "https://jsonplaceholder.typicode.com/posts?_limit=5"
    );
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    const posts = await response.json();
    courses.value = posts.map((post, index) => ({
      id: post.id,
      name: post.title.slice(0, 24),
      code: `CS${100 + index}`,
      credits: 3 + (index % 2),
    }));
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const filteredCourses = computed(() =>
  courses.value.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
);

function handleEnroll(course) {
  store.enroll(course);
  router.push("/profile");
}
</script>

<template>
  <section class="courses-view">
    <h2>Courses</h2>
    <input
      v-model="searchTerm"
      type="text"
      placeholder="Search courses..."
      aria-label="Search courses"
    />

    <p v-if="loading" role="status">Loading courses...</p>
    <p v-if="error" class="error-message">Failed to load courses: {{ error }}</p>

    <div class="course-grid" v-if="!loading">
      <p v-if="filteredCourses.length === 0">No courses found.</p>
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        show-enroll
        @enroll="handleEnroll"
      />
    </div>
  </section>
</template>

<style scoped>
.courses-view input {
  display: block;
  width: 100%;
  max-width: 320px;
  margin: 0.75rem 0 1rem;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
</style>
