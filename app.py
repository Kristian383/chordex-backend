from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta

from resources.user import UserRegister,  UserLogin, FirebaseAuth, PasswordReset, DeleteAccount
from resources.artist import ArtistList
from resources.song import Song, MusicKeys, SpotifyInfo, UsersPaginatedSongList
from resources.website import Website, WebsiteList
from resources.user_notes import UserNotes
from resources.mails import ForgotPassword, ContactMe, DeleteAccountRequest
from resources.playlist import Playlists, PlaylistSongs, SongInPlaylists

import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials


load_dotenv()  # Load environment variables from a .env file if present

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=28)

# Initialize extensions
db = SQLAlchemy(app)
api = Api(app)

CORS(app)
jwt = JWTManager(app)

# firebase auth
cred = credentials.Certificate("./service-account-file.json")
default_app = firebase_admin.initialize_app(cred)

# ROUTES
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, '/login')
api.add_resource(FirebaseAuth, '/firebase')
api.add_resource(DeleteAccountRequest, '/delete-acc-request')
api.add_resource(DeleteAccount, '/delete-acc/<string:token>')

api.add_resource(ForgotPassword, '/forgotpassword')
api.add_resource(PasswordReset, '/resetpassword/<string:token>')
api.add_resource(ContactMe, '/contactme')

api.add_resource(SpotifyInfo, '/spotifyaccess')
api.add_resource(ArtistList, "/artists/<string:email>")

# all songs by artist from certain user   (for specific user)
# api.add_resource(ArtistUserList, "/artist/<string:email>")

api.add_resource(MusicKeys, "/keys")
# api.add_resource(UsersSongList, "/songs/<string:email>") # this is replaced with /songs-paginated
api.add_resource(UsersPaginatedSongList, "/songs-paginated/<string:email>") # /songs-paginated/<string:email>?offset=10&limit=20
api.add_resource(Song, "/song/<string:email>")
api.add_resource(Playlists, "/playlists/<string:email>")
api.add_resource(PlaylistSongs, "/playlist/<string:email>/<string:playlistName>")
api.add_resource(SongInPlaylists, "/song-playlists/<string:email>/<int:songId>")

# inserting and deleting websites
api.add_resource(Website, "/website/<string:email>")

# get all users websites
api.add_resource(WebsiteList, "/websites/<string:email>")

api.add_resource(UserNotes, "/notes/<string:email>")

# admin routes
# api.add_resource(User, "/user/<string:username>")
# api.add_resource(UserNotesList, "/notes")
# api.add_resource(UserList, "/users")
# api.add_resource(User, "/user/<int:user_id>")
#api.add_resource(SongList, "/songs")

if __name__ == "__main__":
    # db.init_app(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
