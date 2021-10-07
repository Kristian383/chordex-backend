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

    def get(self, name):

        song = SongModel.find_by_name(name)

        if song:
            return song.json()
        return name

    def post(self, name):
        if SongModel.find_by_name(name):
            return {'message': "An song with name '{}' already exists.".format(name)}, 400

        data = Song.parser.parse_args()
        artist_id = ArtistModel.find_by_name(
            data["artist"]).json()["artist_id"]

        song = SongModel(data["name"], artist_id)
        try:
            song.save_to_db()
        except:
            return {"message": "An error occured inserting a song."}, 500
        return song.json(), 201

        # return {"message":"found artist id '{}'".format(song.json())}
        # find artist id from database to make song object

    def delete(self, name):
        #ovo poboljsati u slucaju ako ima vise pjesama sa istim imenom
        song = SongModel.find_by_name(name)
        if song:
            try:
                song.delete_from_db()
            except:
                return {"message": "An error occured deleting the song."}, 500

        return {'message': 'Song deleted'}

    def put(self, name):
        data = Song.parser.parse_args()
        song = SongModel.find_by_name(name)

        if song is None:
            song = SongModel(name, **data) #ili data["price"], data["store_id"]
        else:
            # song.price = data["price"]
            #update the song
            pass

        song.save_to_db()

        return song.json()

class SongList(Resource):
    def get(self):
        return {"songs": [song.json() for song in SongModel.find_all()]}
