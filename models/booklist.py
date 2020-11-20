from db import db


class BooklistModel(db.Model):
    __tablename__ = 'booklist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'))

    def __init__(self, name: str, description: str, image: str):
        self.name = name
        self.description= description
        self.image = image

    def json(self):
        return {'name': self.name, "description": self.description, "image": self.image}

    @classmethod
    def find_by_name(cls, name):
        # we can concatenate filter_by's or add each filter separated by a comma
        # SELECT * FROM items WHERE name=name LIMIT 1 (returns ItemModel object)
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
