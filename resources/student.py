from flask_restful import Resource, reqparse

from models.user_model import UserModel, StudentModel
from resources.user_parser import UserParser


class StudentRegister(Resource):

    def post(self):
        student_parser = reqparse.RequestParser()
        student_parser.add_argument('semester', type=int, required=True,
                                    help="Must have a semester.")
        data = UserParser.parser.parse_args()
        data['semester'] = student_parser.parse_args()['semester']

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = StudentModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Student was created successfully."}, 201


class Student(Resource):

    def get(self, username):
        professor = StudentModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found'}, 404


class StudentList(Resource):
    def get(self):
        return {'students': [student.json() for student in StudentModel.query.all()]}
