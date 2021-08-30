try:
    #import the Flask / HTML Render Template / Time-> class
    from flask import Flask, render_template, flash, url_for
    #import the MongoClient class
    from pymongo import MongoClient, errors, message
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

# MongoDB Connection String
MONGO_URI='mongodb://127.0.0.1'

# Declaracion de / raiz
@app.route("/home")
@app.route("/")
def home():
    return render_template ('home.html')

from flask import request
import json
@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    print ('Getting RAW Data')
    print (request.get_data())
    print ('Validate JSON Format')
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted'
    #return render_template ('jsonposted.html', title='Json Post', message=content)

@app.route("/process_documents")
def process_documents():
    # record the start time for the script
    #start_time = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("Dia/hora: {}...........".format(formatear_now))

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

    #except errors.ServerSelectionTimeoutError as err:
    # catch pymongo.errors.ServerSelectionTimeoutError
    #print ("PyMongo ERROR:", err)
    
    #print ("El resultado de mongo : {}".format(results.__inserted_ids))
    #results = collation.find()
        #for r in results:
            #print ("El resultado de mongo : {}".format(r))
    #return "<h1>Import Data on MongoDB, Flask!</h1>"
    return render_template ('process_documents.html', title='Process Documents')

@app.route('/api/docs')
def count_words():
    from flask import jsonify,Response, json
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