from pymongo import MongoClient
from .config import settings

connect = MongoClient(f"mongodb+srv://{settings.database_username}:{settings.database_password}@cluster0.paoutzt.mongodb.net/{settings.database_name}?retryWrites=true&w=majority")

db = connect.todo_db

collection_posts = db['posts']
collection_users = db['users']
collection_comments = db['comments']
collection_conversations = db['conversations']
collection_messages = db['messages']

try:
    connect.admin.command('ping')
    print("Connection With MongoDB Successfully!!!")
except Exception as error:
    print(error)