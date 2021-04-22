from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from items import ItemSource, ItemList
from users import UserRegister
from security import authenticate, identity

apple = Flask(__name__)
api = Api(apple)
apple.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(apple, authenticate, identity)

api.add_resource(ItemSource, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    apple.run(debug=True)