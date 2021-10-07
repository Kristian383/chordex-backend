from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.user_notes import UserNotesModel
from models.user import UserModel


class UserNotes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('notes',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('txt_area_height',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        #ovdje slati username name?
        notes = UserNotesModel.find_by_username(name)

        if notes:
            return notes.json()
        return name

    def post(self,username):

        data = UserNotes.parser.parse_args()

        if not UserModel.find_by_username(username):
            return {"message": "User with that username doesn't exist"}, 400

        #pronaci usera i onda proslijediti njegov id?
        notes = UserNotesModel(username,data["notes"],data["txt_area_height"])  
        
        try:
            notes.save_to_db()
        except:
            return {"message": "An error occured inserting a notes."}, 500
        return notes.json(), 201

        #return {"message": "User created successfully"}, 201