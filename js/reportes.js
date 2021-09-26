$(document).ready(function () {
  $( "#div_filtros" ).hide(); 
  $( "#div_chkFecha" ).hide();  
  $( "#div_pelicula" ).hide();  
  
});

$( function() {
   var dateFormat = "yyyy-mm-dd",
     from = $( "#from" )
       .datepicker({
         changeMonth: true,
         dateFormat: 'yy-mm-dd'
       })
       .on( "change", function() {
         to.datepicker( "option", "minDate", getDate( this ) );
       }),
     to = $( "#to" ).datepicker({
      changeMonth: true,
      dateFormat: 'yy-mm-dd'
     })
     .on( "change", function() {
       from.datepicker( "option", "maxDate", getDate( this ) );
     });

   function getDate( element ) {
     var date;
     try {
       date = $.datepicker.parseDate( dateFormat, element.value );
     } catch( error ) {
       date = null;
     }
     return date;
   }
} );

$('#btnLimpiar').click(function () {

  $('#frmMain')[0].reset();
  $( "#div_filtros" ).hide(); 
  $( "#resultado_rpt" ).empty(); 
  $( "#div_pelicula" ).hide(); 

});

$('#btnConsultar').click(function () {
/* */

  $( "#resultado_rpt" ).empty();  
  var idRpt = $("#list_rpt").val();
  var query = "";
  var params = "";

  if(!idRpt){
    alert("Seleccione un reporte a consultar");
  }

  var inicio   = $("#from").val();
  var final    = $("#to").val();
  var pais     = $("#list_paises").val();
  var cadena   = $("#list_cadena").val();
  var sucursal = $("#list_sucursal").val();
  var pelicula = $("#pelicula").val();

  if ($('#chkFecha').prop('checked')) {
    var sinFecha = true;
  }else{
    if (!inicio || !final) {
      alert("Seleccione el rango de fechas a consultar");
    }
  }
  
  switch (idRpt) {
    case "1": //INGRESO DE PERSONAS

      break;

    case "2": //INGRESO MONETARIO

      if(cadena && pais){
        if(sinFecha){
          //una query
        }else{
          query = "topSucursalsCountryAndChainAndRangeAndDate";
          params = '{"country": "'+pais+'", "range": "10", "dateIni": "'+inicio+'",  "dateFin": "'+final+'", "chain": "'+cadena+'"}';
        }
      }
      
      break;

    case "3": //TOP DE PELICULAS
      
      break;

    case "4": //INFORMACIÓN DE PELÍCULAS
      
      break;
  
    default:
      break;
  }
  
  params = JSON.stringify(params);
  $.ajax({
     url: 'http://127.0.0.1:5000/'+query,
     type: "POST",
     data: params,
     contentType: 'application/json',
     dataType: 'json',
      error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
      success: function (data) {
        createTable(data);
        console.log(data)
          
      }
  });
});

function ctrlFiltros(idRpt) {
  $( "#div_filtros" ).show(); 
  $( "#div_chkFecha" ).show();
  
  if(idRpt == 3){
    $( "#list_sucursal" ).prop( "disabled", true ); 
  }else{
    $( "#list_sucursal" ).prop( "disabled", false ); 
  }

  if(idRpt == 4){
    $( "#div_pelicula" ).show(); 
  }else{
    $( "#div_pelicula" ).hide(); 
  }
}

function createTable(data) {

  
  Object.keys(data).forEach(function(key) {
    var value = data[key];
    console.log(Object.keys(value));
  });

  $("#resultado_rpt").append('<table class="table table-bordered" id="table_rpt"></table>');
  
  $.each(data, function(i, item) {
    var $tr = $('<tr>').append(
      $('<td>').text(item.ingresoTotalSucursal),
      $('<td>').text(item._id.idSucursal),
      $('<td>').text(item._id.nombreSucursal)
    ); 
    $("#table_rpt").append($tr)
  });
  
 //se debería iniciar datatables cuando ya esté lista la tabla
}

