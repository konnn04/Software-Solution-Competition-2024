import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Auth:
    CLIENT_ID = ('YOUR_ID.apps.googleusercontent.com')
    CLIENT_SECRET = 'YOUR_SECRET'
    REDIRECT_URI = 'https://127.0.0.1:5000/login/callback' # Change this to your server IP
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth' # This is google's auth URI
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token' # This is google's token URI
    USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo' # This is google's user info URI
    SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'] # This is the scope of the data you want to access
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


# fsq3P4FPRyom2dJPr+c19BXumxqxo/O6pSqBpSPIi7ZHwxk=