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
    listAssets({ limit: lim, offset: this.assets.length })
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
