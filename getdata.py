try:
    #import the Flask class
    from flask import Flask
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)

def querymongo(input_docname, input_string):
    from getdata import get_database,string_cleanup
    
    # record the start time for the script
    #start_time = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))

    #create/select a collation
    collation = get_database()
    #Value to Search #PARAMETERS
    #input_docname="10825-8.txt"
    #input_string="habia" #Transformarlo o NO a ASCII (******pendiente definir*******)

    #MongoDB findone
    textid= collation.find_one({"doc_name":input_docname},{ "_id": 1,"doc_name": 1, "contents": 1})
    #Validate textif if
    if not textid:
        doc_notfound="doc_name/term not found!"
        print (doc_notfound)
        return doc_notfound
    else:
        print("\nWord: {}".format(input_string))
        print("id: {}".format(textid["_id"]))
        print("doc_name: {}".format(textid["doc_name"]))
        #Convert to ascii textid["contents"]
        import unicodedata
        # ********** REVISAR por posibles "ñ" *********
        texto_ascii= unicodedata.normalize('NFD', textid["contents"]).encode('ascii', 'ignore')
        #Convert cadena tipo bytes a string
        texto_ascii = texto_ascii.decode('ISO-8859-1')  # encoding may vary!

        #Remove special characters
        special_chars = ["¿","¡","!","]","_","-","%","#","\n"]
        texto_ascii = string_cleanup(texto_ascii, special_chars)
        #Remove other special characters".,"
        texto_ascii=texto_ascii.translate({ord(i): ' ' for i in ',.:;"[?()'})

        #Muestra final sin caracteres, ASCII
        #print("\nTexto ascii: {}".format(texto_ascii))
        import re #re Class: string searching and manipulation
        #Count frecuency input_string on textid["contents"] (lower case)
        #print("\nFrecuencia de Palabra buscada ('{}'): {}".format(input_string,len(re.findall(" "+input_string+" ", textid["contents"].lower()))))
        #Count frecuency input_string on texto_ascii (lower case)
        term_frecuency=len(re.findall(" "+input_string+" ", texto_ascii.lower()))
        print("\nFrecuencia de Palabra buscada ASCII ('{}'): {}".format(input_string,term_frecuency))

        # record the finish time for the script
        now = datetime.now()
        formatear_now = now.strftime("%A, %d %B, %Y at %X")
        print("\nFinish - Dia/hora: {}...........".format(formatear_now))

        return term_frecuency 

def get_database():
    #import the MongoClient class
    from pymongo import MongoClient, errors
    #Connection String to DB
    #MONGO_URI="mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"
    MONGO_URI='mongodb://127.0.0.1'
    import os
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") #Get MONGO_URI enviroment varstring connection
    #Declare a client instance of MongoDB PyMongo 
    client = MongoClient(MONGO_URI) #replace MONGO_URI for (app)
    db = client ['PAE']
    #Creating, Select DB
    col = db['textos']
    return col


def string_cleanup(x, notwanted):
    import re #re Class: string searching and manipulation
    for item in notwanted:
        x = re.sub(item, ' ', x)
    return x

