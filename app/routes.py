from app import app, get_google_auth, login_manager
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, House, Room, RoomImage
from app import db
from app.config import Auth
import requests
from app.tool import *
import math
from datetime import datetime
from werkzeug.security import generate_password_hash


def update_template_context():
    user = None
    if current_user.is_authenticated:
        user = current_user
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

@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        f_email = User.query.filter_by(email=email).first()
        f_username = User.query.filter_by(username=username).first()
        f_same = password == password2
        f_safe = password.isalnum() and len(password) >= 8
        f_enough_age = (datetime.now().date() - datetime.strptime(dob, '%Y-%m-%d').date()).days >= 18*365

        if f_email:
            return render_template('register.html', error='Email đã tồn tại!')
        if f_username:
            return render_template('register.html', error='Username đã tồn tại!')
        if not f_same:
            return render_template('register.html', error='Mật khẩu không trùng khớp!')
        if not f_safe:
            return render_template('register.html', error='Mật khẩu không an toàn!')   
        if not f_enough_age:
            return render_template('register.html', error='Chưa đủ 18 tuổi!')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        user = User(
            name=name,
            phone=phone,
            username=username,
            address=address,
            dob= dob_date,
            email=email,
            password=generate_password_hash(password),
            role='renter'
        )
        db.session.add(user)
        db.session.commit()
        return render_template('login.html', success='Đăng ký thành công! Đăng nhập ngay!')
    return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error='Sai tên đăng nhập hoặc mật khẩu!')
        
    return render_template('login.html')

@app.route('/login/google')
def gg_login():   
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI)
    session['oauth_state'] = state
    return redirect(auth_url)

@app.route('/login/callback')
def callback():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login', error='Lỗi xác thực! Vui lòng thử lại.'))
    
    google = get_google_auth(token=token)
    resp = google.get(Auth.USER_INFO)
    if resp.status_code == 200:
        user_info = resp.json()
        if (user_info.get('email').split('@')[1].endswith('.edu.vn') == False):
            return render_template('login.html', error='Chỉ sử dụng Email do trường cấp!')
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                name=user_info['name'],
                email=user_info['email'],
                avatar=user_info['picture'],
                username=user_info['email'].split('@')[0],
                password=generate_password_hash(token['access_token']),
                role = 'student'
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return redirect(url_for('login', error='Lỗi xác thực! Vui lòng thử lại.'))


@app.route('/lookup')
@login_required
def lookup():
    university = getSchoolName(current_user.email)
    page = request.args.get('page', 1, type=int)
    per_page = 15
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    city = request.args.get('city')
    district = request.args.get('district')
    ward = request.args.get('ward')
    price = int(request.args.get('price', 0))

    if lat and len(lat) > 0 and len(lon) > 0:
        # print(lat, lon)
        # try:
        houses = search(lat, lon,price)
        rooms = []
        for house in houses:
            room = Room.query.filter_by(house_id=house.id).all()
            for r in room:
                images = RoomImage.query.filter_by(room_id=r.id).all()
                r.images = images
            for r in room:
                r.house = House.query.get(r.house_id)
            rooms += room

        # Phân trang kết quả
        total = len(rooms)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_rooms = rooms[start:end]

        return render_template('lookup.html', title='Tra cứu', rooms=paginated_rooms, university=university, page=page, total=total, per_page=per_page)
        # except Exception as e:
        #     print(e)
        #     return redirect(url_for('lookup'))
    if city and len(city) > 0:
        # try:
        address = " ".join(filter(None, [city, district, ward]))
        location = getLocation(address)
        if 'error' in location:
            return redirect(url_for('lookup'))
        lat = location['lat']
        lon = location['lon']
        # print(lat, lon)
        houses = search(lat, lon, price)
        rooms = []

        for house in houses:
            room = Room.query.filter_by(house_id=house.id).all()
            for r in room:
                images = RoomImage.query.filter_by(room_id=r.id).all()
                r.images = images
            for r in room:
                r.house = House.query.get(r.house_id)
            rooms += room

        # Phân trang kết quả
        total = len(rooms)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_rooms = rooms[start:end]

        return render_template('lookup.html', title='Tra cứu', rooms=paginated_rooms, university=university, page=page, total=total, per_page=per_page)
        # except Exception as e:
        #     print(e)
        #     return redirect(url_for('lookup'))    
    return render_template('lookup.html', title='Tra cứu', rooms=[], university=university, page=page, total=0, per_page=per_page)




