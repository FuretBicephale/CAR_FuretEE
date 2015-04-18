import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Secure forms
WTF_CSRF_ENABLED = True
SECRET_KEY = '42-23'
