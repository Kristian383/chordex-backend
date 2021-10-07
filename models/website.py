from db import db

class WebsiteModel(db.Model):
    __tablename__ = "useful_website"
    id = db.Column(db.Integer, primary_key=True)
    useful_websites_id = db.Column(db.Integer, db.ForeignKey("useful_websites.id"))
    name = db.Column(db.String(80))
    link = db.Column(db.String(180))


    def __init__(self, name, link):
        self.name = name
        self.link = link

    def json(self):
            return {"name": self.name,
                    "link": self.link,
                    }

