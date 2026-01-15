import os
from pymongo import MongoClient

def get_db():
    user = os.getenv('MONGO_USERNAME')
    password = os.getenv('MONGO_PASSWORD')
    host = os.getenv('MONGO_HOST')
    db_name = os.getenv('MONGO_DB')

    uri = f'mongodb://{user}:{password}@{host}:27017'
    client = MongoClient(uri)
    database = client[db_name]
    collection = database['top_threats']
    return collection