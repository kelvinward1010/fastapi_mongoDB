from pymongo import MongoClient
from .config import settings

connect = MongoClient(f"mongodb+srv://{settings.database_username}:{settings.database_password}@cluster0.paoutzt.mongodb.net/{settings.database_name}?retryWrites=true&w=majority")

db = connect.todo_db

collection_name = db['posts']

try:
    connect.admin.command('ping')
    print("Connection With MongoDB Successfully!!!")
except Exception as error:
    print(error)