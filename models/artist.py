
from db import db
# from models.song import SongModel
# class ArtistUserModel(db.Model):
#     __tablename__ = "artist_user"
#     id = db.Column(db.Integer, primary_key=True)
#     artist_id=db.Column(db.Integer, db.ForeignKey('artist.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     songs = db.relationship("SongModel",lazy="dynamic")  
#     total_songs = db.Column(db.Integer)
#     order = db.Column(db.Integer)

#     def __init__(self, artist_id,user_id):
#         self.artist_id = artist_id
#         self.user_id = user_id

#     @classmethod
#     def find_all(cls):
#         return cls.query.all()

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

class ArtistModel(db.Model):
    __tablename__ = "artist"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80))
    songs = db.relationship("SongModel",lazy="dynamic", cascade="all")  
    total_songs = db.Column(db.Integer)
    order = db.Column(db.Integer)

    def __init__(self, name,user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        return {"name": self.name,
                "totalSongs": self.total_songs,
                "artistId": self.id,
                "userId": self.user_id,
                "songs": [song.json() for song in self.songs.all()],
                "order": self.order
                }
    def check_songs(self):
        return   [song.json() for song in self.songs.all()]

    @classmethod
    def find_by_name(cls, name,user_id):
        # "SELECT * FROM items WHERE name=name LIMIT 1"
        return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, artist_id,user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(id=artist_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all(cls,user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
