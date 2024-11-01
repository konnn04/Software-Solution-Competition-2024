const form = document.querySelector('form');
const formBox = document.querySelector('#form-box');
const addAddress = document.querySelector('#addAddress');

let n = 0

const w = {}

// addAddress.addEventListener('click', () => {
//     n++;
//     const div = document.createElement('div');
//     div.className = 'form-group';
//     div.innerHTML = `
//     <label for="name">
//         <input type="text" placeholder="Họ và tên" name="name" class="name" required>
//     </label>
//     <label for="address">
//         <input type="text" placeholder="Số nhà, ấp, xã,..." name="address" class="address" required>
//     </label>
//     <label for="phone">
//         <input type="text" placeholder="Số điện thoại" name="phone" class="phone" required>
//     </label>
//     <p class="location"></p>

//     `;
//     const delBtn = document.createElement('button');
//     delBtn.className = 'btn btn-danger';
//     delBtn.innerHTML = 'Xóa';
//     delBtn.onclick = () => {
//         div.remove();
//     }
//     div.appendChild(delBtn);
//     formBox.appendChild(div);    
// })

const map = L.map('map')

const customIcon1 = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/1076/1076983.png', // Đường dẫn đến icon tùy chỉnh
    iconSize: [38, 38], // Kích thước của icon
    iconAnchor: [22, 38], // Điểm neo của icon
    popupAnchor: [-3, -76], // Điểm neo của popup
    // shadowUrl: 'https://example.com/path/to/custom-shadow.png', // Đường dẫn đến shadow tùy chỉnh
    // shadowSize: [68, 95], // Kích thước của shadow
    // shadowAnchor: [22, 94] // Điểm neo của shadow
});

const customIcon2 = L.icon({
    iconUrl: 'https://cdn-icons-png.freepik.com/512/1020/1020231.png', // Đường dẫn đến icon tùy chỉnh
    iconSize: [38, 38], // Kích thước của icon
    iconAnchor: [22, 38], // Điểm neo của icon
    popupAnchor: [-3, 0], // Điểm neo của popup
    // shadowUrl: 'https://example.com/path/to/custom-shadow.png', // Đường dẫn đến shadow tùy chỉnh
    // shadowSize: [68, 95], // Kích thước của shadow
    // shadowAnchor: [22, 94] // Điểm neo của shadow
});

let marker = null;

const typeLabel = {
    'residential': ['Khu dân cư', 0.8],
    'commercial': ['Khu thương mại', 0.7],
    'industrial': ['Khu công nghiệp', 0.4],
    'recreational': ['Khu vui chơi giải trí', 0.7],
    'school': ['Trường học', 0.9],
    'hospital': ['Bệnh viện', 1.0],
    'police': ['Cơ quan công an', 1.0],
    'government': ['Cơ quan hành chính', 0.9],
    'stadium': ['Sân vận động', 0.5],
    'market': ['Chợ', 0.6],
    'park': ['Công viên', 0.7],
    'marketplace': ['Trung tâm thương mại', 0.7],
    'college': ['Trường đại học', 0.8],
    'university': ['Trường đại học', 0.8],
    'trunk': ['Quốc lộ, đường chính', 0.7],
    'primary': ['Khu vực đông dân cư', 0.8],
    'secondary': ['Khu vực thưa dân cư', 0.7],
    'tertiary': ['Khu vực ít dân cư', 0.6],
    'pier': ['Bến phà', 0.4],
    'unclassified': ['Không xác định', 0.3],
    'sports_centre': ['Trung tâm thể thao', 0.6],
    'townhall': ['Dinh thự', 0.8],
    'cafe': ['Quán cà phê', 0.7],
    'fast_food': ['Nhà hàng nhanh', 0.7],
    'bank': ['Ngân hàng', 0.9],
    'aerodrome': ['Sân bay', 0.5],
    'motorway': ['Đường cao tốc', 0.4],
    'recreation_ground': ['Khu vui chơi', 0.7],
    'golf_course': ['Sân golf', 0.8],
    'bridge': ['Cây cầu', 0.6],
    'supermarket': ['Siêu thị', 0.7],
    'administrative': ['Khu hành chính', 0.9],
    'fort': ['Pháo đài', 0.7],
    'station': ['Trạm xe lửa', 0.6],
    'miniature_golf': ['Sân golf nhỏ', 0.8],
    'pitch': ['Sân bóng', 0.6],
    'library': ['Thư viện', 0.9],
    'convenience': ['Tiện ích', 0.7],
    'swimming_pool': ['Bể bơi', 0.7],
    'apartments': ['Chung cư', 0.8],
    'house': ['Nhà riêng', 0.9],
    'service': ['Dịch vụ', 0.6],
    'restaurant': ['Nhà hàng', 0.7],
    'parking': ['Bãi đậu xe', 0.5],
    'wastewater_plant': ['Nhà máy xử lý nước thải', 0.3],
    'playground': ['Sân chơi', 0.8],
    'hamlet': ['Thôn xóm', 0.6],
}

