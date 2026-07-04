function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p>{code}</p>
      <span>{credits} credits</span>
      {grade && <p className="grade">Grade: {grade}</p>}
      {onEnroll && (
        <button onClick={() => onEnroll({ id, name, code, credits, grade })}>
          Enroll
        </button>
      )}
    </article>
  );
}

export default CourseCard;
