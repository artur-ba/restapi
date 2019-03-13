import typing

from flask_restful import Resource


class Status(Resource):
    def get(self) -> typing.Tuple[typing.Any, int]:
        return '', 200
