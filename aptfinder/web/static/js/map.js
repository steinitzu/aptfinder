function EncodeQueryData(data)
{
   var ret = [];
   for (var d in data)
      ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
   return ret.join("&");
}

var markers = [];


function add_marker(point, title, map) {
    var marker = new google.maps.Marker({
        position: point,
        title:title
    });
    marker.setMap(map);
    markers.push(marker);
};

function clear_markers(map) {
    markers.forEach(function(marker){
        marker.setMap(null);
    });
    markers = [];
};

function update_listings(circle) {

    var bounds = circle.getBounds().toJSON();
    Object.assign(bounds, {'radius': circle.getRadius(),
                           'center_lat': circle.getCenter().lat(),
                           'center_lng': circle.getCenter().lng()});
    var data = EncodeQueryData(bounds);

    fetch('/get_apts?'+data, {
        method: 'GET',
        credentials: 'same-origin'
    }).then(function(response) {
        response.json().then(function(result) {
            clear_markers(map);
            result.forEach(function(listing){
                var p = new google.maps.LatLng(
                    listing['latitude'] * (180/Math.PI),
                    listing['longitude'] * (180/Math.PI));
                add_marker(p, listing['address'], map);

                console.log(listing);
            });
        });
    });

};

var map;
var center_timer;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 43.660064, lng: -79.568268},
        zoom: 12
    });
    var filter_circle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: map.getCenter(),
        radius: 1000,
        editable: true,
        draggable: true
    });

    google.maps.event.addListener(filter_circle, 'radius_changed', function() {
        update_listings(filter_circle);
    });
    google.maps.event.addListener(filter_circle, 'center_changed', function() {
        // Set a timer to prevent fetching while user is dragging
        clearTimeout(center_timer);
        center_timer = setTimeout(function() { update_listings(filter_circle); },
                                  100);
    });
}
