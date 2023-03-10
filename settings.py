import os
from local import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = (
    'orm',
)

ALLOWED_HOSTS = [
    '127.0.0.1:8000',
]
