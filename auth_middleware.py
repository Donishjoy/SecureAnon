from functools import wraps
import jwt
from flask import request,abort
from flask import current_app
from pymongo import MongoClient
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
user_collection=db["User"]

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None 
        if "Authorization" in request.headers:
            token=request.headers["Authorization"].split("")[1]
        if not token:
            return{
                "message":"Authentication is failed",
                "data":None,
                "error":"Unauthorized"
            },401
        try:
            data=jwt.decode(token,current_app.config["SECRET_KEY"],algorithms=["HS256"])
            email=data['email']
            current_user=user_collection.get_by_email(email)
            if current_user is None:
                return{
                    "message":"Invalid Authentication token!",
                    "data":None,
                    "error":"Unauthorized"
                },401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return{
                "message":"Something went wrong",
                "data":None,
                "error":str(e)
            },500
        return f(current_user,*args,**kwargs)
    return decorated