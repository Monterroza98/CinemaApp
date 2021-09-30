from flask import Flask, app, request, jsonify, redirect, url_for
import pandas as pd
import xlrd
from Models.MongoConnection import *
import re
from datetime import datetime, tzinfo, timezone
import json as js
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    response = jsonify(message="exito")

    f = request.files.getlist('file')
    for file in f:
        processFiles(file)
    return redirect("http://localhost/reportes.html")


def processFiles(file):
    print(file.filename)
    j = pd.read_excel(file.stream, skiprows=2, index_col=None,
                      usecols="B,E:G,H,J,L,N,P,R,T,V,X,AA,AC,AE,AG,AI,AK,AM,AO,AQ,AT",
                      names=["titulo", "sucursal", "cadena", "idSucursal", "admJueves", "admViernes",
                             "admSabado", "admDomingo", "admWeekend", "admLunes", "admMartes",
                             "admMiercoles", "admTotal", "ingJueves", "ingViernes", "ingSabado",
                             "ingDomingo", "ingWeekend", "ingLunes", "ingMartes", "ingMiercoles",
                             "ingTotal", "idTitulo"])
    # Obtenemos el nombre del archivo para sacar el id
    filename = file.filename.split("/")
    filename = filename[len(filename)-1].split(".")
    filename = filename[0]
    fecha = filename[2:]
    pais = filename[:2]
    # Convertimos el dataframe a json
    fileToJSON = j.to_json(orient="records")
    # Convertimos el JSON a objeto de Python
    content = js.loads(fileToJSON)
    newJSON = {"_id": filename, "fecha": fecha,
               "pais": pais, "content": content}
    # Convertimos el objeto python a JSON
    result = js.dumps(newJSON)
    # Insertamos el objeto a Mongo (col es coleccion)
    x = MongoConnection.insertOne(js.loads(result))
    # print(js.loads(result))
    print(x.inserted_id)
    return


