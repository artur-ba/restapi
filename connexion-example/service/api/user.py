import logging
import typing

from sqlalchemy.orm import exc
from werkzeug import exceptions

from service.models import database
from service.models import user

LOG = logging.getLogger(__name__)


def _get_user(user_id: str) -> user.UserDB:
    try:
        single_user = user.UserDB.query.filter_by(id=user_id).one()
    except exc.NoResultFound:
        LOG.exception('User does not exist')
        exceptions.NotFound(description='User does not exist')
    return single_user


def get(user_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    LOG.info('Received request to get user by id')
    single_user = _get_user(user_id)
    return user.User(
        id=str(single_user.id),
        userName=single_user.user_name,
        firstName=single_user.first_name,
        lastName=single_user.last_name,
        email=single_user.email,
        address=single_user.address,
        postalCode=single_user.postal_code,
    ).dict(), 200


def delete(user_id: str) -> typing.Tuple[typing.Any, int]:
    LOG.info('Received request to delete user')
    single_user = _get_user(user_id)
    try:
        database.db.session.delete(single_user)
        database.db.session.commit()
    except Exception:
        LOG.exception('Failed to delete user')
        exceptions.InternalServerError(description='Failed to delete user')
    return '', 204
