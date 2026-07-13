<script setup>
import { useEnrollmentStore } from "../stores/enrollment.js";

const store = useEnrollmentStore();
</script>

<template>
  <header class="site-header">
    <div class="site-title">Student Portal</div>
    <nav aria-label="Main navigation">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <span class="enrolled-badge">Enrolled: {{ store.enrolledCourses.length }}</span>
  </header>
</template>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background-color: #1f2b45;
  color: #ffffff;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.site-title {
  font-weight: bold;
  font-size: 1.25rem;
}

nav {
  display: flex;
  gap: 1.5rem;
}

nav a {
  color: #ffffff;
  text-decoration: none;
}

nav a:hover,
nav a.router-link-active {
  text-decoration: underline;
}

.enrolled-badge {
  background-color: #33456d;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.875rem;
}
</style>
