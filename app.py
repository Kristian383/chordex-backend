from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister, User
from resources.artist import Artist,ArtistList
from resources.song import Song,SongList

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = "kiki"

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(ArtistList, "/artists")
api.add_resource(Artist, "/artist/<string:name>")
api.add_resource(SongList, "/songs")
api.add_resource(Song, "/song/<string:name>")
# api.add_resource(User, "/user/<string:username>")








if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000)