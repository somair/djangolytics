import os
from djangolytics.settings import *

DATABASES["default"] = {'ENGINE': 'django.db.backends.sqlite3'}
os.environ["GA_CLIENT_ID"] = "asdf"
os.environ["GA_CLIENT_SECRET"] = "asdf"
