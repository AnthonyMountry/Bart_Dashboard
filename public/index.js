// auto run this when the file is loaded
(() => {
  document
    .getElementById("fileUpload")
    .addEventListener("change", readFile, false);
})();

function readFile() {
  const file = this.files[0]; // get the first file object
  const reader = new FileReader();
  var bytes_read = 0; // here for tracking progress
  reader.readAsText(file, "utf-8");

  // onload is triggered when the file
  // is finished being read
  reader.onload = (e) => {
    console.log("reader.onload", e);
    console.log("data:", e.target.result);
    // TODO 1. put data in the ready state
    //      2. upload the data when submit is pressed
  };
  reader.onerror = (e) => {
    console.log("Error:", e);
    // TODO display error on page
  };
  reader.onprogress = (e) => {
    bytes_read += e.total;
    console.log("read", bytes_read, "bytes");
    // TODO loading bar
  };
}

function upload(url, data) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": contentTypes["xlsx"],
    },
    body: data,
  }).then((resp) => resp.json());
}

const contentTypes = {
  xls: "application/vnd.ms-excel",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  csv: "text/csv",
};
