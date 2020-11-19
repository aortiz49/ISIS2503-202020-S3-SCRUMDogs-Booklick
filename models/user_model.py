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
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))
    semester = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username: str, email: str, code: int, first_name: str, last_name: str,
                 password: str, description: str, picture: str, semester: int):
        self.username = username
        self.email = email
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.description = description
        self.picture = picture
        self.semester = semester

    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                'password': self.password, 'description': self.description,
                'picture': self.picture, 'semester': self.semester}


class ProfessorModel(UserModel):
    _tablename_ = 'professor'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))

    _mapper_args_ = {
        'polymorphic_identity': 'professor',
    }

    def _init_(self, username: str, email: str, code: int, first_name: str, last_name: str,
               password: str, description: str, picture: str):
        self.username = username
        self.email = email
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.description = description
        self.picture = picture

    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                'password': self.password, 'description': self.description, 'picture': self.picture}


class AdminModel(UserModel):
    _tablename_ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))

    _mapper_args_ = {
        'polymorphic_identity': 'admin',
    }

    def _init_(self, username: str, email: str, code: int, first_name: str, last_name: str,
               password: str, description: str, picture: str):
        self.username = username
        self.email = email
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.description = description
        self.picture = picture

    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                'password': self.password, 'description': self.description, 'picture': self.picture}