@app.route('/rent/addrenter', methods=['GET', 'POST'])
@login_required
def addRenter():
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    
    
    if request.method == 'POST':
        try:
            addRenterNew(request)
            return redirect(url_for('rent'))
        except Exception as e:
            # print(e)        
            return render_template('addRenter.html', title='Thêm chỗ thuê', error='Đã xảy ra lỗi!')
    
    return render_template('addRenter.html', title='Thêm chỗ thuê')

@app.route('/rent/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editHouse(id):
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    house = House.query.get(id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        house.name = name
        house.description = description
        db.session.commit()
        return redirect(url_for('seeRooms', id=id))
    return render_template('editHouse.html', title='Chỉnh sửa chỗ thuê', house=house)

@app.route('/rent/delete/<int:id>')
@login_required
def deleteHouse(id):
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    house = House.query.get(id)
    db.session.delete(house)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/house/<int:id>/rooms', methods=['GET', 'POST'])
@login_required
def seeRooms(id):
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    house = House.query.get(id)
    rooms = Room.query.filter_by(house_id=id).all()
    return render_template('rooms.html', title='Phòng trọ', house=house, rooms=rooms)

@app.route('/house/<int:id>/addroom', methods=['GET', 'POST'])
@login_required
def addRoom(id):
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    
    last_room = Room.query.filter_by(house_id=id).order_by(Room.id.desc()).first()
        
    house = House.query.get(id)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        area = request.form['area']
        description = request.form['description']
        type = request.form['type']
        max_people = request.form['numMax']
        current_people = request.form['numCur']
        matching = request.form['matching']
        images = request.files.getlist('images')

        urls = []
        for image in images:
            url = upload_image_to_server(image)
            if 'url' in url:
                urls.append(url['url'])

        room = Room(
            name=f"{name} - {house.name}",
            price=price,
            area=area,
            description=description,
            type=type,
            house_id=id,
            max_people= int(max_people),
            current_people= int(current_people),
            matching= True if matching == 'true' else False
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
    
    return render_template('addRoom.html', title='Thêm phòng trọ', house=house, last_room=last_room)

@app.route('/room/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editRoom(id):
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    
    room = Room.query.get(id)
    house = House.query.get(room.house_id)

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        area = request.form['area']
        description = request.form['description']
        type = request.form['type']
        max_people = request.form['numMax']
        current_people = request.form['numCur']
        matching = request.form['matching']

        room.name = name
        room.price = price
        room.area = area
        room.description = description
        room.type = type
        room.max_people = int(max_people)
        room.current_people = int(current_people)
        room.matching = True if matching == 'true' else False
        db.session.commit()

        return redirect(url_for('seeRooms', id=room.house_id))
    return render_template('editRoom.html', title='Chỉnh sửa phòng trọ', room=room, house=house)

@app.route('/room/delete/<int:id>')
@login_required
def deleteRoom(id):
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':
        return redirect(url_for('home'))
    room = Room.query.get(id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('rent'))


@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    #  Kiểm tra quyền truy cập
    if current_user.role != 'renter':

        return redirect(url_for('home'))
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
    type = request.form['type']
    importance = request.form['importance']
    place_rank = request.form['place_rank']
    
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
        type=type,
        description=description,
        full_address= full_address,
        renter = current_user.id,
        importance=importance,
        place_rank=place_rank
    )
    db.session.add(house)
    db.session.commit()

    
        
    # db.session.add(house_image)
    # db.session.commit()
    


    


    