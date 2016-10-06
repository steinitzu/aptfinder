var markers = [];
var listings = [];
var sort_order;
var map;
var center_timer;

class Listing {
    constructor(data) {
        // Accepts json data
        this.data = data;
        var p = new google.maps.LatLng(
            // TODO: Should request coords in degrees
            data['latitude'] * (180/Math.PI),
            data['longitude'] * (180/Math.PI));
        this.marker = new google.maps.Marker({
            position: point,
            title: data['title']});
        // Can be added through Stamp.appendChildren
        this.el = Stamp.expand(ctx.import('ltempl'), data);
    }
}

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


function clear_listings_el() {
    var listingsel = document.getElementById("listings");
    while (listingsel.firstChild) {
        listingsel.removeChild(listingsel.firstChild);
    };
};


function add_to_listings_el(listing) {
    var expanded = Stamp.expand(ctx.import('ltempl'), listing);
    Stamp.appendChildren(document.getElementById('listings'), expanded);
};


function populate_listings_el(){
    listings.forEach(function(listing){
        add_to_listings_el(listing);
    });
};

function sort_listings(key) {
    var reverse;
    if (sort_order) {
        reverse = true;
        sort_order = false;
    } else {
        reverse = false;
        sort_order = true;
    };
    sort_by_key(listings, key, reverse=reverse);
    clear_listings_el();
    populate_listings_el();

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
            // Clear text listings
            clear_listings_el();

            listings = [];
            result.forEach(function(listing){
                add_to_listings_el(listing);
                var p = new google.maps.LatLng(
                    listing['latitude'] * (180/Math.PI),
                    listing['longitude'] * (180/Math.PI));
                add_marker(p, listing['address'], map);
                listings.push(listing);
            });
        });
    });
};

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
