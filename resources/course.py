import copy

from flask_restful import Resource, reqparse

from models.course import CourseModel
from resources.user_parser import UserParser


class CourseRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Must have a name.")
    parser.add_argument('code', type=str, required=True, help="Must have a code.")
    parser.add_argument('description', type=str, required=True, help="Must have a description.")

    def post(self):
        data = CourseRegister.parser.parse_args()

        if CourseModel.find_by_code(data['code']):
            return {"message": f"Course with code: {data['code']} already exists."}, \
                   400

        course = CourseModel(**data)  # unpacking the dictionary
        course.save_to_db()

        return {"message": f"Course was created successfully."}, 201


class CourseCode(Resource):

    def get(self, code: int):
        # only search courses
        course = CourseModel.find_by_code(code)
        if course:
            return course.json(), 200
        return {'message': 'Course not found.'}, 404

    def put(self, code):

        # This parser will be used to update fields that can me modifiable
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)

        data = parser.parse_args()
        course = CourseModel.find_by_code(code)

        if course is None:
            # If the course isn't found, create a new coruse using the Course parser

            # Creates a copy of the Course parser and removes the 'code' argument so that
            #   it is no longer necessary in the request body
            put_parser = copy.copy(parser)
            put_parser.remove_argument('code')

            data1 = put_parser.parse_args()
            data1['code'] = code

            admin = CourseModel(**data1)
            admin.save_to_db()
            return admin.json(), 201

        course.name = data['name']
        course.description = data['description']

        course.save_to_db()
        return course.json(), 200

    def delete(self, code):
        course_to_delete = CourseModel.find_by_code(code)
        if course_to_delete:
            course_to_delete.delete_from_db()
            return {'message': 'Course deleted.'}, 200
        return {'message': 'Nothing to delete.'}, 204


class CourseName(Resource):

    def get(self, name: str):
        # only search courses
        course = CourseModel.find_by_name(name)
        if course:
            return course.json()
        return {'message': 'Course not found.'}, 404


class CourseList(Resource):
    def get(self):
        return {'courses': [course.json() for course in CourseModel.query.all()]}
