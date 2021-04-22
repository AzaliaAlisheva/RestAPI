from werkzeug.security import safe_str_cmp

from users import User

users = [
    User(1, 'user1', '123'),
    User(2, 'user2', '456'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)


