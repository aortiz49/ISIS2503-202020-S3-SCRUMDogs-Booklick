import copy

from flask_restful import Resource, reqparse

from models.booklist import BooklistModel
from models.major_model import MajorModel


class BooklistRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Must have a name.")
    parser.add_argument('description', type=str, required=True, help="Must have a description.")
    parser.add_argument('image', type=str, required=True, help="Must have an image.")

    def post(self):
        data = BooklistRegister.parser.parse_args()

        if BooklistModel.find_by_name(data['name']):
            return {"message": f"booklist {data['name']} already exists."}, 200

        booklist = BooklistModel(**data)  # unpacking the dictionary
        booklist.save_to_db()

        return {"message": f"Booklist was created successfully."}, 201


class BooklistName(Resource):

    def get(self, name: str):
        # only search booklists
        booklist = BooklistModel.find_by_name(name)
        if booklist:
            return booklist.json()
        return {'message': 'Booklist not found.'}, 404

    def put(self, name: str):

        data = BooklistRegister.parser.parse_args()
        booklist = BooklistModel.find_by_name(name)

        if booklist is None:

            created_booklist = BooklistModel(**data)
            created_booklist.save_to_db()
            return created_booklist.json(), 201

        booklist.name = data['name']
        booklist.save_to_db()
        return booklist.json(), 200

    def delete(self, name: str):
        booklist_to_delete = BooklistModel.find_by_name(name)
        if booklist_to_delete:
            booklist_to_delete.delete_from_db()
            return {'message': 'Booklist deleted.'}, 200
        return {}, 204


class BooklistList(Resource):
    def get(self):
        return {'booklists': [booklist.json() for booklist in BooklistModel.query.all()]}
