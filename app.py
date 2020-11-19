import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.admin import AdminRegister, Admin
from resources.professor import Professor, ProfessorRegister
from resources.student import Student, StudentRegister, StudentList
from security import authenticate, identity

app = Flask(__name__)

app.config['DEBUG'] = True

# search for DATABSE_URL variable. If not found, run sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# turns off Flask-SQLALchemy modification tracker, leaving SQLAlchemy modification tracker on
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'andy'

# when we initialize the jwt object, it will use the app and the authenticate and identity
# functions to allow for the authentication of users:
#   1. this creates a new endpoint where we send a username and a password
#   2. these credentials are received by the authenticate function which will find the correct user
#       object using the username
#   3. the password received will be compared to the username object's password. If they match,
#       the user will be returned and it becomes the identity
#   4. the auth endpoiint returns jwt token
#   5. the identity function is called and it uses the jwt token to get the user id to return the
#       correct userid that the jwt token represents
#   6. if the above work, then the user is authenticated
jwt = JWT(app, authenticate, identity)  # /auth

api = Api(app)  # This will allow us to very easily. add our resources to the app

# This is going to tell our API that the resources we created are now going to be
# accessible via our API


api.add_resource(Student, '/students/<string:username>')
api.add_resource(Professor, '/professors/<string:username>')
api.add_resource(Admin, '/admins/<string:username>')

api.add_resource(StudentRegister, '/students/')
api.add_resource(ProfessorRegister, '/professors/')
api.add_resource(AdminRegister, '/admins/')

api.add_resource(StudentList, '/studentList/')

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
