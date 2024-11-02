
async function initFacilities() {
    const schoolName = document.getElementById('school').innerText;
    const facilities = document.getElementById('facilities');
    await fetch(`https://nominatim.openstreetmap.org/search.php?q=${schoolName}&format=jsonv2`)
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            const option = document.createElement('option');
            option.value = element.lat + ',' + element.lon;
            option.text = element.display_name;
            facilities.appendChild(option);
        });
    }).catch(err => {
        console.log(err)
    })
}

function triggerEvent (element, event) {
    const facilities = document.getElementById('facilities');
    const city = document.getElementById('city');
    const district = document.getElementById('district');
    const ward = document.getElementById('ward');
    const price = document.getElementById('price');
    
    city.addEventListener('change', (e) => {
        resetFacilities()
    })

    district.addEventListener('change', (e) => {
        resetFacilities()
    })

    ward.addEventListener('change', (e) => {
        resetFacilities()
    })
    
    facilities.addEventListener('change', (e) => {
        resetAddress()
        const latlon = e.target.value.split(',')
        const lat = latlon[0]
        const lon = latlon[1]
        document.getElementById("lat").value = lat
        document.getElementById("lon").value = lon
    })
}

function resetAddress() {
    document.getElementById('city').value = ''
    document.getElementById('district').value = ''
    document.getElementById('ward').value = ''
}

function resetFacilities() {
    document.getElementById('facilities').value = ''
}

function praseArgs() {
    const lat = document.getElementById('lat')
    const lon = document.getElementById('lon')
    const city = document.getElementById('city')
    const district = document.getElementById('district')
    const ward = document.getElementById('ward')
    const price = document.getElementById('price')
    const facilities = document.getElementById('facilities')

    const args = new URLSearchParams(window.location.search)
    if (args.has('lat') && args.has('lon')) {
        lat.value = args.get('lat')
        lon.value = args.get('lon')
        facilities.value = args.get('lat') + ',' + args.get('lon')
    }
    if (args.has('city')) {
        city.value = args.get('city')
    }
    if (args.has('district')) {
        district.value = args.get('district')
    }
    if (args.has('ward')) {
        ward.value = args.get('ward')
    }
    if (args.has('price')) {
        price.value = args.get('price')
    }
    
}

function search() {
    const lat = document.getElementById('lat').value;
    const lon = document.getElementById('lon').value;
    const city = document.getElementById('city').value;
    const district = document.getElementById('district').value;
    const ward = document.getElementById('ward').value;
    const price = document.getElementById('price').value;

    let url = new URL(window.location.href.split('?')[0]);
    
    if (lat != '') {
        url.searchParams.set('lat', lat);
    }
    if (lon != '') {
        url.searchParams.set('lon', lon);
    }
    if (city != '') {
        url.searchParams.set('city', city);
    }
    if (district != '') {
        url.searchParams.set('district', district);
    }
    if (ward != '') {
        url.searchParams.set('ward', ward);
    }
    if (price != '') {
        url.searchParams.set('price', price);
    }

    window.location.href = url.href    
}

window.onload = async ()=>{
    await initFacilities()
    // await praseArgs()
    await triggerEvent()
}

