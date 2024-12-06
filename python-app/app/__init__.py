import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(env='dev'):
    app = Flask(__name__)
    mongo_ip = os.getenv('MONGO_IP', 'localhost:27017')
    db_username = os.getenv('DB_USERNAME', '')
    db_password = os.getenv('DB_PASSWORD', '')

    if env=='test':
        app.config['MONGO_URI'] = f'mongodb://{mongo_ip}/todoapp_test'
    else:
        app.config['MONGO_URI'] = f'mongodb://{db_username}:{db_password}@{mongo_ip}/todos?ssl=true&tlsAllowInvalidCertificates=true'

    mongo.init_app(app)

    from app.routes import init_routes
    init_routes(app)

    return app
