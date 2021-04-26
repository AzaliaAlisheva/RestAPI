from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.items import ItemResource, ItemList
from resources.users import UserRegister
from security import authenticate, identity
from db import db

apple = Flask(__name__)
api = Api(apple)
apple.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(apple, authenticate, identity)

db.init_app(apple)
apple.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
apple.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api.add_resource(ItemResource, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    apple.run(debug=True)