import os
from flask_migrate import Migrate
from flask_restful import Api

from app import create_app, db
from app.resource import BoardResource

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


api = Api(app)
api.add_resource(BoardResource, '/board')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)
