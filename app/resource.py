from flask_restful import Resource
from .model import Board

class BoardResource(Resource):

    def get(self):
        return "This is working"
