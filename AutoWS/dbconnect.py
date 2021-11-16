import pymongo
from pymongo import MongoClient

def post(resultados):
    CONNECTION_STRING = 'mongodb+srv://root:6qUXpW5ONvG1ZivT@cluster0.0ir8k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    dbname = client['pricetravel_precios']
    collection_name = dbname["paquetes"]
    collection_name.insert_one(resultados)

