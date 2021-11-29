from db import db

class UserNotesModel(db.Model):
    __tablename__ = "user_notes"
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(8000))
    txt_area_height = db.Column(db.Integer)
    username_id=db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, username_id,notes="", txt_area_height=600):
        self.notes = notes
        self.txt_area_height = txt_area_height
        self.username_id = username_id

    def json(self):
            return {"notes": self.notes,
                    "txtAreaHeight": self.txt_area_height
                    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userId(cls, user_id):
        return cls.query.filter_by(username_id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
