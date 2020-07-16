import os
import sys
import base64
import pyotp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#basedir = os.getcwd()
DB_CONFIG = {
    "PROJECT_ID": "project-name"
    "DB_NAME": "prac",
    "TABLE_NAME": "table_name"
}
CAR_INFO_TABLE = '{}.{}.{}'.format(DB_CONFIG['PROJECT_ID'], DB_CONFIG['DB_NAME'], DB_CONFIG['TABLE_NAME'])

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    SQLALCHEMY_RECORD_QUERIES = True
   #SECRET_KEY = os.getenv('SECRET_KEY', pyotp.random_base32())
   #TOTP = pyotp.TOTP(SECRET_KEY)
    JWT_ALGORITHM = 'RS256'
   #JWT_PRIVATE_KEY = open(os.path.join(basedir, 'rsa_private.pem')).read()
   #JWT_PUBLIC_KEY = open(os.path.join(basedir, 'rsa_public.pem')).read()
    JWT_PRIVATE_KEY = "" 
    JWT_PUBLIC_KEY = "" 
    JWT_ERROR_MESSAGE_KEY = 'message'

class DevelopmentConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass
 
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
} 
