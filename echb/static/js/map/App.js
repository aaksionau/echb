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
    this.helper = new Helper();
  }
  showRegions() {
    document.getElementById("regions").innerHTML = tmpl(
      "regions-list",
      this.regions
    );
    $("#regions").on("click", "li a", function(e) {
      $(".aside__menu-link").removeClass("aside__menu-link--active");
      $(this).addClass("aside__menu-link--active");
      return false;
    });
    $("#regions").on("click", "li a", () => {
      const region = document.getElementsByClassName(
        "aside__menu-link--active"
      );
      const regionId = region[0].dataset.region;
      //if there is a google routes on the map - clear it
      this.gMap.resetDirections();
      this.gMap.filterGpointsByRegion(regionId);
      return false;
    });
  }
  initializeClosestChurches() {
    $("#get_closest_churches").on("click", () => {
      this.showclosestChurches();
      return false;
    });
    $("#closest-churches-list").on("click", "li a", function(el) {
      $(this)
        .parent()
        .children(".church__closest-list")
        .toggleClass("church__closest-list--none");
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
          if (position) {
            this.setUserPosition(position);
            this.filterGpointsByChurchIds();
            this.showListOfChurches();
            this.gMap.addUserGpoint(this.userPosition);
          }
        },
        function() {
          this.helper.showMessage("Невозможно определить ваше положение.");
        }
      );
    } else {
      // Browser doesn't support Geolocation
      this.helper.showMessage(
        "Ваш браузер не поддерживает функцию Геолокации."
      );
    }
  }
  addDistanceFromUserPosition() {
    this.churches.forEach(church => {
      church.distanceFromUser = this.helper.calculateDistance(
        church,
        this.userPosition
      );
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
