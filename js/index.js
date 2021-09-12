$(document).ready(function () {
   $("#iptFile").fileinput({

   });
});


$("#btnSend").on("click", function () {
   var fdFiles = new FormData();
   /*var listFiles = $("#iptFile")[0].files;
   $.each(listFiles, function (index, value) {  
      fdFiles.append('archivo'+index, value);
   });

   for (var key of fdFiles.entries()) {
      console.log(key[0] + ', ' + key[1]);
  }*/

  fdFiles.append('prueba', '12345')

  $.ajax({
   url: 'http://127.0.0.1:5000/upload',
   cache: false,
   //contentType: false,
   headers: { "Content-Type": "multipart/form-data" },
   processData: false,
   data: fdFiles,
   type: 'POST',
   crossDomain: true,
   success: function(response) {
       console.log(response);
   },
   error: function(error) {
       console.log(error);
   }
});

// despues de migrar a un server
   /*$.ajax({
      type: 'POST',
      url: 
   });*/
});