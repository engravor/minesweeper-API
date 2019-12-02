from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.dialects import postgresql
from app import db
from datetime import datetime


class Board(db.Model):
    __tablename__ = 'boards'

    id = Column(types.Integer, primary_key=True)
    rows = Column(types.Integer, nullable=False)
    columns = Column(types.Integer, nullable=False)
    creation_date = Column(types.DateTime, nullable=False, default=datetime.utcnow)
    mines = Column(postgresql.JSON)
    current_game_state = Column(postgresql.JSON)

    owner_id = Column(types.Integer(), ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", backref='board', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'

    id = Column(types.Integer, primary_key=True)
    username = Column(types.String, nullable=False, unique=True)
    password = Column(types.String, nullable=False)

    boards = db.relationship("Boards")
