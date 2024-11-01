import requests
from flask import jsonify
import os
from werkzeug.utils import secure_filename
from flask import current_app
import time
import math
from app.models import House, User, Review, Room

def flood_prediction(lat, lon):
    url = f"https://flood-api.open-meteo.com/v1/flood?latitude={lat}&longitude={lon}&daily=river_discharge,river_discharge_max&models=forecast_v4"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()

    try:
        daily_data = response.get('daily', {})
        river_discharge_max = daily_data.get('river_discharge_max', [])
        
        # Tính mức độ ngập lụt
        flood_levels = []
        for discharge in river_discharge_max:
            if discharge < 700:
                flood_levels.append('không')
            elif discharge < 1200:
                flood_levels.append('khá thấp')
            elif discharge < 2000:
                flood_levels.append('thấp')
            elif discharge < 3000:
                flood_levels.append('trung bình')
            else:
                flood_levels.append('cao')

        # Tính mức độ thường xuyên gặp ngập lụt
        flood_days = [i for i, level in enumerate(flood_levels) if level in ['trung bình', 'cao']]
        if len(flood_days) > 1:
            intervals = [flood_days[i] - flood_days[i - 1] for i in range(1, len(flood_days))]
            average_interval = sum(intervals) / len(intervals)
        else:
            average_interval = float('inf')  # Không đủ dữ liệu để tính

    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to process data'}), 500

    return jsonify({
        'flood_levels': flood_levels,
        'average_interval': average_interval
    })

