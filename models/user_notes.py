from db import db

class UserNotesModel(db.Model):
    __tablename__ = "user_notes"
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(8000))
    txt_area_height = db.Column(db.Integer)
    username_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    #useful_links= db.relationship("WebsiteModel",lazy="dynamic")      #ovo cak odvojiti mogu

    def __init__(self, username_id,notes="", txt_area_height=200):
        self.notes = notes
        self.txt_area_height = txt_area_height
        self.username_id = username_id

    def json(self):
            return {"notes": self.notes,
                    "txtAreaHeight": self.txt_area_height,
                    #"userId": self.username_id,
                    #"id":self.id
                    #"useful_links": [link.json() for link in self.useful_links.all()]
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

    # @classmethod
    # def find_by_noteId(cls, id):
    #     return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
