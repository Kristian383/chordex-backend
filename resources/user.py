
from base64 import decode
from flask_restful import Resource, reqparse
from models.artist import ArtistModel
from models.user import UserModel
# from models.user_notes import UserNotesModel
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required  # (
# create_access_token,
# jwt_required,
# get_jwt_identity
# )
from firebase_admin import auth
import os


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
        return {
            'token': access_token,
            "user": user.username
        }, 201


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

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(
                identity=user.id)
            return {"token": access_token,
                    "user": user.username
                    }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserList(Resource):
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}


class DeleteAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def delete(self, token):
        data = DeleteAccount.parser.parse_args()
        email = data["email"]
        user = UserModel.verify_authenticity_token(token, email)

        if user is None:
            return {"message": "Your link doesnt work anymore. It could be already used or expired."}, 400
        #
        try:
            [artist.delete_from_db()
             for artist in ArtistModel.find_all_user_artists(user.id)]
            user.delete_from_db()
            return {"message": "Your account has been deleted."
                    }, 200
        except:
            return {"message": "Couldn't delete account."}, 500


class PasswordReset(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self, token):
        data = PasswordReset.parser.parse_args()
        new = data["new"]
        email = data["email"]
        user = UserModel.verify_authenticity_token(token, email)
        if user is None:
            return {"message": "That is an invalid or expired token."}, 400

        user.password = generate_password_hash(new, method="sha256")
        try:
            user.save_to_db()
        except:
            return {"message": "Something went wrong with saving new password."}, 500

        return {"message": "Done"}


class FirebaseAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('google_token',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = FirebaseAuth.parser.parse_args()
        google_token = data['google_token']
        try:
            decoded_token = auth.verify_id_token(google_token)
            email = decoded_token["email"]
            username = decoded_token["name"]
            user = UserModel.find_by_email(email)
            if not user:
                user = UserModel(username, os.environ.get(
                    "GOOGLE_USER_PASSWORD"), email)
                user.save_to_db()

            access_token = create_access_token(
                identity=user.id)
            return {
                "token": access_token,
                "email": user.email,
                "user": user.username}
        except:
            return {"message": "Something went wrong."}, 500


# class User(Resource):  # nece trebati za frontend
#     @classmethod
#     def get(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {"message": "user not found"}, 404
#         return user.json()

#     @classmethod
#     def delete(cls, user_id):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {"message": "User not found"}, 404
#         user.delete_from_db()
#         return {"message": "User deleted"}, 200
