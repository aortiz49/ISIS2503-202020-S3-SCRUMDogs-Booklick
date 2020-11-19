from flask_restful import Resource

from models.user_model import AdminModel, UserModel
from resources.user_parser import UserParser


class AdminRegister(Resource):

    def get(self, username):
        admin = AdminModel.find_by_username(username)
        if admin:
            return admin.json()
        return {'message': 'admin not found'}, 404

    def post(self):
        data = UserParser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = AdminModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"admin was created successfully."}, 201


class Admin(Resource):

    def get(self, username):
        admin = AdminModel.find_by_username(username)
        if admin:
            return admin.json()
        return {'message': 'admin not found'}, 404
