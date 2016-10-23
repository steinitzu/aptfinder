var map;
var center_timer;

class Listing {
    constructor(data) {
        // Accepts json data
        this.data = data;
        var p = new google.maps.LatLng(
            data['lat_deg'],
            data['lng_deg']);
        this.marker = new google.maps.Marker({
            position: p,
            title: data['title']});
        // Can be added through Stamp.appendChildren
        this.el = this.new_el();
        // function highlight(el) {
        //     console.log(el);
        // }
        this.marker.addListener('mouseup', this.toggle_pin.bind(this));


        this.pinned = false;
    }

    toggle_pin() {
        let el = document.getElementById('listing-'+this.data.id);
        let cls = el.className;
        if (cls === 'pinned') {
            el.className = '';
            this.pinned = false;
        } else {
            el.className = 'pinned';
            this.pinned = true;
        }
        el.scrollIntoView();
    }

    new_el() {
        this.el = Stamp.expand(ctx.import('ltempl'), this.data);
        return this.el;
    }
}

class ListingsMgr {
    constructor(...listings) {
        this.listings = listings;
        this.pinned = [];
        this.sort_order = false;
    }

    clear_markers() {
        this.listings.forEach(function(listing){
            if (listing.pinned) {
                return;
            };
            // Remove from map
            listing.marker.setMap(null);
        });
    }

    clear_list_view() {
        var listings_el = document.getElementById("listings");
        let children = Array.from(listings_el.children);
        children.forEach(function(child) {
            if (child.className === 'pinned') {
                return;
            };
            listings_el.removeChild(child);

        });
    }

    clear_data() {
        let new_list = [];
        this.listings.forEach(function(listing) {
            if(listing.pinned) {
                new_list.push(listing);
            };
        });
        this.listings = new_list;

    }

    // Clear all unpinned listings from map, sidebar and array
    clear_all() {
        this.clear_markers();
        this.clear_list_view();
        this.clear_data();
    }

    fill_markers() {
        this.listings.forEach(function(listing){
            listing.marker.setMap(map);
        });
    }


    add_to_list_view(listing) {
        Stamp.appendChildren(document.getElementById('listings'),
                             listing.new_el());
        let el = document.getElementById('listing-'+listing.data['id']);
        el.addEventListener('mouseup', listing.toggle_pin.bind(listing));


    }

    fill_list_view() {
        this.listings.forEach( this.add_to_list_view );
    }

    replace_listings(...listings) {
        this.clear_all();
        this.listings.push.apply(this.listings, listings);
        this.fill_markers();
        this.fill_list_view();
    }

    refresh() {
        this.clear_list_view();
        this.clear_markers();
        this.fill_markers();
        this.fill_list_view();
    }

    add(listing) {
        this.listings.push(listing);
        listing.marker.setMap(map);
        this.add_to_list_view(listing);
    }

    sort(key) {
        // should prepend data to key before sort (listing.data)
        var reverse = this.sort_order;
        this.sort_order = !this.sort_order;
        console.log(this.listings);
        sortByKey(this.listings, key, reverse);
        console.log(this.listings);
        this.refresh();
    };
}


var listingsmgr = new ListingsMgr();


function update_listings(circle) {

    var bounds = circle.getBounds().toJSON();
    Object.assign(bounds, {'radius': circle.getRadius(),
                           'center_lat': circle.getCenter().lat(),
                           'center_lng': circle.getCenter().lng(),
                           'coordtype': 'degrees'});
    var data = EncodeQueryData(bounds);

    fetch('/get_apts?'+data, {
        method: 'GET',
        credentials: 'same-origin'
    }).then(function(response) {
        response.json().then(function(result) {
            listingsmgr.clear_all();
            result.forEach(function(data){
                listingsmgr.add(new Listing(data));
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
        strokeColor: '#4dff4d',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#4dff4d',
        strokeOpacity: 0.1,
        map: this.map,
        center: this.map.getCenter(),
        radius: 5000,
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
