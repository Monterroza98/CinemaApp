from flask import Flask,app,request,jsonify
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['POST','GET'])
@cross_origin()
def upload_file(): 
    response=jsonify(message="test") 
    print(response) 
    #f = request.form.getList('')
    f = request.form.get('prueba')
    #for key, value in f.items():
	#   print(key)
    print(f)
    #for file in f:
        #print(f.filename)
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return(response,200)


