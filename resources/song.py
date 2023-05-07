# import flask
# from flask.json import jsonify
from flask_restful import Resource, reqparse
from models.song import SongModel
from models.artist import ArtistModel
from models.user import UserModel
from flask_jwt_extended import jwt_required

from flask import request
import requests
import os
from dotenv import load_dotenv


load_dotenv()
spotify_access = ""


def refreshSpotifyAcess():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": "Basic " + os.environ.get("API_TOGETHER")},
    )
    try:
        global spotify_access
        spotify_access = response.json()["access_token"]
        return spotify_access
    except:
        return None


class MusicKeys(Resource):
    pitchClass = ["C", "C#", "D", "D#", "E",
                  "F", "F#", "G", "G#", "A", "A#", "B"]
    mode = ["minor", "major"]
    musicKeys = [
        {
            "key": "C",
            "relativeMinor": "A",
            "notes": ["C", "D", "E", "F", "G", "A", "B"],
        },
        {
            "key": "G",
            "relativeMinor": "E",
            "notes": ["G", "A", "B", "C", "D", "E", "F#"],
        },
        {
            "key": "D",
            "relativeMinor": "B",
            "notes": ["D", "E", "F#", "G", "A", "B", "C#"],
        },
        {
            "key": "A",
            "relativeMinor": "F#",
            "notes": ["A", "B", "C#", "D", "E", "F#", "G#"],
        },
        {
            "key": "E",
            "relativeMinor": "C#",
            "notes": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        },
        {
            "key": "B",
            "relativeMinor": "G#",
            "notes": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        },
        {
            "key": "F#",
            "relativeMinor": "D#",
            "notes": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
        },
        {
            "key": "C#",
            "relativeMinor": "A#",
            "notes": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
        },
        {
            "key": "F",
            "relativeMinor": "D",
            "notes": ["F", "G", "A", "Bb", "C", "D", "E"],
        },
        {
            "key": "Bb",
            "relativeMinor": "G",
            "notes": ["Bb", "C", "D", "Eb", "F", "G", "A"],
        },
        {
            "key": "Eb",
            "relativeMinor": "C",
            "notes": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        },
        {
            "key": "Ab",
            "relativeMinor": "F",
            "notes": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
        },
        {
            "key": "Db",
            "relativeMinor": "Bb",
            "notes": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
        },
        {
            "key": "Gb",
            "relativeMinor": "Eb",
            "notes": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
        },
        {
            "key": "Cb",
            "relativeMinor": "Ab",
            "notes": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
        },
    ]

    def get(self):
        return {"musicKeys": self.musicKeys}


class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "songName", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "artist", type=str, required=True, help="This field cannot be left blank!"
    )
    # parser.add_argument(
    #     "user_email", type=str, required=True, help="This field cannot be left blank!"
    # )
    parser.add_argument(
        "firstKey", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "firstKeyNotes",
        type=str,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "secondKeyNotes",
        type=str,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "firstChordProgression",
        type=str,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "secondKey", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "secondChordProgression",
        type=str,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "practicedPrcntg",
        type=int,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "isFavorite", type=bool, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "isMySong", type=bool, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "bpm", type=int, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "capo", type=int, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "songText", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "ytLink", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "chordsWebsiteLink",
        type=str,
        required=False,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "acoustic", type=bool, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "electric", type=bool, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "difficulty", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "tuning", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "lastViewed", type=str, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "songId", type=int, required=False, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "imgUrl", type=str, required=False, help="This field cannot be left blank!"
    )

    # def get(self, name, email):
    #     user = UserModel.find_by_email(email)

    #     if not user:
    #         return {"message": "User with that email doesn't exist"}, 400

    #     # user_id = UserModel.find_by_username(username).json()["id"]

    #     song = SongModel.find_by_name(name, user.id)

    #     if song:
    #         return song.json()
    #     return name

    # @jwt_required()

    def post(self, email):
        data = Song.parser.parse_args()
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400

        if user.userHasBenefits() == False and user.count_all_user_songs() >= 30:
            return {"message": "Limit of songs exceeded"}, 403

        artist = ArtistModel.find_by_name(data["artist"], user.id)

        if artist and SongModel.checkIfArtistHasSong(
            artist.id, user.id, data["songName"]
        ):

            return {
                "message": "Artist '{0}' already has a song with name '{1}'.".format(
                    data["artist"], data["songName"]
                )
            }, 400

        if artist is None:
            artist = ArtistModel(data["artist"], user.id)
            global spotify_access
            if (data["isMySong"] != True) and artist.insertImgUrl(
                spotify_access
            ) == "expired":
                print("token expired")
                spotify_access = refreshSpotifyAcess()
                artist.insertImgUrl(spotify_access)
            try:
                artist.save_to_db()
            except:
                return {"message": "An error occured inserting an artist."}, 500
        img_url = ""
        if data["imgUrl"] == "":
            img_url = artist.img_url
        else:
            img_url = data["imgUrl"]

        # try:
        #     artist.save_to_db()
        # except:
        #     return {"message": "An error occured inserting an artist img."}, 500

        song = SongModel(
            data["songName"],
            artist.id,
            user.id,
            data["firstKey"],
            data["firstKeyNotes"],
            data["firstChordProgression"],
            data["secondKey"],
            data["secondKeyNotes"],
            data["secondChordProgression"],
            data["practicedPrcntg"],
            data["isFavorite"],
            data["isMySong"],
            data["bpm"],
            data["capo"],
            data["songText"],
            data["ytLink"],
            data["chordsWebsiteLink"],
            data["acoustic"],
            data["electric"],
            data["difficulty"],
            data["tuning"],
            data["lastViewed"],
            img_url
            #  data["imgUrl"]
        )

        try:
            song.save_to_db()
        except:
            return {"message": "An error occured inserting a song."}, 500
        resp = artist.json()
        return {"song": song.json(), "artist": resp}, 201

    def put(self, email):
        data = Song.parser.parse_args()
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400
        song = SongModel.find_by_id(data["songId"], user.id)

        if song is None:
            return {"msg": "song is none"}
        else:
            song.name = data["songName"]
            song.first_key = data["firstKey"]
            song.first_notes = data["firstKeyNotes"]
            song.first_chord_progression = data["firstChordProgression"]
            song.second_key = data["secondKey"]
            song.second_key_notes = data["secondKeyNotes"]
            song.second_chord_progression = data["secondChordProgression"]
            song.learned_prcntg = data["practicedPrcntg"]
            song.is_favorite = data["isFavorite"]
            song.is_my_song = data["isMySong"]
            song.bpm = data["bpm"]
            song.capo = data["capo"]
            song.song_text = data["songText"]
            song.yt_link = data["ytLink"]
            song.chords_website_link = data["chordsWebsiteLink"]
            song.acoustic = data["acoustic"]
            song.electric = data["electric"]
            song.difficulty = data["difficulty"]
            song.tuning = data["tuning"]
            song.last_viewed = data["lastViewed"]
            song.img_url = data["imgUrl"]

        try:
            song.save_to_db()
            # artist.save_to_db()
            return {"message": "Song updated", "song": song.json()}, 200
        except:
            return {"message": "An error occured updating the song."}, 500

    def delete(self, email):
        data = Song.parser.parse_args()
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400

        artist = ArtistModel.find_by_name(data["artist"], user.id)
        song = SongModel.find_by_name(data["songName"], user.id, artist.id)
        if song:
            try:
                song.delete_from_db()
                if len(artist.check_songs()) == 0:
                    artist.delete_from_db()
                    return {"message": "Song and Artist deleted"}, 200

                return {"message": "Song deleted"}, 200
            except:
                return {"message": "An error occured deleting the song."}, 500
        else:
            return {"message": "Song doesnt exist"}, 400