function triggerEvents(){
    const check = document.getElementById('check-location');
    const lat = document.getElementById('latitude');
    const lon = document.getElementById('longitude');
    const overlay = document.getElementById('overlay');
    const closeLoca = document.getElementById('close-check-location');
    const fullAddress = document.getElementById('full-address');
    const fullAddress2 = document.getElementById('full-address2');
    const type = document.getElementById('type');
    const type2 = document.getElementById('type2');
    const hard = document.getElementById('hard');
    const submit = document.getElementById('submit');

    const city = document.getElementById('city');
    const district = document.getElementById('district');
    const ward = document.getElementById('ward');
    const street = document.getElementById('street');
    const locationAlert = document.getElementById('location-alert');
    const importance = document.getElementById('importance');
    const place_rank = document.getElementById('place_rank')


    closeLoca.addEventListener('click', () => {
        overlay.classList.remove('show')
    })
    
    check.addEventListener('click', async () => {
        check.disabled = true;
        if (!city.value || !district.value || !ward.value) {
            console.log('Please fill in all fields')
            locationAlert.className = 'alert alert-danger';
            locationAlert.innerHTML = 'Vui lòng điền đầy đủ địa chỉ để tiếp tục';
            return
        }

        const address = `${street.value} ${ward.value} ${district.value} ${city.value}`;
        // console.log(address);
        
        await fetch(`https://nominatim.openstreetmap.org/search.php?q=${address}&format=jsonv2`)
            .then(response => response.json())
            .then(data => {
                check.disabled = false;
                if (data.length === 0) {
                    locationAlert.className = 'alert alert-danger';
                    locationAlert.innerHTML = 'Địa chỉ không hợp lệ, không thể mở bản đồ';
                    type.value = 'Không xác định';
                    type2.value = 'Không xác định';
                    fullAddress.value = '';
                    fullAddress2.value =    '';
                    importance.value = '';
                    place_rank.value = '';
                    return
                }
                overlay.classList.add('show')
                const latValue = parseFloat(data[0].lat)
                const lonValue = parseFloat(data[0].lon)
                lat.value = latValue
                lon.value = lonValue     
                        
                map.setView([latValue, lonValue], 13)
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }).addTo(map)

                if (marker) {
                    marker.setLatLng([latValue, lonValue], {icon: customIcon1})
                } else {
                    marker = L.marker([latValue, lonValue], {icon: customIcon1}).addTo(map).bindTooltip("Địa chỉ tìm thấy", { permanent: true, direction: "top" })
                }

                let marker2 = null;
                 // Add click event to the map
                map.on('click', function(e) {
                    // console.log(e.latlng)
                    const loncation = e.latlng;
                    // Update the latitude and longitude fields
                    lat.value = loncation.lat;
                    lon.value = loncation.lng;
                    // Add or update the marker
                    if (marker2) {
                        marker2.setLatLng(e.latlng);
                    } else {
                        marker2 = L.marker(e.latlng, {icon : customIcon2}).addTo(map).bindTooltip("Địa chỉ bạn chọn", { permanent: true, direction: "top" })
                    }

                    fetch(`https://flood-api.open-meteo.com/v1/flood?latitude=${loncation.lat}&longitude=${loncation.lng}&daily=river_discharge,river_discharge_max&models=forecast_v4`)
                    .then(response => response.json())
                    .then(floodData => {
                        // console.log(floodData);
                        const riverDischargeMax = floodData.daily.river_discharge_max;
                        let floodRisk = '0';
                        if (riverDischargeMax.some(discharge => discharge >= 2000)) {
                            floodRisk = '4';
                        } else if (riverDischargeMax.some(discharge => discharge >= 1200)) {
                            floodRisk = '3';
                        } else if (riverDischargeMax.some(discharge => discharge >= 700)) {
                            floodRisk = '2';
                        } else if (riverDischargeMax.some(discharge => discharge >= 500)) {
                            floodRisk = '1';
                        }
                        hard.value = floodRisk;
                        // hard.value = floodRisk === 'Cao' ? 'Có nguy cơ ngập lụt cao' : floodRisk === 'Trung bình' ? 'Có nguy cơ ngập lụt trung bình' : floodRisk === 'Thấp' ? 'Có nguy cơ ngập lụt thấp' : 'Không có nguy cơ ngập lụt';
                    })
                    .catch(error => console.error('Error fetching flood data:', error));

                    fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${loncation.lat}&lon=${loncation.lng}`)
                    .then(response => response.json())
                    .then(data => {
                        const displayName = data.display_name.toLowerCase();
                        const s = `${ward.value}, ${district.value}, ${city.value}`.toLowerCase().trim()
                        console.log(data.type)

                        // console.log(displayName)
                        // console.log(s)
                        const check = displayName.includes(ward.value.toLowerCase()) && displayName.includes(district.value.toLowerCase()) && displayName.includes(city.value.toLowerCase());
                        // if (check) {
                            locationAlert.className = 'alert alert-success';
                            locationAlert.innerHTML = 'Tọa độ hợp lệ';
                            type.value = typeLabel[data.type][0] || 'Không xác định';
                            type2.value = typeLabel[data.type][0] || 'Không xác định';
                            fullAddress.value = data.display_name;
                            fullAddress2.value = data.display_name;
                            importance.value = data.importance;
                            place_rank.value = data.place_rank;

                        // } else {
                        //     locationAlert.className = 'alert alert-danger';
                        //     locationAlert.innerHTML = 'Tọa độ không nằm trong địa chỉ đã nhập';
                        //     type.value = 'Không xác định';
                        //     fullAddress.value = '';
                        //     fullAddress2.value = '';
                        //     hard.value = '';
                        // }
                    })
                    .catch(error => console.error('Error fetching address:', error));
                });
            })
            .catch(error => {
                check.disabled = false;
                console.error('Error fetching address:', error)
                locationAlert.className = 'alert alert-danger';
                locationAlert.innerHTML = 'Địa chỉ không hợp lệ, không thể mở bản đồ';

            })
    })
}

window.onload = triggerEvents;