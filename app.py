from flask import Flask,app,request,jsonify,redirect,url_for
from flask_cors import CORS,cross_origin
import pandas as pd
from werkzeug.datastructures import Headers
import xlrd

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file(): 
    response=jsonify(message="exito") 

    #f = request.files.getlist('file')
    f = request.files['file']

    #print(j)

    #print(f)
    #return(response,200)

    j= pd.read_excel(f.stream, skiprows=2, index_col=None, usecols=[1,2,3,4,5])

    #df = j.to_csv(encoding='latin-1', header=True)

    #j.drop(axis=1, columns=[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46])
    #j.drop(axis=1, inplace=True, columns=['Rank'])
    print(j)

    return redirect("http://127.0.0.1")



