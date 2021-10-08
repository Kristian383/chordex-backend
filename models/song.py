
from sqlalchemy.sql.functions import user
from db import db
from sqlalchemy.sql import func


class SongModel(db.Model):
    __tablename__ = "song"

    # sve null moze osim name i artista
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False) 
    name = db.Column(db.String(80))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))       #ovo artist prepoznaje jer je u artistModel to tablename?

    first_key = db.Column(db.String(30))
    first_chord_progression = db.Column(db.String(80))
    second_key = db.Column(db.String(80))
    second_chord_progression = db.Column(db.String(80))
    # first_key_notes = db.Column(db.String(80))       #ovo imamo na frontendu
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

    # sql alchemy kreira date automatski, ali ovo treba u put azurirati
    # last_viewed = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, name,
                 artist_id,
                 user_id,
                 first_key=None,
                 first_chord_progression=None,
                 second_key=None,
                 second_chord_progression=None,
                 learned_prcntg=None,
                 is_favorite=None,
                 is_my_song=None,
                 bpm=None,
                 capo=None,
                 song_text=None,
                 yt_link=None,
                 chords_website_link=None,
                 acoustic=None,
                 electric=None,
                 difficulty=None,
                 
                 last_viewed=None,
                 ):
        self.name = name
        self.artist_id = artist_id
        self.user_id = user_id
        self.first_key = first_key
        self.first_chord_progression = first_chord_progression
        self.second_key = second_key
        self.second_chord_progression = second_chord_progression
        self.learned_prcntg = learned_prcntg
        self.is_favorite = is_favorite
        self.is_my_song = is_my_song
        self.bpm = bpm
        self.song_text = song_text
        self.yt_link = yt_link
        self.chords_website_link = chords_website_link
        self.acoustic = acoustic
        self.electric = electric
        self.difficulty = difficulty
        self.capo = capo
        # self.last_viewed = last_viewed

    def json(self):
        return {"name": self.name,
                "artist_id": self.artist_id,
                "user_id": self.user_id,
                "first_key": self.first_key,
                "first_chord_progression": self.first_chord_progression,
                "second_key": self.second_key,
                "second_chord_progression": self.second_chord_progression,
                "learned_prcntg": self.learned_prcntg,
                "is_favorite": self.is_favorite,
                "is_my_song": self.is_my_song,
                "bpm": self.bpm,
                "song_text": self.song_text,
                "yt_link": self.yt_link,
                "chords_website_link": self.chords_website_link,
                "acoustic": self.acoustic,
                "electric": self.electric,
                "difficulty": self.difficulty,
                "capo": self.capo,
                # "last_viewed": self.last_viewed
                }

    @classmethod
    def find_by_name(cls, name,user_id):
        # "SELECT * FROM items WHERE name=name LIMIT 1" 
        return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_user_songs(cls,user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
