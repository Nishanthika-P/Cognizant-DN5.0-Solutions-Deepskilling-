"""
courses/routes.py
Hands-On 5, Task 2: routes now backed by the real database via SQLAlchemy
instead of the in-memory list used in Hands-On 4.
"""
from flask import Blueprint, jsonify, request
from app import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

REQUIRED_FIELDS = ['name', 'code', 'credits']


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return make_response_json([c.to_dict() for c in courses])


@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Request body must be JSON'}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({'error': f'Missing required fields: {missing}'}), 400

    course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data.get('department_id'),
    )
    db.session.add(course)
    db.session.commit()
    return make_response_json(course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    for field in ('name', 'code', 'credits', 'department_id'):
        if field in data:
            setattr(course, field, data[field])
    db.session.commit()
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return '', 204


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def course_students(course_id):
    course = Course.query.get_or_404(course_id)
    enrollments = Enrollment.query.filter_by(course_id=course.id).all()
    students = [e.student.to_dict() for e in enrollments]
    return make_response_json(students)
