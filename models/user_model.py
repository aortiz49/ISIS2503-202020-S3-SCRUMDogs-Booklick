# =============================================================================
# File name: user_model.py
# Author: Andy Ortiz
# Date created: 11/17/2020
# Date last modified: 11/17/2020
# Python Version: 3.8.5
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

from db import db


class UserModel(db.Model):
    __tablename__ = 'booklick_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    code = db.Column(db.Integer)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'booklick_user',
        'polymorphic_on': type
    }

    @classmethod
    def find_by_username(cls, username):
        # we can concatenate filter_by's or add each filter separated by a comma
        # SELECT * FROM items WHERE name=name LIMIT 1 (returns ItemModel object)
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        # session is a collection of objects we can write to the db
        db.session.add(self)  # will also update
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class StudentModel(UserModel):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))
    semester = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username: str, password: str, email: str,
                 description: str, picture: str, code: int, semester: int):

        self.username = username
        self.password = password
        self.email = email
        self.description = description
        self.picture = picture
        self.code = code
        self.semester = semester

    def json(self):
        return {'name': self.name, 'code': self.code, 'semester': self.semester}


class ProfessorModel(UserModel):
    __tablename__ = 'professor'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }

    def __init__(self, username: str, password: str, email: str,
                 description: str, picture: str, code: int):
        self.username = username
        self.password = password
        self.email = email
        self.description = description
        self.picture = picture
        self.code = code

    def json(self):
        return {'name': self.name, 'code': self.code}


class AdminModel(UserModel):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username: str, password: str, email: str,
                 description: str, picture: str, code: int):
        self.username = username
        self.password = password
        self.email = email
        self.description = description
        self.picture = picture
        self.code = code

    def json(self):
        return {'name': self.name, 'code': self.code}
