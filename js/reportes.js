$(document).ready(function () {
  $("#div_filtros").hide();
  $("#div_chkFecha").hide();
  $("#div_chkSort").hide();
  $("#div_rango").hide();
  $("#div_cadena").hide();
  $("#div_pais").hide();
  $("#div_movies").hide();
});

$(function () {
  var dateFormat = "yyyy-mm-dd",
    from = $("#from")
      .datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'yy-mm-dd'
      })
      .on("change", function () {
        to.datepicker("option", "minDate", getDate(this));
      }),
    to = $("#to").datepicker({
      changeMonth: true,
      changeYear: true,
      dateFormat: 'yy-mm-dd'
    })
      .on("change", function () {
        from.datepicker("option", "maxDate", getDate(this));
      });

  function getDate(element) {
    var date;
    try {
      date = $.datepicker.parseDate(dateFormat, element.value);
    } catch (error) {
      date = null;
    }
    return date;
  }
});

$('#btnLimpiar').click(function () {
  $('#frmMain')[0].reset();
  $("#div_filtros").hide();
  $("#resultado_rpt").empty();
  $("#div_rango").hide();
  $("#list_data").html('<option value="0" hidden>Seleccione</option>')
});

function ctrlFiltros(data) {
  if (data == "1") {
    $("#div_filtros").show();
    $("#div_chkFecha").show();
    $("#div_chkSort").show();
    $("#div_rango").show();
    $("#div_pais").show();
    $("#div_movies").hide();
    $("#div_cadena").hide();
    getCountry()
  } else if (data == "2") {
    $("#div_filtros").show();
    $("#div_chkFecha").show();
    $("#div_chkSort").hide();
    $("#div_rango").show();
    $("#div_pais").hide();
    $("#div_cadena").hide();
    $("#div_movies").hide();
  } else if (data == "3") {
    $("#div_filtros").show();
    $("#div_chkFecha").hide();
    $("#div_chkSort").hide();
    $("#div_rango").hide();
    $("#div_pais").hide();
    $("#div_cadena").show();
    $("#div_movies").hide();
    getCircuit()
  } else if (data == "4") {
    $("#div_filtros").show();
    $("#div_chkFecha").hide();
    $("#div_chkSort").hide();
    $("#div_rango").hide();
    $("#div_pais").show();
    $("#div_cadena").show();
    $("#div_movies").show();
    getCountry()
    getMovies()
  }
  else {
    $("#div_pais").hide();
    $("#div_filtros").hide();
    $("#div_chkFecha").hide();
    $("#div_chkSort").hide();
    $("#div_rango").hide();
    $("#div_cadena").hide();
    $("#div_movies").hide();
  }

}

//ESTE ES EL METODO PARA CONSULTAR
function consultarReporte() {
  $("#resultado_rpt").empty();
  var query = "";
  var params = "";

  var reporte = $("#list_rpt").val();

  if (reporte == "0") {
    alert("Seleccione un reporte y data a consultar");
    return
  }

  var inicio = $("#from").val();
  var final = $("#to").val();
  var pais = $("#list_paises").val();
  var cadena = $("#list_cadena").val();
  var rango = $("#rango").val();

  if (!rango) { rango = 10; }

  if ($('#chkSort').prop('checked')) {
    var sort = 1;
  } else {
    var sort = -1;
  }

  if ($('#chkFecha').prop('checked')) {
    var sinFecha = true;
  } else {
    if (!inicio || !final) {
      alert("Seleccione el rango de fechas a consultar o elija el checkbox");
      return 
    }
  }

  switch (reporte) {
    case "1": //TopMovie

      if (pais) {
        if (sinFecha) {
          query = "TopMoviesByCountry";
          params = '{"country": "' + pais + '", "range": "' + rango + '", "sort": "' + sort + '"}';
        } else {
          query = "TopMoviesByCountryAndDate";
          params = '{"country": "' + pais + '", "range": "' + rango + '", "dateIni": "' + inicio + '",  "dateFin": "' + final + '", "sort": "' + sort + '"}';
        }
      } else {
        if (sinFecha) {
          query = "TopMovies";
          params = '{"range": "' + rango + '", "sort": "' + sort + '"}';
        } else {
          query = "TopMoviesByDate";
          params = '{"range": "' + rango + '", "dateIni": "' + inicio + '",  "dateFin": "' + final + '", "sort": "' + sort + '"}';
        }
      }

      break;

    case "2": //TopCountry
      if (sinFecha) {
        query = "TopCountries";
        params = '{}';
      } else {
        query = "TopCountriesByDate";
        params = '{"dateIni": "' + inicio + '",  "dateFin": "' + final + '"}';
      }
      break;

    case "3":
      query = "CircuitByCountry";
      params = '{"circuit": "' + cadena + '","dateIni": "' + inicio + '",  "dateFin": "' + final + '"}';
      break;

    case "4": //TopMovie
      var movie = $('#movies').val()


      if (movie) {
        if (pais) {
          if (cadena) {
            query = "MovieByCountryAndCircuit";
            params = '{"country": "' + pais + '","movie": "' + movie + '","circuit": "' + cadena + '",  "dateIni": "' + inicio + '",  "dateFin": "' + final + '"}';
          } else {
            query = "MoviesByDateAndCountry";
            params = '{"country": "' + pais + '","movie": "' + movie + '", "dateIni": "' + inicio + '",  "dateFin": "' + final + '"}';
          }
        } else {
          query = "MovieByDate";
          params = '{"movie": "' + movie + '", "dateIni": "' + inicio + '",  "dateFin": "' + final + '"}';
        }
      } else {
        alert('Ingrese la pelicula a consultar')
        return
      }

      break;



    default: break;
  }


  params = JSON.stringify(params);
  $.ajax({
    url: 'http://127.0.0.1:5000/' + query,
    type: "POST",
    data: params,
    contentType: 'application/json',
    dataType: 'json',
    error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
    success: function (data) {
      console.log(data)
      createTable(data);
    }
  });

}

