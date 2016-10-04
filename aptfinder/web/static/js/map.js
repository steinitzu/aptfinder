function EncodeQueryData(data)
{
   var ret = [];
   for (var d in data)
      ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
   return ret.join("&");
}


function update_listings(circle) {

    var data = EncodeQueryData({'radius': circle.getRadius(),
                                'lat': circle.getCenter().lat(),
                                'lng': circle.getCenter().lng()});
    fetch('/get_apts?'+data, {
        method: 'GET',
        credentials: 'same-origin'
    }).then(function(response) {
        response.json().then(function(result) {
            // TODO: Display results
            result.forEach(function(listing){
                var p = new google.maps.LatLng(
                    listing['latitude'] * (180/Math.PI),
                    listing['longitude'] * (180/Math.PI));
                var marker = new google.maps.Marker({
                    position: p,
                    title:listing['address']
                });
                marker.setMap(map);

                // TODO: delete the old markers
                console.log(marker);

                console.log(listing);
            });
        });
    });

};

var map;
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
        update_listings(filter_circle);
    });
}
