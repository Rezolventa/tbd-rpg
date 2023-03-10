"""Переименуйте этот файл в local.py и пропишите доступ к базе."""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tbd-rpg',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = '123'
