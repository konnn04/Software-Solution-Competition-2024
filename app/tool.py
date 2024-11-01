import requests
from flask import jsonify
import os
from werkzeug.utils import secure_filename
from flask import current_app
import time

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