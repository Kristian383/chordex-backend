
from db import db
import requests
from sqlalchemy import func
import logging

class ArtistModel(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    songs = db.relationship("SongModel", lazy="dynamic",cascade="all,delete")
                 
    img_url = db.Column(db.String(80))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        return {"name": self.name,
                "artistId": self.id,
                "userId": self.user_id,
                "artistImg": self.img_url
                # "songs": [song.json() for song in self.songs.all()],
                }

    def getArtistInfo(self):
        return {
            "name": self.name,
            "artistId": self.id,
            "userId": self.user_id,
            "artistImg": self.img_url
        }

    def check_songs(self):
        return [song.json() for song in self.songs.all()]

    @classmethod
    def find_by_name(cls, name, user_id):
        # return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()
        return cls.query.filter_by(user_id=user_id).filter(func.lower(cls.name) == func.lower(name)).first()

    @classmethod
    def find_by_id(cls, artist_id, user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(id=artist_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def insertImgUrl(self, token):
        if not token:
            return "expired"

        url = f"https://api.spotify.com/v1/search?q=artist:{self.name}&type=artist&limit=1"
        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            
            data = response.json()
            img_url = data["artists"]["items"][0]["images"][1]["url"]
            
            self.img_url = img_url
            self.save_to_db()

        except (requests.RequestException, KeyError, IndexError) as e:
            logging.error(f"Error fetching or processing image URL: {e}")
            return "expired"

    @classmethod
    def find_all_user_artists(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
