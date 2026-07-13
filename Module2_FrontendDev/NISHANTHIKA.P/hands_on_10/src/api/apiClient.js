import axios from "axios";

// A single configured Axios instance that every API module goes through.
// Changing the baseURL here (dev vs prod) affects the whole app.
const apiClient = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 5000,
});

// Request interceptor: attaches a mock auth token to every request.
apiClient.interceptors.request.use((config) => {
  config.headers.Authorization = "Bearer mock-student-portal-token";
  return config;
});

// Response interceptor: (a) unwraps response.data so callers work with
// plain data instead of the Axios response wrapper, and (b) standardises
// errors into a simple { message, statusCode } shape so components never
// have to deal with raw HTTP status codes or Axios error internals.
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response ? error.response.status : null;
    const message = error.response
      ? `Request failed with status ${statusCode}`
      : error.message || "Network error";
    return Promise.reject({ message, statusCode });
  }
);

export default apiClient;
