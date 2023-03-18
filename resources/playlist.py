from models.playlist import PlaylistModel
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.song import SongModel

class Playlists(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('playlist_name',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('new_playlist_name',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def get(self):
        data = Playlists.parser.parse_args();
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404
        
        playlists = [playlist.name for playlist in PlaylistModel.find_all_user_playlists(user.id)]
        return { "playlists": playlists }
    
    def post(self):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 400
        name = data['playlist_name']
        if not name:
            return {"message": "Playlist name is missing"}, 400
        if PlaylistModel.find_by_name(user.id, name):
            return {"message": "Playlist with that name already exists"}, 400
        playlist = PlaylistModel(name, user.id)
        try:
            playlist.save_to_db()
        except:
            return {"message": "An error occured inserting a playlist."}, 500
        return {'message': f'Playlist {playlist.name} created successfully'}, 201
    
    def delete(self):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        name = data['playlist_name']
        if not user:
            return {"message": "User not found"}, 400
        existing_playlist = PlaylistModel.find_by_name(user.id, name)
        if not existing_playlist:
            return {"message": "Playlist with that name not found"}, 404
        if existing_playlist:
            try:
                existing_playlist.delete_from_db()
            except:
                return {"message": "An error occured deleting a playlist."}, 500
        return {'message': f'Playlist {existing_playlist.name} deleted successfully'}, 201

    def put(self):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 400

        name = data['playlist_name']
        new_name = data['new_playlist_name']
        if not name and not new_name:
            return {"message": "Playlist name is missing"}, 400
        if PlaylistModel.find_by_name(user.id, new_name):
            return {"message": "Playlist with that name already exists"}, 400

        existing_playlist = PlaylistModel.find_by_name(user.id, name)
        if not existing_playlist:
            return {"message": "Playlist with that name not found"}, 404
        try:
            existing_playlist.name = new_name
            existing_playlist.save_to_db()
            return {'message': f'Playlist is saved with a name {existing_playlist.name}'}
        except:
            return {"message": f"Failed to update playlist name from {name} to {new_name}"}, 500
        

class PlaylistSongs(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=False, help="This field cannot be left blank.")
    parser.add_argument('playlist_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def get(self):
        data = PlaylistSongs.parser.parse_args();
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404
        playlist = PlaylistModel.find_by_name(user.id, data["playlist_name"])
        if playlist:
            return {"songs": [song.id for song in playlist.songs.all()]}
        return {"message": "Playlist not found"}, 404

    def post(self):
        data = PlaylistSongs.parser.parse_args();
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {'message': 'User not found'}, 404

        playlist = PlaylistModel.find_by_name(user.id, data["playlist_name"])
        if not playlist:
            return {'message': 'Playlist not found.'}, 404

        song = SongModel.find_by_id(data['song_id'], user.id)
        if not song:
            return {'message': 'Song not found.'}, 404

        if song in playlist.songs:
            return {'message': 'Song already exists in the playlist.'}, 409
        try:
            playlist.songs.append(song)
            playlist.save_to_db()
        except:
            return {"message": "An error occured upon adding a song into the playlist."}, 500
        return {'message': 'Song added to the playlist successfully.'}, 201
    
    def delete(self):
        data = PlaylistSongs.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404
        playlist = PlaylistModel.find_by_name(user.id, data["playlist_name"])
        if not playlist:
            return {'message': 'Playlist not found.'}, 404
        song = SongModel.find_by_id(data['song_id'], user.id)
        playlist_songs = playlist.json()["songs"]
        if not song or song.id not in playlist_songs:
            return {'message': 'Song not found.'}, 404
        try:
            playlist.songs.remove(song)
            playlist.save_to_db()
        except:
            return {"message": "An error occured deleting a song from playlist."}, 500
        return {'message': f'Song deleted successfully from {playlist.name} playlist'}