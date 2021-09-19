from typing import Counter
from flask import Flask, app, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
import pandas as pd
from werkzeug.datastructures import Headers
import xlrd

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

    j = pd.read_excel(file.stream, skiprows=2, index_col=None,
                      usecols="B,E:G,H,J,L,N,P,R,T,V,X,Z,AA,AC,AE,AG,AI,AK,AM,AO,AQ,AS,AT")
    filename = file.filename.split("/")
    filename = filename[len(filename)-1].split(".")
    filename = filename[0]
    # CR2019-01-03.xls
    #country = filename[1][:2]
    #date = filename[1].split("-")
    #year = date[0][4:]
    #month = date[1]
    #uploadToDatabase(j, country, year, month)
    return


#def uploadToDatabase(dataframe, country, *date):
#    print(dataframe)
#    return
