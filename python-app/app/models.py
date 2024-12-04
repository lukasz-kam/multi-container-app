from . import mongo
from bson import ObjectId
from pymongo import ReturnDocument

class Todo:

    @staticmethod
    def get_all():
        return mongo.db.todos.find()

    @staticmethod
    def get_by_id(todo_id):
        return mongo.db.todos.find_one({'_id': ObjectId(todo_id)})

    @staticmethod
    def create(todo_data):
        return mongo.db.todos.insert_one(todo_data)

    @staticmethod
    def update(todo_id, data):
        return mongo.db.todos.find_one_and_update({'_id': ObjectId(todo_id)}, {'$set': data}, return_document=ReturnDocument.AFTER )

    @staticmethod
    def delete(todo_id):
        return mongo.db.todos.delete_one({'_id': ObjectId(todo_id)})