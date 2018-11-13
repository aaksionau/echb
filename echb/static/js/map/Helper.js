class Helper {
  constructor() {
    this.userPosition = {};
  }
  getUserCoordinates() {
    // Try HTML5 geolocation.
    let userPosition = {};
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.success, function() {
        showMessage("Невозможно определить ваше положение.");
      });
      console.log(`outside: ${userPosition}`);
    } else {
      // Browser doesn't support Geolocation
      showMessage("Ваш браузер не поддерживает функцию Геолокации.");
    }
  }
  success(pos) {
    var crd = pos.coords;

    console.log("Your current position is:");
    console.log(`Latitude : ${crd.latitude}`);
    console.log(`Longitude: ${crd.longitude}`);
    console.log(`More or less ${crd.accuracy} meters.`);
  }
  showMessage(message) {
    $("#messages").innerHTML = message;
  }
}
