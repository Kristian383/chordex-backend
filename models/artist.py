
from db import db
# from models.song import SongModel

class ArtistModel(db.Model):
    __tablename__ = "artist"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    songs = db.relationship("SongModel",lazy="dynamic")  # this will be list of different songs         #llazy dynamic omogucuje songs.all()
    total_songs = db.Column(db.Integer)
    order = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name,
                "total_songs": self.total_songs,
                "artist_id": self.id,
                "songs": [song.json() for song in self.songs.all()],
                "order": self.order}

    @classmethod
    def find_by_name(cls, name):
        # "SELECT * FROM items WHERE name=name LIMIT 1"
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
