import sqlite3

from flask import make_response, jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item:
    def __init__(self, id_, item_name, price):
        self.id = id_
        self.item_name = item_name
        self.price = price

    def __str__(self):
        return "Item(id='%s')" % self.id

    @staticmethod
    def find_by_name(item_name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE name=?"
        row = cur.execute(query, (item_name,)).fetchone()

        con.close()

        item = Item(*row) if row else None
        return item

    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE id =?"
        row = cur.execute(query, (_id,)).fetchone()

        con.close()

        item = Item(*row) if row else None
        return item

    @staticmethod
    def add_item(name, data):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cur.execute(query, (name, data['price']))

        con.commit()
        con.close()

    @staticmethod
    def change_item(name, data):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "UPDATE items SET name = ?, price = ? WHERE name = ?"
        cur.execute(query, (name, data['price'], name))

        con.commit()
        con.close()

    @staticmethod
    def delete_item(name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cur.execute(query, (name, ))

        con.commit()
        con.close()


class ItemSource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)

    # POST /items/<name>/ -> price
    @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return make_response(jsonify({'message': "Item {} already exists".format(name)}), 208)
        data = self.parser.parse_args()
        Item.add_item(name, data)
        return make_response(jsonify({'item_name': name, 'price': data['price']}), 201)

    # GET /items/<name>/
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if not item:
            return make_response(jsonify({'message': "Item {} doesn't exist".format(name)}), 404)
        return make_response(jsonify({"item_name": item.item_name, "price": item.price}), 200)

    # PUT /items/<name>/
    @jwt_required()
    def put(self, name):
        item = Item.find_by_name(name)
        if item:
            self.parser.add_argument('price')
            data = self.parser.parse_args()
            Item.change_item(name, data)
            return make_response(jsonify({"item_name": name, "price": data['price']}), 200)
        return self.post(name)

    # DELETE /items/<name>/
    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            Item.delete_item(name)
            return '', 204
        return make_response(jsonify({'message': "Item {} doesn't exist".format(name)}), 404)


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=list, location='json', required=True)

    # POST /items -> list [{name, price}]
    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        valid_list = []
        not_valid_list = []
        for item in data['items']:
            if not Item.find_by_name(item['item_name']):
                valid_list.append(item['item_name'])
                Item.add_item(item['item_name'], item)
            else:
                not_valid_list.append(item['item_name'])
        if not_valid_list:
            return make_response(jsonify({'message': "Item{} {} already exist{}".format(
                's' if len(not_valid_list) > 1 else '', not_valid_list, '' if len(not_valid_list) > 1 else 's'),
                                          'added': valid_list}), 208)
        return make_response(jsonify(data['items']), 201)

    # GET /items
    @jwt_required()
    def get(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items"
        row = cur.execute(query).fetchall()

        con.close()
        return_list = []
        for el in row:
            return_list.append({"item_name": el[1], "price": el[2]})
        return make_response(jsonify(return_list), 200)
