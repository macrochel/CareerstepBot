from decouple import config
from pymongo.mongo_client import MongoClient
client = MongoClient(config("ATLAS"))

def init():
    dbc = client["careerBot"]
    coll = dbc["users"]
    return dbc, coll

def initUser(coll, message):
    data = coll.find({ "_id": message.chat.id })
    if data == None:
        model = {
            "_id": message.chat.id, 
            "userId": message.chat.id, 
            "name": " ", 
            "city": " ", 
            "photo": " ", 
            "goal": " ", 
            "phone": " ", 
            "email": " ", 
            "education": " ", 
            "expierence": " ", 
            "hardSkills": " ", 
            "softSkills": " ", 
            "addInfo": " "
        }
        return coll.insert_one(model)

def findUser(coll, message):
    data = coll.find_one({ "_id": message.chat.id })
    return data

def addCollumn(coll, name, message):
    id = {"_id": message.chat.id}
    data = {"$set": {name: message.text}}
    coll.update_one(id, data)

def addCollumnEmpty(coll, name, message):
    id = {"_id": message.chat.id}
    data = {"$set": {name: "Nothing"}}
    coll.update_one(id, data)

def uploadPhoto(coll, src, message):
    id = {"_id": message.chat.id}
    data = {"$set": {"photo": src}}
    coll.update_one(id, data)