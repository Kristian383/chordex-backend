from collections import UserList
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from datetime import datetime
from datetime import timedelta
from datetime import timezone

# from flask_jwt import JWT
# from security import authenticate, identity

from resources.user import UserRegister, User, UserList, UserLogin , UserLogout, TokenRefresh
from resources.artist import Artist, ArtistList, ArtistUserList
from resources.song import Song, SongList, UsersSongList, MusicKeys
from resources.website import Website, WebsiteList
from resources.user_notes import UserNotes, UserNotesList

from db import db
from blocklist import BLOCKLIST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
# app.config["JWT_COOKIE_SECURE"] = True                                     ###staviti true
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "kiki"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# app.config['JWT_AUTH_URL_RULE'] = '/login'        #jwt flask

#app.secret_key = "kiki"           #ovo iz env vaditi

api = Api(app)

CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()


# jwt = JWT(app, authenticate, identity)             # vraca access token
jwt = JWTManager(app)             # vraca access token

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    return jti in BLOCKLIST

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response

        
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

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

##ROUTES

# @app.route("/login2", methods=["POST"])
# def login2():
#     response = jsonify({"msg": "login successful"})
#     access_token = create_access_token(identity="example_user")
#     set_access_cookies(response, access_token)
#     return response

api.add_resource(UserRegister, "/register")
api.add_resource(UserList, "/users")
api.add_resource(User, "/user/<int:user_id>")

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(TokenRefresh, '/refresh')


# vraca sve userove artiste s pjesmama
api.add_resource(ArtistList, "/artists")
# ispisuje sve pjesme odredenog artista   (za odredenog usera)
api.add_resource(ArtistUserList, "/artist/<string:username>")
# ispisuje sve pjesme artista odredenog usera
api.add_resource(Artist, "/artist/<string:name>")

api.add_resource(SongList, "/songs")
api.add_resource(MusicKeys, "/keys")
api.add_resource(UsersSongList, "/songs/<string:username>")
api.add_resource(Song, "/song/<string:username>")
# api.add_resource(Song, "/song/<int:user_id>")

# ovo sluzi za ubacivanje webvssite linkova
api.add_resource(Website, "/website/<string:username>")
# dohvacanje svih websiteova od usera
api.add_resource(WebsiteList, "/websites/<string:username>")
#api.add_resource(WebsiteList, "/websites")

# api.add_resource(UserNotesList, "/notes")   #provjera za developera
api.add_resource(UserNotes, "/notes/<string:username>")


# api.add_resource(User, "/user/<string:username>")


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000)
