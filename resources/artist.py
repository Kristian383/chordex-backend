from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.artist import ArtistModel


class Artist(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # parser.add_argument('order',
    #                     type=int,
    #                     required=True,
    #                     help="Every item needs a store id!"
    #                     )

    #@jwt_required()
    def get(self,name):

        artist=ArtistModel.find_by_name(name)

        if artist:
            return artist.json()
        return name

    
    def post(self, name):
        if ArtistModel.find_by_name(name):
            return {'message': "An artist with name '{}' already exists.".format(name)}, 400

        # data = Artist.parser.parse_args()

        artist = ArtistModel(name)
        # self.insert(artist["name"])
        try:
            artist.save_to_db()
        except:
            return {"message": "An error occured inserting the artist."}, 500
        return artist.json(), 201

    def delete(self, name):
        artist = ArtistModel.find_by_name(name)
        if artist:
            artist.delete_from_db()

        return {'message': 'Artist deleted'}

class ArtistList(Resource):
    def get(self):
        return {"artists": [artist.json() for artist in ArtistModel.find_all()]}


class ArtistUser(Resource):
    def get(self):
        pass