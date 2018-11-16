class App {
  constructor(regions, churches, gMap, closestChurchesQnty) {
    this.regions = regions;
    this.churches = churches;

    this.gMap = gMap;

    this.closestChurchesQnty = closestChurchesQnty;
    this.showRegions();
    this.showChurches();
    this.initializeClosestChurches();
    this.userPosition = {};
    this.closestChurches = [];
  }
  showRegions() {
    document.getElementById("regions").innerHTML = tmpl(
      "regions-list",
      this.regions
    );
    $("#regions").on("click", "li a", function(e) {
      $(".regions-list__link").removeClass("regions-list__link--active");
      $(this).addClass("regions-list__link--active");
      return false;
    });
    $("#regions").on("click", "li a", () => {
      const region = document.getElementsByClassName(
        "regions-list__link--active"
      );
      const regionId = region[0].dataset.region;
      this.gMap.resetDirections();
      this.gMap.filterGpointsByRegion(regionId);
      return false;
    });
  }
  initializeClosestChurches() {
    $("#get_closest_churches").on("click", () => {
      //!!!TODO: make getting coordinates more clear
      this.showclosestChurches();
      return false;
    });
    $("#closest-churches-list").on("click", "li a", function(el) {
      $(this)
        .parent()
        .children(".closest-churches-list__list")
        .toggleClass("closest-churches-list__list--none");
      return false;
    });
    $("#closest-churches-list").on(
      "click",
      "li .closest-churches-list__button",
      el => {
        let churchCoordinates = {
          lat: el.target.dataset.lat,
          lng: el.target.dataset.lng
        };
        this.gMap.calculateRoute(churchCoordinates, this.userPosition);
        return false;
      }
    );
  }
  filterGpointsByChurchIds() {
    this.addDistanceFromUserPosition(this.userPosition);
    this.closestChurches = this.getClosestChurches();
    //Get closest churches id to filter on them later
    let closestChurchIds = this.closestChurches.reduce((acc, church) => {
      acc.push(church.pk);
      return acc;
    }, []);
    this.gMap.filterGpointsByChurchIds(closestChurchIds);
  }
  showListOfChurches() {
    document.getElementById("closest-churches-list").innerHTML = tmpl(
      "church-info-search",
      this.closestChurches
    );
  }
  setUserPosition(userPosition) {
    this.userPosition = userPosition.coords;
  }
  showclosestChurches() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.setUserPosition(position);
          if (position) {
            this.filterGpointsByChurchIds();
            this.showListOfChurches();
            this.gMap.addUserGpoint(this.userPosition);
          }
        },
        function() {
          this.showMessage("Невозможно определить ваше положение.");
        }
      );
    } else {
      // Browser doesn't support Geolocation
      this.showMessage("Ваш браузер не поддерживает функцию Геолокации.");
    }
  }
  showMessage(message) {
    $("#messages").innerHTML = message;
  }
  getRadian(x) {
    return (x * Math.PI) / 180;
  }
  addDistanceFromUserPosition() {
    var R = 6371; // radius of earth in km

    this.churches.forEach(church => {
      var dLat = this.getRadian(church.fields.lat - this.userPosition.latitude);
      var dLong = this.getRadian(
        church.fields.lng - this.userPosition.longitude
      );
      var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.getRadian(this.userPosition.latitude)) *
          Math.cos(this.getRadian(this.userPosition.latitude)) *
          Math.sin(dLong / 2) *
          Math.sin(dLong / 2);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      church.distanceFromUser = Math.round(R * c);
    });
  }
  getClosestChurches() {
    this.churches.sort(
      (church1, church2) => church1.distanceFromUser - church2.distanceFromUser
    );
    return this.churches.slice(0, this.closestChurchesQnty);
  }
  showChurches() {
    const gmarkers = [];
    this.churches.forEach(church => {
      let gmarker = this.gMap.createGmapMarker(church);
      this.gMap.addChurchClickListener(church, gmarker);
      gmarkers.push(gmarker);
    });
    this.gMap.addMarkersToMap(gmarkers);
  }
}

class Data {
  constructor(regionsUrl, churchesUrl) {
    this.regionsUrl = regionsUrl;
    this.churchesUrl = churchesUrl;
    this.regionsData = [];
  }
  getPromise() {
    return new Promise((resolve, reject) => this.getRegions(resolve));
  }
  getRegions(resolve, reject) {
    fetch(this.regionsUrl)
      .then(response => response.json())
      .then(regions => this.getChurches(regions, resolve));
  }
  getChurches(regions, resolve) {
    this.regionsData = regions;
    fetch(this.churchesUrl)
      .then(response => response.json())
      .then(churches => {
        let data = this.addRegionNameToChurch(regions, churches);
        resolve(data);
      });
  }
  addRegionNameToChurch(regions, churches) {
    let data = {};
    data.regions = regions;
    data.churches = churches.map(church => {
      church.fields["region_name"] = this.getRegionNameById(
        church.fields.region
      );
      return church;
    });
    return data;
  }
  getRegionNameById(regionId) {
    return this.regionsData.filter(region => region.pk == regionId)[0].fields
      .name;
  }
}

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
