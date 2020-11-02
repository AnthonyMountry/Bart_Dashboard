const BASE_URL = "http://127.0.0.1:5000";

function handleReadFile() {
  const file = this.files[0]; // get the first file object
  const button = document.getElementById("fileUploadSubmit");
  const handleUpload = (e) => {
    e.preventDefault(); // prevent redirect
    var t0 = performance.now();
    upload(file); // upload the data
    e.preventDefault(); // prevent redirect
    document.getElementById("fileUpload").value = null; // clear the filename
    button.removeEventListener("click", handleUpload); // remove the event listener
    console.log(`uploaded '${file.name}' after ${performance.now() - t0}ms`);
  };
  // add a callback to the "submit" button
  button.addEventListener("click", handleUpload);
}

function upload(file) {
  // TODO experiment with compression
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
