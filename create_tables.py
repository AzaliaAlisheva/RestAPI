from db import db

from models.users import User
from models.items import Item

db.create_all()

user = User(username='anatolii', password='123')
db.session.add(user)

item = Item(item_name='I want banana too', price='123')
db.session.add(item)
db.session.commit()