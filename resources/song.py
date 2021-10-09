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
    parser.add_argument('first_key',
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

        artist = ArtistModel.find_by_name(data["artist"], user_id)

        if artist is None:
            artist = ArtistModel(data["artist"], user_id)
            try:
                artist.save_to_db()
            except:
                return {"message": "An error occured inserting an artist."}, 500

        song = SongModel(data["name"], artist.id, user_id)
        try:
            song.save_to_db()
        except:
            return {"message": "An error occured inserting a song."}, 500
        return song.json(), 201

    def delete(self,  username):
        # omoguciti kaskadno brisanje artista ako nema vise pjesama
        data = Song.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(data["name"], user_id)
        if song:
            try:
                song.delete_from_db()
                return {'message': 'Song deleted'}
            except:
                return {"message": "An error occured deleting the song."}, 500
        else:
            return {'message': 'Song doesnt exist'}, 400

    def put(self, username):
        data = Song.parser.parse_args()

        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(data["name"], user_id)

        if song is None:
            artist = ArtistModel.find_by_name(data["artist"], user_id)
            # ili data["price"], data["store_id"]
            song = SongModel(data["name"], artist.id, user_id)
        else:
            # song.price = data["price"]
            # update the song
            song.first_key = data["first_key"]

        try:
            song.save_to_db()
            return {'message': 'Song updated', "updated": song.json()}, 200
        except:
            return {"message": "An error occured deleting the song."}, 500


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
