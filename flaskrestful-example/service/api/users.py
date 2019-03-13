import typing

import flask_restful

from service.models import user


class Users(flask_restful.Resource):
    @flask_restful.marshal_with(user.USER_FIELDS)
    def get(self) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:
        return [u.to_dict() for u in user.User.query.all()], 200
