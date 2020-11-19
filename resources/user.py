#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File name: user_model.py
# Author: Andy Ortiz
# Date created: 11/15/2020
# Date last modified: 11/15/2020
# Python Version: 3.9.0
# =============================================================================
# =============================================================================
# Imports
# =============================================================================
import sqlite3

from flask_restful import Resource, reqparse

from models.user_model import StudentModel, ProfessorModel, AdminModel, UserModel

parser = reqparse.RequestParser()

parser.add_argument('username', type=str, required=True, help="Must have a username.")
parser.add_argument('password', type=str, required=True, help="Must have a password.")
parser.add_argument('email', type=str, required=True, help="Must have an email.")
parser.add_argument('description', type=str, required=False)
parser.add_argument('picture', type=str, required=False)
parser.add_argument('code', type=int, required=True, help="Must have a code.")


class StudentResource(Resource):
    global parser
    student_parser = reqparse.RequestParser()
    student_parser.add_argument('semester', type=int, required=True, help="Must have a semester.")

    def get(self, username):
        student = StudentModel.find_by_username(username)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404

    def post(self):
        data = parser.parse_args()
        data['semester'] = StudentResource.student_parser.parse_args()['semester']

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = StudentModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Student was created successfully."}, 201


class ProfessorResource(Resource):
    global parser

    def get(self, username):
        professor = ProfessorModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found'}, 404

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = ProfessorModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Professor was created successfully."}, 201


class AdminResource(Resource):
    global parser

    def get(self, username):
        professor = AdminModel.find_by_username(username)
        if professor:
            return professor.json()
        return {'message': 'Professor not found'}, 404

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User with username: {data['username']} already exists!"}, 400

        if UserModel.find_by_code(data['code']):
            return {"message": f"User with code: {data['code']} already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": f"User with email: {data['email']} already exists!"}, 400

        user = AdminModel(**data)  # unpacking the dictionary
        user.save_to_db()

        return {"message": f"Admin was created successfully."}, 201
