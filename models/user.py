from enum import unique
from db import db
from werkzeug.security import generate_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os

from dotenv import load_dotenv
load_dotenv()


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    songs = db.relationship("SongModel", lazy="dynamic", cascade="all,delete")
    websites = db.relationship("WebsiteModel", lazy="dynamic", cascade="all,delete")

    def json(self):
        return {"username": self.username,
                "id": self.id,
                "email": self.email,
                "songs": [song.json() for song in self.songs.all()],
                "websites": [website.json() for website in self.websites.all()]
                }

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.email = email

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_reset_pass_token(cls, user_id, expires_sec=1800):
        secret = os.environ.get("SECRET_KEY")
        pass_hash = cls.find_by_id(user_id).password
        s = Serializer(secret+pass_hash, expires_sec)
        token = s.dumps({"user_id": user_id}).decode("utf-8")
        return token

    @classmethod
    def verify_reset_pass_token(cls, token, email):
        user = cls.find_by_email(email)
        if not user:
            return None
        secret = os.environ.get("SECRET_KEY")+user.password
        s = Serializer(secret)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None

        return cls.find_by_id(user_id)

    def count_all_user_songs(self):
        return len(self.songs.all())

    def userHasBenefits(self):
        if self.id in [1,2]:
            return True
        return False
        

