from decouple import config
from pymongo.mongo_client import MongoClient

client = MongoClient(config('URI'))

try:
    client.admin.command('ping')
    print('Pinged your deployment. You successfully connected to MongoDB!')
except Exception as e:
    print(e)