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
    return redirect("http://localhost")


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
    # Convertimos el dataframe a json
    fileToJSON = j.to_json(orient="records")
    # Convertimos el JSON a objeto de Python
    content = js.loads(fileToJSON)
    newJSON = {"_id": filename, "fecha": fecha, "content": content}
    # Convertimos el objeto python a JSON
    result = js.dumps(newJSON)
    # Insertamos el objeto a Mongo (col es coleccion)
    x = MongoConnection.insertOne(js.loads(result))
    print(x.inserted_id)
    return

# ----------------------------------------------Controllers------------------------------------------------------------

# TOP INGRESO DE PERSONAS DURANTE EL FIN DE SEMANA POR PAIS Y EN UN RANGO ESPECIFICO.


@app.route('/topWkndCountryAndRange', methods=['POST'])
@cross_origin()
def topWkndByCountryAndRange():
    country = request.args.get('country')
    range = request.args.get('range')
    date = request.args.get('date')
    date = date.split("-")
    y = date[0]
    m = date[1]
    d = date[2]

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
                            '$gt': datetime(y, m, d, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalAdm': {
                    '$sum': '$content.admWeekend'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalAdm': -1
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP INGRESO DE PERSONAS DURANTE LA SEMANA POR PAIS Y EN UN RANGO ESPECIFICO.


@app.route('/topWkCountryAndRange', methods=['POST'])
@cross_origin()
def topWkByCountryAndRange():
    result = [
        {
            '$match': {
                '_id': re.compile(r"CR")
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
                            '$gt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalAdm': {
                    '$sum': '$content.admTotal'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalAdm': -1
            }
        }, {
            '$limit': 10
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE EL FIN DE SEMANA POR PAIS Y EN UN RANGO ESPECIFICO.


@app.route('/topMoneyWkndCountryAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkndCountryAndRange():
    result = [
        {
            '$match': {
                '_id': re.compile(r"CR")
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
                            '$gt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalIngresos': {
                    '$sum': '$content.ingWeekend'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': 10
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE LA SEMANA POR PAIS Y EN UN RANGO ESPECIFICO.


@app.route('/topMoneyWkCountryAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndRange():
    result = [
        {
            '$match': {
                '_id': re.compile(r"CR")
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
                            '$gt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalIngresos': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': 10
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP MAYOR INGRESO DE DINERO POR SEMANA, CADENA Y POR RANGO ESPECIFICO.


@app.route('/tophigherMoneyWkCountryAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndRange():
    result = [
        {
            '$match': {
                '_id': re.compile(r"SV"),
                'content.cadena': re.compile(r"Cinepolis")
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
                            '$gt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalIngresos': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': 10
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE EL FIN DE SEMANA POR PAIS, SUCURSAL Y EN UN RANGO ESPECIFICO.


@app.route('/topMoneyWkCountryAndSucursalAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndSucursalAndRange():
    result = [
        {
            '$match': {
                '_id': re.compile(r"CR"),
                'content.cadena': re.compile(r"Cinepolis")
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
                            '$gt': datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
                '_id': '$content.idTitulo',
                'totalIngresos': {
                    '$sum': '$content.ingWeekend'
                },
                'uniqueValues': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': 10
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response
