import pymongo
from pymongo import collation
from pymongo.errors import PyMongoError


def token_required(f):
    from flask import request, jsonify
    import jwt
    from functools import wraps
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
    
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            from app import app
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = 'id'
        except:
            return jsonify({'message': 'token is invalid'})
    
        return f(current_user, *args, **kwargs)
    return decorator


def get_database():
    #import the MongoClient class
    from pymongo import MongoClient
    #Connection String to DB
    MONGO_URI='mongodb://127.0.0.1/?serverSelectionTimeoutMS=3000'
    #MONGO_URI='mongodb+srv://cadupar1973:QRZ81VncrWaH8j0n@pae-itops-001.jv5cl.mongodb.net/PAE?retryWrites=true&w=majority'
    #import os #for MONGO_URI enviroment connection string 
    #app.config["MONGO_URI"] = os.getenv("MONGO_URI") #Get MONGO_URI enviroment varstring connection
    #Declare a client instance of MongoDB PyMongo 
    client = MongoClient(MONGO_URI) #replace MONGO_URI for (app)
    db = client ['PAE']
    #Creating, Select DB
    col = db['textos']
    return col