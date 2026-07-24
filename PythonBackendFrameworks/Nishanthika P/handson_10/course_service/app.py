"""
course_service/app.py
Hands-On 10, Task 1: Course Service - owns Department + Course data.
Runs on port 5001, its own SQLite database (course_service.db).
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'department_id': self.department_id,
        }


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    return jsonify([c.to_dict() for c in Course.query.all()])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    course = Course(
        name=data['name'], code=data['code'],
        credits=data['credits'], department_id=data.get('department_id'),
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """Called by Student Service (via the gateway) to verify a course exists."""
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course.to_dict())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
