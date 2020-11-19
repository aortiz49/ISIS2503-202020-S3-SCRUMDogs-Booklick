from flask_restful import Resource, reqparse

from models.user_model import UserModel, StudentModel
from resources.user_parser import UserParser


class StudentRegister(Resource):
    student_parser = reqparse.RequestParser()
    student_parser.add_argument('semester', type=int, required=True,
                                help="Must have a semester.")

    def post(self):

        data = UserParser.parser.parse_args()
        data['semester'] = StudentRegister.student_parser.parse_args()['semester']

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

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

        data = parser.parse_args()
        student = StudentModel.find_by_code(code)

        if student is None:
            # If the student isn't found, create a new student using the user parser
            data1 = UserParser.parser.parse_args()
            data1['semester'] = StudentRegister.student_parser.parse_args()['semester']

            student = StudentModel(**data1)
            student.save_to_db()
            return student.json(), 201

        student.username = data['username']
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.description = data['description']
        student.picture = data['picture']

        student.save_to_db()
        return student.json(), 200


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
