import os
import typing

import flask_restful
import yaml


class Swagger(flask_restful.Resource):
    def get(self) -> typing.Tuple[typing.Any, int]:
        try:
            with open(os.path.join(os.path.dirname(__file__), '../swagger.yaml'), 'r') as swagger_file:
                return yaml.safe_load(swagger_file)
        except (IOError, yaml.YAMLError):
            flask_restful.abort(500, message='Unable to process swagger spec file')
        return '', 200
