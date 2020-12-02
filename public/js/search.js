function search(input) {
  let type = document.getElementById("search-record-type").value;
  if (input === undefined || input === null) {
    input = document.getElementById("searchbar").value;
  }
  if (type === "asset") {
    searchAssets(input);
  } else if (type === "mpu") {
    searchMPU();
  }
}

function removeElement(elementId) {
  // Removes an element from the document
  return document.getElementById(elementId).remove();
}

function searchMPU() {
  if (!!document.getElementById("data")) {
    removeElement("data");
    removeElement("tableHeading");
  }

  var Table = document.getElementById("readings-table");
  Table.innerHTML = "";

  let input = document.getElementById("searchbar").value;
  input = input.toLowerCase();

  const retrieveData = async (input) => {
    const response = await fetch("http://127.0.0.1:5000/api/mpu/" + input); //calling MPU api with provided id to get the data
    const myJson = await response.json(); //extract JSON from the http response
    return myJson;
  };

  let resultJson = retrieveData(input);

  const div = document.createElement("div");
  div.id = "data";
  div.innerHTML = `
    <div class="mpu-data-view">
        <div class="mpu-id"><p><b>MPU ID: </b></p><p id="id"></p>
        </div>
        <div class="mpu-name"><p><b>MPU NAME: </b></p><p id="name"></p></div>
        <div class="mpu-ranking"><p><b>MPU RANKING: </b></p><p id="ranking"></p></div>
    </div>`;

  let dataElement = document.getElementById("data-display").appendChild(div);

  let dataElement1 = document.getElementById("id");
  let dataElement2 = document.getElementById("name");
  let dataElement3 = document.getElementById("ranking");

  // FOR TESTING
  resultJson = {
    id: "01SX001",
    name: "Wheel Truing Machine",
    ranking: 12,
  };

  dataElement1.innerHTML = resultJson["id"];
  dataElement2.innerHTML = resultJson["name"];
  dataElement3.innerHTML = resultJson["ranking"];
}

// FUNCTION TO PERFORM SEARCH USING INPUT IN SEARCH BAR FOR ASSET
function searchAssets(input) {
  //   if (!!document.getElementById("data")) {
  //     removeElement("data");
  //   }
  //   if (!!document.getElementById("tableHeading")) {
  //     removeElement("tableHeading");
  //   }

  let dataElement = document.getElementById("data-display");
  if (!input) {
    dataElement.innerHTML = `No search term`;
    return;
  }
  // fetch the search api
  listAssets({ limit: 10, search: input })
    .then((assets) => {
      if (assets.length === 0) {
        dataElement.innerHTML = `Could not find \"${input}\"`;
        return;
      } else {
        dataElement.innerHTML = "";
      }

      let div;
      for (i in assets) {
        let asset = assets[i];
        if (i % 2 == 0) {
          div = document.createElement("div");
          div.classList.add("row");
        }
        const search_box = `
        <div class="asset-data-view col-sm">
            <div class="asset-num">
                <p>Asset: </p> <p id="num${i}"></p>
            </div>
            <div class="asset-bartdept">
                <p> BART DEPT: </p><p id="bartdept${i}"></p>
            </div>
            <div class="asset-descrip">
                <p>DESCRIPTION: </p><p id="description${i}"></p>
            </div>
            <div class="asset-status">
                <p>STATUS: </p> <p id="status${i}"></p>
            </div>
        </div>`;
        div.innerHTML += search_box;
        dataElement.appendChild(div);

        let dataElement1 = document.getElementById("num" + i);
        let dataElement2 = document.getElementById("bartdept" + i);
        let dataElement3 = document.getElementById("description" + i);
        let dataElement4 = document.getElementById("status" + i);

        dataElement1.innerHTML = `<a href="/asset?assetnum=${asset["num"]}">${asset["num"]}</a>`;
        dataElement2.innerHTML = asset["bartdept"];
        dataElement3.innerHTML = asset["description"];
        dataElement4.innerHTML = asset["status"];
      }
    })
    .catch((error) => {
      console.log(error);
      // TODO render an error message
    });
  return;

  var Table = document.getElementById("readings-table");
  Table.innerHTML = "";
  //   createAssetTable(resultJson["meter_readings"]);
}

// TO CREATE A ASSET READING TABLE AND POPULATING IT WITH DATA USING THE RESPONSE JSON.
function createAssetTable(data) {
  let table_data = data;

  let thead = document.querySelector("table").createTHead();
  thead.style.textAlign = "left";
  let row = thead.insertRow();

  for (let key in table_data[0]) {
    let th = document.createElement("th");
    let text = document.createTextNode(key.toUpperCase());
    th.appendChild(text);
    row.appendChild(th);
  }

  for (let element of table_data) {
    let row = document.querySelector("table").insertRow();
    for (key in element) {
      let cell = row.insertCell();
      let text = document.createTextNode(element[key]);
      cell.appendChild(text);
    }
  }
}
