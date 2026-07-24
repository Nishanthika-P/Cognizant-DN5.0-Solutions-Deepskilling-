"""
config.py
Hands-On 4, Task 1, step 38: app configuration.
"""
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///coursemanager.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