class UsersSongList(Resource):
    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User with that email doesn't exist"}, 400
        songs = [
            song.json() for song in SongModel.find_all_user_songs(user.id)
        ] 

        for song in songs:
            artist = ArtistModel.find_by_id(song["artistId"], song["userId"])
            song["artist"] = artist.name
        return {"songs": songs}

class UsersPaginatedSongList(Resource):
    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=2, type=int)
        print("offset", offset)
        if not user:
            return {"message": "User with that email doesn't exist"}, 400
        songs = [
            song.json() for song in SongModel.find_user_songs_paginated(user.id, offset, limit)
        ] 
        for song in songs:
            artist = ArtistModel.find_by_id(song["artistId"], song["userId"])
            song["artist"] = artist.name
        return {"songs": songs}

# admin routes

class SongList(Resource):
    def get(self):
        return {"songs": [song.json() for song in SongModel.find_all()]}


class SpotifyInfo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "songName", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "artist", type=str, required=True, help="This field cannot be left blank!"
    )

    # def getArtistImg(self, artist, token):
    #     url = "https://api.spotify.com/v1/search?q=artist:"+artist+"&type=artist&limit=1"
    #     response = requests.get(
    #         url, headers={'Authorization': 'Bearer '+token})
    #     if response.ok:
    #         return response.json()["artists"]["items"][0]["images"][-1]["url"]

    def getTrackInfo(self, song, artist, token):
        url = (
            "https://api.spotify.com/v1/search?q=track:"
            + song
            + "+artist:"
            + artist
            + "&type=track%2Cartist"
        )

        response = requests.get(
            url, headers={"Authorization": "Bearer " + token})
        if response.ok:
            track = response.json()["tracks"]["items"][0]["album"]
            artist_name = track["artists"][0]["name"]
            image_url = track["images"][1]["url"]
            track_id = response.json()["tracks"]["items"][0]["id"]
            info_url = "https://api.spotify.com/v1/audio-analysis/{}".format(
                track_id)
            song_name = response.json()["tracks"]["items"][0]["name"]
        else:
            return None
        response_detailed = requests.get(
            info_url, headers={"Authorization": "Bearer " + token}
        )
        if response_detailed.ok:
            detailed_data = response_detailed.json()
            tempo = round(detailed_data["track"]["tempo"])
            key = MusicKeys.pitchClass[detailed_data["track"]["key"]]
            mode = MusicKeys.mode[detailed_data["track"]["mode"]]
            key = key + " " + mode
            return {
                "key": key,
                "bpm": tempo,
                "imgUrl": image_url,
                "artist": artist_name,
                "songName": song_name,
            }
        return None

    def post(self):
        data = SpotifyInfo.parser.parse_args()

        global spotify_access
        spotify_data = None
        try:
            spotify_data = self.getTrackInfo(
                data["songName"], data["artist"], spotify_access
            )
        except:
            # return {"message": "something went wrong"}, 404
            pass
        if spotify_data == None:
            try:
                response = refreshSpotifyAcess()
                spotify_access = response
                spotify_data = self.getTrackInfo(
                    data["songName"], data["artist"], spotify_access
                )
                return spotify_data
            except:
                return {"message": "something went wrong"}, 404

        return spotify_data
