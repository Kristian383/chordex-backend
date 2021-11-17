
# import sqlite3
from flask_jwt_extended.utils import get_jti
from flask_restful import Resource, reqparse
from models.user import UserModel

from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_unverified_jwt_headers


)

from blocklist import BLOCKLIST

from flask import jsonify, make_response
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

        if UserModel.find_by_username(data["username"]) or UserModel.find_by_email(data["email"]):
            return {"message": "User with that username or email already exists"}, 400

        user = UserModel(data["username"], data["password"], data["email"])
        user.save_to_db()

        access_token = create_access_token(identity=user.id)
        # refresh_token = create_refresh_token(identity=user.id)
        return {
            'token': access_token,
            "user": user.username
            # 'refresh_token': refresh_token
        }, 201
        # response = make_response(jsonify({}))
        # response = jsonify({"msg": "login successful"})
        # set_access_cookies(response, access_token)
        # set_refresh_cookies(response, refresh_token)

        # return response, 201


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

        # if user and safe_str_cmp(user.password, data['password']):
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(
                identity=user.id)  # , fresh=True  # identity staviti mail?
            # refresh_token = create_refresh_token(identity=user.id)
            # return {
            #     'access_token': access_token,
            #     'refresh_token': refresh_token
            # }, 200
            # response = jsonify({"msg": "login successful"})
            # response = make_response(jsonify())
            # set_access_cookies(response, access_token)
            # set_refresh_cookies(response, refresh_token)
            # response.headers.add('Access-Control-Allow-Origin', '*')

            return {"token": access_token,
                    "user": user.username
                    }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # jti is "JWT ID", a unique identifier for a JWT.
        response = jsonify()
        unset_jwt_cookies(response)
        # jti = get_jwt()['jti']
        # BLOCKLIST.add(jti)

        # return {"message": "Successfully logged out"}, 200
        return response, 200


class TokenRefresh(Resource):
    # @jwt_refresh_token_required
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=user_id).first()
        access_token = create_access_token(identity=user.id)

        # new_token = create_access_token(identity=user_id, fresh=False)
        response = jsonify()
        set_access_cookies(response, access_token)

        return response, 201


class UserList(Resource):
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}
