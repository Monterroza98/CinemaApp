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

# TOP INGRESO DE PERSONAS DURANTE EL FIN DE SEMANA POR PAIS Y EN UN RANGO ESPECIFICO. 1
@app.route('/topWkndCountryAndRange', methods=['POST'])
@cross_origin()
def topWkndCountryAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
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

@app.route('/topWkndCountryAndRangeAll', methods=['POST'])
@cross_origin()
def topWkndCountryAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])

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

# TOP INGRESO DE PERSONAS DURANTE LA SEMANA POR PAIS Y EN UN RANGO ESPECIFICO. 2
@app.route('/topWkCountryAndRange', methods=['POST'])
@cross_origin()
def topWkCountryAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topWkCountryAndRangeAll', methods=['POST'])
@cross_origin()
def topWkCountryAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
    
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE EL FIN DE SEMANA POR PAIS Y EN UN RANGO ESPECIFICO. 3
@app.route('/topMoneyWkndCountryAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkndCountryAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])

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
        },  {
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topMoneyWkndCountryAndRangeAll', methods=['POST'])
@cross_origin()
def topMoneyWkndCountryAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])

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
        },{
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE LA SEMANA POR PAIS Y EN UN RANGO ESPECIFICO. 4
@app.route('/topMoneyWkCountryAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])
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
        },  {
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topMoneyWkCountryAndRangeAll', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    range = int(paramDic['range'])

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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP MAYOR INGRESO DE DINERO POR SEMANA, CADENA Y POR RANGO ESPECIFICO. 5
@app.route('/tophigherMoneyWkCountryAndRangeAndChain', methods=['POST'])
@cross_origin()
def topHigherMoneyWkCountryAndRangeAndChain():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
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
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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
        },  {
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/tophigherMoneyWkCountryAndRangeAndChainAll', methods=['POST'])
@cross_origin()
def topHigherMoneyWkCountryAndRangeAndChainAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])

    result = [
        {
            '$match': {
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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
        },{
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP DE INGRESO DE DINERO DURANTE EL FIN DE SEMANA POR PAIS, SUCURSAL Y EN UN RANGO ESPECIFICO. 6
@app.route('/topMoneyWkCountryAndSucursalAndRange', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndSucursalAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    sucursal = paramDic['Sucursal']
    range = int(paramDic['range'])
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
                '_id': re.compile(country),
                'content.cadena': re.compile(sucursal)
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
        },  {
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topMoneyWkCountryAndSucursalAndRangeAll', methods=['POST'])
@cross_origin()
def topMoneyWkCountryAndSucursalAndRangAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    sucursal = paramDic['Sucursal']
    range = int(paramDic['range'])

    result = [
        {
            '$match': {
                '_id': re.compile(country),
                'content.cadena': re.compile(sucursal)
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
        },{
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP INGRESO DE PERSONAS DURANTE LA SEMANA POR PAIS, POR CADENA Y EN UN RANGO ESPECIFICO. 7
@app.route('/topWkCountryAndChainAndRange', methods=['POST'])
@cross_origin()
def topWkCountryAndChainAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
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
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topWkCountryAndChainAndRangeAll', methods=['POST'])
@cross_origin()
def topWkCountryAndChainAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
    
    result = [
        {
            '$match': {
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# TOP INGRESO DE PERSONAS DURANTE EL FIN DE SEMANA POR PAIS Y EN UN RANGO ESPECIFICO.8
@app.route('/topWkndCountryAndChainAndRange', methods=['POST'])
@cross_origin()
def topWkndCountryAndChainAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
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
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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

@app.route('/topWkndCountryAndChainAndRangeAll', methods=['POST'])
@cross_origin()
def topWkndCountryAndChainAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
    
    result = [
        {
            '$match': {
                '_id': re.compile(country),
                'content.cadena': re.compile(chain)
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

# TOP 10 DE PELICULAS POR CADENA, POR PAIS, POR RANGO 9 en desarrollo
@app.route('/topMovieCountryAndChainAndRange', methods=['POST'])
@cross_origin()
def topMovieCountryAndChainAndRange():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
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
            '$match': {
                'content.cadena': chain
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$content.idSucursal',
                    'idtitulo': '$content.idTitulo'
                },
                'ingresosTotalesSucursal': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValuesSucursal': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$unwind': {
                'path': '$uniqueValuesSucursal'
            }
        }, {
            '$group': {
                '_id': '$uniqueValuesSucursal.titulo',
                'totalIngresos': {
                    '$sum': '$uniqueValuesSucursal.ingTotal'
                },
                'uniqueValues': {
                    '$addToSet': '$uniqueValuesSucursal'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topMovieCountryAndChainAndRangeAll', methods=['POST'])
@cross_origin()
def topMovieCountryAndChainAndRangeAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])

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
            '$match': {
                'content.cadena': chain
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$content.idSucursal',
                    'idtitulo': '$content.idTitulo'
                },
                'ingresosTotalesSucursal': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValuesSucursal': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$unwind': {
                'path': '$uniqueValuesSucursal'
            }
        }, {
            '$group': {
                '_id': '$uniqueValuesSucursal.titulo',
                'totalIngresos': {
                    '$sum': '$uniqueValuesSucursal.ingTotal'
                },
                'uniqueValues': {
                    '$addToSet': '$uniqueValuesSucursal'
                }
            }
        }, {
            '$sort': {
                'totalIngresos': -1
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

####### TOP 10 Sucursales con mas ingresos por cadena y pais en un rango de tiempo 10
@app.route('/topSucursalsCountryAndChainAndRangeAndDate', methods=['POST'])
@cross_origin()
def topSucursalsCountryAndChainAndRangeAndDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
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
            '$match': {
                'content.cadena': chain
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$content.idSucursal',
                    'idtitulo': '$content.idTitulo'
                },
                'ingresosTotalesSucursal': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValuesSucursal': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$_id.idSucursal',
                    'nombreSucursal': {
                        '$last': '$uniqueValuesSucursal.sucursal'
                    }
                },
                'ingresoTotalSucursal': {
                    '$sum': '$ingresosTotalesSucursal'
                }
            }
        }, {
            '$sort': {
                'ingresoTotalSucursal': -1
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/topSucursalsCountryAndChainAndRangeAndDateAll', methods=['POST'])
@cross_origin()
def topSucursalsCountryAndChainAndRangeAndDateAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    range = int(paramDic['range'])
    
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
        },{
            '$unwind': {
                'path': '$content'
            }
        }, {
            '$match': {
                'content.cadena': chain
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$content.idSucursal',
                    'idtitulo': '$content.idTitulo'
                },
                'ingresosTotalesSucursal': {
                    '$sum': '$content.ingTotal'
                },
                'uniqueValuesSucursal': {
                    '$addToSet': '$content'
                }
            }
        }, {
            '$group': {
                '_id': {
                    'idSucursal': '$_id.idSucursal',
                    'nombreSucursal': {
                        '$last': '$uniqueValuesSucursal.sucursal'
                    }
                },
                'ingresoTotalSucursal': {
                    '$sum': '$ingresosTotalesSucursal'
                }
            }
        }, {
            '$sort': {
                'ingresoTotalSucursal': -1
            }
        }, {
            '$limit': range
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# Busqueda ganacia por pelicula por rango (para indicar fin de semana e ingresos de dinero solo se cambiar content.ingTotal por content.ingWeekend, ingreso por persona admWeekend e ingreso total de personas por semana admTotal ) 11
@app.route('/searchProfitsMovieDate', methods=['POST'])
@cross_origin()
def searchProfitsMovieDate():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
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
                            '$lt': datetime(yf, mf, df, 0, 0, 0, tzinfo=timezone.utc)
                        }
                    }
                ]
            }
        }, {
            '$group': {
                '_id': {
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/searchProfitsMovieDateAll', methods=['POST'])
@cross_origin()
def searchProfitsMovieDateAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    movie = paramDic['movie']
    
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
            '$group': {
                '_id': {
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# Busqueda ganacia por pelicula por ranago y pais (para indicar fin de semana e ingresos de dinero solo se cambiar content.ingTotal por content.ingWeekend, ingreso por persona admWeekend e ingreso total de personas por semana admTotal ) 12
@app.route('/searchProfitsMovieCountryAndDate', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDate():
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
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/searchProfitsMovieCountryAndDateAll', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDateAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    movie = paramDic['movie']
    
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
            '$group': {
                '_id': {
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# Busqueda ganacia por pelicula por ranago y pais y cadena(para indicar fin de semana e ingresos de dinero solo se cambiar content.ingTotal por content.ingWeekend, ingreso por persona admWeekend e ingreso total de personas por semana admTotal ) 13
@app.route('/searchProfitsMovieCountryAndDateAndChain', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDateAndChain():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
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
                    }, {
                        'content.cadena': chain
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
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/searchProfitsMovieCountryAndDateAndChainAll', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDateAndChainAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    movie = paramDic['movie']
    
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
                        'content.cadena': chain
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
            '$group': {
                '_id': {
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

# Busqueda ganacia por pelicula por ranago y pais, cadena y sucursal (para indicar fin de semana e ingresos de dinero solo se cambiar content.ingTotal por content.ingWeekend, ingreso por persona admWeekend e ingreso total de personas por semana admTotal )14
@app.route('/searchProfitsMovieCountryAndDateAndChainAndSucursal', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDateAndChainAndSucursal():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    sucursal = paramDic['sucursal']
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
                    }, {
                        'content.cadena': chain
                    }, {
                        'content.sucursal': re.compile(sucursal)
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
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response

@app.route('/searchProfitsMovieCountryAndDateAndChainAndSucursalAll', methods=['POST'])
@cross_origin()
def searchProfitsMovieCountryAndDateAndChainAndSucursalAll():
    parameters = request.get_json()
    paramDic = js.loads(parameters)
    country = paramDic['country']
    chain = paramDic['chain']
    sucursal = paramDic['sucursal']
    movie = paramDic['movie']
    
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
                        'content.cadena': chain
                    }, {
                        'content.sucursal': re.compile(sucursal)
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
            '$group': {
                '_id': {
                    'idTitutlo': '$content.idTitulo',
                    'titulo': '$content.titulo'
                },
                'total': {
                    '$sum': '$content.ingTotal'
                }
            }
        }
    ]
    response = MongoConnection.aggregate(result)
    response = list(response)
    response = js.dumps(response)
    return response
