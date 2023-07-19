from decouple import config
from pymongo.mongo_client import MongoClient

client = MongoClient(config('URI'))