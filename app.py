from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

apple = Flask(__name__)
api = Api(apple)

items = [
    {
        'item_name': 'default-item',
        'price': 200
    }
]

parser = reqparse.RequestParser()


class Item(Resource):
    # POST /items/<name>/ -> price
    def post(self, name):
        if list(filter(lambda x: x['item_name'] == name, items)):
            return make_response(jsonify({'message': "Item {} already exists".format(name)}), 208)
        parser.add_argument('price', type=int)
        data = parser.parse_args()
        item = {
            'item_name': name,
            'price': data['price']
        }
        items.append(item)
        return make_response(jsonify(item), 201)

    # GET /items/<name>/
    def get(self, name):
        if not list(filter(lambda x: x['item_name'] == name, items)):
            return make_response(jsonify({'message': "Item {} doesn't exist".format(name)}), 404)
        return make_response(list(filter(lambda x: x['item_name'] == name, items)), 200)

    # PUT /items/<name>/
    def put(self, name):
        for i in range(len(items)):
            if items[i]['item_name'] == name:
                parser.add_argument('price', type=int)
                parser.add_argument('item_name')
                data = parser.parse_args()
                items[i] = {
                    'item_name': data['item_name'],
                    'price': data['price']
                }
                return make_response(jsonify(items[i]), 200)
        return self.post(name)

    # DELETE /items/<name>/
    def delete(self, name):
        for i in range(len(items)):
            if items[i]['item_name'] == name:
                del items[i]
                return make_response(jsonify({'message': "Item {} successfully deleted".format(name)}), 204)
        return make_response(jsonify({'message': "Item {} doesn't exist".format(name)}), 404)


api.add_resource(Item, '/items/<string:name>')


class ItemList(Resource):
    # POST /items -> list [{name, price}]
    def post(self):
        parser.add_argument('items', type=list, location='json')
        data = parser.parse_args()
        not_valid_list = []
        valid_list = []
        for item in data['items']:
            if not list(filter(lambda x: x['item_name'] == item['item_name'], items)):
                valid_list.append(item)
            else:
                not_valid_list.append(item['item_name'])
        items.extend(valid_list)
        if not_valid_list:
            return make_response(jsonify({'message': "Item{} {} already exist{}".format('s' if len(not_valid_list) > 1 else '', not_valid_list, '' if len(not_valid_list) > 1 else 's'), 'added': valid_list}), 208)
        return make_response(jsonify(data['items']), 201)

    #GET /items
    def get(self):
        return make_response(jsonify({'items': items}), 200)


api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    apple.run(debug=True)