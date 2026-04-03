from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["gig_protect"]