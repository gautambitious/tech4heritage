Dropzone.options.myAwesomeDropzone = {
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 5, // MB
  uploadMultiple: false,
  maxFiles: 1,
  acceptedFiles: "image/*",
  dictDefaultMessage: "Drop an image here to enhance!",
};

Dropzone.options.myAwesomeDropzone = {
  init: function () {
    this.on("complete", function (file) {
      console.log("Nice")
    });
}
};
