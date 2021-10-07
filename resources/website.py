from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.website import WebsiteModel


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

    def get(self, name):

        website = WebsiteModel.find_by_name(name)

        if website:
            return website.json()
        return name

    def post(self, name):
        if WebsiteModel.find_by_name(name):
            return {'message': "An website with name '{}' already exists.".format(name)}, 400

        data = Website.parser.parse_args()

        website = WebsiteModel(data["name"], data["link"])
        # self.insert(artist["name"])
        try:
            website.save_to_db()
        except:
            return {"message": "An error occured inserting the website."}, 500
        return website.json(), 201

class WebsiteList(Resource):
    def get(self):
        return {"websites": [website.json() for website in WebsiteModel.find_all()]}
