from flask import Flask,app,request,jsonify,redirect,url_for
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file(): 
    response=jsonify(message="exito") 

    f = request.files.getlist('file')

    print(f)
    #return(response,200)
    return redirect("http://127.0.0.1")



