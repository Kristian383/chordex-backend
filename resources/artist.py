from models.song import SongModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.artist import ArtistModel
from models.user import UserModel
from flask import request


class Artist(Resource):
    parser = reqparse.RequestParser()
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
    # parser.add_argument('order',
    #                     type=int,
    #                     required=True,
    #                     help="Every item needs a store id!"
    #                     )

    # @jwt_required()
    #nece nam trebati ovo 
    def get(self, name):
        data = Artist.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]

        artist = ArtistModel.find_by_name(name, user_id)

        if artist:
            return artist.json()

        return {"message": "No songs by artist {}".format(name)}, 400

    def post(self, name):
        data = Artist.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]
        if ArtistModel.find_by_name(name, user_id):
            return {'message': "An artist with name '{}' already exists.".format(name)}, 400

        artist = ArtistModel(name, user_id)

        try:
            artist.save_to_db()
        except:
            return {"message": "An error occured inserting the artist."}, 500
        return artist.json(), 201

    def delete(self, name):
        data = Artist.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]

        artist = ArtistModel.find_by_name(name, user_id)
        if artist:
            try:
                artist.delete_from_db()
            except:
                return {"message": "An error occured deleting the artist."}, 500
        else:
            return {'message': 'Artist doesnt exist'},400
        return {'message': 'Artist deleted'}


class ArtistList(Resource): #get all users artists     with their songs
    parser = reqparse.RequestParser()
    # parser.add_argument('username',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    def get(self,username):
        # data = ArtistList.parser.parse_args()
        #user = UserModel.find_by_username(data["username"])
        numOfLoads = int(request.args["numOfLoads"])
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User with that username doesn't exist"}, 400


        return {"artists": [artist.json() for artist in ArtistModel.find_all_user_artists(user.id,numOfLoads)]}


class ArtistUserList(Resource):       #ovo vraca pjesme jednog artista 
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('artist',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # @jwt_required()
    def get(self, username):
        data = ArtistUserList.parser.parse_args()
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(data["username"]).json()["id"]

        artist = ArtistModel.find_by_name(data["artist"], user_id)

        if artist is None:
            return {'message': "An artist with name '{}' doesn't exist.".format(data["artist"])}, 400

        return {"songs": [song.json() for song in SongModel.find_all_user_songs_by_artist(user_id, artist.id)],
                "artist": artist.name
                }  # vraca all songs by artist
