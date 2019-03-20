import typing

import flask_restplus

api = flask_restplus.Namespace('status', description='Check service status')


@api.route('')
class Status(flask_restplus.Resource):
    @api.doc('Gets service status')
    def get(self) -> typing.Tuple[typing.Any, int]:
        return '', 200
