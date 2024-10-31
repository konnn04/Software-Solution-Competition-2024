
function initFacilities() {
    const schoolName = document.getElementById('school').innerText;
    const facilities = document.getElementById('facilities');
    fetch(`https://nominatim.openstreetmap.org/search.php?q=${schoolName}&format=jsonv2`)
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

window.onload = ()=>{
    initFacilities()
}

