from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, current_user
from app.config import Auth
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session
from werkzeug.security import generate_password_hash

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'somethingsecret'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session( Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
    return oauth

from app import routes

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
class UserModelView(MyModelView):
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)

from app.models import User, House, Room, RoomImage, Review

admin = Admin(app, name='Quản trị', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(House, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(RoomImage, db.session))
admin.add_view(ModelView(Review, db.session))




