
from db import db

class ArtistModel(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    songs = db.relationship("SongModel", lazy="dynamic", cascade="all")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        return {"name": self.name,
                "artistId": self.id,
                "userId": self.user_id,
                "songs": [song.json() for song in self.songs.all()],
                }

    def getArtistInfo(self):
        return {
            "name": self.name,
            "artistId": self.id,
            "userId": self.user_id,
        }

    def check_songs(self):
        return [song.json() for song in self.songs.all()]

    @classmethod
    def find_by_name(cls, name, user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()
    

    @classmethod
    def find_by_id(cls, artist_id,user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(id=artist_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_user_artists(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
