import pymongo
from pymongo import MongoClient

def connect():
    CONNECTION_STRING = 'mongodb+srv://root:6qUXpW5ONvG1ZivT@cluster0.0ir8k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    return client['pricetravel_precios']
