import pymongo
from pymongo import MongoClient

client = MongoClient()

client = MongoClient("mongodb://127.0.0.1:27017/test22")
db = client["t22"]

#collection_name = dbname["user_1_items"]
tutorial1 = {
    "numberplate":False ,
    
}
#collection_name.insert_many([item_1,item_2])
  
tutorial = db.tutorial
tutorial.insert_one(tutorial1)



