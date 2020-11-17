async function listAssets(limit) {
  let url;
  if (limit === null) {
    url = BASE_URL + "/api/assets";
  } else {
    url = BASE_URL + `/api/assets?limit=${limit}`;
  }
  return await fetch(url)
    .then((resp) => resp.json())
    .then((json) => json.assets.map((raw) => new Asset(raw)));
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
