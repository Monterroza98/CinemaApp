$(document).ready(function () {
  $( "#div_filtros" ).hide(); 
  $( "#div_chkFecha" ).hide();  
  $( "#div_rango" ).hide();  
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
  if(data != "0"){
    $( "#div_filtros" ).show(); 
    $( "#div_chkFecha" ).show();
    $( "#div_rango" ).show();
  }else{
    $( "#div_filtros" ).hide(); 
    $( "#div_chkFecha" ).hide();
    $( "#div_rango" ).hide();
  }
 
}

function ctrlData(idRpt) {
  var options = '';
  $("#list_data").html('<option value="0" hidden>Seleccione</option>')

  switch (idRpt) {
    case "TopPeople":
      options += '<option value="Week">Week</option>';
      options += '<option value="Weekend">Weekend</option>';
      break;
    case "TopMoney":
      options += '<option value="Week">Week</option>';
      options += '<option value="Weekend">Weekend</option>';
      break;
    case "TopMovie":
      options += '<option value="General">General</option>';
      break;
    case "TopSucursal":
      options += '<option value="General">General</option>';
      break;
    default:
      break;
  }
  $("#list_data").append(options)
}

//ESTE ES EL METODO PARA CONSULTAR
function consultarReporte() {
  $( "#resultado_rpt" ).empty(); 
  var query = "";
  var params = "";

  var reporte = $("#list_rpt").val();
  var data    = $("#list_data").val();

  if(reporte == "0" || data == "0"){
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

  var consulta = reporte + data;

  switch (consulta) {
    case "TopPeopleWeek":

      if(pais){
        if(cadena){
          (sinFecha ? ''/*CountryChainAll*/:''/*CountryChainFecha*/)
        }else{
          (sinFecha ? ''/*CountryAll*/:''/*CountryFecha*/)
        }
      }else{
        (sinFecha ? ''/*RegionAll*/:''/*RegionFecha*/)
      }
      
      break;
    case "TopPeopleWeekend":
      if(pais){
        if(cadena){
          (sinFecha ? ''/*CountryChainAll*/:''/*CountryChainFecha*/)
        }else{
          (sinFecha ? ''/*CountryAll*/:''/*CountryFecha*/)
        }
      }else{
        (sinFecha ? ''/*RegionAll*/:''/*RegionFecha*/)
      }
      break;
    case "TopMoneyWeek":
      if(pais){
        if(cadena){
          (sinFecha ? ''/*CountryChainAll*/:''/*CountryChainFecha*/)
        }else{
          (sinFecha ? ''/*CountryAll*/:''/*CountryFecha*/)
        }
      }else{
        (sinFecha ? ''/*RegionAll*/:''/*RegionFecha*/)
      }
      break;
    case "TopMoneyWeekend":
      if(pais){
        if(cadena){
          (sinFecha ? ''/*CountryChainAll*/:''/*CountryChainFecha*/)
        }else{
          (sinFecha ? ''/*CountryAll*/:''/*CountryFecha*/)
        }
      }else{
        (sinFecha ? ''/*RegionAll*/:''/*RegionFecha*/)
      }
      break;
    case "TopMovieGeneral":
      
      break;
    case "TopSucursalGeneral":
      
      break;

    default:break;
  }

/*
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
      }
  });*/

}

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
}

