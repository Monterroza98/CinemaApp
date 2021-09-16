from flask import Flask,app,request,jsonify,redirect,url_for
from flask_cors import CORS,cross_origin
import pandas as pd

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file(): 
    response=jsonify(message="exito") 

    #f = request.files.getlist('file')
    f = request.files['file']

    print(f)
    #return(response,200)

    df = pd.read_csv(f, encoding='latin-1', error_bad_lines=False)
    print(df)

    return redirect("http://127.0.0.1")



