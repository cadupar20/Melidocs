try:
    #import the Flask / HTML Render Template / Time-> class
    from flask import Flask, render_template, flash, url_for, jsonify, request
    #import the MongoClient class
    from pymongo import MongoClient
    #import the datetime class
    from datetime import datetime
    #import Jwt Extented for Manage Token 
    from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

app.config['SECRET_KEY']= '5914e1d26c7abef2b45176ac5423bfc0'
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "5914e1d26c7abef2b45176ac5423bfc0"
jwt = JWTManager(app)


# Declaracion de path / y home
@app.route("/home")
@app.route("/")
def home():
    return render_template ('home.html')

# Declaracion de path /api/docs
@app.route('/api/docs')
@jwt_required()
def count_words():
    from flask import jsonify, request
    doc_name = request.args.get('doc_name', default = "NONE", type = str)
    term = request.args.get('term', default = '*', type = str)
    print("\ndoc_name: {} - term: {}".format(doc_name,term))
    if doc_name !='NONE' and term !='*':
        if len(doc_name)>4:
            from getdata import querymongo
            from model import get_database
            #Validation doc_name has .txt in string
            ExtensionString = ".txt"
            if doc_name.find(ExtensionString) != -1:
                print ("Found .txt!")
            else:
                print ("Not found! .txt")
                ExtensionString = ".txt"
                doc_name=doc_name+ExtensionString
            #Call MongoDB function
            term_frecuency=querymongo(doc_name,term)
            print("Doc_name: {} - Term: {} - Frecuency:{}".format(doc_name,term,term_frecuency))
            return jsonify(dict(texto=[doc_name, term,term_frecuency]))
        else:
            resp = jsonify('doc_name not match in the API. Please check the API documentation.')
            resp.status_code = 500
            return resp           
    else:
        resp = jsonify('doc_name and/or term not found in query string. Please check the API documentation.')
        resp.status_code = 500
        return resp

# Declaracion de path /import_txt
@app.route('/import_txt')
@jwt_required()
def import_txt():
    from importtxt import importfiles_toDB
    #Function to process .txt file from ..\downloads
    updatedTXTFiles,importedTXTFiles=importfiles_toDB()
    jsonfile=jsonify(dict(message=['TXT inserted',importedTXTFiles, 'TXT updated',updatedTXTFiles]))
    response = jsonfile
    response.headers["Content-Type"] = "application/json"  
    #return  jsonify(dict(message=['TXT inserted',importedTXTFiles, 'TXT updated',updatedTXTFiles]))
    return response

# Seguridad del sitio
# Declaracion de path /login
@app.route('/login1')
def login():
    import jwt
    import datetime
    token = jwt.encode({'public_id' : 'id', 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'], "HS256")
    print("token generado: {}".format(token))
    return jsonify({'token' : token})


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def tokenlogin_access():
    import datetime
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username, fresh=True)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200