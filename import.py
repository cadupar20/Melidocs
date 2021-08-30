try:
    #import the Flask class
    from flask import Flask
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)

#except errors.ServerSelectionTimeoutError as err:
#    catch pymongo.errors.ServerSelectionTimeoutError
#    print ("PyMongo ERROR:", err)

# record the start time for the script
#start_time = time.time()
now = datetime.now()
formatear_now = now.strftime("%A, %d %B, %Y at %X")
print("\nStart - Dia/hora: {}...........".format(formatear_now))

def get_database():
    #import the MongoClient class
    from pymongo import MongoClient
    #Connection String to DB
    #MONGO_URI="mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"
    MONGO_URI='mongodb://127.0.0.1'
    #Declare a client instance of MongoDB PyMongo 
    client = MongoClient(MONGO_URI)
    return client ['PAE']

#Creating, Select DB
db = get_database()
#Creating, Select Collation
collation = db['textos']

def listfiles():
    #import os class
    import os
    
    files = os.listdir('.\downloads')
    #print("\nFiles on directory: {}".format(files))
    print("\nFiles on directory: {}".format(len(files)))
    return files

filestoProcess = listfiles()

def InsertFilestoMongo(filestoProcess):
    count=0
    new_documents=[]
    #print ("\nLargo Lista files: {}".format(len(filestoProcess)))
    for file in filestoProcess:
        # do for each file
        #print ("Nombre Archivo a abrir:{}".format(file))

        #Open-File
        fileopened = open('.\\downloads\\'+ file,'r', encoding="utf-8")
        #print("File Opened: {}".format(fileopened))
        #Read-File
        texto = fileopened.read()
        
        #Creating a doc to insert
        new_documents ={"doc_name": file, "contents": texto}
        #print("Documento a insertar: {}.".format(new_documents))
        # Insert doc into Collation
        results = collation.insert_one(new_documents)

        # print the API response from the MongoDB server
        #print ("\ninsert_one() result:", results)

        #Counter
        count+=1  
        #Close file 
        fileopened.close()
    return count

FilesProccesed=InsertFilestoMongo(filestoProcess)

print ("\nCantidad de Files procesados :  {}".format(FilesProccesed))

# record the finish time for the script
now = datetime.now()
formatear_now = now.strftime("%A, %d %B, %Y at %X")
print("\nFinish - Dia/hora: {}...........".format(formatear_now))