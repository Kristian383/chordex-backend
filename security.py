from models.user import UserModel
from werkzeug.security import safe_str_cmp, check_password_hash


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # ili by email
    # user = UserModel.find_by_email(email)
    if user and check_password_hash(user.password, password):
    # if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
