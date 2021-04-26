from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from db import db
from models.users import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', type=int, required=True)

    def post(self):
        data = self.parser.parse_args()
        if User.query.filter_by(username=data['username']).first():
            return make_response(jsonify({'message': "User {} already exists".format(data['username'])}), 208)
        user = User(username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify(data), 201)