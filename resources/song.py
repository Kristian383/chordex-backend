import flask
from flask.json import jsonify
from flask_restful import Resource, reqparse
from models.song import SongModel
from models.artist import ArtistModel
from models.user import UserModel
from flask_jwt_extended import jwt_required
from flask import request

import json


class MusicKeys(Resource):
    musicKeys = [
        {"key": "C", "relativeMinor": "A", "notes": [
            "C", "D", "E", "F", "G", "A", "B"]},
        {"key": "G", "relativeMinor": "E", "notes": [
            "G", "A", "B", "C", "D", "E", "F#"]},
        {"key": "D", "relativeMinor": "B", "notes": [
            "D", "E", "F#", "G", "A", "B", "C#"]},
        {"key": "A", "relativeMinor": "F#", "notes": [
            "A", "B", "C#", "D", "E", "F#", "G#"]},
        {"key": "E", "relativeMinor": "C#", "notes": [
            "E", "F#", "G#", "A", "B", "C#", "D#"]},
        {"key": "B", "relativeMinor": "G#", "notes": [
            "B", "C#", "D#", "E", "F#", "G#", "A#"]},
        {"key": "F#", "relativeMinor": "D#", "notes": [
            "F#", "G#", "A#", "B", "C#", "D#", "E#"]},
        {"key": "C#", "relativeMinor": "A#", "notes": [
            "C#", "D#", "E#", "F#", "G#", "A#", "B#"]},
        {"key": "F", "relativeMinor": "D", "notes": [
            "F", "G", "A", "Bb", "C", "D", "E"]},
        {"key": "Bb", "relativeMinor": "G", "notes": [
            "Bb", "C", "D", "Eb", "F", "G", "A"]},
        {"key": "Eb", "relativeMinor": "C", "notes": [
            "Eb", "F", "G", "Ab", "Bb", "C", "D"]},
        {"key": "Ab", "relativeMinor": "F", "notes": [
            "Ab", "Bb", "C", "Db", "Eb", "F", "G"]},
        {"key": "Db", "relativeMinor": "Bb", "notes": [
            "Db", "Eb", "F", "Gb", "Ab", "Bb", "C"]},
        {"key": "Gb", "relativeMinor": "Eb", "notes": [
            "Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"]},
        {"key": "Cb", "relativeMinor": "Ab", "notes": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"]}]

    def get(self):
        return {"musicKeys": self.musicKeys}


class Song(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('songName',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('artist',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstKey',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstKeyNotes',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('secondKeyNotes',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstChordProgression',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('secondKey',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('secondChordProgression',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('practicedPrcntg',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('isFavorite',
                        type=bool,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('isMySong',
                        type=bool,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('bpm',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('capo',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('songText',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ytLink',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('chordsWebsiteLink',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('acoustic',
                        type=bool,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('electric',
                        type=bool,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('difficulty',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('tuning',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastViewed',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('songId',
                        type=int,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    def get(self, name, username):
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        user_id = UserModel.find_by_username(username).json()["id"]

        song = SongModel.find_by_name(name, user_id)

        if song:
            return song.json()
        return name
    # @jwt_required()

    def post(self, username):
        data = Song.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        if SongModel.find_by_name(data["songName"], user.id):
            return {'message': "An song with name '{}' already exists.".format(data["songName"])}, 400

        artist = ArtistModel.find_by_name(data["artist"], user.id)

        if artist is None:
            artist = ArtistModel(data["artist"], user.id)
            try:
                artist.save_to_db()
            except:
                return {"message": "An error occured inserting an artist."}, 500

        # return {"msg":data}

        song = SongModel(data["songName"], artist.id, user.id,
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
                         data["tuning"]
                         #  data["lastViewed"],
                         )
        # firstKeyNotes
        # secondKeyNotes
        # return {"msg":song.json()}
        try:
            song.save_to_db()
        except:
            return {"message": "An error occured inserting a song."}, 500
        resp = artist.json()
        return {
            "songs": song.json(),
            "artist": resp
        }, 201

    def put(self, username):
        data = Song.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        # return {"msg":data}
        song = SongModel.find_by_id(data["songId"], user.id)

        if song is None:
            return {"msg": "song is none"}
            # artist = ArtistModel.find_by_name(data["artist"], user.id)
            # if artist is None:
            #     artist = ArtistModel(data["artist"], user.id)
            # try:
            #     artist.save_to_db()
            # except:
            #     return {"message": "An error occured inserting an artist."}, 500
            # song = SongModel(data["songName"], artist.id, user.id)
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

        try:
            song.save_to_db()
            return {'message': 'Song updated', "updated": song.json()}, 200
        except:
            return {"message": "An error occured deleting the song."}, 500

    def delete(self, username):
        data = Song.parser.parse_args()
        user = UserModel.find_by_username(username)

        if not user:
            return {"message": "User with that username doesn't exist"}, 400

        song = SongModel.find_by_name(data["songName"], user.id)
        if song:
            try:
                artist = ArtistModel.find_by_name(data["artist"], user.id)
                song.delete_from_db()
                if len(artist.check_songs()) == 0:
                    artist.delete_from_db()
                    return {"message": "Song and Artist deleted"}, 200

                return {'message': 'Song deleted'}, 200
            except:
                return {"message": "An error occured deleting the song."}, 500
        else:
            return {'message': 'Song doesnt exist'}, 400


class SongList(Resource):
    def get(self):
        return {"songs": [song.json() for song in SongModel.find_all()]}


class UsersSongList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    

    # @jwt_required()
    def get(self, username):
        #data = UsersSongList.parser.parse_args()
        numOfLoads = int(request.args["numOfLoads"])
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User with that username doesn't exist"}, 400
        #return {"numOfLoads":queryStringRaw}
        songs = [song.json()
                 for song in SongModel.find_all_user_songs(user.id,numOfLoads)]

        # artists=[]
        for song in songs:
            artist = ArtistModel.find_by_id(song["artistId"], song["userId"])
            song["artist"] = artist.name
            # artists.append(artist.json())
        return {"songs": songs}

#  song = SongModel(data["name"], artist.id, user_id,
        # data["first_key"],
        # data["first_chord_progression"],
        # data["second_key"],
        # data["second_chord_progression"],
        # data["learned_prcntg"],
        # data["is_favorite"],
        # data["is_my_song"],
        # data["bpm"],
        # data["capo"],
        # data["song_text"],
        # data["yt_link"],
        # data["chords_website_link"],
        # data["acoustic"],
        # data["electric"],
        # data["difficulty"],
        # data["last_viewed"])
