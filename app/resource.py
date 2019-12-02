from flask import request
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from .model import Board, User
from .schema import init_game_schema, register_user_schema, user_schema
from app import db
import flask


class RegisterUserResource(Resource):

    def post(self):
        args = register_user_schema.load(request.get_json() or {})
        if db.session.query(User).filter(User.username == args.get('username')).first():
            return 'This username is already taken. Choose a different one.', 400
        user = User(username=args.get('username'), password=args.get('password'))
        db.session.add(user)
        db.session.commit()
        return flask.json.loads(user_schema.dumps(user)), 201


class BoardResource(Resource):

    def post(self):
        try:
            args = init_game_schema.load(request.get_json() or {})
        except ValidationError as e:
            return e.messages, 400

    def get(self):
        return "This is working"
