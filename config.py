from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
SECRET_KEY = environ.get('SECRET_KEY', 'change-this-in-production')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
'sqlite:///' + path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Uploads
UPLOAD_FOLDER = path.join(basedir, 'static', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB


# Email (bookings)
MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = environ.get('MAIL_USE_TLS', 'True') == 'True'
MAIL_USE_SSL = environ.get('MAIL_USE_SSL', 'False') == 'True'
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
BOOKING_EMAIL = environ.get('BOOKING_EMAIL', MAIL_USERNAME)
