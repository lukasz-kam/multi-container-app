import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(env='dev'):
    app = Flask(__name__)
    mongo_ip = os.getenv('MONGO_IP', 'localhost:27017')

    if env=='test':
        app.config['MONGO_URI'] = f'mongodb://{mongo_ip}/todoapp_test'
    else:
        app.config['MONGO_URI'] = f'mongodb://{mongo_ip}/todoapp'

    mongo.init_app(app)

    from app.routes import init_routes
    init_routes(app)

    return app
