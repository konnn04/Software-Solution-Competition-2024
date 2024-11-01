from app import db, app
from app.models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    db.create_all()
    
    # Create a test user
    user = User(
        username='test1234',
        password=generate_password_hash('test1234'),
        email = 'example@gmail.com',
        name = 'Test User',
        role = 'renter',
        phone = '0123456789',
        address = '123 Example Street',
        dob = datetime(1999, 1, 1)
    )
    db.session.add(user)
    db.session.commit()