# TopMoviesByCountryAndDate
@app.route('/TopMoviesByCountryAndDate', methods=['POST'])
@cross_origin()
def TopMoviesByCountryAndDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
    sort = int(paramDic['sort'])
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$match': {
                '_id': re.compile(country)
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais',
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }, {
            '$sort': {
                'Ingreso total': sort
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TopMoviesByCountry


@app.route('/TopMoviesByCountry', methods=['POST'])
@cross_origin()
def TopMoviesByCountry():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
    sort = int(paramDic['sort'])
    result = [
        {
            '$match': {
                '_id': re.compile(country)
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais',
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }, {
            '$sort': {
                'Ingreso total': sort
            }
        }, {
            '$limit': range
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TopMovies


@app.route('/TopMovies', methods=['POST'])
@cross_origin()
def TopMovies():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    range = int(paramDic['range'])
    sort = int(paramDic['sort'])
    result = [
        {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': {
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }, {
            '$sort': {
                'Ingreso total': sort
            }
        }, {
            '$limit': range
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TopMoviesByDate


@app.route('/TopMoviesByDate', methods=['POST'])
@cross_origin()
def TopMoviesByDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    range = int(paramDic['range'])
    sort = int(paramDic['sort'])
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])
    result = [
        {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': {
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }, {
            '$sort': {
                'Ingreso total': sort
            }
        }, {
            '$limit': range
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# -----------------------------------------------------------------------------------------

# MovieByDate


@app.route('/MovieByDate', methods=['POST'])
@cross_origin()
def MovieByDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    dateIni = paramDic['dateIni']
    movie = paramDic['movie']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$match': {
                'content.titulo': movie
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso  total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# MoviesByDateAndCountry


@app.route('/MoviesByDateAndCountry', methods=['POST'])
@cross_origin()
def MoviesByDateAndCountry():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    movie = paramDic['movie']
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'content.titulo': movie
                    }, {
                        '_id': re.compile(country)
                    }
                ]
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso  total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response


# MovieByCountryAndCircuit
@app.route('/MovieByCountryAndCircuit', methods=['POST'])
@cross_origin()
def MovieByCountryAndCircuit():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    movie = paramDic['movie']
    circuit = paramDic['circuit']
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'content.titulo': movie
                    }, {
                        '_id': re.compile(country)
                    }, {
                        'content.cadena': re.compile(circuit)
                    }
                ]
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais',
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso  total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# MovieByCountryCircuitAndTheater


@app.route('/MovieByCountryCircuitAndTheater', methods=['POST'])
@cross_origin()
def MovieByCountryCircuitAndTheater():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    circuit = int(paramDic['circuit'])
    theater = int(paramDic['theater'])
    movie = int(paramDic['movie'])
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'content.titulo': movie
                    }, {
                        '_id': re.compile(country)
                    }, {
                        'content.cadena': re.compile(circuit)
                    }, {
                        'content.sucursal': re.compile(theater)
                    }
                ]
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais',
                    'ID Titulo': '$content.idTitulo',
                    'Titulo': '$content.titulo'
                },
                "Ingreso  total": {
                    '$sum': "$content.ingTotal"
                },
                "Admision total de personas": {
                    '$sum': "$content.admTotal"
                },
                "Ingreso monetario por fin de semana": {
                    '$sum': "$content.ingWeekend"
                },
                "Admision de personas por fin de semana": {
                    '$sum': "$content.admWeekend"
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# ----------------------------------------------------------

# GetMovies


@app.route('/GetMovies', methods=['POST'])
@cross_origin()
def GetMovies():
    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': '$content.titulo'
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# GetCircuits


@app.route('/GetCircuitsByCountry', methods=['POST'])
@cross_origin()
def GetCircuitsByCountry():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    result = [
        {
            '$match': {
                '_id': re.compile(country)
            }
        }, {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': '$content.cadena'
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response


@app.route('/GetCircuits', methods=['POST'])
@cross_origin()
def GetCircuits():
    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': '$content.cadena'
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# GetTheaters


@app.route('/GetTheaters', methods=['POST'])
@cross_origin()
def GetTheaters():
    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': '$content.sucursal'
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# GetCountries


@app.route('/GetCountries', methods=['POST'])
@cross_origin()
def GetCountries():
    result = [
        {
            '$group': {
                '_id': '$pais'
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# -------------------------------------------------------------------------

# TopCountries


@app.route('/TopCountries', methods=['POST'])
@cross_origin()
def TopCountries():

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais'
                },
                'Ingreso  total': {
                    '$sum': '$content.ingTotal'
                },
                'Ingreso de personas': {
                    '$sum': '$content.admTotal'
                },
                'Ingreso de personas por fin de semanas': {
                    '$sum': '$content.ingWeekend'
                },
                'Ingreso por fin de semanas': {
                    '$sum': '$content.admWeekend'
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TopCountriesByDate


@app.route('/TopCountriesByDate', methods=['POST'])
@cross_origin()
def TopCountriesByDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'pais': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lte': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'Pais': '$pais'
                },
                'Ingreso  total': {
                    '$sum': '$content.ingTotal'
                },
                'Ingreso de personas': {
                    '$sum': '$content.admTotal'
                },
                'Ingreso de personas por fin de semanas': {
                    '$sum': '$content.ingWeekend'
                },
                'Ingreso por fin de semanas': {
                    '$sum': '$content.admWeekend'
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# ------------------------------------------------------------------------------

# CircuitByCountry


@app.route('/CircuitByCountry', methods=['POST'])
@cross_origin()
def CircuitByCountry():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    circuit = paramDic['circuit']

    dateIni = paramDic['dateIni']
    dateIni = dateIni.split("-")
    yi = int(dateIni[0])
    mi = int(dateIni[1])
    di = int(dateIni[2])

    dateFin = paramDic['dateFin']
    dateFin = dateFin.split("-")
    yf = int(dateFin[0])
    mf = int(dateFin[1])
    df = int(dateFin[2])

    result = [
        {
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$project': {
                '_id': True,
                'content': True,
                'fecha': True,
                'pais': True,
                'date': {
                    '$dateFromString': {
                        'dateString': '$fecha',
                        'format': '%Y-%m-%d'
                    }
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'date': {
                            '$gt': datetime(yi, mi, di, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }, {
                        'date': {
                            '$lt': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$match': {
                'content.cadena': circuit
            }
        }, {
            '$group': {
                '_id': {
                    'pais': '$pais'
                },
                'Ingreso  total': {
                    '$sum': '$content.ingTotal'
                },
                'Ingreso de personas': {
                    '$sum': '$content.admTotal'
                },
                'Ingreso de personas por fin de semanas': {
                    '$sum': '$content.ingWeekend'
                },
                'Ingreso por fin de semanas': {
                    '$sum': '$content.admWeekend'
                }
            }
        }
    ]

    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response
