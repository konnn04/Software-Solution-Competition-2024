from app import app, get_google_auth, login_manager
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, House, HouseImage
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
    houses = House.query.all()
    houses_with_images = []
    for house in houses:
        images = HouseImage.query.filter_by(house_id=house.id).all()
        house.images = images
        houses_with_images.append(house)

    university = None
    if current_user.is_authenticated:
        university = getSchoolName(current_user.email)


    return render_template('home.html', title='Trang chủ', houses = houses_with_images, university = university)


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

@app.route('/lookup', methods=['GET', 'POST'])
@login_required
def lookup():
    if request.method == 'POST':
        return redirect(url_for('home'))
    university = getSchoolName(current_user.email)
    return render_template('lookup.html', title='Tra cứu', university=university)

@app.route('/detail/<int:id>')
def detail(id):
    house = House.query.get(id)
    images = HouseImage.query.filter_by(house_id=id).all()
    house.images = images
    return render_template('detail.html', title='Chi tiết', house=house)

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
    images = request.files.getlist('images')
    print(request.files)

    if not images:
        print("No images found")
        return redirect(url_for('addRenter'))
    
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
        full_address= full_address
    )
    db.session.add(house)
    db.session.commit()

    for i, image in enumerate(images):
        upload_result = upload_image_to_server(image,i)
        if 'url' in upload_result:
            house_image = HouseImage(
                house_id=house.id,
                url=upload_result['url']
            )
            db.session.add(house_image)
            db.session.commit()
        else:
            print(upload_result['error'])
        
    # db.session.add(house_image)
    # db.session.commit()
    



    


    


    