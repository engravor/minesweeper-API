import flask
from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, abort
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.attributes import flag_modified

from app import db
from .model import Board, User
from .schema import init_game_schema, register_user_schema, user_schema, board_schema, cell_schema


class RegisterUserResource(Resource):

    def post(self):
        args = register_user_schema.load(request.get_json() or {})
        if db.session.query(User).filter(User.username == args.get('username')).first():
            abort(400, message='This username is already taken. Choose a different one.')
        user = User(username=args.get('username'), password=args.get('password'))
        db.session.add(user)
        db.session.commit()
        return flask.json.loads(user_schema.dumps(user)), 201


class BoardCollectionResource(Resource):

    @jwt_required()
    def post(self):
        try:
            args = init_game_schema.load(request.get_json() or {})
            new_board = Board(owner=current_identity, rows=args.get('rows'), columns=args.get('columns'))
            new_board.generate_mines_positions(args.get('mines'))
            new_board.initialize_board()
            db.session.add(new_board)
            db.session.commit()
            return flask.json.loads(board_schema.dumps(new_board)), 201
        except ValidationError as e:
            abort(400, message=e.messages)

    @jwt_required()
    def get(self):
        user_boards = board_schema.dumps(current_identity.boards, many=True)
        return flask.json.loads(user_boards)


class BoardEntityResource(Resource):

    @jwt_required()
    def get(self, board_id):
        board = Board.query.filter_by(id=board_id, owner=current_identity).first()
        if board:
            return flask.json.loads(board_schema.dumps(board))
        else:
            abort(400, message="The board does not exist or you don't have enough privileges to see it.")


class CellResource(Resource):

    def post(self, board_id):
        board = Board.query.filter_by(id=board_id).first()
        if board:
            args = cell_schema.load(request.get_json() or {})
            try:
                self.__validate_params(board, args)
                board.reveal_cell(args.get('row'), args.get('column'), args.get('operation'))
                flag_modified(board, 'current_game_state')
                db.session.add(board)
                db.session.commit()
                return flask.json.loads(board_schema.dumps(board))
            except ValidationError as e:
                abort(400, message=e.messages)
        else:
            abort(400, message="The board does not exist or you don't have enough privileges to see it.")

    def __validate_params(self, board, args):
        if args.get('row') > board.rows:
            raise ValidationError('Row out of range.')
        if args.get('column') > board.rows:
            raise ValidationError('Column out of range.')
        if args.get('operation') not in ['X', '?', 'F']:
            raise ValidationError('Invalid Operation.')

class PauseResumeResource(Resource):

    def post(self, board_id):
        board = Board.query.filter_by(id=board_id).first()
        if board:
            action = request.args.get('action')
            if action in ['pause', 'resume']:
                action_method = getattr(board, action)
                ok, message = action_method()
                if not ok:
                    abort(400, message=message)
                db.session.add(board)
                db.session.commit()
                return flask.json.loads(board_schema.dumps(board))
            else:
                abort(400, message="Invalid operations.")
        else:
            abort(400, message="The board does not exist or you don't have enough privileges to see it.")