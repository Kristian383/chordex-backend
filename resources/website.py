from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.website import WebsiteModel
from models.user import UserModel


class Website(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('link',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    def post(self, username):
        data = Website.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        if WebsiteModel.find_by_name(data["name"], user.id):
            return {'message': "An website with name '{}' already exists.".format(data["name"])}, 400

        website = WebsiteModel(data["name"], data["link"], user.id)
        try:
            website.save_to_db()
        except:
            return {"message": "An error occured inserting the website."}, 500
        return {'message': 'Website inserted'}, 201

    def delete(self, username):
        data = Website.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        website = WebsiteModel.find_by_name(data["name"], user.id)

        if website:
            try:
                website.delete_from_db()
            except:
                return {"message": "An error occured while deleting the website."}, 500
        else:
            return {'message': 'Website doesnt exist'}, 400
        return {'message': 'Website deleted'}, 201


class WebsiteList(Resource):

    def get(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        return {"websites": [website.json() for website in WebsiteModel.find_all_users_websites(user.id)]}
