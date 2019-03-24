import logging
import typing

import flask_restful
from sqlalchemy.orm import exc

from service.models import database
from service.models import user

LOG = logging.getLogger(__name__)


class User(flask_restful.Resource):
    def _get_user(self, user_id: str) -> user.User:
        try:
            single_user = user.User.query.filter_by(id=user_id).one()
        except exc.NoResultFound:
            LOG.exception('User does not exist')
            flask_restful.abort(404, message='User does not exist')
        return single_user

    @flask_restful.marshal_with(user.USER_FIELDS)
    def get(self, user_id: str) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:
        LOG.info('Received request to get user by id')
        single_user = self._get_user(user_id)
        return single_user.to_dict(), 200

    def delete(self, user_id: str) -> typing.Tuple[typing.Any, int]:
        LOG.info('Received request to delete user')
        single_user = self._get_user(user_id)
        try:
            database.db.session.delete(single_user)
            database.db.session.commit()
        except Exception:
            LOG.exception('Failed to delete user')
            flask_restful.abort(500, message='Failed to delete user')
        return '', 204
