// Mapa (https://leafletjs.com/)
if (document.getElementById("map")) {
  var defaultCoords = getDefaultCoords();
  var defaultZoom = getDefaultZoom();
  var map = L.map('map').setView(defaultCoords, defaultZoom);
  var marker = L.marker(defaultCoords).addTo(map);
  var popup = L.popup();
  var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  var locationErrorMessage = document.getElementById("location-error");


  // Obtener geolocalización del navegador
  function getLocation() {
    deleteLocationCookies();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, errorGettingLocation, {timeout: 3000});
    } else {
      locationErrorMessage.innerHTML = "Compartir la localización no es posible en este navegador.";
    }
  }

  function errorGettingLocation(error) {
    locationErrorMessage.innerHTML = "No ha sido posible obtener la localización. Mensaje del error : '" + error.message + "'.";
  }

  function showPosition(position) {
    var coords = {};
    coords.latitude = position.coords.latitude;
    coords.longitude = position.coords.longitude;
    goTo(coords);
  }

  function goTo(coordinates) {
    var zoom = 17;
    saveLocationCookies(coordinates, zoom);
    map.setView([coordinates.latitude, coordinates.longitude], zoom)
    map.removeLayer(marker)
    marker = L.marker([coordinates.latitude, coordinates.longitude]).addTo(map);
  }

  function onMapClick(event) {
    var text = '¿Quieres buscar la información catastral de este punto?<br>'
    var linkParameters = "latitude=" + event.latlng.lat + "&longitude=" + event.latlng.lng
    var link = '<a href="/el-corredor/catastro?' + linkParameters + '">SI</a>'
    var popupContent = text + link
    popup.setLatLng(event.latlng).setContent(popupContent).openOn(map);
  }

  map.on('click', onMapClick);
}


// Catastro
if (document.getElementById("copyReferenceLink")) {
  document.getElementById("copyReferenceLink").onclick = function() {
    var reference = document.getElementById("reference").textContent;
    navigator.clipboard.writeText(reference);
    document.getElementById("copyReference").innerHTML='<span class="link-disabled">La Referencia Catastral ha sido copiada en el portapapeles</span>';
  };
}


// Localización
function saveLocationCookies(coordinates, zoom) {
  setCookie("latitude", coordinates.latitude);
  setCookie("longitude", coordinates.longitude);
  setCookie("zoom", zoom);
}

function deleteLocationCookies() {
  deleteCookie("latitude");
  deleteCookie("longitude");
  deleteCookie("zoom");
}

function getDefaultCoords() {
  if (checkCookie("latitude") && checkCookie("longitude")) {
    return [parseFloat(getCookie("latitude")), parseFloat(getCookie("longitude"))];
  } else {
    return [40.42068475830824, -3.7028843129534112];
  }
}

function getDefaultZoom() {
  if (checkCookie("zoom")) {
    return parseInt(getCookie("zoom"));
  } else {
    return 6;
  }
}


// Cookies
function setCookie(name, value) {
  document.cookie = name + "=" + value;
}

function deleteCookie(name) {
  setCookie(name, "");
}

function getCookie(name) {
  name += "=";
  let ca = document.cookie.split(";");
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie(name) {
  if (getCookie(name) != "") {
    return true;
  } else {
    return false;
  }
}
