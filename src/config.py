from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SECRET_JWT = os.environ.get('SECRET')

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_PORT = int(os.environ.get('MAIL_PORT'))
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME')

