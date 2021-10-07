
from db import db
from sqlalchemy.sql import func

class SongModel(db.Model):
    __tablename__ = "song"

    # sve null moze osim name i artista
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))

    first_key = db.Column(db.String(30))
    first_chord_progression = db.Column(db.String(80))
    # first_key_notes = db.Column(db.String(80))       #ovo imamo na frontendu
    second_key = db.Column(db.String(80))
    second_chord_progression = db.Column(db.String(80))
    # second_key_notes = db.Column( #  db.String(80), db.ForeignKey("musickey.notes"))    #ovo imamo na frontendu

    learned_prcntg = db.Column(db.Integer)
    is_favorite = db.Column(db.Boolean)
    is_my_song = db.Column(db.Boolean)
    bpm = db.Column(db.Integer)
    capo = db.Column(db.Integer)
    song_text = db.Column(db.String(8000))  # ovo su song notes pa povecati vjv
    yt_link = db.Column(db.String(200))
    chords_website_link = db.Column(db.String(200))
    acoustic = db.Column(db.Boolean)
    electric = db.Column(db.Boolean)
    difficulty = db.Column(db.String(80))

    # name = db.Column(db.String(80))
    # name = db.Column(db.String(80))
    # sql alchemy kreira date automatski, ali ovo treba u put azurirati
    last_viewed = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, name,
    artist_id,
    first_key=None,
    first_chord_progression=None,
    ):
        self.name = name
        self.artist_id = artist_id
        self.first_key = first_key
        self.first_chord_progression = first_chord_progression
        

    def json(self):
        return {"name": self.name,
                "artist_id": self.artist_id,
                "first_key": self.first_key,
                "first_chord_progression": self.first_chord_progression,
                }

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
