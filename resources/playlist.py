from models.playlist import PlaylistModel
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.song import SongModel
from flask_jwt_extended import jwt_required, get_jwt_identity

## Add, delete, get, change playlist
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

    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only get playlists for your own account."}, 403
        
        playlists = [playlist.name for playlist in PlaylistModel.find_all_user_playlists(user.id)]
        return { "playlists": playlists }
    
    @jwt_required()
    def post(self, email):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only add playlist for your own account."}, 403

        name = data['playlist_name']
        if not name:
            return {"message": "Playlist name is missing"}, 400

        if user.userHasBenefits() == False and len(PlaylistModel.find_all_user_playlists(user.id)) >= 4:
            return {"message": "Limit of playlists exceeded"}, 403

        if PlaylistModel.find_by_name(user.id, name):
            return {"message": "Playlist with that name already exists"}, 400

        playlist = PlaylistModel(name, user.id)

        try:
            playlist.save_to_db()
        except:
            return {"message": "An error occured inserting a playlist."}, 500
        return {'message': f'Playlist {playlist.name} created successfully'}, 201
    
    @jwt_required()
    def delete(self, email):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(email)
        name = data['playlist_name']
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only delete playlist for your own account."}, 403

        existing_playlist = PlaylistModel.find_by_name(user.id, name)
        if not existing_playlist:
            return {"message": "Playlist with that name not found"}, 404

        if existing_playlist:
            try:
                existing_playlist.delete_from_db()
            except:
                return {"message": "An error occured deleting a playlist."}, 500
        return {'message': f'Playlist {existing_playlist.name} deleted successfully'}, 201

    @jwt_required()
    def put(self, email):
        data = Playlists.parser.parse_args()
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only change playlist name for your own account."}, 403

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
        
## Lists all songs in a specific playlist
class PlaylistSongs(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('song_id', type=int, required=False, help="This field cannot be left blank.")
    
    @jwt_required()
    def get(self, email, playlistName):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only get songs in playlist for your own account."}, 403

        playlist = PlaylistModel.find_by_name(user.id, playlistName)
        if playlist:
            return {"songs": [song.id for song in playlist.songs.all()]}
        return {"message": "Playlist not found"}, 404

    @jwt_required()
    def post(self, email, playlistName):
        data = PlaylistSongs.parser.parse_args();
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': 'User not found'}, 404

        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only add songs in playlist for your own account."}, 403

        playlist = PlaylistModel.find_by_name(user.id, playlistName)
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
        return {'message': f'{song.name} added to the playlist "{playlist.name}" successfully.'}, 201

    @jwt_required()
    def delete(self, email, playlistName):
        data = PlaylistSongs.parser.parse_args()
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only delete songs in playlist for your own account."}, 403

        playlist = PlaylistModel.find_by_name(user.id, playlistName)
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
    
## Lists all playlists that contain a specific song
class SongInPlaylists(Resource):
    @jwt_required()
    def get(self, email, songId):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User not found"}, 404
        
        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only get song playlists for your own account."}, 403
        
        playlists = PlaylistModel.find_all_playlists_of_a_song(user.id, songId)
        filtered_playlists = [playlist.name for playlist in playlists]
        return {"playlists": filtered_playlists}