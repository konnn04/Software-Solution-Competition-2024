from app import app, get_google_auth, login_manager
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, House, Room, RoomImage
from app import db
from app.config import Auth
import requests
from app.tool import *

def update_template_context():
    user = None
    if current_user.is_authenticated:
        user = dict(name=current_user.name, avatar=current_user.avatar)
    return dict(user=user)

app.context_processor(update_template_context)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    room = Room.query.all()
    for r in room:
        images = RoomImage.query.filter_by(room_id=r.id).all()
        r.images = images
    for r in room:
        r.house = House.query.get(r.house_id)
    university = None
    if current_user.is_authenticated:
        university = getSchoolName(current_user.email)


    return render_template('home.html', title='Trang chủ', rooms = room, university = university)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def gg_login():    
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI)
    session['oauth_state'] = state
    return redirect(auth_url)

@app.route('/login/callback')
def callback():
    if 'oauth_state' not in session:
        return redirect(url_for('login'))
    
    state = session['oauth_state']
    if state != request.args.get('state'):
        return redirect(url_for('login'))
    
    google = get_google_auth(state=state)

    try:
        token = google.fetch_token(
            Auth.TOKEN_URI, 
            client_secret=Auth.CLIENT_SECRET, 
            authorization_response=request.url
        )
    except Exception as e:
        print(e)
        return 'HTTPError occurred.'
    
    google = get_google_auth(token=token)
    resp = google.get(Auth.USER_INFO)
    if resp.status_code == 200:
        user_info = resp.json()
        # if (user_info.get('email').split('@')[1].endswith('.edu.vn') == False):
        #     return render_template('login.html', error='Chỉ sử dụng Email do trường cấp!')


        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                name=user_info['name'],
                email=user_info['email'],
                avatar=user_info['picture'],
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return 'Could not fetch your information.', 400
    
@app.route('/rent/addrenter', methods=['GET', 'POST'])
def addRenter():
    if request.method == 'POST':
        try:
            addRenterNew(request)
        except Exception as e:
            print(e)        
        return redirect(url_for('home'))
    
    return render_template('addRenter.html', title='Thêm người thuê')

@app.route('/rent/delete/<int:id>')
def deleteHouse(id):
    house = House.query.get(id)
    db.session.delete(house)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/house/<int:id>/rooms', methods=['GET', 'POST'])
def seeRooms(id):
    house = House.query.get(id)
    rooms = Room.query.filter_by(house_id=id).all()
    return render_template('rooms.html', title='Phòng trọ', house=house, rooms=rooms)

@app.route('/house/<int:id>/addroom', methods=['GET', 'POST'])
def addRoom(id):
    house = House.query.get(id)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        area = request.form['area']
        description = request.form['description']
        type = request.form['type']
        n = request.form['num']
        images = request.files.getlist('images')

        urls = []
        for image in images:
            url = upload_image_to_server(image)
            if 'url' in url:
                urls.append(url['url'])

        for i in range(int(n)):
            room = Room(
                name=f"[{i+1}] {name}",
                price=price,
                area=area,
                description=description,
                type=type,
                house_id=id
            )
            db.session.add(room)
            db.session.commit()
            for url in urls:
                room_image = RoomImage(
                    url=url,
                    room_id=room.id
                )
                db.session.add(room_image)
                db.session.commit()

        


        return redirect(url_for('seeRooms', id=id))
    
    return render_template('addRoom.html', title='Thêm phòng trọ', house=house)

@app.route('/room/delete/<int:id>')
def deleteRoom(id):
    room = Room.query.get(id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/lookup', methods=['GET', 'POST'])
@login_required
def lookup():
    if request.method == 'POST':
        return redirect(url_for('home'))
    university = getSchoolName(current_user.email)
    return render_template('lookup.html', title='Tra cứu', university=university)

@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    if request.method == 'POST':
        return redirect(url_for('home'))
    houses = House.query.filter_by(renter=current_user.id).all()
    for house in houses:
        n = Room.query.filter_by(house_id=house.id).count()
        house.n = n

    return render_template('rent.html', title='Thuê nhà', houses=houses)

@app.route('/detail/<int:id>')
def detail(id):
    house = House.query.get(id)
    images = RoomImage.query.join(Room).filter(Room.house_id == id).all()
    return render_template('detail.html', title='Chi tiết', house=house, images=images)

def addRenterNew(request):
    name = request.form['name']
    city = request.form['city']
    district = request.form['district']
    ward = request.form['ward']
    street = request.form['street']
    lat = request.form['lat']
    lon = request.form['lon']
    flood = request.form['flood']
    description = request.form['description']
    full_address = request.form['full-address']
    
    h = House.query.filter_by(name=name).first()
    
    if h:
        return redirect(url_for('login'))
    
    house = House(
        name=name,
        city=city,
        district=district,
        ward=ward,
        street=street,
        lat=lat,
        lon=lon,
        flood=flood,
        description=description,
        full_address= full_address,
        renter = current_user.id
    )
    db.session.add(house)
    db.session.commit()

    
        
    # db.session.add(house_image)
    # db.session.commit()
    



    


    


    