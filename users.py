import sqlite3

from flask import make_response, jsonify
from flask_restful import Resource

from flask_restful import reqparse


class User():
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM users WHERE username=?"
        row = cur.execute(query, (username,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM users WHERE id =?"
        row = cur.execute(query, (_id,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', type=int, required=True)

    def post(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        data = self.parser.parse_args()
        if User.find_by_username(data['username']):
            return make_response(jsonify({'message': "User {} already exists".format(data['username'])}), 208)
        create_user = 'INSERT INTO users VALUES (NULL, ?, ?)'
        user = (data['username'], data['password'])
        cur.execute(create_user, user)
        con.commit()
        con.close()
        return make_response(jsonify(data), 201)
