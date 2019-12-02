import random
from datetime import datetime

from sqlalchemy import Column, types, ForeignKey, JSON
from sqlalchemy.ext.mutable import MutableDict
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Board(db.Model):
    __tablename__ = 'boards'

    id = Column(types.Integer, primary_key=True)
    rows = Column(types.Integer, nullable=False)
    columns = Column(types.Integer, nullable=False)
    creation_date = Column(types.DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(types.DateTime, nullable=True)
    status = Column(types.String)
    mines = Column(MutableDict.as_mutable(JSON))
    current_game_state = Column(MutableDict.as_mutable(JSON))

    owner_id = Column(types.Integer(), ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", backref='board', lazy='joined')

    def generate_mines_positions(self, mines):
        self.mines = dict(mines=[])
        while mines > 0:
            column_pos = random.randint(0, self.columns - 1)
            row_pos = random.randint(0, self.rows - 1)
            if [row_pos, column_pos] not in self.mines.get("mines"):
                self.mines.get("mines").append([row_pos, column_pos])
                mines -= 1

    def initialize_board(self):
        self.status = 'playing'
        self.current_game_state = dict(state=[
            ['-' for j in range(self.columns)] for i in range(self.rows)
        ])

    def update_current_state(self, row, column, mark):
        self.current_game_state.get("state")[row][column] = mark

    def reveal_cell(self, row, column, operation):
        if operation == 'X':
            self.__show_cell(row, column)
        elif operation in ['F', '?']:
            self.update_current_state(row, column, operation)


    def __show_cell(self, row, column):
        if self.current_game_state.get('state')[row][column] == '-':
            if [row, column] in self.mines.get('mines'):
                self.status = 'game_over'
                self.end_date = datetime.utcnow()
                self.update_current_state(row, column, '#')
                self.__show_all_mines()
            else:
                self.__show_self_and_neighbors(row, column)

    def __show_all_mines(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.current_game_state.get('state')[row][column] in ['-', '?'] and [row, column] in self.mines.get(
                        'mines'):
                    self.update_current_state(row, column, '#')
                elif self.current_game_state.get('state')[row][column] == 'F' and [row, column] in self.mines.get(
                        'mines'):
                    self.update_current_state(row, column, '#!')

    def __show_self_and_neighbors(self, row, column):
        i_top = row - 1 if row > 0 else row
        j_left = column - 1 if column > 0 else column
        i_bottom = row + 1 if row < self.rows - 1 else row
        j_right = column + 1 if column < self.columns - 1 else column

        neighbor_mines = 0
        neighbors_list = []

        for i in range(i_top, i_bottom + 1):
            for j in range(j_left, j_right + 1):
                if i == row and j == column:
                    continue
                if isinstance(self.current_game_state.get('state')[i][j], int):
                    continue
                neighbors_list.append((i, j))

        for i, j in neighbors_list:
            if [i, j] in self.mines.get('mines'):
                neighbor_mines += 1

        self.current_game_state.get("state")[row][column] = neighbor_mines

        if neighbor_mines == 0:
            for i, j in neighbors_list:
                self.current_game_state.update(self.__show_self_and_neighbors(i, j))

        return self.current_game_state


class User(db.Model):
    __tablename__ = 'users'

    id = Column(types.Integer, primary_key=True)
    username = Column(types.String, nullable=False, unique=True)
    password_hash = Column(types.String, nullable=False)

    boards = db.relationship("Board")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
