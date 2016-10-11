function circleRadiusChanged(circle) {
    console.log(circle.getRadius());
    console.log(<Listings />);
};

var _centerTimer = null;
function circleCenterChanged(circle) {
    clearTimeout(_centerTimer);
    _centerTimer = setTimeout(function() {
        console.log(circle.getCenter().lat(), circle.getCenter().lng());
    }, 80);
};


var circleCenterTimer = null;

class ParentMan extends React.Component {

    constructor(props) {
        super(props);
        this.state = {items: []};

    }

    componentDidMount() {
        this._circleCenterTimer = null;
    }

    render() {
        const childrenWithProps = React.Children.map(this.props.children,
                                                     (child) => React.cloneElement(child, {
                                                         circleRadiusChanged: this.circleRadiusChanged,
                                                         circleCenterChanged: this.circleCenterChanged,
                                                         items: this.state.items,
                                                         parent: this
                                                     }));
        return(
                <div>
                <div className="eight columns">
                {childrenWithProps[0]}
            </div>
                <div className="four columns">
                {childrenWithProps[1]}
            </div>
                </div>
        );
    }

    newListings(e) {
        console.log('hello');
    }

    componentWillUpdate(nextProps, nextState) {
        console.log('updating parent');
    }

    circleRadiusChanged(c, props) {
        var that = this;
        console.log('CIRCLE HAS CHANGED RADIUS');
        props.parent.loadData(c);
    }

    circleCenterChanged(c, props) {
        clearTimeout(circleCenterTimer);
        circleCenterTimer = setTimeout((t) => props.parent.loadData(c), 80);
    }

    loadData(circle) {
        var bounds = circle.getBounds().toJSON();
        Object.assign(bounds, {'radius': circle.getRadius(),
                               'center_lat': circle.getCenter().lat(),
                               'center_lng': circle.getCenter().lng(),
                               'coordtype': 'degrees'});
        var data = EncodeQueryData(bounds);

        fetch('/get_apts'+'?'+data, {
            method: 'GET',
            credentials: 'same-origin'})
            .then(response => response.json())
            .then(json => {
                this.setState({items: json});
            });
    }
}


class GMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {zoom: 14};

    }

    render() {
        return (<div className="GMap">
                <div className='GMap-canvas' ref="mapCanvas">
                </div>
                </div>);
    }

    componentDidMount() {
        this.map = this.createMap();
        this.circle = this.createCircle();
        this.markers = [];
        google.maps.event.addListener(this.map, 'zoom_changed', () => this.handleZoomChange());
        this.circle.addListener('radius_changed', (e) => this.props.circleRadiusChanged(this.circle, this.props));
        this.circle.addListener('center_changed', (e, p) => this.props.circleCenterChanged(this.circle, this.props));
    }

    componentDidUnMount() {
        google.maps.event.clearListeners(map, 'zoom_changed');
    }

    componentWillUpdate(nextProps, nextState) {
        console.log(nextProps);
        for (var i = 0; i < this.markers.length; i++) {
            this.markers[i].setMap(null);
        }
        this.markers = [];
        for (var i = 0; i < nextProps.items.length; i++) {
            var p = new google.maps.LatLng(
                nextProps.items[i]['latitude'],
                nextProps.items[i]['longitude']);

            this.markers.push(this.createMarker(p));
        };
    }

    createMap() {
        let mapOptions = {
            zoom: this.state.zoom,
            center: this.mapCenter()
        };
        return new google.maps.Map(this.refs.mapCanvas, mapOptions);
    }

    mapCenter() {
        return new google.maps.LatLng(
            43.660064,
            -79.568268
        );
    }

    createMarker(pos) {
        return new google.maps.Marker({
            position: pos,
            map: this.map
        });
    }

    createCircle() {
        return new google.maps.Circle({
            strokeColor: '#4dff4d',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#4dff4d',
            strokeOpacity: 0.1,
            map: this.map,
            center: this.map.getCenter(),
            radius: 1000,
            editable: true,
            draggable: true
        });
    }

    handleZoomChange() {
        this.setState({
            zoom: this.map.getZoom()
        });
    }
}



class Listings extends React.Component {

    constructor(props) {
        super(props);
        this.state = {items: []};

    }

    componentDidMount() {
        //console.log(this.props.children);
    }

    loadData(circle) {
        var bounds = circle.getBounds().toJSON();
        Object.assign(bounds, {'radius': circle.getRadius(),
                               'center_lat': circle.getCenter().lat(),
                               'center_lng': circle.getCenter().lng(),
                               'coordtype': 'degrees'});
        var data = EncodeQueryData(bounds);

        fetch('/get_apts'+'?'+data, {
            method: 'GET',
            credentials: 'same-origin'})
            .then(response => response.json())
            .then(json => {
                this.setState({items: json});
            });

    }

    render() {
        console.log('listings render');
        return (
                <ul className="listings-list">
                {this.props.items.map(item => (
                        <li key={item.id}>
                        <a className="hide-overflow" href={item.url}>
                        {item.title}
                    </a>
                        {item.price_currency} - {item.price}
                    </li>))}
            </ul>
        );
    }

    componentWillUpdate(nextProps, nextState) {
        console.log('updating listings ', nextProps);
        sortByKey(nextProps.items, 'price');
    }

};


var initialCenter = { lng: -90.1056957, lat: 29.9717272 };


ReactDOM.render(<ParentMan><GMap key='gmap'/><Listings key='listings' /></ParentMan>, document.getElementById('parent-container'));
