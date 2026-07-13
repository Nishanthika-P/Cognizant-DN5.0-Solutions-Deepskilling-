<template>
  <section class="hero">
    <h1>Welcome to the Student Portal</h1>
    <p>Browse your courses, manage your profile, and track enrollment.</p>
    <RouterLink to="/courses">
      <button>Explore Courses</button>
    </RouterLink>
  </section>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 3rem 1rem;
}

.hero button {
  margin-top: 1rem;
}
</style>
