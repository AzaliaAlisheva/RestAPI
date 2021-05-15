from flask import make_response, jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from db import db
from models.items import Item


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)

    # POST /items/<name>/ -> price
    @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return make_response(jsonify({'message': "Item {} already exists".format(name)}), 208)
        data = self.parser.parse_args()
        item = Item(item_name=name, price=data["price"])
        db.session.add(item)
        db.session.commit()
        return make_response(jsonify({'item_name': name, 'price': data['price']}), 201)

    # GET /items/<name>/
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if not item:
            return make_response(jsonify({'message': "Item {} doesn't exist".format(name)}), 404)
        return make_response(jsonify({"item_name": item.item_name, "price": item.price}), 200)

    # PUT /items/<name>/ -> price
    @jwt_required()
    def put(self, name):
        item = Item.find_by_name(name)
        if item:
            self.parser.add_argument('price') #changed to price
            data = self.parser.parse_args()
            Item.price = data["price"]
            return make_response(jsonify({"item_name": name, "price": data['price']}), 200)
        return self.post(name)

    # DELETE /items/<name>/
    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            db.session.delete(item)
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
                item = Item(item_name=item['item_name'], price=item["price"])
                db.session.add(item)
                db.session.commit()
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
        row = Item.get_all()
        return_list = []
        for el in row:
            return_list.append({"item_name": el.item_name, "price": el.price})
        return make_response(jsonify(return_list), 200)

