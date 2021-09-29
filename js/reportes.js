$(document).ready(function () {
  $( "#div_filtros" ).hide(); 
  $( "#div_chkFecha" ).hide();  
  $( "#div_rango" ).hide();  //
  $( "#div_cadena" ).hide();
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
  $( "#div_rango" ).hide();
  $("#list_data").html('<option value="0" hidden>Seleccione</option>')
});

function ctrlFiltros(data) {
  if(data == "1" || data == "2"){
    $( "#div_filtros" ).show(); 
    $( "#div_chkFecha" ).show();
    $( "#div_rango" ).show();
  }else{
    $( "#div_filtros" ).hide(); 
    $( "#div_chkFecha" ).hide();
    $( "#div_rango" ).hide();
    $( "#div_cadena" ).hide();
  }
 
}

//ESTE ES EL METODO PARA CONSULTAR
function consultarReporte() {
  $( "#resultado_rpt" ).empty(); 
  var query = "";
  var params = "";

  var reporte = $("#list_rpt").val();

  if(reporte == "0"){
    alert("Seleccione un reporte y data a consultar");
  }

  var inicio = $("#from").val();
  var final  = $("#to").val();
  var pais   = $("#list_paises").val();
  var cadena = $("#list_cadena").val();
  var rango  = $("#rango").val();

  if(!rango){rango = 10;}
  if ($('#chkFecha').prop('checked')) {
    var sinFecha = true;
  }else{
    if (!inicio || !final) {
      alert("Seleccione el rango de fechas a consultar o elija el checkbox");
    }
  }

  /* 
  query = "topWkndCountryAndRange";
  params = '{"country": "'+pais+'", "range": "10", "dateIni": "'+inicio+'",  "dateFin": "'+final+'"}';

    if(pais){
        if(cadena){
          (sinFecha ? '':'')
        }else{
          (sinFecha ? '':'')
        }
      }else{
        (sinFecha ? '':'')
      }
  */

  switch (reporte) {
    case "1": //TopMovie

      if(pais){
        if(sinFecha){
          query = "TopMoviesByCountry";
          params = '{"country": "'+pais+'", "range": "'+rango+'"}';
        }else{
          query = "TopMoviesByCountryAndDate";
          params = '{"country": "'+pais+'", "range": "'+rango+'", "dateIni": "'+inicio+'",  "dateFin": "'+final+'"}';
        }
      }else{
        if(sinFecha){
          query = "TopMovies";
          params = '{"range": "'+rango+'"}';
        }else{
          query = "TopMoviesByDate";
          params = '{"range": "'+rango+'", "dateIni": "'+inicio+'",  "dateFin": "'+final+'"}';
        }
      }
      
      break;

    case "2": //TopCountry
        if(sinFecha){
          //TopCountrybyCountry
          query = "";
          params = '{"country": "'+pais+'", "range": "'+rango+'"}';
        }else{
          //TopCountrybyCountryAndDate
          query = "";
          params = '{"country": "'+pais+'", "range": "'+rango+'", "dateIni": "'+inicio+'",  "dateFin": "'+final+'"}';
        }
        break;

    case "3":
      
        break;



    default:break;
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

}

function createTable(data) {

  col_id  = [];
  col_total = [];

  Object.keys(data[0]).forEach(function(key) { //los que no estan dentro de _id
    col_total.unshift(key);

  });
  col_total.pop();//para quitar la col de "_id"
  
  Object.keys(data[0]['_id']).forEach(function(key) {
    col_id.unshift(key);
  });

  var thead = '<thead><tr class="info">';
  $.each(col_id, function(i, item) {
    thead += '<th>'+item+'</th>';
  });
  $.each(col_total, function(i, item) {
    thead += '<th>'+item+'</th>';
  });
  thead += '</tr></thead>';

  $("#resultado_rpt").append('<table class="table table-bordered" id="table_rpt">'+thead+'<tbody></tbody></table>');
  
  $.each(data, function(i, item) {

    var tds = '';

    $.each(col_id, function(i, prueba) {
      var content = item['_id'][prueba];
      tds += '<td>'+(content)+'</td>';
    });
    $.each(col_total, function(i, prueba) {
      var content = item[prueba];
      tds += '<td>'+(content)+'</td>';
    });
    var $tr = $('<tr>').append(tds); 
    $("#table_rpt tbody").append($tr);

  });
  
  $("#table_rpt").dataTable({
    dom: 'Bfrtip',
    'aaSorting': [],
    buttons: [
        'csv'
    ]
  });
}


/*
function createTable(data) {

  columns = [];
  rows = [];
  Object.keys(data[0]).forEach(function(key) {
    columns.unshift(key);
    rows.unshift(key);
  });
  rows.pop();
  
  Object.keys(data[0]['_id']).forEach(function(key) {
    columns.unshift(key);
    rows.unshift(key);
  });

  columns.pop();

  var thead = '<thead><tr>';
  $.each(columns, function(i, item) {
    thead += '<th>'+item+'</th>';
  });
  thead += '</tr></thead>';

  $("#resultado_rpt").append('<table class="table table-bordered" id="table_rpt">'+thead+'<tbody></tbody></table>');
  
  $.each(data, function(i, item) {

    var tds = '';

    $.each(rows, function(i, prueba) {

        if ((i +1) == rows.length) {
          var content = item[prueba];
        }else{
          var content = item['_id'][prueba];
        }

        console.log("SIN ID: "+item[prueba]);
        console.log(item['_id'][prueba]);

      tds += '<td>'+(content)+'</td>';

    });


    var $tr = $('<tr>').append(tds); 
    $("#table_rpt tbody").append($tr)

  });
  
  $("#table_rpt").dataTable({
    dom: 'Bfrtip',
    buttons: [
        'csv'
    ]
  });
}*/

