// Initialize and add the map

function get_set_project_markers(map){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var projects = JSON.parse(this.responseText);
      for(var i = 1; i < projects.length; ++i){
        set_marker(projects[0], projects[i], map);
      }
    }
  };
  xhttp.open("GET", SITE_SETTINGS["BASE_URL"] + "/get_projects/", true);
  xhttp.send();
}

function set_marker(headers, project, map){
  // The marker, positioned at Uluru
  var coords = project[8];
  coords = coords.replaceAll("(", "[");
  coords = coords.replaceAll(")", "]");
  coords = coords = "[" + coords + "]";
  
  coords = JSON.parse(coords);
  
  var pin_coord = {lat: coords[0][0], lng: coords[0][1]}
  
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
  