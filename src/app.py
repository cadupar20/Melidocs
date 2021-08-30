#import the Flask / HTML Render Template / Time-> class
from flask import Flask, render_template, flash
#import the MongoClient class
from pymongo import MongoClient

app = Flask(__name__)
# MongoDB Connection String
MONGO_URI='mongodb://127.0.0.1'

if __name__ == "__main__":
    app.run(debug=True)

# Declaracion de / raiz
@app.route("/home")
@app.route("/")
def home():
    #return "<h1>Hello, Flask!</h1>"
    return render_template ('home.html')

@app.route("/process-script")
def DataImportDB():

    # record the start time for the script
    #start_time = time.time()

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
    print ("El resultado de mongo : {}".format(results))
    #results = collation.find()
        #for r in results:
            #print ("El resultado de mongo : {}".format(r))
    return "<h1>Import Data on MongoDB, Flask!</h1>"
