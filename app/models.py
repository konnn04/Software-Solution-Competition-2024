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

    renter = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)

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
    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())    

    

    def __repr__(self):
        return '<Room %r>' % self.name

class RoomImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    
    def __repr__(self):
        return '<RoomImage %r>' % self.url

# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String(200), nullable=False)
    

    def __repr__(self):
        return '<House %r>' % self.name

