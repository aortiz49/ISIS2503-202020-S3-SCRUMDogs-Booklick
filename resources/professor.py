from flask_restful import Resource

from models.user_model import ProfessorModel, UserModel
from resources.user_parser import UserParser


class ProfessorRegister(Resource):

    def get(self, username):
        professor = ProfessorModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found'}, 404

    def post(self):
        data = UserParser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = ProfessorModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Professor was created successfully."}, 201


class Professor(Resource):

    def get(self, username):
        professor = ProfessorModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found'}, 404
