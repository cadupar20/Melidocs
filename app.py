try:
    #import the Flask / HTML Render Template / Time-> class
    from flask import Flask, render_template, flash, url_for
    #import the MongoClient class
    from pymongo import MongoClient
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

app.config['SECRET_KEY']= '5914e1d26c7abef2b45176ac5423bfc0'

# Declaracion de path / y home
@app.route("/home")
@app.route("/")
def home():
    return render_template ('home.html')

#from flask import request
#import json

#@app.route("/create_docs")
def create_docs():
    # record the start time for the script
    #start_time = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("Dia/hora: {}...........".format(formatear_now))
    # MongoDB Connection String
    MONGO_URI='mongodb://127.0.0.1'
    # declare a client instance of the MongoDB PyMongo driver 
    client = MongoClient(MONGO_URI)
      
    #Creating, Select DB
    db = client ['PAE']
    #Creating, Select Collation
    collation = db['items']
    #Objets to insert
    product1= {"name":"mouse"}
    product2= {"name":"keyboard"}
    #Insert Objects on collation
    results = collation.insert_many([product1,product2])
    
    # print the API response from the MongoDB server
    print ("\ninsert_many() result:", results)
    # get the total numbers of docs inserted
    total_docs = len(results.inserted_ids)

    # print the number of docs entries inserted
    print ("total entries inserted:", total_docs)

    #print ("El resultado de mongo : {}".format(results.__inserted_ids))
    #results = collation.find()
        #for r in results:
            #print ("El resultado de mongo : {}".format(r))
    #return "<h1>Import Data on MongoDB, Flask!</h1>"
    return render_template ('process_documents.html', title='Create Docs in MongoDB')

# Declaracion de path /api/docs
@app.route('/api/docs')
def count_words():
    from flask import jsonify, request
    doc_name = request.args.get('doc_name', default = "NONE", type = str)
    term = request.args.get('term', default = '*', type = str)
    print("\ndoc_name: {} - term: {}".format(doc_name,term))
    if doc_name !='NONE' and term !='*':
        if len(doc_name)>4:
            from getdata import querymongo,get_database, string_cleanup
            ExtensionString = ".txt"
            if doc_name.find(ExtensionString) != -1:
                print ("Found .txt!")
                #Call MongoDB function
                term_frecuency=querymongo(doc_name,term)
                print("Doc_name: {} - Term: {} - Frecuency:{}".format(doc_name,term,term_frecuency))
                return jsonify(dict(texto=[doc_name, term,term_frecuency])) # or whatever is required
            else:
                print ("Not found! .txt")
                doc_name=doc_name+ExtensionString
                #Call MongoDB function
                term_frecuency=querymongo(doc_name,term)
                print("Doc_name: {} - Term: {} - Frecuency:{}".format(doc_name,term,term_frecuency))
                return jsonify(dict(texto=[doc_name, term,term_frecuency])) # or whatever is required
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
def import_txt():
    from importtxt import importfiles_toDB
    from flask import jsonify
    #Function to process .txt file from ..\downloads
    updatedTXTFiles,importedTXTFiles=importfiles_toDB()
    jsonfile=jsonify(dict(message=['TXT inserted',importedTXTFiles, 'TXT updated',updatedTXTFiles]))
    response = jsonfile
    response.headers["Content-Type"] = "application/json"  
    #return  jsonify(dict(message=['TXT inserted',importedTXTFiles, 'TXT updated',updatedTXTFiles]))
    return response

 # Seguridad del sitio
# Declaracion de path /login
@app.route('/login')
def tokenlogin_access():
    from flask import jsonify
    import jwt
    import datetime
    token = jwt.encode({'public_id' : 'id', 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
    print("token obtenido: {}".format(token))
    return jsonify({'token' : token})
