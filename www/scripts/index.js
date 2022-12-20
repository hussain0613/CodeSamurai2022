// Initialize and add the map

function get_set_project_markers(map){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var projects = JSON.parse(this.responseText);
      for(var i = 1; i < projects.length; ++i){
        set_marker(projects[i], map);
      }
    }
  };
  xhttp.open("GET", SITE_SETTINGS["BASE_URL"] + "/project/get/", true);
  xhttp.send();
}

function set_marker(project, map){
  // The marker, positioned at Uluru
  var pin_coord = {lat: project["latitude"], lng: project["longitude"]}
  
  const marker = new google.maps.Marker({
    position: pin_coord,
    map: map,
  });
}

function initMap() {
    var default_center = {lat: 23.76, lng: 90.41 };
    var map_zoom = 8;

    // The map, centered at default_center
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: map_zoom,
      center: default_center,
    });
    get_set_project_markers(map);
  }

  window.initMap = initMap;
  