import { useState } from "react";

function StudentProfile() {
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    semester: "",
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <section className="profile-form">
      <h2>Student Profile</h2>
      <form>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          value={profile.name}
          onChange={handleChange}
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={profile.email}
          onChange={handleChange}
        />

        <label htmlFor="semester">Semester</label>
        <input
          id="semester"
          name="semester"
          type="number"
          min="1"
          max="8"
          value={profile.semester}
          onChange={handleChange}
        />
      </form>

      <p className="profile-preview">
        Preview: {profile.name || "—"} ({profile.email || "—"}), Semester{" "}
        {profile.semester || "—"}
      </p>
    </section>
  );
}

export default StudentProfile;
