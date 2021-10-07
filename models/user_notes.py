from db import db

class UserNotesModel(db.Model):
    __tablename__ = "user_notes"
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(8000))
    txt_area_height = db.Column(db.Integer)
    username_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    #useful_links= db.relationship("WebsiteModel",lazy="dynamic")      #ovo cak odvojiti mogu

    def __init__(self, username,notes="", txt_area_height=200):
        self.notes = notes
        self.txt_area_height = txt_area_height
        self.username = username

    def json(self):
            return {"notes": self.notes,
                    "txt_area_height": self.txt_area_height,
                    "username_id": self.username_id,
                    #"useful_links": [link.json() for link in self.useful_links.all()]
                    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, name):
        # "SELECT * FROM items WHERE name=name LIMIT 1"
        return cls.query.filter_by(name=name).first()
