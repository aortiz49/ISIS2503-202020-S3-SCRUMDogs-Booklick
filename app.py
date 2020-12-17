import os
from flask import Flask, jsonify, url_for, session
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity, get_jwt_claims
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from werkzeug.utils import redirect

from blacklist import BLACKLIST
from authlib.integrations.flask_client import OAuth

from models.user_model import UserModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'L2SKy23OA5BhHcyta0lY4b5VKTCIrQN7'
api = Api(app)
oauth = OAuth(app)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

app.app_context().push()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["500 per day", "500 per hour"]
)

app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access
# and refresh tokens
jwt = JWTManager(app)  # /auth


@app.route('/oauth_test_area')
def hello_world():
    email = dict(session).get('email', None)
    return {"email": email}


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    my_email = user_info['email']
    usr = UserModel.find_by_email(my_email)
    code = None
    if usr:
        return redirect('https://booklick.herokuapp.com/students/'+str(usr.code))
    else:
        return redirect('https://booklick.me/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return user.role


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.code


# This method will check if a token is blacklisted, and will be called automatically
# when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(
        error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


# JWT configuration ends

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),
        'current_roles': get_jwt_claims()
    }
    return jsonify(ret), 200


from resources.content import ContentList, Content, ContentByInterests, ContentFile
from security import Login, Logout, TokenRefresh
from resources.course import CourseRegister, CourseCode, CoursesList
from resources.major import MajorRegister, MajorName, MajorsList
from resources.professor import ProfessorRegister, ProfessorUsername, ProfessorCode, \
    ProfessorCoursesList, ProfessorRegBooklist, ProfessorRegCourse, ProfessorDeleteCourse, \
    ProfessorBooklist, ProfessorBooklistsList, ProfessorsList
from resources.student import StudentRegister, StudentCode, StudentsList, StudentBooklistsList, \
    StudentBooklist, StudentRegBooklist, StudentRegCourse, StudentCoursesList, StudentDeleteCourse
from resources.admin import AdminUsername, AdminCode, AdminsList, AdminRegister, AdminRegBooklist, \
    AdminBooklist, AdminBooklistsList
from resources.booklist import BookListRegContent, BooklistRegister, BooklistContentList, \
    BooklistName, BooklistList

api.add_resource(Content, '/content/<string:id>', '/content/')
api.add_resource(ContentList, '/contents/')
api.add_resource(ContentByInterests, '/interests/<string:key>')
api.add_resource(ContentFile, '/upload/')
# api.add_resource(Login, '/login/')
# api.add_resource(Logout, '/logout/')
api.add_resource(TokenRefresh, '/refresh/')

api.add_resource(BookListRegContent, '/booklists/<string:name>/')
api.add_resource(BooklistRegister, '/booklists/')
api.add_resource(BooklistContentList, '/booklists/<string:name>/contents/')

api.add_resource(StudentRegister, '/students/')
api.add_resource(StudentCode, '/students/<int:code>')
api.add_resource(StudentsList, '/studentslist/')
api.add_resource(StudentBooklistsList, '/students/<int:code>/booklists/')
api.add_resource(StudentBooklist, '/students/<int:code>/booklists/<string:name>')
api.add_resource(StudentRegBooklist, '/students/<int:code>/booklists/')
api.add_resource(StudentRegCourse, '/students/<int:code>/courses/')
api.add_resource(StudentCoursesList, '/students/<int:code>/courses/')
api.add_resource(StudentDeleteCourse, '/students/<int:code>/courses/<string:course_code>')

api.add_resource(ProfessorUsername, '/professors/<string:username>')
api.add_resource(ProfessorCode, '/professors/<int:code>')
api.add_resource(ProfessorCoursesList, '/professors/<int:code>/courses/')
api.add_resource(ProfessorRegBooklist, '/professors/<int:code>/booklists/')
api.add_resource(ProfessorRegCourse, '/professors/<int:code>/courses/')
api.add_resource(ProfessorDeleteCourse, '/professors/<int:code>/courses/<string:course_code>')
api.add_resource(ProfessorBooklist, '/professors/<int:code>/booklists/<string:name>')
api.add_resource(ProfessorBooklistsList, '/professors/<int:code>/booklists/')
api.add_resource(ProfessorsList, '/professorslist/')
api.add_resource(ProfessorRegister, '/professors/')

api.add_resource(AdminUsername, '/admins/<string:username>')
api.add_resource(AdminCode, '/admins/<int:code>')
api.add_resource(AdminsList, '/adminlist/')
api.add_resource(AdminRegBooklist, '/admins/<int:code>/booklists/')
api.add_resource(AdminBooklist, '/admins/<int:code>/booklists/<string:name>')
api.add_resource(AdminBooklistsList, '/admins/<int:code>/booklists/')
api.add_resource(AdminRegister, '/admins/')

api.add_resource(CourseRegister, '/courses/')
api.add_resource(CourseCode, '/courses/<string:course_code>')
api.add_resource(CoursesList, '/courseslist/')

api.add_resource(MajorRegister, '/majors/')
api.add_resource(MajorName, '/majors/<string:name>')
api.add_resource(MajorsList, '/majorslist/')
api.add_resource(BooklistName, '/booklists/<string:name>')
api.add_resource(BooklistList, '/booklistslist/')

if __name__ == '__main__':
    from db import db
    from bkrypt import bcrypt

    db.init_app(app)
    db.create_all()
    bcrypt.init_app(app)
    app.run(port=5000, debug=True)
