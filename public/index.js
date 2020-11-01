// auto run this when the file is loaded
(() => {
  document
    .getElementById("fileUpload")
    .addEventListener("change", readAndUpload, false);
  document
    .getElementById("fileUploadSubmit")
    .addEventListener("click", (e) => e.preventDefault());
})();

const BASE_URL = "http://127.0.0.1:5000";

function readAndUpload() {
  const file = this.files[0]; // get the first file object
  const button = document.getElementById("fileUploadSubmit");
  console.log(file);

  const handleUpload = (e) => {
    var t0 = performance.now();
    e.preventDefault(); // prevent redirect
    upload(file); // upload the data
    document.getElementById("fileUpload").value = null; // clear the filename
    button.removeEventListener("click", handleUpload); // remove the event listener
    console.log(`uploaded '${file.name}' after ${performance.now() - t0}ms`);
  };
  // add a callback to the "submit" button
  button.addEventListener("click", handleUpload);
}

function upload(file) {
  // TODO gzip data before sending
  var form = new FormData();
  var url = new URL(BASE_URL + "/api/upload");

  form.append("file", file);
  url.search = new URLSearchParams({
    filename: file.name,
    type: "<fill this in>",
  });

  return fetch(url, {
    method: "POST",
    body: form,
  })
    .then((resp) => resp.json())
    .catch((err) => {
      console.log("Caught Fetch Error: ", err);
    });
}

const contentTypes = {
  xls: "application/vnd.ms-excel",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  csv: "text/csv",
};
