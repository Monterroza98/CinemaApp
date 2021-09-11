$(document).ready(function () {
   $("#iptFile").fileinput({

   });
});


$("#btnSend").on("click", function () {
   var fdFiles = new FormData();
   var listFiles = $("#iptFile")[0].files;
   $.each(listFiles, function (index, value) {  
      fdFiles.append(index, value);
   });

   for (var key of fdFiles.entries()) {
      console.log(key[0] + ', ' + key[1]);
  }

  $.ajax({
   url: ':8080/upload',
   cache: false,
   contentType: false,
   processData: false,
   data: fdFiles,
   type: 'POST',
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