function getCountry() {
  $.ajax({
    url: 'http://127.0.0.1:5000/GetCountries',
    type: "POST",
    contentType: 'application/json',
    dataType: 'json',
    error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
    success: function (data) {

      $('#list_paises').empty()
      $('#list_cadena').empty()
      $('#list_paises').append('<option value="' + "" + '">' + "Seleccione" + '</option>')
      $('#list_cadena').append('<option value="' + "" + '">' + "Seleccione" + '</option>')
      Object.keys(data).forEach(function (key) {
        //console.log(data[key]['_id']);
        $('#list_paises').append('<option value="' + data[key]['_id'] + '">' + data[key]['_id'] + '</option>')
      });

    }
  });
}

function getMovies() {
  $.ajax({
    url: 'http://127.0.0.1:5000/GetMovies',
    type: "POST",
    contentType: 'application/json',
    dataType: 'json',
    error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
    success: function (data) {

      $('#list_movies').empty()
      Object.keys(data).forEach(function (key) {
        //console.log(data[key]['_id']);
        $('#list_movies').append('<option value="' + data[key]['_id'] + '"/>')
      });

    }
  });
}

function getCircuit() {
  $.ajax({
    url: 'http://127.0.0.1:5000/GetCircuits',
    type: "POST",
    contentType: 'application/json',
    dataType: 'json',
    error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
    success: function (data) {

      $('#list_cadena').empty()
      $('#list_cadena').append('<option value="' + "" + '">' + "Seleccione" + '</option>')
      Object.keys(data).forEach(function (key) {
        //console.log(data[key]['_id']);
        $('#list_cadena').append('<option value="' + data[key]['_id'] + '">' + data[key]['_id'] + '</option>')
      });

    }
  });

}

function getCircuitByCountry() {
  var paisSelected = $('#list_paises option:selected').val()
  var params = '{"country": "' + paisSelected + '"}';
  params = JSON.stringify(params);
  console.log(params)
    / $.ajax({
      url: 'http://127.0.0.1:5000/GetCircuitsByCountry',
      type: "POST",
      data: params,
      contentType: 'application/json',
      dataType: 'json',
      error: function (jqXHR, textStatus, errorThrown) { alert("Error") },
      success: function (data) {

        $('#list_cadena').empty()
        $('#list_cadena').append('<option value="' + "" + '">' + "Seleccione" + '</option>')
        Object.keys(data).forEach(function (key) {
          //console.log(data[key]['_id']);
          $('#list_cadena').append('<option value="' + data[key]['_id'] + '">' + data[key]['_id'] + '</option>')
        });

      }
    });

}

function createTable(data) {

  if (data.length == 0) {
    alert("La consulta no se encontro ningun registro");
  } else {
    col_id = [];
    col_total = [];

    Object.keys(data[0]).forEach(function (key) { //los que no estan dentro de _id
      col_total.unshift(key);

    });
    col_total.pop();//para quitar la col de "_id"

    Object.keys(data[0]['_id']).forEach(function (key) {
      col_id.unshift(key);
    });

    var thead = '<thead><tr class="info">';
    $.each(col_id, function (i, item) {
      thead += '<th>' + item + '</th>';
    });
    $.each(col_total, function (i, item) {
      thead += '<th>' + item + '</th>';
    });
    thead += '</tr></thead>';

    $("#resultado_rpt").append('<table class="table table-bordered" id="table_rpt">' + thead + '<tbody></tbody></table>');

    $.each(data, function (i, item) {

      var tds = '';

      $.each(col_id, function (i, prueba) {
        var content = item['_id'][prueba];
        tds += '<td>' + (content) + '</td>';
      });
      $.each(col_total, function (i, prueba) {
        var content = item[prueba];
        tds += '<td>' + (content) + '</td>';
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

}