"""
student_service/app.py
Hands-On 10, Task 1: Student Service - owns Student + Enrollment data.
Runs on port 5002, its own SQLite database (student_service.db).

Task 2: the /enroll endpoint calls Course Service (via HTTP) to verify
the course exists before creating the enrollment - this is the
inter-service communication step.
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# In a real deployment this would come from config/service discovery,
# not be hard-coded - kept simple for the exercise.
COURSE_SERVICE_URL = 'http://127.0.0.1:5001'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)  # NOT a local FK - Course lives in another service

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id, 'course_id': self.course_id}


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll(student_id):
    """
    Task 2, step 100-101: verify the course exists by calling Course
    Service; return 503 if Course Service is unreachable.
    """
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    course_id = data.get('course_id')

    try:
        resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=3)
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Course Service is unavailable - cannot verify course before enrolling'
        }), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 400

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)
