from enum import unique
from db import db
from werkzeug.security import generate_password_hash

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(580))

    number_of_songs=db.Column(db.Integer)
    number_of_my_songs=db.Column(db.Integer)
    number_of_artists=db.Column(db.Integer)

    def json(self):
        return {"username": self.username,
                "id": self.id,
                "email": self.email,
                "number_of_songs": self.number_of_songs,
                "number_of_my_songs": self.number_of_my_songs,
                "number_of_artists": self.number_of_artists,
                }

    def __init__(self, username, password,email):
        self.username = username
        self.password = generate_password_hash(password,method="sha256")
        self.email= email

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
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
