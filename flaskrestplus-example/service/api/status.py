import typing

import flask_restplus

api = flask_restplus.Namespace('status', description='Check service status')


@api.route('')
class Status(flask_restplus.Resource):
    @api.doc(
        'Gets service status',
        responses={
            '200': 'Service is operational',
            '500': 'Service is unable to handle the request',
        },
    )
    def get(self) -> typing.Tuple[typing.Any, int]:
        return '', 200
