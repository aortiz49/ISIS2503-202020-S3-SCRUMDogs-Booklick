from flask_restful import Resource, reqparse

from models.user_model import UserModel, StudentModel
from resources.user_parser import UserParser
import copy


class StudentRegister(Resource):
    student_parser = reqparse.RequestParser()
    student_parser.add_argument('semester', type=int, required=True,
                                help="Must have a semester.")

    def post(self):

        data = UserParser.parser.parse_args()
        data['semester'] = StudentRegister.student_parser.parse_args()['semester']

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists."}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists."}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists."}, 400

        user = StudentModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Student was created successfully."}, 201


class StudentCode(Resource):

    def get(self, code: int):
        # only search students
        student = StudentModel.find_by_code(code)
        if student:
            return student.json(), 200
        return {'message': 'Student not found.'}, 404

    def put(self, code):

        # This parser will be used to update fields that can me modifiable
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('picture', type=str, required=False)

        student = StudentModel.find_by_code(code)
        data = parser.parse_args()

        if student is None:
            # If the student isn't found, create a new student using the User parser

            # Creates a copy of the User parser and removes the 'code' argument so that
            #   it is no longer necessary in the request body
            put_parser = copy.copy(UserParser.parser)
            put_parser.remove_argument('code')

            data1 = put_parser.parse_args()

            # add 'code' and 'semester' to the data1 dictionary so that it can unpacked properly
            data1['code'] = code
            data1['semester'] = StudentRegister.student_parser.parse_args()['semester']

            admin = StudentModel(**data1)
            admin.save_to_db()
            return admin.json(), 201

        student.username = data['username']
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.description = data['description']
        student.picture = data['picture']

        student.save_to_db()
        return student.json(), 200

    def delete(self, code):
        student_to_delete = StudentModel.find_by_code(code)
        if student_to_delete:
            student_to_delete.delete_from_db()
            return {'message': 'Student deleted.'}, 200
        return {'message': 'Nothing to delete.'}, 204


class StudentUsername(Resource):

    def get(self, username: str):
        # only search students
        student = StudentModel.find_by_username(username)
        if student:
            return student.json(), 200
        return {'message': 'Student not found.'}, 404


class StudentList(Resource):
    def get(self):
        return {'students': [student.json() for student in StudentModel.query.all()]}
