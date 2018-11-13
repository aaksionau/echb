class App {
  constructor(regions, churches, gMap, helper) {
    this.regions = regions;
    this.churches = churches;
    this.gMap = gMap;
    this.helper = helper;

    this.closestChurchesCount = 6;

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
      this.gMap.filterChurches(this.filterByRegion);
      return false;
    });
  }
  initializeClosestChurches() {
    $("#closestChurches").on("click", () => {
      this.helper.getUserCoordinates();
      if (this.helper.userPosition) {
        this.gMap.filterChurches(this.filterByUserPosition);
      }
    });
  }
  filterByRegion(gmarker) {
    const region = document.getElementsByClassName(
      "regions-list__link--active"
    );
    const regionId = region[0].dataset.region;
    if (regionId != 0) {
      return gmarker.regionId == regionId;
    } else {
      return true;
    }
  }
  addDistanceFromUserPosition(userPosition) {
    var R = 6371; // radius of earth in km

    this.churches.forEach(church => {
      var dLat = rad(mlat - userPosition.lat);
      var dLong = rad(mlng - userPosition.lng);
      var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.getRadian(userPosition.lat)) *
          Math.cos(this.getRadian(userPosition.lat)) *
          Math.sin(dLong / 2) *
          Math.sin(dLong / 2);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      church.distanceFromUser = R * c;
    });
  }
  filterByUserPosition(gmarker) {
    if (this.userPosition) {
      this.addDistanceFromUserPosition(userPosition);
      let sortedByDistanceChurches = this.getClosestChurches();
      sortedByDistanceChurches.forEach(church => {
        if (gmarker.churchId == church.pk) {
          return true;
        } else {
          return false;
        }
      });
    }
  }
  getClosestChurches() {
    this.churches.sort(
      (church1, church2) => church1.distance - church2.distance
    );
    return churches.slice(0, this.closestChurchesCount);
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
