from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/todoapp'

    mongo.init_app(app)

    from app.routes import init_routes
    init_routes(app)

    return app
