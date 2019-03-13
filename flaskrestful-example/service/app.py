from flask import Flask
from flask_restful import Api

from service.api import status
from service.api import swagger
from service.api import users
from service.models import database

application = Flask('service')
application.config.from_object('service.config')

api = Api(application)
database.db.init_app(application)

api.add_resource(status.Status, '/status')
api.add_resource(swagger.Swagger, '/swagger')
api.add_resource(users.Users, '/users')
