/* This is the boiler plate code for file uploads
// auto run this when the file is loaded
  (() => {
    document
      .getElementById("fileUpload")
      .addEventListener("change", handleReadFile);
    // set a default event listener that does nothing
    document
      .getElementById("fileUploadSubmit")
      .addEventListener("click", (e) => e.preventDefault());
  })();
*/

function handleReadFile(event) {
  const file = this.files[0]; // get the first file object
  const button = document.getElementById("fileUploadSubmit");
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
  // TODO experiment with compression
  var form = new FormData();
  let url = "/api/upload";
  form.append("file", file);
  // var search = new URLSearchParams({
  //   filename: file.name,
  //   type: "<fill this in>",
  // });
  // console.log(search);
  return fetch(url, {
    method: "POST",
    body: form,
  })
    .then((resp) => resp.json())
    .catch((err) => {
      console.log("Caught Fetch Error: ", err);
    });
}
