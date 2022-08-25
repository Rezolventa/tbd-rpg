import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = (
    'orm',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tbd-rpg',
        'USER': 'postgres',
        'PASSWORD': '31337',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# CHANGE THE SECRET KEY IN YOUR CODE
SECRET_KEY = '4cCI6MTQQQTQ0NzgwNwwwwWF0IjoxNjM5NDQ3ODA2fQ'

ALLOWED_HOSTS = [
    '127.0.0.1:8000',
]