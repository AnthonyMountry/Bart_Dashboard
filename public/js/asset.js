const encode = encodeURIComponent; // bc i dont want to write the whole thing every time

async function listAssets(params) {
  let query = new URLSearchParams(params);
  return await fetch(`/api/assets?${query}`)
    .then((resp) => resp.json())
    .then((json) => json["assets"].map((raw) => new Asset(raw)));
}

class Asset {
  constructor(data) {
    if (typeof data === "number") {
      this.assetnum = data;
      fetch(BASE_URL + `/api/asset/${this.assetnum}`)
        .then((resp) => resp.json())
        .then((json) => {
          if (json.num != assetnum) {
            console.log("Error: backend returned the wrong asset number");
          }
          this.bartdept = json.bartdept;
          this.description = json.description;
          this.status = json.status;
        });
    } else {
      this.bartdept = data.bartdept;
      this.assetnum = data.num;
      this.description = data.description;
      this.status = data.status;
    }
  }

  getReadings() {
    //This should fetch data and display the result
    //https://www.geeksforgeeks.org/get-and-post-method-using-fetch-api/?ref=rp
    const url = "/api/asset/15384437/readings"; // NOTE: i think this works too
    fetch("http://127.0.0.1:5000/api/asset/15384437/readings")
      // Converting received data to JSON
      .then((response) => response.json())
      .then((json) => {
        // Create a variable to store HTML
        let li = `<tr><th>date</th><th>reading</th></tr>`;
        // Loop through each data and add a table row
        json.meter_readings.forEach((asset) => {
          //unsure if correct
          li += `<tr>
                <td>${asset.date} </td>
                <td>${asset.reading}</td>
            </tr>`;
        });

        // Display result
        document.getElementById("readingsList").innerHTML = li;
      });
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
    this.fetchTable();
  }
  toggle() {
    if (this.visable) {
      this.table.innerHTML = "";
    } else {
      this.fetchTable();
    }
    this.visable = !this.visable;
  }

  fetchTable() {
    // if there are assets in the cache then use them
    this.table.innerHTML += `<tr>
      <th>Asset</th>
      <th>Department</th>
      <th>Status</th>
    </tr>`;
    if (this.assets.length != 0) {
      this.showAssets(this.assets);
      return;
    }
    listAssets({ limit: 10, offset: 0 })
      .then((assets) => {
        this.assets = assets; // cache the result
        this.showAssets(assets);
      })
      .catch((error) => {
        console.log(error);
        this.table.innerHTML = `
                      <p class="errorMsg"><span style="color:red;">Error</span>: Could not get assets</p>`;
      });
  }

  showAssets(assets) {
    for (let i = 0; i < assets.length; i++) {
      let asset = assets[i];
      this.table.innerHTML += `<tr>
        <td><a href="/api/asset/${asset.assetnum}/readings">${asset.assetnum}</a></td>
        <td>${asset.bartdept}</td>
        <td>${asset.status}</td>
      </tr>`;
    }
    if (this.assets.length >= this.limit) {
      return;
    }
    const id = "showMoreAssets";
    this.table.innerHTML += `<button id="${id}">show more...</button>`;
    const more = document.getElementById(id);
    const callback = (event) => {
      listAssets({ limit: 10, offset: this.assets.length }).then((assets) => {
        more.removeEventListener("click", callback); // remove itself
        this.table.removeChild(more);
        this.assets = this.assets.concat(assets);
        this.showAssets(assets); // render new and add the more button
      });
    };
    // add the click handler
    more.addEventListener("click", callback);
  }
}
