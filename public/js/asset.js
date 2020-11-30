const encode = encodeURIComponent; // bc i dont want to write the whole thing every time

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
      this.assetnum = data;
    } else {
      this.bartdept = data.bartdept;
      this.assetnum = data.num;
      this.status = data.status;
      this.description = data.description;
    }
  }

  init() {
    fetch(`/api/asset/${this.assetnum}`)
      .then((resp) => {
        if (resp.status != 200) {
          console.log("Could not find asset " + data);
          throw resp.json();
        }
        return resp.json();
      })
      .then((json) => {
        if (json.num != this.assetnum) {
          console.log("Error: wrong asset number recvieved");
        }
        this.bartdept = json.bartdept;
        this.description = json.description;
        this.status = json.status;
      })
      .catch((error) => console.log("got error:", error));
  }

  async readings(graph) {
    return await fetch(`/api/asset/${this.assetnum}/readings`)
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
    this.table.innerHTML = `<tr>
      <th>Asset</th>
      <th>Department</th>
      <th>Status</th>
    </tr>`;
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
    for (let i = 0; i < assets.length; i++) {
      let asset = assets[i];
      this.table.innerHTML += `<tr>
        <td><a href="/asset?assetnum=${asset.assetnum}">${asset.assetnum}</a></td>
        <td>${asset.bartdept}</td>
        <td>${asset.status}</td>
      </tr>`;
    }
    // limit of -1 == no limit
    if (this.limit > 0 && this.assets.length >= this.limit) {
      return;
    }
    const id = "showMoreAssets";
    this.table.innerHTML += `<button id="${id}">show more...</button>`;
    const more = document.getElementById(id);

    const callback = (event) => {
      more.removeEventListener("click", callback); // remove itself
      this.table.removeChild(more);
      listAssets({ limit: 10, offset: this.assets.length }).then((assets) => {
        this.assets = this.assets.concat(assets);
        this.showAssets(assets); // render new and add the more button
      });
    };
    // add the click handler
    more.addEventListener("click", callback);
  }
}
