
# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt

)

from blocklist import BLOCKLIST

# jwt_refresh_token_required,
#     get_jwt_identity,
#     get_raw_jwt


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]) and UserModel.find_by_email(data["email"]):
            return {"message": "User with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # parser.add_argument('username',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )

    def post(self):
        data = UserLogin.parser.parse_args()

        # user = UserModel.find_by_username(data['username'])
        user = UserModel.find_by_email(data['email'])

        # this is what the `authenticate()` function did in security.py

        # if user and safe_str_cmp(user.password, data['password']):
        if user and check_password_hash(user.password, data['password']):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            access_token = create_access_token(
                identity=user.id, fresh=True)  # identity staviti mail?
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

# class TokenRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200

class UserList(Resource):
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}
