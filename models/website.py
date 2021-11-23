from db import db

class WebsiteModel(db.Model):
    __tablename__ = "website"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    link = db.Column(db.String(150))
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, link,user_id):
        self.name = name
        self.link = link
        self.user_id = user_id

    def json(self):
            return {"name": self.name,
                    "link": self.link
                    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name,user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_users_websites(cls,user_id):
        return cls.query.filter_by(user_id=user_id)

