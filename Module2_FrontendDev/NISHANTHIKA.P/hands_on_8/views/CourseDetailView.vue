<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useEnrollmentStore } from "../stores/enrollment.js";

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const course = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const courseId = route.params.id;
  try {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/posts/${courseId}`
    );
    if (!response.ok) {
      throw new Error(`Course ${courseId} not found`);
    }
    const post = await response.json();
    course.value = {
      id: post.id,
      name: post.title.slice(0, 24),
      code: `CS${100 + Number(courseId)}`,
      credits: 3 + (Number(courseId) % 2),
    };
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

function handleEnroll() {
  if (!course.value) return;
  store.enroll(course.value);
  router.push("/profile");
}
</script>

<template>
  <section class="course-detail">
    <p v-if="loading" role="status">Loading course...</p>
    <p v-else-if="error" class="error-message">{{ error }}</p>
    <template v-else-if="course">
      <h2>{{ course.name }}</h2>
      <p>{{ course.code }}</p>
      <p>{{ course.credits }} credits</p>
      <button @click="handleEnroll">Enroll</button>
    </template>
  </section>
</template>

<style scoped>
.course-detail {
  background: #ffffff;
  border: 1px solid #dfe3ea;
  border-radius: 8px;
  padding: 1.5rem;
  max-width: 400px;
}

.course-detail button {
  margin-top: 1rem;
}
</style>
