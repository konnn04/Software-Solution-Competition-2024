import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Auth:
    CLIENT_ID = ('....apps.googleusercontent.com')
    CLIENT_SECRET = '...'
    # REDIRECT_URI = 'https://127.0.0.1:5000/login/callback'
    REDIRECT_URI = '...'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
class Config:
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess" 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")
# class ProdConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")
    
# config = {
# "dev": DevConfig,
# "prod": ProdConfig,
# "default": DevConfig
# }


