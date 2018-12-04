class Helper {
  getRadian(x) {
    return (x * Math.PI) / 180;
  }
  calculateDistance(church, userPosition) {
    var R = 6371; // radius of earth in km
    var dLat = this.getRadian(church.fields.lat - userPosition.latitude);
    var dLong = this.getRadian(church.fields.lng - userPosition.longitude);
    var a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.getRadian(userPosition.latitude)) *
        Math.cos(this.getRadian(userPosition.latitude)) *
        Math.sin(dLong / 2) *
        Math.sin(dLong / 2);
    var distance = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * distance);
  }
  showMessage(message) {
    $("#messages").innerHTML = message;
  }
}
