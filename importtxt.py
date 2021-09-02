try:
    #import the Flask class
    from flask import Flask
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)

def importfiles_toDB():
    # record the start time for the script
    #start_time = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))
    from importtxt import listfiles,InsertFilestoMongo
    filestoProcess = listfiles()
    FilesProccesed = InsertFilestoMongo(filestoProcess)
    print ("\nCantidad de Files procesados :  {}".format(FilesProccesed))
    # record the finish time for the script
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nFinish - Dia/hora: {}...........".format(formatear_now))
    return FilesProccesed

def listfiles():
    #import os class
    import os
    files = os.listdir('.\downloads')
    #print("\nFiles on directory: {}".format(files))
    print("\nFiles on directory: {}".format(len(files)))
    return files

def InsertFilestoMongo(filestoProcess):
    count_upddocs=0
    count_newdocs=0
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

        from model import get_database
        #Creating, Select DB
        #db = get_database()
        #create/select a collation
        #collation = db['textos']

        #create/select a collation
        collation = get_database()

        #MongoDB findone
        textid= collation.find_one({"doc_name":file},{ "_id": 1,"doc_name": 1})
        #Validate textif if
        if not textid:
            doc_notfound="doc_name not found!..."
            # print (doc_notfound)
            #Creating a doc to insert
            new_documents = {"doc_name": file, "contents": texto}
            #print("Documento a insertar: {}.".format(new_documents))
            # Insert doc into Collation
            results = collation.insert_one(new_documents)
            # print the API response from the MongoDB server
            # print ("\ninsert_one() result:", results)
            count_newdocs += 1    
        else:
            doc_found = "doc_name found"
            # print (doc_found)
            # Update doc into Collation
            results = collation.update_one({"doc_name":file},{"$set":{"contents": texto}},upsert=True)
            #Counter Updates docs 
            count_upddocs += 1 
 
        #Close file 
        fileopened.close()
    return count_upddocs,count_newdocs