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
    start = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))

    #create/select a collation
    collation = get_database()

    import pymongo.errors #import ConnectionFailure,ServerSelectionTimeoutError    
    try:
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
            #Count frecuency input_string on textid["contents"] (lower case)
            #print("\nFrecuencia de Palabra buscada ('{}'): {}".format(input_string,len(re.findall(" "+input_string+" ", textid["contents"].lower()))))
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
        return "ConnectionFailure to MongoDB"
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Could not connect to MongoDB: (Timeout) {} ".format(e))
        return "Timeout to MongoDB"
    except Exception as e:
        print("Exception: {}".format(e))
        return "Exception to MongoDB"


def string_cleanup(x, notwanted):
    import re #re Class: string searching and manipulation
    for item in notwanted:
        x = re.sub(item, ' ', x)
    return x

def Frecuency_Words_MongoDB (input_docname, input_string):    
    #06-AGO Time Control
    import time
    start = time.time()
    now = datetime.now()
    formatear_now = now.strftime("%A, %d %B, %Y at %X")
    print("\nStart - Dia/hora: {}...........".format(formatear_now))
    term_frecuency=0

    #Import Mongo Connection
    from model import get_database
    #create/select a collation
    collation = get_database()
    import pymongo.errors #import ConnectionFailure,ServerSelectionTimeoutError    
    try:
        #MongoDB Find Doc
        #incluir script MongoDB ******NUEVO******
        #textid=collation.find_one({"doc_name":input_docname},{ "_id": 0,"doc_name": 1, "contents": 1})

        # Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/
        pipeline = [
            {"$match": {"doc_name": "10825-8.txt"}}, 
            {"$project": {"occurences": {"$regexFindAll": {
                            "input": "$contents",
                            "regex": regex("[\u00A1\u00BF'\\['#'\"'\\s._-]virgilio[-_\\s.%'\\)',;'\\['$?!:#'\"']"),
                            "options": "isx"
                        }
                    }
                }
            }, 
            {"$unwind":"$occurences"}, 
            {"$group": {"_id": None,"totalOccurences": {"$sum": 1.0 }}
            }, 
            {"$sort":([ ("totalOccurences", -1) ])
            }       ]
        textid=collation.aggregate(pipeline)

        #Validate textif if
        if not textid:
            doc_notfound="doc_name/term not found!"
            print (doc_notfound)
            return doc_notfound
        else:
            print("\nWord: {}".format(input_string))
            print("doc_name: {}".format(textid["doc_name"]))
            print("totalOccurences: {}".format(textid["totalOccurences"]))
         

            # record the finish time for Mongo steps
            now = datetime.now()
            formatear_now = now.strftime("%A, %d %B, %Y at %X")
            print("\nFinish - Dia/hora: {}...........".format(formatear_now))
            end =  time.time()
            print("Execution time in seconds: ",(end-start))
            return term_frecuency,(end-start)

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: (ConnectionFailure) {}".format(e))
        return "ConnectionFailure to MongoDB"
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Could not connect to MongoDB: (Timeout) {} ".format(e))
        return "Timeout to MongoDB"
    except Exception as e:
        print("Exception: {}".format(e))
        return "Exception to MongoDB" 