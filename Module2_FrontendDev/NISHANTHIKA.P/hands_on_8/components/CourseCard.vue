<script setup>
const props = defineProps({
  id: { type: [Number, String], required: true },
  name: { type: String, required: true },
  code: { type: String, required: true },
  credits: { type: Number, required: true },
  grade: { type: String, default: "" },
  showEnroll: { type: Boolean, default: false },
});

const emit = defineEmits(["enroll"]);

function onEnroll() {
  emit("enroll", { id: props.id, name: props.name, code: props.code, credits: props.credits });
}
</script>

<template>
  <article class="course-card">
    <h3>
      <RouterLink :to="`/courses/${id}`">{{ name }}</RouterLink>
    </h3>
    <p>{{ code }}</p>
    <span>{{ credits }} credits</span>
    <p v-if="grade" class="grade">Grade: {{ grade }}</p>
    <button v-if="showEnroll" @click="onEnroll">Enroll</button>
  </article>
</template>

<style scoped>
.course-card {
  background: #ffffff;
  border: 1px solid #dfe3ea;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.course-card h3 a {
  color: inherit;
  text-decoration: none;
}

.course-card h3 a:hover {
  text-decoration: underline;
}

.grade {
  margin-top: 0.4rem;
  color: #4b5563;
  font-size: 0.875rem;
}
</style>
