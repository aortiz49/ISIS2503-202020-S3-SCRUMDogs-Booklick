from flask_restful import Resource, reqparse

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


class ProfessorCode(Resource):

    def get(self, code: int):
        # only search professors
        professor = ProfessorModel.find_by_code(code)
        if professor:
            return professor.json(), 200
        return {'message': 'Professor not found.'}, 404

    def put(self, code):

        # This parser will be used to update fields that can me modifiable
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('picture', type=str, required=False)

        data = parser.parse_args()
        professor = ProfessorModel.find_by_code(code)

        if professor is None:
            # If the professor isn't found, create a new professor using the user parser
            data1 = UserParser.parser.parse_args()

            professor = ProfessorModel(**data1)
            professor.save_to_db()
            return professor.json(), 201

        professor.username = data['username']
        professor.first_name = data['first_name']
        professor.last_name = data['last_name']
        professor.description = data['description']
        professor.picture = data['picture']

        professor.save_to_db()
        return professor.json(), 200


class ProfessorUsername(Resource):

    def get(self, username: str):
        # only search students
        professor = ProfessorModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found.'}, 404


class ProfessorList(Resource):
    def get(self):
        return {'professors': [professor.json() for professor in ProfessorModel.query.all()]}
