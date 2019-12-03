from datetime import datetime
from marshmallow import Schema, fields, validates_schema
from marshmallow.exceptions import ValidationError


class RegisterUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


register_user_schema = RegisterUserSchema()


class InitGameSchema(Schema):
    rows = fields.Integer(required=True)
    columns = fields.Integer(required=True)
    mines = fields.Integer(required=True)

    @validates_schema()
    def validate_game_params(self, data, **kwargs):
        if data['rows'] <= 0 or data['columns'] <= 0 or data['mines'] <= 0:
            raise ValidationError("All values for rows, columns and mines should be greater than 0.")
        board_size = data['rows'] * data['columns']
        if data['mines'] > board_size:
            raise ValidationError("Mines number should be lower than the amount of cells in the board.")


init_game_schema = InitGameSchema()


class BoardSchema(Schema):
    id = fields.String()
    rows = fields.Integer()
    columns = fields.Integer()
    creation_date = fields.DateTime(format='iso8601')
    mines = fields.Method("get_mines_number")
    current_game_state = fields.String()
    time_tracking = fields.Method("time_elapsed")

    def get_mines_number(self, obj):
        return len(obj.mines.get('mines'))

    def time_elapsed(self, obj):
        time_traking = obj.end_date - obj.creation_date if obj.end_date else datetime.utcnow() - obj.creation_date
        return str(time_traking)


board_schema = BoardSchema()


class UserSchema(Schema):
    username = fields.String()


user_schema = UserSchema()


class CellSchema(Schema):
    column = fields.Integer()
    row = fields.Integer()
    operation = fields.String()


cell_schema = CellSchema()
