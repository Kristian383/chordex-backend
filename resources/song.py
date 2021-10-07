from flask_restful import Resource, reqparse
from models.song import SongModel
from models.artist import ArtistModel

class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('artist',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self,name):

        song=SongModel.find_by_name(name)

        if song:
            return song.json()
        return name

    def post(self,name):
        if SongModel.find_by_name(name):
            return {'message': "An song with name '{}' already exists.".format(name)}, 400

        data = Song.parser.parse_args()
        artist_id=ArtistModel.find_by_name(data["artist"])

        return {"message":"found artist id '{}'".format(artist_id)}
        #find artist id from database to make song object


class SongList(Resource):
    def get(self):
        return {"songs": [song.json() for song in SongModel.find_all()]}