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
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):

        website = WebsiteModel.find_by_name(name)

        if website:
            return website.json()
        return name

    def post(self, name):
        data = Website.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]

        if WebsiteModel.find_by_name(name,user_id):
            return {'message': "An website with name '{}' already exists.".format(name)}, 400

        data = Website.parser.parse_args()

        website = WebsiteModel(data["name"], data["link"],user_id)
        # self.insert(artist["name"])
        try:
            website.save_to_db()
        except:
            return {"message": "An error occured inserting the website."}, 500
        return {'message': 'Website inserted'}, 201

    def delete(self, name):
        data = Website.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]
        
        website = WebsiteModel.find_by_name(name,user_id)

        if website:
            try:
                website.delete_from_db()
            except:
                return {"message": "An error occured while deleting the website."}, 500

        return {'message': 'Website deleted'}, 201


class WebsiteList(Resource):
    def get(self):
        return {"websites": [website.json() for website in WebsiteModel.find_all()]}
