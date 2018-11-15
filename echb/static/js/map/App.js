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
      this.gMap.filterGpointsByRegion(regionId);
      return false;
    });
  }
  initializeClosestChurches() {
    $("#closestChurches").on("click", () => {
      //!!!TODO: make getting coordinates more clear
      this.getUserCoordinates();
      return false;
    });
  }
  setUserPosition(userPosition) {
    this.userPosition = userPosition.coords;
    if (this.userPosition) {
      this.addDistanceFromUserPosition(this.userPosition);
      let closestChurches = this.getClosestChurches();
      //Get closest churches id to filter on them later
      closestChurches = closestChurches.reduce((acc, church) => {
        acc.push(church.pk);
        return acc;
      }, []);
      this.gMap.filterGpointsByChurchIds(closestChurches);
    }
  }
  getUserCoordinates() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.setUserPosition(position);
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
      church.distanceFromUser = R * c;
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
