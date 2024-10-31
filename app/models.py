from app import db
import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean, default=True)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())    
    
    def __repr__(self):
        return '<User %r>' % self.email
    
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    city = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(120), nullable=False)
    ward = db.Column(db.String(120), nullable=False)
    street = db.Column(db.String(120), nullable=True)

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    flood = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    full_address = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())    
    
class HouseImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    
    house = db.relationship('House', backref=db.backref('images', lazy=True))
    
    def __repr__(self):
        return '<House %r>' % self.name

# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String(200), nullable=False)
    

    def __repr__(self):
        return '<House %r>' % self.name

