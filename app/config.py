import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Auth:
    CLIENT_ID = ('656250180334-q2b5a7spt3lcjqfdgslotqiha1qaaj6j.apps.googleusercontent.com')
    CLIENT_SECRET = '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'
    REDIRECT_URI = 'https://127.0.0.1:5000/login/callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
# class Config:
#     APP_NAME = "Test Google Login"
#     SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret" 
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