import copy
from flask_restful import Resource, reqparse

from models.user_model import ProfessorModel, UserModel
from resources.user_parser import UserParser



class ProfessorRegister(Resource):

    def post(self):
        data = UserParser.parser.parse_args()

        # ensure username is proper
        if not data['username'][0].isalpha():
            return {"message": f"Invalid username."}, 400

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists."}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists."}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists."}, 400

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

    def put(self, code: int):

        # This parser will be used to update fields that can me modifiable
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('picture', type=str, required=False)

        data = parser.parse_args()
        professor = ProfessorModel.find_by_code(code)

        if not data['username'][0].isalpha():
            return {'message': 'Invalid username.'}, 400

        if professor is None:
            # If the professor isn't found, create a new professor using the User parser

            # Creates a copy of the User parser and removes the 'code' argument so that
            #   it is no longer necessary in the request body
            put_parser = copy.copy(UserParser.parser)
            put_parser.remove_argument('code')

            data1 = put_parser.parse_args()
            data1['code'] = code

            admin = ProfessorModel(**data1)
            admin.save_to_db()
            return admin.json(), 201

        professor.username = data['username']
        professor.first_name = data['first_name']
        professor.last_name = data['last_name']
        professor.description = data['description']
        professor.picture = data['picture']

        professor.save_to_db()
        return professor.json(), 200

    def delete(self, code):
        professor_to_delete = ProfessorModel.find_by_code(code)
        if professor_to_delete:
            professor_to_delete.delete_from_db()
            return {'message': 'Professor deleted.'}, 200
        return {}, 204


class ProfessorUsername(Resource):

    def get(self, username: str):
        # only search students
        professor = ProfessorModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found.'}, 404


class ProfessorsList(Resource):
    def get(self):
        return {'professors': [professor.json() for professor in ProfessorModel.query.all()]}
