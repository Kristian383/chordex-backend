
from sqlalchemy.sql.functions import user
from db import db
from sqlalchemy.sql import func

from models.artist import ArtistModel
from sqlalchemy import func


    
class SongModel(db.Model):
    __tablename__ = "song"

    # sve null moze osim name i artista
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # ovo artist prepoznaje jer je u artistModel to tablename?
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))

    first_key = db.Column(db.String(20))
    first_key_notes = db.Column(db.String(30))
    first_chord_progression = db.Column(db.String(40))
    second_key = db.Column(db.String(20))
    second_key_notes = db.Column(db.String(30))
    second_chord_progression = db.Column(db.String(40))

    learned_prcntg = db.Column(db.Integer)
    is_favorite = db.Column(db.Boolean)
    is_my_song = db.Column(db.Boolean)
    bpm = db.Column(db.Integer)
    capo = db.Column(db.Integer)
    song_text = db.Column(db.String(15000))  # ovo su song notes pa povecati vjv
    yt_link = db.Column(db.String(150))
    chords_website_link = db.Column(db.String(150))
    acoustic = db.Column(db.Boolean)
    electric = db.Column(db.Boolean)
    difficulty = db.Column(db.String(10))
    tuning = db.Column(db.String(20))

    # sql alchemy kreira date automatski, ali ovo treba u put azurirati
    last_viewed = db.Column(db.String(40))

    def __init__(self, name,
                 artist_id,
                 user_id,
                 first_key=None,
                 first_key_notes=None,
                 first_chord_progression=None,
                 second_key=None,
                 second_key_notes=None,
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
                 tuning=None,
                 last_viewed=None,
                 ):
        self.name = name
        self.artist_id = artist_id
        self.user_id = user_id
        self.first_key = first_key
        self.first_key_notes=first_key_notes
        self.first_chord_progression = first_chord_progression
        self.second_key = second_key
        self.second_key_notes = second_key_notes
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
        self.tuning = tuning
        self.last_viewed = last_viewed

    def json(self):
        return {"songName": self.name,
                "songId": self.id,
                "artistId": self.artist_id,
                "userId": self.user_id,
                "firstKey": self.first_key,
                "firstKeyNotes": self.first_key_notes,
                "firstChordProgression": self.first_chord_progression,
                "secondKey": self.second_key,
                "secondKeyNotes": self.second_key_notes,
                "secondChordProgression": self.second_chord_progression,
                "practicedPrcntg": self.learned_prcntg,
                "isFavorite": self.is_favorite,
                "isMySong": self.is_my_song,
                "bpm": self.bpm,
                "songText": self.song_text,
                "ytLink": self.yt_link,
                "chordsWebsiteLink": self.chords_website_link,
                "acoustic": self.acoustic,
                "electric": self.electric,
                "difficulty": self.difficulty,
                "capo": self.capo,
                "tuning": self.tuning,
                "lastViewed": self.last_viewed
                }


    # @classmethod
    # def find_artist_name(cls):
    #     name=ArtistModel.query.all() 
    #     return  name
        #().filter_by(id=artist_id).first()
        
    #poboljšati da je moguce ista pjesma ali razliciti artisti 
    @classmethod
    def find_by_name(cls, name, user_id):
        # "SELECT * FROM items WHERE name=name LIMIT 1"
        return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()

    @classmethod
    def checkIfArtistHasSong(cls, artist_id, user_id,name):
        return cls.query.filter_by(user_id=user_id).filter_by(id=artist_id).filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, song_id,user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(id=song_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_user_songs(cls, user_id,load_number):
        #starting_index=load_number*20
        skip=0
        if load_number!=1:
            skip=(load_number-1)*2
        return cls.query.filter_by(user_id=user_id).order_by(cls.last_viewed.desc()).limit(2).offset(skip)
        #.limit(page_size).offset(skip)

    # @classmethod
    # def find_all_user_songs_by_desc_order(cls, user_id):
    #     return cls.query.filter_by(user_id=user_id).desc()

    # @classmethod
    # def find_all_user_songs_by_asc_order(cls, user_id):
    #     return cls.query.filter_by(user_id=user_id).asc()

    @classmethod
    def find_all_user_my_songs(cls, user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(is_my_song=True)

    @classmethod
    def find_all_user_songs_by_artist(cls, user_id, artist_id):
        return cls.query.filter_by(user_id=user_id).filter_by(artist_id=artist_id)

    @classmethod
    def count_all_user_songs_by_artist(cls, user_id, artist_id):
        return cls.query.filter_by(user_id=user_id).filter_by(artist_id=artist_id).count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
