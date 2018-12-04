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
