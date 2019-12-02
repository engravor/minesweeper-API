from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.dialects import postgresql
from app import db
from datetime import datetime
import random


class Board(db.Model):
    __tablename__ = 'boards'

    id = Column(types.Integer, primary_key=True)
    rows = Column(types.Integer, nullable=False)
    columns = Column(types.Integer, nullable=False)
    creation_date = Column(types.DateTime, nullable=False, default=datetime.utcnow)
    mines = Column(postgresql.JSON)
    current_game_state = Column(postgresql.JSON)

    owner_id = Column(types.Integer(), ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", backref='board', lazy='joined')

    def generate_mines_positions(self, mines):
        self.mines = []
        while mines > 0:
            column_pos = random.randint(0, self.columns - 1)
            row_pos = random.randint(0, self.rows - 1)
            if [row_pos, column_pos] not in self.mines:
                self.mines.append([row_pos, column_pos])
                mines -= 1


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
