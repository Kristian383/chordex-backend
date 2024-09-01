from models.song import SongModel
from flask_restful import Resource  # , reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.artist import ArtistModel
from models.user import UserModel
# from flask import request

# get all users artists with their info
class ArtistList(Resource):
    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User with that email doesn't exist"}, 400
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only request artists for your own account."}, 403

        artists = [artist.getArtistInfo()
                   for artist in ArtistModel.find_all_user_artists(user.id)]
        for artist in artists:
            artist_id = artist["artistId"]
            artist["totalSongs"] = SongModel.count_all_user_songs_by_artist(
                user.id, artist_id)

        return {"artists": artists}

# test routes

# class Artist(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('artist',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('username',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )

#     def post(self, name):
#         data = Artist.parser.parse_args()
#         user = UserModel.find_by_username(data["username"])
#         if not user:
#             return {"message": "User with that username doesn't exist"}, 400

#         user_id = UserModel.find_by_username(data["username"]).json()["id"]
#         if ArtistModel.find_by_name(name, user_id):
#             return {'message': "An artist with name '{}' already exists.".format(name)}, 400

#         artist = ArtistModel(name, user_id)

#         try:
#             artist.save_to_db()
#         except:
#             return {"message": "An error occured inserting the artist."}, 500
#         return artist.json(), 201

#     def delete(self, name):
#         data = Artist.parser.parse_args()
#         user = UserModel.find_by_username(data["username"])
#         if not user:
#             return {"message": "User with that username doesn't exist"}, 400

#         user_id = UserModel.find_by_username(data["username"]).json()["id"]

#         artist = ArtistModel.find_by_name(name, user_id)
#         if artist:
#             try:
#                 artist.delete_from_db()
#             except:
#                 return {"message": "An error occured deleting the artist."}, 500
#         else:
#             return {'message': 'Artist doesnt exist'}, 400
#         return {'message': 'Artist deleted'}


# class ArtistUserList(Resource):  # ovo vraca pjesme jednog artista
#     parser = reqparse.RequestParser()
#     parser.add_argument('email',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     parser.add_argument('artist',
#                         type=str,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#     # @jwt_required()
#     def get(self, email):
#         data = ArtistUserList.parser.parse_args()
#         user = UserModel.find_by_email(email)
#         if not user:
#             return {"message": "User with that email doesn't exist"}, 400

#         artist = ArtistModel.find_by_name(data["artist"], user.id)

#         if artist is None:
#             return {'message': "An artist with name '{}' doesn't exist.".format(data["artist"])}, 400

#         return {"songs": [song.json() for song in SongModel.find_all_user_songs_by_artist(user.id, artist.id)],
#                 "artist": artist.name
#                 }  # vraca all songs by artist
