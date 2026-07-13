import apiClient from "./apiClient.js";

function mapPostToCourse(post, index) {
  return {
    id: post.id,
    name: post.title.slice(0, 24),
    code: `CS${100 + index}`,
    credits: 3 + (index % 2),
    grade: "-",
  };
}

export async function getAllCourses() {
  const posts = await apiClient.get("/posts?_limit=5");
  return posts.map(mapPostToCourse);
}

export async function getCourseById(id) {
  const post = await apiClient.get(`/posts/${id}`);
  return mapPostToCourse(post, Number(id));
}

// Simulated enrollment call — JSONPlaceholder accepts POSTs and echoes
// back a fake created resource, which is enough to demonstrate the shape
// of a real enrollment API call going through the centralised client.
export async function enrollStudent(studentId, courseId) {
  return apiClient.post("/posts", {
    studentId,
    courseId,
    title: `enrollment-${studentId}-${courseId}`,
  });
}
