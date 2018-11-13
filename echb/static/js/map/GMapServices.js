class GMapServices {
  constructor(lat, lng, zoom, divId, google) {
    this.map = this.createMap(lat, lng, zoom, divId);
    this.map.gmarkers = [];
    this.directionsService = new google.maps.DirectionsService();
    this.directionsDisplay = new google.maps.DirectionsRenderer();
    this.infoWindow = new google.maps.InfoWindow();
  }
  createMap(lat, lng, zoom, divId) {
    return new google.maps.Map(document.getElementById(divId), {
      center: {
        lat: lat,
        lng: lng
      },
      zoom: zoom
    });
  }
  addChurchClickListener(church, gmarker) {
    google.maps.event.addListener(
      gmarker,
      "click",
      (function(church, gmarker, infoWindow) {
        const popupContent = tmpl("church-info-gmap", church.fields);
        return function() {
          infoWindow.setContent(popupContent);
          infoWindow.open(this.map, gmarker);
        };
      })(church, gmarker, this.infoWindow)
    );
  }
  createGmapMarker(church) {
    return new google.maps.Marker({
      position: new google.maps.LatLng(church.fields.lat, church.fields.lng),
      map: this.map,
      regionId: church.fields.region, //for filtering markers by regionId
      churchId: church.pk, //for filtering markers by Array of closest to user churches
      icon: "/static/img/church-gmap.png"
    });
  }
  filterChurches(filter) {
    var bounds = new google.maps.LatLngBounds();
    this.map.gmarkers.forEach(gmarker => {
      if (filter(gmarker)) {
        let pt = new google.maps.LatLng(
          gmarker.position.lat(),
          gmarker.position.lng()
        );
        bounds.extend(pt);
        gmarker.setVisible(true);
      } else {
        gmarker.setVisible(false);
      }
    });
    this.map.fitBounds(bounds);
  }
  getRadian(x) {
    return (x * Math.PI) / 180;
  }
  calculateRoute(lat, lng) {
    const start = new google.maps.LatLng(userPosition.lat, userPosition.lng);
    const end = new google.maps.LatLng(lat, lng);
    let bounds = new google.maps.LatLngBounds();
    bounds.extend(start);
    bounds.extend(end);
    map.fitBounds(bounds);
    const request = {
      origin: start,
      destination: end,
      travelMode: google.maps.TravelMode.DRIVING
    };
    this.directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
        directionsDisplay.setMap(map);
      } else {
        console.log(
          "Directions Request from " +
            start.toUrlValue(6) +
            " to " +
            end.toUrlValue(6) +
            " failed: " +
            status
        );
      }
    });
  }
  addMarkersToMap(gmarkers) {
    this.map.gmarkers = gmarkers;
  }
}
