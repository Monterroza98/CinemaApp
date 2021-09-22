from flask import Flask, app, request, jsonify, redirect, url_for
import pandas as pd
import xlrd
from Controllers.CinemaController import * 

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    response = jsonify(message="exito")

    f = request.files.getlist('file')
    for file in f:
        processFiles(file)
    return redirect("http://localhost")


def processFiles(file):

    j = pd.read_excel(file.stream, skiprows=2, index_col=None,
                      usecols="B,E:G,H,J,L,N,P,R,T,V,X,Z,AA,AC,AE,AG,AI,AK,AM,AO,AQ,AS,AT")
    filename = file.filename.split("/")
    filename = filename[len(filename)-1].split(".")
    filename = filename[0]
    fileToJSON = j.to_json(orient="records")
    # ESTE METODO DE ABAJO ES PARA KATIRO!!!!!
#aInsertar = {"_id": filename, "content": fileToJSON}
    # ESTE SERIA EL METODO DE KATIRO
    CinemaController.uploadToDatabase(filename, fileToJSON)
    # CR2019-01-03.xls
    #country = filename[1][:2]
    #date = filename[1].split("-")
    #year = date[0][4:]
    #month = date[1]
    #uploadToDatabase(j, country, year, month)
    return

# EJEMPLO DE METODO DE KATIRO QUE RECIBE DOS PARAMETROS


#def uploadToDatabase(filename, fileContent):
#    print(fileContent)
#   return
