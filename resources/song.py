from flask_restful import Resource, reqparse
from models.song import SongModel
from models.artist import ArtistModel
from models.user import UserModel


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
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name, username):
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(name, user_id)

        if song:
            return song.json()
        return name

    def post(self, username):
        data = Song.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        if SongModel.find_by_name(data["name"], user_id):
            return {'message': "An song with name '{}' already exists.".format(data["name"])}, 400

        # return data
        # check if there is artist already in database

        # data = Song.parser.parse_args()
        artist = ArtistModel.find_by_name(data["artist"],user_id)

        if artist is None:
            #make an artist
            artist=ArtistModel(data["artist"])
            pass



        song = SongModel(data["name"], artist.id,user_id)
        try:
            song.save_to_db()
        except:
            return {"message": "An error occured inserting a song."}, 500
        return song.json(), 201

        # return {"message":"found artist id '{}'".format(song.json())}
        # find artist id from database to make song object

    def delete(self, name, username):
        # ovo poboljsati u slucaju ako ima vise pjesama sa istim imenom
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(name, user_id)
        if song:
            try:
                song.delete_from_db()
            except:
                return {"message": "An error occured deleting the song."}, 500

        return {'message': 'Song deleted'}

    def put(self, name, username):
        data = Song.parser.parse_args()

        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(name, user_id)

        if song is None:
            # ili data["price"], data["store_id"]
            song = SongModel(name, **data)
        else:
            # song.price = data["price"]
            # update the song
            pass

        song.save_to_db()

        return song.json()


class SongList(Resource):
    def get(self):
        return {"songs": [song.json() for song in SongModel.find_all()]}


class UsersSongList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def get(self, username):
        #data = UsersSongList.parser.parse_args()
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]
        return {"songs": [song.json() for song in SongModel.find_all_user_songs(user_id)]}
