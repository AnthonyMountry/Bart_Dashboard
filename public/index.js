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
