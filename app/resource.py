from flask import request
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from .model import Board, User
from .schema import init_game_schema, register_user_schema, user_schema, board_schema
from app import db
import flask
from flask_jwt import jwt_required, current_identity


class RegisterUserResource(Resource):

    def post(self):
        args = register_user_schema.load(request.get_json() or {})
        if db.session.query(User).filter(User.username == args.get('username')).first():
            return 'This username is already taken. Choose a different one.', 400
        user = User(username=args.get('username'), password=args.get('password'))
        db.session.add(user)
        db.session.commit()
        return flask.json.loads(user_schema.dumps(user)), 201


class BoardCollectionResource(Resource):

    @jwt_required
    def post(self):
        try:
            args = init_game_schema.load(request.get_json() or {})
            new_board = Board(owner=current_identity, rows=args.get('rows'), columns=args.get('columns'))
            new_board.generate_mines_positions(args.get('mines'))
            db.session.add(new_board)
            db.session.commit()
            return flask.json.loads(board_schema.dumps(new_board)), 201
        except ValidationError as e:
            return e.messages, 400

    @jwt_required
    def get(self):
        user_boards = board_schema.dumps(current_identity.boards, many=True)
        return flask.json.loads(user_boards)


class BoardEntityResource(Resource):

    @jwt_required()
    def get(self, board_id):
        board = Board.query.filter_by(id=board_id).first_or_404()
        return flask.json.loads(board_schema.dumps(board))
