<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useEnrollmentStore } from "../stores/enrollment.js";

const store = useEnrollmentStore();
// storeToRefs keeps reactivity when destructuring state/getters out of the
// store. Plain destructuring (const { enrolledCourses } = store) would
// break reactivity in Vue's Composition API.
const { enrolledCourses, totalCredits } = storeToRefs(store);

const profile = ref({
  name: "",
  email: "",
  semester: "",
});
</script>

<template>
  <section class="profile-view">
    <h2>Student profile</h2>

    <form>
      <label for="name">Name</label>
      <input id="name" v-model="profile.name" type="text" />

      <label for="email">Email</label>
      <input id="email" v-model="profile.email" type="email" />

      <label for="semester">Semester</label>
      <input id="semester" v-model="profile.semester" type="number" min="1" max="8" />
    </form>

    <h3>Enrolled courses</h3>
    <p v-if="enrolledCourses.length === 0">No courses enrolled yet.</p>
    <ul v-else class="enrolled-list">
      <li v-for="course in enrolledCourses" :key="course.id">
        <span>{{ course.name }} ({{ course.code }}) - {{ course.credits }} credits</span>
        <button @click="store.unenroll(course.id)">Remove</button>
      </li>
    </ul>
    <p v-if="enrolledCourses.length > 0" class="total-credits">
      Total credits: {{ totalCredits }}
    </p>
  </section>
</template>

<style scoped>
.profile-view form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 320px;
  margin-bottom: 1.5rem;
}

.profile-view label {
  font-size: 0.875rem;
  color: #4b5563;
}

.enrolled-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 480px;
}

.enrolled-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border: 1px solid #dfe3ea;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
}

.enrolled-list button {
  padding: 0.3rem 0.7rem;
  border: 1px solid #b3261e;
  background-color: #ffffff;
  color: #b3261e;
}

.enrolled-list button:hover {
  background-color: #b3261e;
  color: #ffffff;
}

.total-credits {
  margin-top: 0.75rem;
  font-weight: bold;
}
</style>
