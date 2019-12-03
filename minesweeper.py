import os
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt import JWT
from app.jwt import authenticate, identity
from flask_cors import CORS

from app import create_app, db
from app.resource import BoardCollectionResource, BoardEntityResource, RegisterUserResource, CellResource, \
    PauseResumeResource
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
jwt = JWT(app, authenticate, identity)
cors = CORS(app)

api = Api(app)
api.add_resource(BoardCollectionResource, '/boards')
api.add_resource(BoardEntityResource, '/boards/<int:board_id>')
api.add_resource(PauseResumeResource, '/boards/<int:board_id>/status')
api.add_resource(CellResource, '/play/<int:board_id>')
api.add_resource(RegisterUserResource, '/register')

### swagger specific ###
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    app.config['SWAGGER_URL'],
    app.config['API_URL'],
    config={
        'app_name': "minesweeper-API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=app.config['SWAGGER_URL'])
### end swagger specific ###

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
