try:
    #import the Flask class
    from flask import Flask
    #import the datetime class
    from datetime import datetime
except Exception as e:
    print("Some modules are missing {}".format(e))

def querymongo(input_docname, input_string):
    from model import get_database
    from getdata import string_cleanup #function to remove special character
    import re #re Class: string searching and manipulation
    # record the start time for the script
    #06-AGO
    import time
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))
    #create/select a collation
    collation = get_database()

    import pymongo.errors #import ConnectionFailure,ServerSelectionTimeoutError    
    try:
        start = time.time()
        #MongoDB findone
        textid= collation.find_one({"doc_name":input_docname},{ "_id": 1,"doc_name": 1, "contents": 1})
        end1 =  time.time()
        print("Execution DB time in seconds: ",(end1-start))
        #Validate textif if
        if not textid:
            doc_notfound="doc_name/term not found!"
            print (doc_notfound)
            return doc_notfound,0
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
            #Count frecuency input_string on texto_ascii (lower case)
            term_frecuency=len(re.findall(" "+input_string+" ", texto_ascii.lower()))
            print("\nFrecuencia de Palabra buscada ASCII ('{}'): {}".format(input_string,term_frecuency))

            # record the finish time for the script
            now = datetime.now()
            formatear_now = now.strftime("%A, %d %B, %Y at %X")
            print("\nFinish - Dia/hora: {}...........".format(formatear_now))
            end =  time.time()
            print("Execution time in seconds: ",(end-start))
            return term_frecuency,(end-start) 
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: (ConnectionFailure) {}".format(e))
        return "ConnectionFailure to MongoDB",0
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Could not connect to MongoDB: (Timeout) {} ".format(e))
        return "Timeout to MongoDB",0
    except Exception as e:
        print("Exception: {}".format(e))
        return "Exception to MongoDB",0


def string_cleanup(x, notwanted):
    import re #re Class: string searching and manipulation
    #remove special characters "notwanted"
    for item in notwanted:
        x = re.sub(item, ' ', x)
    return x

def Frecuency_Words_MongoDB (input_docname, input_string):    
    #06-AGO Time Control
    import time
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))
    #Import Mongo Connection
    from model import get_database
    #create/select a collation
    collation = get_database()
    #New libraries for MongoDB aggregate
    from bson.regex import Regex
    from bson.son import SON
    #Manage MongoDB Issue Errors 
    import pymongo.errors #import ConnectionFailure,ServerSelectionTimeoutError    
    try:
        cursorlist=[] #to use with aggregate
        #MongoDB Find Doc
        start = time.time()
        cursor = collation.aggregate([{"$match": {'doc_name':input_docname}},
                        {"$project": {"occurences": {"$regexFindAll": {"input": "$contents",
                        "regex": Regex("[¡¿'\('\[',("");:'\"'#\s._-]"+input_string+"[-_\s.%'\)''\(''\[''\]',;'$?!:'\"'#]"),"options": "is"}}}},
                         {"$unwind": "$occurences"},
                        {"$group": {"_id": 'null',"totalOccurences": {"$sum": 1}}},
                        {"$sort":SON([ ("totalOccurences", -1) ])} 
                        ])
        end =  time.time()
        #retrieve cursor variable
        for i in cursor:
            cursorlist=i
 
        if not cursorlist:
            doc_notfound="doc_name/term not found!"
            print (doc_notfound)
            return doc_notfound,0
        else:
            print("\nWord: {}".format(input_string))
            print("doc_name: {}".format(input_docname))
            print("totalOccurences: {}".format(cursorlist["totalOccurences"]))

            # record the finish time for Mongo steps
            now = datetime.now()
            formatear_now = now.strftime("%A, %d %B, %Y at %X")
            print("\nFinish - Dia/hora: {}...........".format(formatear_now))
            print("Execution time in seconds: ",(end-start))
            return cursorlist["totalOccurences"],(end-start)

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: (ConnectionFailure) {}".format(e))
        return "ConnectionFailure to MongoDB",0
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Could not connect to MongoDB: (Timeout) {} ".format(e))
        return "Timeout to MongoDB",0
    except Exception as e:
        print("Exception: {}".format(e))
        return "Exception to MongoDB",0




def contar_palabra (input_docname, input_string):
    from model import get_database
    from getdata import string_cleanup #function to remove special character
    import re #re Class: string searching and manipulation
    # record the start time for the script
    import time
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))
    #create/select a collation
    collation = get_database()

    import pymongo.errors #import ConnectionFailure,ServerSelectionTimeoutError    
    try:
        start = time.time()
        #MongoDB findone
        textid= collation.find_one({"doc_name":input_docname},{ "_id": 1,"doc_name": 1, "contents": 1})
        end1 =  time.time()
        print("Execution DB time in seconds: ",(end1-start))
        #Validate textif if
        if not textid:
            doc_notfound="doc_name/term not found!"
            print (doc_notfound)
            return doc_notfound,0
        else:
            #print("\nWord: {}".format(input_string))
            #print("id: {}".format(textid["_id"]))
            #print("doc_name: {}".format(textid["doc_name"]))
     
            #Remove other special characters
            texto=textid["contents"].translate({ord(i): ' ' for i in '&\_¡!-"¿?#@!;,:().[]'})
            #print("contents: {}".format(texto.lower()))
     
            #Count frecuency on texto
            term_frecuency=len(re.findall(input_string.lower(), texto.lower()))
            
            # record the finish time for the script
            now = datetime.now()
            formatear_now = now.strftime("%A, %d %B, %Y at %X")
            print("\nFinish - Dia/hora: {}...........".format(formatear_now))
            end =  time.time()
            print("Execution time in seconds: ",(end-start))
            return term_frecuency,(end-start) 
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: (ConnectionFailure) {}".format(e))
        return "ConnectionFailure to MongoDB",0
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Could not connect to MongoDB: (Timeout) {} ".format(e))
        return "Timeout to MongoDB",0
    except Exception as e:
        print("Exception: {}".format(e))
        return "Exception to MongoDB",0


def string_cleanup(x, notwanted):
    import re #re Class: string searching and manipulation
    #remove special characters "notwanted"
    for item in notwanted:
        x = re.sub(item, ' ', x)
    return x