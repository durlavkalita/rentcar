import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  API_URL = "/static/swagger.yaml"
  SWAGGER_URL = "/api/docs"
  REDIS_HOST = 'redis'
  REDIS_PORT = 6379
