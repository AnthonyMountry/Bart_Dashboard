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

class AssetTable {
  constructor(tableID, limit) {
    if (limit === undefined) {
      this.limit = 20;
    } else {
      this.limit = limit;
    }
    this.table = document.getElementById(tableID);
    this.visable = false;
    this.assets = [];
  }

  render() {
    this.visable = true;
    this.fetchTable(10);
  }

  toggle() {
    if (this.visable) {
      this.table.innerHTML = "";
    } else {
      this.fetchTable();
    }
    this.visable = !this.visable;
  }

  fetchTable(lim) {
    if (lim === undefined) {
      lim = 10;
    }
    // if there are assets in the cache then use them
    this.table.innerHTML = `<thead><tr>
      <th>Asset</th>
      <th>Department</th>
      <th>Status</th>
      <th>Description</th>
    </thead></tr>`;
    if (this.assets.length != 0) {
      this.showAssets(this.assets);
      return;
    }
    listAssets({ limit: lim, offset: 0 })
      .then((assets) => {
        this.assets = assets; // cache the result
        this.showAssets(assets);
      })
      .catch((error) => {
        console.log(error);
        this.table.innerHTML = `<p class="errorMsg">
          <span style="color:red;">Error</span>: Could not get assets
        </p>`;
      });
  }

  showAssets(assets) {
    this.table.innerHTML += "<tbody>";
    for (let i = 0; i < assets.length; i++) {
      let asset = assets[i];
      this.table.innerHTML += `<tr>
        <td scope="row"><a href="/asset?assetnum=${asset.num}">${asset.num}</a></td>
        <td>${asset.bartdept}</td>
        <td>${asset.status}</td>
        <td>${asset.description}</td>
      </tr>`;
    }
    this.table.innerHTML += "</tbody>";
    // limit of -1 == no limit
    if (this.limit > 0 && this.assets.length >= this.limit) {
      return;
    }
    const moreid = "showMoreAssets";
    // const lessid = "showLessAssets";
    this.table.innerHTML += `<button id="${moreid}">show more</button>`;
    // this.table.innerHTML += `<button id="${lessid}">show less</button>`;
    const more = document.getElementById(moreid);
    // const less = document.getElementById(lessid);

    const callback = (event) => {
      more.removeEventListener("click", callback); // remove itself
      this.table.removeChild(more);
      // this.table.removeChild(less);
      listAssets({ limit: 10, offset: this.assets.length }).then((assets) => {
        this.assets = this.assets.concat(assets);
        this.showAssets(assets); // render new and add the more button
      });
    };
    // add the click handler
    more.addEventListener("click", callback);
  }
}
