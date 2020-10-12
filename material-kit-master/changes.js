$("#loading").hide();

Dropzone.options.myAwesomeDropzone = {
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 5, // MB
  uploadMultiple: false,
  maxFiles: 1,
  acceptedFiles: "image/*",
  dictDefaultMessage: "Drop an image here to enhance!",
};
Dropzone.confirm.myAwesomeDropzone = function(question, accepted, rejected) {
  console.log("This nigga works");
  rejected()
};
Dropzone.options.myAwesomeDropzone = {
  init: function () {
    this.on("sending", function (file) {
      if(confirm("Would you be okay to let us use this image to enhance our service?")){
        $("#my-awesome-dropzone").hide();
        $("#loading").show();
      }
    });
    this.on("success", function (file) {
      window.location.href = "./result.html";
    });
    this.on("error", function (file) {
      console.log('bruh ass');
    });
  },
};
