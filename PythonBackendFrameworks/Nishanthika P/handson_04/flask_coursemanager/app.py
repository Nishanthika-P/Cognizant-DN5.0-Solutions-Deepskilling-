"""
app.py
Hands-On 4, Task 1, step 37: application factory pattern.
Hands-On 4, Task 2, step 45: JSON error handlers (404/500).
"""
from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
