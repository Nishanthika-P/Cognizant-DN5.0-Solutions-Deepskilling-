"""
ASGI config for coursemanager project.
One-line role: ASGI entry point used by asynchronous servers
(e.g. Daphne, Uvicorn) to run the Django app with async support.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')

application = get_asgi_application()
