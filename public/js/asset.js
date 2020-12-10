async function listAssets(params) {
  let url;
  if (params === undefined) {
    url = "/api/assets";
  } else {
    let query = new URLSearchParams(params);
    url = `/api/assets?${query}`;
  }
  return await fetch(url)
    .then((resp) => resp.json())
    .then((json) => json["assets"].map((raw) => new Asset(raw)));
}

class Asset {
  constructor(data) {
    if (typeof data === "number") {
      this.num = data;
    } else {
      for (const attr in data) {
        this[attr] = data[attr];
      }
    }
  }

  async init() {
    return await fetch(`/api/asset/${this.num}`)
      .then((resp) => {
        if (resp.status != 200) {
          console.log("Could not find asset " + data);
          throw resp.json();
        }
        return resp.json();
      })
      .then((json) => {
        if (json.num != this.num) {
          console.log("Error: wrong asset number recvieved");
        }
        this.bartdept = json.bartdept;
        this.description = json.description;
        this.status = json.status;
        return this;
      })
      .catch((error) => console.log("got error:", error));
  }

  async readings(graph) {
    return await fetch(`/api/asset/${this.num}/readings`)
      .then((resp) => resp.json())
      .then((json) => {
        let readings = json.meter_readings;
        let fn = (r) => {
          return {
            date: new Date(r.readingdate),
            reading: r.reading,
            name: r.metername,
          };
        };
        if (graph) {
          fn = (r) => {
            return {
              x: new Date(r.readingdate),
              y: r.reading,
              name: r.metername,
            };
          };
        }
        return readings.map(fn);
      })
      .catch((err) => console.log("asset readings error:", err));
  }
}
