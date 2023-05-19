var input = document.getElementById('myImage');
var img = document.getElementById('preview');
input.addEventListener('change', function(event) {
  var file = event.target.files[0];
  if (file.type.match('image.*')) {
    var reader = new FileReader();
    reader.onload = function() {
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  }
});
