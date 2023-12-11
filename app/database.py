from pymongo import MongoClient

connect = MongoClient("mongodb+srv://kelvinward1010:123456789IMP@cluster0.paoutzt.mongodb.net/database?retryWrites=true&w=majority")

db = connect.todo_db

collection_name = db['posts']

try:
    connect.admin.command('ping')
    print("Connection Successfully!!!")
except Exception as error:
    print(error)