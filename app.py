from collections import UserList
from flask import Flask  # , jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from datetime import timedelta


from resources.user import UserRegister, User, UserList, UserLogin
from resources.artist import ArtistList, ArtistUserList
from resources.song import Song, SongList, UsersSongList, MusicKeys
from resources.website import Website, WebsiteList
from resources.user_notes import UserNotes
from resources.mails import ForgotPassword, ContactMe, PasswordReset

from db import db
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# app.config["EMAIL_PASSWORD"]=os.environ.get("EMAIL_PASS")
# app.config["EMAIL_ADRESS"]=os.environ.get("EMAIL_USER")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

api = Api(app)
#mail = Mail(app)

CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

# ROUTES
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, '/login')
api.add_resource(ForgotPassword, '/forgotpassword')
api.add_resource(PasswordReset, '/resetpassword/<string:token>')
api.add_resource(ContactMe, '/contactme')

# get all user artists with artist info
api.add_resource(ArtistList, "/artists/<string:username>")

# all songs by artist from certain user   (za odredenog usera)
api.add_resource(ArtistUserList, "/artist/<string:username>")

api.add_resource(MusicKeys, "/keys")
api.add_resource(UsersSongList, "/songs/<string:username>")
api.add_resource(Song, "/song/<string:username>")

# oinserting and deleting websites
api.add_resource(Website, "/website/<string:username>")

# get all users websites
api.add_resource(WebsiteList, "/websites/<string:username>")

api.add_resource(UserNotes, "/notes/<string:username>")

# admin routes
# api.add_resource(User, "/user/<string:username>")
# api.add_resource(UserNotesList, "/notes")   #provjera za developera
# api.add_resource(UserList, "/users") #all users
# api.add_resource(User, "/user/<int:user_id>")#samo za postman koristim
#api.add_resource(SongList, "/songs")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000)

# @jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(jwt_header, jwt_payload):
#     jti = jwt_payload["jti"]

#     return jti in BLOCKLIST

# @jwt.expired_token_loader
# def expired_token_callback():
#     return jsonify({
#         'message': 'The token has expired.',
#         'error': 'token_expired'
#     }), 401

# @jwt.invalid_token_loader
# def invalid_token_callback(error):
#     return jsonify({
#         'message': 'Signature verification failed.',
#         'error': 'invalid_token'
#     }), 401

# @jwt.unauthorized_loader
# def missing_token_callback(error):
#     return jsonify({
#         "description": "Request does not contain an access token.",
#         'error': 'authorization_required'
#     }), 401

# @jwt.revoked_token_loader
# def revoked_token_callback():
#     return jsonify({
#         "description": "The token has been revoked.",
#         'error': 'token_revoked'
#     }), 401
