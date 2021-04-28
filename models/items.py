from db import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Item %r>' % self.item_name

    @staticmethod
    def find_by_name(name):
        return Item.query.filter_by(item_name=name).first()

    @staticmethod
    def get_all():
        return Item.query.all()