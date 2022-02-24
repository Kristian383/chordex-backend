from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.user_notes import UserNotesModel
from models.user import UserModel


class UserNotes(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('username',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    parser.add_argument('notes',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('txtAreaHeight',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    def get(self, email):
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400

        user_notes = UserNotesModel.find_by_userId(user.id)

        if user_notes:
            return user_notes.json()
        return {"message": "User has no notes"}, 200

    # def post(self, username):

    #     data = UserNotes.parser.parse_args()

    #     user = UserModel.find_by_username(username)

    #     if not user:
    #         return {"message": "User with that username doesn't exist"}, 400

    #     user_id = UserModel.find_by_username(username).json()["id"]

    #     user_notes=UserNotesModel.find_by_userId(user_id)
    #     if user_notes:
    #         user_notes.notes=data["notes"]
    #         user_notes.txt_area_height=data["txt_area_height"]

    #     try:
    #         user_notes.save_to_db()
    #     except:
    #         return {"message": "An error occured inserting a notes."}, 500
    #     return {"message": "Note created."}, 201

    def put(self, email):
        data = UserNotes.parser.parse_args()
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400

        user_notes = UserNotesModel.find_by_userId(user.id)

        if user_notes is None:
            user_notes = UserNotesModel(
                user.id, data["notes"], data["txtAreaHeight"])
        else:
            user_notes.notes = data["notes"]
            user_notes.txt_area_height = data["txtAreaHeight"]

        try:
            user_notes.save_to_db()
        except:
            return {"message": "An error occured inserting a notes."}, 500
        return user_notes.json(), 201

    # ovo zapravo necemo moci deletati, jedino kad se user makne
    def delete(self, email):
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "User with that email doesn't exist"}, 400

        note = UserNotesModel.find_by_userId(user.id)
        try:
            note.delete_from_db()
        except:
            return {"message": "An error occured deleting a note."}, 500
        return {"message": "Note deleted."}, 200

        # return {"message": "User created successfully"}, 201


class UserNotesList(Resource): #/notes
    def get(self):
        return {"notes": [note.json() for note in UserNotesModel.find_all()]}
