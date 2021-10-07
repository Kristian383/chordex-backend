from db import db

class UsefulWebsitesModel(db.Model):
    __tablename__ = "useful_websites"
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(8000))
    txt_area_height = db.Column(db.Integer)
    useful_links= db.relationship("WebsiteModel",lazy="dynamic")

    def __init__(self, notes, txt_area_height):
        self.notes = notes
        self.txt_area_height = txt_area_height

    def json(self):
            return {"notes": self.notes,
                    "txt_area_height": self.txt_area_height,
                    "useful_links": [link.json() for link in self.useful_links.all()]
                    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
