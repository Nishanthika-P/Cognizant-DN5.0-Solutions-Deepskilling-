"""
courses/routes.py
Hands-On 4:
  Task 1 - Blueprint with basic GET / and POST / (in-memory list).
  Task 2 - full CRUD, field validation, consistent JSON envelope.
"""
from flask import Blueprint, jsonify, request

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory store (Hands-On 5 replaces this with a real database)
_courses = []
_next_id = 1

REQUIRED_FIELDS = ['name', 'code', 'credits']


def make_response_json(data, status_code=200):
    """Task 2, step 44: consistent JSON envelope for every response."""
    return jsonify({'status': 'success', 'data': data}), status_code


def _find_course(course_id):
    return next((c for c in _courses if c['id'] == course_id), None)


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(_courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    global _next_id
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Request body must be JSON'}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({'error': f'Missing required fields: {missing}'}), 400

    course = {'id': _next_id, **data}
    _courses.append(course)
    _next_id += 1
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = _find_course(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = _find_course(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Request body must be JSON'}), 400

    course.update(data)
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global _courses
    course = _find_course(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404

    _courses = [c for c in _courses if c['id'] != course_id]
    return '', 204
