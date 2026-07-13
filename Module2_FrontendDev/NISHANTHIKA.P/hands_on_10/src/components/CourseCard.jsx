function CourseCard({ id, name, code, credits, onEnroll }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p>{code}</p>
      <span>{credits} credits</span>
      {onEnroll && (
        <button onClick={() => onEnroll({ id, name, code, credits })}>
          Enroll
        </button>
      )}
    </article>
  );
}

export default CourseCard;
