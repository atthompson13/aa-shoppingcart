"""Test settings for Shopping Cart"""
from allianceauth.project_template.project_name.settings.base import *

# Test database
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}

# Disable logging during tests
LOGGING_CONFIG = None

# Use fast password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Test-specific settings
SECRET_KEY = 'test-secret-key'
DEBUG = True

INSTALLED_APPS += [
    'shopping_cart',
]
