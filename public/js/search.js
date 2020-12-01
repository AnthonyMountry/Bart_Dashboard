function removeElement(elementId) {
    // Removes an element from the document
    return document.getElementById(elementId).remove();
}

function searchMPU() { 
    if(!!document.getElementById('data')){
        removeElement("data");
        removeElement("tableHeading")
    }

    var Table = document.getElementById("readings-table");
    Table.innerHTML = "";

    let input = document.getElementById('searchbar').value 
    input=input.toLowerCase(); 

    const retrieveData = async (input) => {
        const response = await fetch('http://127.0.0.1:5000/api/mpu/'+input); //calling MPU api with provided id to get the data
        const myJson = await response.json(); //extract JSON from the http response
        return myJson
        }

    let resultJson = retrieveData(input)

    const div = document.createElement('div')
    div.id = "data"
    div.innerHTML = `<div class="data-view"><div class="mpu-id"><p><b>MPU ID: </b></p><p id="id"></p></div>
    <div class="mpu-name"><p><b>MPU NAME: </b></p><p id="name"></p></div> 
    <div class="mpu-ranking"><p><b>MPU RANKING: </b></p><p id="ranking"></p></div></div>`

    let dataElement = document.getElementById('data-display').appendChild(div); 
    
    let dataElement1 = document.getElementById('id'); 
    let dataElement2 = document.getElementById('name'); 
    let dataElement3 = document.getElementById('ranking'); 

    // FOR TESTING
    resultJson = {
        "id": "01SX001",
        "name": "Wheel Truing Machine",
        "ranking": 12,
        }

    dataElement1.innerHTML = resultJson['id']
    dataElement2.innerHTML = resultJson['name']
    dataElement3.innerHTML = resultJson['ranking']
} 

// FUNCTION TO PERFORM SEARCH USING INPUT IN SEARCH BAR FOR ASSET
function searchAssets() { 
    if(!!document.getElementById('data')){
        removeElement("data");
    }
    if(!!document.getElementById("tableHeading")){
        removeElement("tableHeading");
    }
    let input = document.getElementById('searchbar').value 
    input=input.toLowerCase(); 

    const retrieveData = async (input) => {
        const response = await fetch('http://127.0.0.1:5000/api/asset/'+input+'/readings'); //calling MPU api with provided id to get the data
        const myJson = await response.json(); //extract JSON from the http response
        return myJson
    }

    let resultJson = retrieveData(input)

    const div = document.createElement('div');
    div.id = "data"
    div.innerHTML = `<div class="asset-data-view"><div class="asset-num"><p>Asset NUM: </p> <p id="num"></p></div>
    <div class="asset-bartdept"><p> BART DEPT: </p><p id="bartdept"></p></div> 
    <div class="asset-descrip"><p>DESCRIPTION: </p><p id="description"></p></div>
    <div class="asset-status"><p>STATUS: </p> <p id="status"></p></div></div>`

    const tableHeading = document.createElement('h2');
    tableHeading.id = "tableHeading";
    tableHeading.innerHTML = "ASSET READINGS";
    let dataElement = document.getElementById('data-display') 
    dataElement.appendChild(div);
    dataElement.appendChild(tableHeading);

    let dataElement1 = document.getElementById('num'); 
    let dataElement2 = document.getElementById('bartdept'); 
    let dataElement3 = document.getElementById('description'); 
    let dataElement4 = document.getElementById('status'); 

    // FOR TESTING
    resultJson = {
        "bartdept": "AFC",
        "description": "COIN HANDLING",
        "num": 123456,
        "status": "OPERATING",
        "meter_readings": [
            {"reading": 10000001, "readingdate": "Thu, 16 Mar 2017 00:00:00 GMT"},
            {"reading": 10000002, "readingdate": "Fri, 17 Mar 2017 00:00:00 GMT"}
        ]
    }

    dataElement1.innerHTML = resultJson['num']
    dataElement2.innerHTML = resultJson['bartdept']
    dataElement3.innerHTML = resultJson['description']
    dataElement4.innerHTML = resultJson['status']

    var Table = document.getElementById("readings-table");
    Table.innerHTML = "";

    createAssetTable(resultJson["meter_readings"])
} 

// TO CREATE A ASSET READING TABLE AND POPULATING IT WITH DATA USING THE RESPONSE JSON.
function createAssetTable(data) {

    let table_data = data;

    let thead = document.querySelector("table").createTHead();
    thead.style.textAlign="left";
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