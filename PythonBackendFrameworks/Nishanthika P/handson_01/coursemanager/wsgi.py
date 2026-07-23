"""
WSGI config for coursemanager project.
One-line role: WSGI entry point used by synchronous production
servers (e.g. Gunicorn) to run the Django app.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')

application = get_wsgi_application()
