var echbNS = echbNS || {};
echbNS.ChurchOnMap = {
    init: function (id, distance, position, churchId) {
        this.id = id;
        this.distance = distance;
        this.position = position;
        this.churchId = churchId;
    }
};
echbNS.Core = function (google) {
    var map, infoWindow, directionsService, directionsDisplay;
    var gmarkers = [];
    var userPosition = null;
    var closestChurches = [];

    var getUserCoordinates = function () {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                userPosition = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
            }, function () {
                console.log('Невозможно определить ваше положение.');
            });
        } else {
            // Browser doesn't support Geolocation
            console.log('Невозможно определить ваше положение.');
        }
    };

    function rad(x) {
        return x * Math.PI / 180;
    }
    var getClosestChurches = function (churchesQuantity) {
        var R = 6371; // radius of earth in km
        var churches = [];
        var closest = -1;

        //to exclude user position marker
        filtered_markers = map.markers.filter(marker => marker.church_id != undefined);

        for (i = 0; i < filtered_markers.length; i++) {
            var mlat = filtered_markers[i].position.lat();
            var mlng = filtered_markers[i].position.lng();
            var dLat = rad(mlat - userPosition.lat);
            var dLong = rad(mlng - userPosition.lng);
            var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(rad(userPosition.lat)) * Math.cos(rad(userPosition.lat)) * Math.sin(dLong / 2) * Math.sin(dLong / 2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            var d = R * c;
            let church = Object.create(echbNS.ChurchOnMap)
            church.init(i, d, filtered_markers[i].position, filtered_markers[i].church_id);
            churches.push(church);
        }
        churches.sort((church1, church2) => church1.distance - church2.distance);
        closestChurches = churches.slice(0, churchesQuantity);
        return closestChurches;
    };

    var calculateRoute = function (lat, lng) {
        var start = new google.maps.LatLng(userPosition.lat, userPosition.lng);
        var end = new google.maps.LatLng(lat, lng);
        var bounds = new google.maps.LatLngBounds();
        bounds.extend(start);
        bounds.extend(end);
        map.fitBounds(bounds);
        var request = {
            origin: start,
            destination: end,
            travelMode: google.maps.TravelMode.DRIVING
        };
        directionsService.route(request, function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
                directionsDisplay.setMap(map);
            } else {
                console.log("Directions Request from " + start.toUrlValue(6) + " to " + end.toUrlValue(6) + " failed: " + status);
            }
        });
    };

    //HELPERS
    //Google map pointer filters
    var filterByRegion = function (gmarker, options) {
        church = churches.filter(church => church.pk == gmarker.church_id)[0].fields;
        //options contain one int value Region, for example 10
        return church.region == options || options == 0;
    };

    var filterByClosestChurches = function (gmarker, options) {
        return closestChurches.filter(church => church.position == gmarker.position).length > 0;
    };

    var filterMarkers = function (filter, options) {
        var bounds = new google.maps.LatLngBounds();
        gmarkers.forEach(gmarker => {
            if (filter(gmarker, options)) {
                let pt = new google.maps.LatLng(gmarker.position.lat(), gmarker.position.lng());
                bounds.extend(pt);
                gmarker.setVisible(true);
            } else {
                gmarker.setVisible(false);
            }
        });
        map.fitBounds(bounds);
    };

    var addRegionNameToChurch = function addRegionNameToChurch() {
        churches.forEach(church => {
            let churchFields = church.fields;
            regions.forEach(region => {
                if (churchFields.region == region.pk) {
                    churchFields.region_name = region.fields.name;
                }
            });
        });
    };

    var addChurchMarkersToMap = function () {
        churches.forEach(church => {
            churchInfo = church.fields;
            gmarker = new google.maps.Marker({
                position: new google.maps.LatLng(churchInfo.lat, churchInfo.lng),
                map: map,
                church_id: church.pk,
                icon: '/static/img/church-gmap.png'
            });
            gmarkers.push(gmarker);

            google.maps.event.addListener(gmarker, 'click', (function (churchInfo, gmarker) {
                var content = tmpl("church-info-gmap", churchInfo);
                return function () {
                    infoWindow.setContent(content);
                    infoWindow.open(map, gmarker);
                };
            })(churchInfo, gmarker));
        });
        map.markers = gmarkers;
    };

    var addUserPositionToMap = function () {
        var gmarker = new google.maps.Marker({
            position: new google.maps.LatLng(userPosition.lat, userPosition.lng),
            map: map,
            person_location: true,
            icon: '/static/img/location.png'
        });
        map.markers.push(gmarker);
    };

    var initializeMap = function (lat, lng, zoom, divId) {
        directionsService = new google.maps.DirectionsService();
        directionsDisplay = new google.maps.DirectionsRenderer();
        infoWindow = new google.maps.InfoWindow();
        getUserCoordinates();

        map = new google.maps.Map(document.getElementById(divId), {
            center: {
                lat: lat,
                lng: lng
            },
            zoom: zoom
        });
    };

    return {
        addChurchMarkersToMap,
        filterMarkers,
        filterByRegion,
        filterByClosestChurches,
        calculateRoute,
        addUserPositionToMap,
        getClosestChurches,
        initializeMap
    };
};