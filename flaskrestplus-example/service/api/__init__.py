from flask_restplus import Api

from .status import api as status_api
from .users import api as users_api

api = Api(
    title='Sample service',
    version='1.0.0',
    description='Example of Flask-RESTplus service',
)

api.add_namespace(status_api)
api.add_namespace(users_api)
