from werkzeug.security import safe_str_cmp


# used to authenticate a user
from models.user_model import UserModel


def authenticate(username, password):
    # another way of accessing a dictionary and lets
    # us set a default value if there isn't a username key for this username
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):  # takes in a payload (contents of JWT token
    # we can extract the user id and retrieve the specific user
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