def upload_image_to_server(image):
    # name = str(name)
    try:
        if image.filename == '':
            return {'error': 'No selected file'}

        filename = secure_filename(image.filename)
        filename = f"{os.path.splitext(filename)[0]}_{int(time.time())}{os.path.splitext(filename)[1]}"
        file_path = os.path.join(current_app.root_path, 'static', 'file', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        image.save(file_path)
        file_url = f"/static/file/{filename}"
        return {'url': file_url}
    except Exception as e:
        print(e)
        return {'error': 'Failed to upload image'}
    
def getSchoolName(email):
    domain = email.split('@')[1]
    list = {
        "vnu.edu.vn": "Dai hoc Quoc gia Ha Noi",
        "hcmus.edu.vn": "Dai hoc Khoa hoc Tu nhien - DHQG TP.HCM",
        "hust.edu.vn": "Dai hoc Bach Khoa Ha Noi",
        "uit.edu.vn": "Dai hoc Cong nghe Thong tin - DHQG TP.HCM",
        "hcmut.edu.vn": "Dai hoc Bach Khoa - DHQG TP.HCM",
        "ftu.edu.vn": "Dai hoc Ngoai Thuong",
        "neu.edu.vn": "Dai hoc Kinh te Quoc dan",
        "rmit.edu.vn": "RMIT Viet Nam",
        "hanu.edu.vn": "Dai hoc Ha Noi",
        "ueh.edu.vn": "Dai hoc Kinh te TP.HCM",
        "hcmussh.edu.vn": "Dai hoc Khoa hoc Xa hoi va Nhan van - DHQG TP.HCM",
        "ulis.vnu.edu.vn": "Dai hoc Ngoai ngu - DHQG Ha Noi",
        "vnua.edu.vn": "Hoc vien Nong nghiep Viet Nam",
        "tlu.edu.vn": "Dai hoc Thuy Loi",
        "tdtu.edu.vn": "Dai hoc Ton Duc Thang",
        "fpt.edu.vn": "Dai hoc FPT",
        "hcmue.edu.vn": "Dai hoc Su pham TP.HCM",
        "ptit.edu.vn": "Hoc vien Cong nghe Buu chinh Vien thong",
        "hcmuaf.edu.vn": "Dai hoc Nong Lam TP.HCM",
        "dtu.edu.vn": "Dai hoc Duy Tan",
        "hvnh.edu.vn": "Hoc vien Ngan hang",
        "hvcsnd.edu.vn": "Hoc vien Canh sat Nhan dan",
        "ntu.edu.vn": "Dai hoc Nha Trang",
        "huflit.edu.vn": "Dai hoc Ngoai ngu - Tin hoc TP.HCM",
        "huph.edu.vn": "Dai hoc Y te Cong cong",
        "vnuhcm.edu.vn": "Dai hoc Quoc gia TP.HCM",
        "uef.edu.vn": "Dai hoc Kinh te - Tai chinh TP.HCM",
        "duytan.edu.vn": "Dai hoc Duy Tan",
        "hubt.edu.vn": "Dai hoc Kinh doanh va Cong nghe Ha Noi",
        "tmu.edu.vn": "Dai hoc Thuong mai",
        "tvu.edu.vn": "Dai hoc Tra Vinh",
        "buh.edu.vn": "Dai hoc Ngan hang TP.HCM",
        "agu.edu.vn": "Dai hoc An Giang",
        "lhu.edu.vn": "Dai hoc Lac Hong",
        "ou.edu.vn": "Dai hoc Mo Thanh Pho Ho Chi Minh",
        "huce.edu.vn": "Dai hoc Xay dung Ha Noi",
        "hcmulaw.edu.vn": "Dai hoc Luat TP.HCM",
        "vgu.edu.vn": "Dai hoc Viet Duc",
        "hvktmm.edu.vn": "Hoc vien Ky thuat Mat ma",
        "cdsp.edu.vn": "Cao dang Su pham",
        "cdkt.edu.vn": "Cao dang Kinh te",
        "cdcn.edu.vn": "Cao dang Cong nghe",
        "cdyt.edu.vn": "Cao dang Y te",
        "cdspkt.edu.vn": "Cao dang Su pham Ky thuat"
    }

    return list.get(domain, "Không xác định")

def getFacilities(school):
    return {   }

def getLocation(address):
    url = "https://nominatim.openstreetmap.org/search.php?q=" + address + "&format=json".lower().replace(" ", "%20")
    # print(url)
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to get location'}  
    response = response.json()
    if len(response) > 0:
        print(response)
        return {'lat': response[0]['lat'], 'lon': response[0]['lon']}
    return {'error': 'Failed to get location'}

def distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def traficAPI(slat, slon, elat, elon):
    start_lat = slat
    start_lon = slon
    end_lat = elat
    end_lon = elon

    if not start_lat or not start_lon or not end_lat or not end_lon:
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        # Sử dụng OpenRouteService để lấy thông tin giao thông
        api_key = '5b3ce3597851110001cf6248341b48b6fe0d464685943bef1eb12692'
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "coordinates": [
                [float(start_lon), float(start_lat)],
                [float(end_lon), float(end_lat)]
            ],
            "extra_info": ["steepness", "waycategory", "waytype", "surface", "tollways", "traildifficulty", "suitability", "roadaccessrestrictions", "countryinfo", "green", "noise", "airquality", "weather", "traffic"]
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()
        traffic_info = data.get('routes', [])[0].get('segments', [])[0].get('steps', [])

        # Đánh giá độ kẹt xe dựa trên thông tin giao thông
        congestion_levels = []
        for step in traffic_info:
            congestion = step.get('traffic', {}).get('congestion', 'unknown')
            congestion_levels.append(congestion)

        return jsonify({'congestion_levels': congestion_levels})
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': f"Failed to fetch data: {e}"}), 500
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.content}")
        return jsonify({'error': 'Failed to process data'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Failed to process data'}), 500



def search(lat,lon, price):
    lat = float(lat)
    lon = float(lon)
    houses = House.query.all()
    for h in houses:
        d = distance(lat, lon, h.lat, h.lon)
        h.distance = round(d*0.7, 2)

    houses = sorted(houses, key=lambda x: x.distance)
    return houses

