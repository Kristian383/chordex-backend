from db import db

playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class PlaylistModel(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    songs = db.relationship('SongModel', secondary=playlist_songs, backref='playlists', lazy="dynamic")
    
    def __init__(self, name, user_id):
       self.name = name
       self.user_id = user_id

    def json(self):
        return {
            "name": self.name,
            "id": self.id,
            "user_id": self.user_id,
            "songs": [song.id for song in self.songs]
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_user_playlists(cls, _user_id):
        return cls.query.filter_by(user_id=_user_id).all()
    
    @classmethod
    def find_all_playlists_of_a_song(cls, _user_id, _songId):
        return cls.query.filter_by(user_id=_user_id).filter(cls.songs.any(id=_songId)).all()
    
    @classmethod
    def find_by_name(cls, _user_id, _name):
        return cls.query.filter_by(user_id=_user_id).filter_by(name = _name).first()