class Listing {
    constructor(data) {
        Object.assign(this, data);
    }
}


class ListingCollection {

    constructor(){
        this.listings = {};
        this.events = {};
    }

    add(listing) {
        // Add new listing
        this.listings[listing['id']] = listing;
        this.notify('added', listing);
    }

    remove(listing) {
        // remove given listing
        let x = this.listings[listing['id']];
        delete this.listings[listing['id']];
        this.notify('removed', x);

    }

    clear() {
        for (var key in this.listings) {
            this.remove(this.listings[key]);
        }
        this.notify('cleared', null);
    }

    fill(data) {
        data.forEach(function(d) {
            let l = new Listing(d);
            this.add(l);
        }.bind(this));
        this.notify('reloaded', this.listings);
    }


    subscribe(event, callback) {
        if (!(event in this.events)) {
            this.events[event] = [];
        };
        this.events[event].push(callback);
    }

    notify(event, data) {
        let events = this.events[event];
        for (var e in events) {
            events[e](event, data);
        };

    }
}

class Filter {
    constructor(collection, circle, bedrooms) {
        this.collection = collection;

        let doFilter = function() {
            this.get(
                {'bedrooms': bedrooms.value},
                circle);
        }.bind(this);

        var centerTimer;

        bedrooms.addEventListener('change', doFilter);

        circle.addListener('radius_changed', doFilter);
        circle.addListener('center_changed', function() {
            // Set a timer to prevent fetching while user is dragging
            clearTimeout(centerTimer);
            centerTimer = setTimeout(doFilter, 100);
        });
    }

    get(filter, circle) {
        let bounds = circle.getBounds().toJSON();
        Object.assign(bounds, {'radius': circle.getRadius(),
                               'center_lat': circle.getCenter().lat(),
                               'center_lng': circle.getCenter().lng(),
                               'coordtype': 'degrees'});
        Object.assign(bounds, filter);
        let data = EncodeQueryData(bounds);
        fetch('/get_apts?'+data, {
            method: 'GET',
            credentials: 'same-origin'
        }).then(function(response) {
            response.json().then(function(result) {
                this.collection.clear();
                this.collection.fill(result);
            }.bind(this));
        }.bind(this));
    }
}


class ListView {
    constructor(collection) {
        this.collection = collection;
        this.collection.subscribe('added', this.onAdded.bind(this));
        this.collection.subscribe('removed', this.onRemoved.bind(this));
        this.collection.subscribe('reloaded', this.onReloaded.bind(this));
        // Store the last sort key and order
        this.sortInfo = {'key': 'price', 'reverse': false};
    }

    onAdded(event, listing) {
        this.add(listing);
    }

    onRemoved(event, listing) {
        let listingsel = document.getElementById('listings'); // TODO: make obj attr
        let child = document.getElementById('listing-'+listing['id']);
        listingsel.removeChild(child);
    }

    onReloaded(event, listings) {
        // Called after collection is reloaded (all listings replaced)
        // Make sure previous sort order persists after update
        this.sortInfo.reverse = !this.sortInfo.reverse;
        this.sort(this.sortInfo.key);
    }

    add(listing) {
        let el = Stamp.expand(ctx.import('ltempl'), listing);
        Stamp.appendChildren(document.getElementById('listings'), el);
    }

    clear() {
        let listingsEl = document.getElementById('listings');
        let children = Array.from(listingsEl.children);
        children.forEach(function(child) {
            listingsEl.removeChild(child);
        });
    }

    fill(listings) {
        // Fill with a list of listings
        listings.forEach(function(listing) {
            this.add(listing);
        }.bind(this));
    }

    sort(key) {
        let sorted = [];
        for (var k in this.collection.listings) {
            sorted[sorted.length] = this.collection.listings[k];
        };
        if (this.sortInfo.key === key) {
            this.sortInfo.reverse = !this.sortInfo.reverse;
        } else {
            this.sortInfo.key = key;
            this.sortInfo.reverse = false;
        };
        sortByKey(sorted, this.sortInfo.key, this.sortInfo.reverse);
        this.clear();
        this.fill(sorted);
    }
}


class MapView {
    constructor(collection, map) {
        this.map = map;
        this.markers = {};
        this.collection = collection;
        this.collection.subscribe('added', this.onAdded.bind(this));
        this.collection.subscribe('removed', this.onRemoved.bind(this));
    }

    onAdded(event, listing) {
        if (listing['id'] in this.markers) {
            this.markers[listing['id']].setMap(null);
        };
        let p = new google.maps.LatLng(listing['lat_deg'], listing['lng_deg']);
        let marker = new google.maps.Marker({
            position: p,
            title: this['title']});
        marker.setMap(this.map);
        this.markers[listing['id']] = marker;
    }

    onRemoved(event, listing) {
        let marker = this.markers[listing['id']];
        if (marker) {
            marker.setMap(null);
        }
        delete this.markers[listing['id']];
    }
}


var lcol = new ListingCollection();
var listview = new ListView(lcol);
var map;
var mapview;
var filter;


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 43.660064, lng: -79.568268},
        zoom: 12
    });
    filter_circle = new google.maps.Circle({
        strokeColor: '#4dff4d',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#4dff4d',
        strokeOpacity: 0.1,
        map: this.map,
        center: this.map.getCenter(),
        radius: 3000,
        editable: true,
        draggable: true
    });
    mapview = new MapView(lcol, map);
    filter = new Filter(lcol, filter_circle, document.getElementById('filter_bedrooms'));
 }
