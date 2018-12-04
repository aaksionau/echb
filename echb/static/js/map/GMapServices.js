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
  filterGpointsByChurchIds(churchIds) {
    var bounds = new google.maps.LatLngBounds();
    this.map.gmarkers.forEach(gmarker => {
      if (churchIds.indexOf(gmarker.churchId) > -1) {
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
  filterGpointsByRegion(regionId) {
    var bounds = new google.maps.LatLngBounds();
    this.map.gmarkers.forEach(gmarker => {
      let filter = regionId != 0 ? gmarker.regionId == regionId : true;

      if (filter) {
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
  addUserGpoint(userPosition) {
    const userGpoint = new google.maps.Marker({
      position: new google.maps.LatLng(
        userPosition.latitude,
        userPosition.longitude
      ),
      map: this.map,
      regionId: 0,
      churchId: 0,
      icon: "/static/img/location.png"
    });
    this.map.gmarkers.push(userGpoint);
  }
  resetDirections() {
    this.directionsDisplay.setMap(null);
  }
  calculateRoute(churchCoordinates, userCoordinates) {
    const start = new google.maps.LatLng(
      userCoordinates.latitude,
      userCoordinates.longitude
    );
    const end = new google.maps.LatLng(
      churchCoordinates.lat,
      churchCoordinates.lng
    );
    let bounds = new google.maps.LatLngBounds();
    bounds.extend(start);
    bounds.extend(end);
    this.map.fitBounds(bounds);
    const request = {
      origin: start,
      destination: end,
      travelMode: google.maps.TravelMode.DRIVING
    };
    this.directionsService.route(request, (response, status) => {
      if (status == google.maps.DirectionsStatus.OK) {
        this.directionsDisplay.setDirections(response);
        this.directionsDisplay.setMap(this.map);
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
