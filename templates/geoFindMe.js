function geoFindMe() {
  var output = document.getElementById("location");
  var map = document.getElementById("map");

  if (!navigator.geolocation){
    output.value = "Geolocation is not supported by your browser";
    return;
  }

  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;

    output.value = latitude + ', ' + longitude;
	
	document.getElementById('location').setAttribute('disabled', 'disabled');
	
	var img = new Image();
    img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latitude + "," + longitude + "&zoom=13&size=300x300&sensor=false&key=AIzaSyAs6LEx2djutDP5siKOfU5J1Dlsa2led-A";

    map.appendChild(img);
	
  }

  function error(e) {
	console.log(e);
    output.value = "Unable to retrieve your location";
  }

  output.value = "Locating...";

  navigator.geolocation.getCurrentPosition(success, error);
}