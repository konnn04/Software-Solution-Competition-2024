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

const typeLabel = {
    'residential':'Khu dân cư',
    'commercial':'Khu thương mại',
    'industrial':'Khu công nghiệp',
    'recreational':'Khu vui chơi giải trí',
    'school':'Trường học',
    'hospital':'Bệnh viện',
    'police':'Cơ quan công an',
    'government':'Cơ quan hành chính',
    'stadium':'Sân vận động',
    'market':'Chợ',
    'park':'Công viên',
    'marketplace':'Trung tâm thương mại',
    'college':'Trường đại học',
    'university':'Trường đại học',
    'trunk':'Quốc lộ, đường chính',
    'primary':'Khu vực bậc 1',
    'secondary':'Khu vực bậc 2',
    'tertiary':'Khu vực bậc 3',
    'pier':'Bến phà',
    'unclassified':'Không xác định',
    'sports_centre':'Trung tâm thể thao',
    'townhall':'Dinh thự',
    'cafe':'Quán cà phê',
    'fast_food':'Nhà hàng nhanh',
    'bank':'Ngân hàng',
    'aerodrome':'Sân bay',
    'motorway':'Đường cao tốc',
    'recreation_ground':'Khu vui chơi',
    'golf_course':'Sân golf',
    'bridge':'Cây cầu',
    'supermarket':'Siêu thị',
    'administrative':'Khu hành chính',
    'fort':'Pháo đài',
    'station':'Trạm xe lửa',
    'miniature_golf':'Sân golf nhỏ',    
    'pitch':'Sân bóng',
    'library':'Thư viện',
    'convenience':'Tiện ích',
    'swimming_pool':'Bể bơi',
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
    const hard = document.getElementById('hard');
    const submit = document.getElementById('submit');

    const city = document.getElementById('city');
    const district = document.getElementById('district');
    const ward = document.getElementById('ward');
    const street = document.getElementById('street');
    const locationAlert = document.getElementById('location-alert');

    let marker = null;

    closeLoca.addEventListener('click', () => {
        overlay.classList.remove('show')
    })
    
    check.addEventListener('click', () => {
        if (!city.value || !district.value || !ward.value) {
            console.log('Please fill in all fields')
            locationAlert.className = 'alert alert-danger';
            locationAlert.innerHTML = 'Vui lòng điền đầy đủ địa chỉ để tiếp tục';
            return
        }

        const address = `${street.value} ${ward.value} ${district.value} ${city.value}`;
        // console.log(address);
        overlay.classList.add('show')
        fetch(`https://nominatim.openstreetmap.org/search.php?q=${address}&format=jsonv2`)
            .then(response => response.json())
            .then(data => {
                // console.log(data)
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
                    marker.setLatLng([latValue, lonValue]);
                } else {
                    marker = L.marker([latValue, lonValue]).addTo(map);
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
                        marker2 = L.marker(e.latlng).addTo(map);
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
                        // console.log(data.category)
                        console.log(displayName)
                        console.log(s)
                        const check = displayName.includes(ward.value.toLowerCase()) && displayName.includes(district.value.toLowerCase()) && displayName.includes(city.value.toLowerCase());
                        // if (check) {
                            locationAlert.className = 'alert alert-success';
                            locationAlert.innerHTML = 'Tọa độ hợp lệ';
                            type.value = typeLabel[data.type] || 'Không xác định';
                            fullAddress.value = data.display_name;
                            fullAddress2.value = data.display_name;

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
                console.error('Error fetching address:', error)
                locationAlert.className = 'alert alert-danger';
                locationAlert.innerHTML = 'Địa chỉ không hợp lệ';
            })
    })
}

window.onload = triggerEvents;