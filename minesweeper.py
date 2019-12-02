import os
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt import JWT
from app.jwt import authenticate, identity

from app import create_app, db
from app.resource import BoardCollectionResource, BoardEntityResource, RegisterUserResource

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
jwt = JWT(app, authenticate, identity)

api = Api(app)
api.add_resource(BoardCollectionResource, '/boards')
api.add_resource(BoardEntityResource, '/boards/<int:board_id>')
api.add_resource(RegisterUserResource, '/register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
