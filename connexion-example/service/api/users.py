import logging
import typing
import uuid

from sqlalchemy.orm import exc
from werkzeug import exceptions

from service.models import database
from service.models import user

LOG = logging.getLogger(__name__)


def get(last_name: typing.Optional[str] = None) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:

    LOG.info('Received request to list users')
    if last_name:
        users = user.UserDB.query.filter(user.UserDB.last_name.like(f'%{last_name}%'))
    else:
        users = user.UserDB.query.all()
    return [
        user.User(
            id=str(u.id),
            userName=u.user_name,
            firstName=u.first_name,
            lastName=u.last_name,
            email=u.email,
            address=u.address,
            postalCode=u.postal_code,
        ).dict() for u in users
    ], 200


def post(body: typing.Dict[str, typing.Any]) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    LOG.info('Received request to create a new user')
    try:
        single_user = user.UserDB.query.filter_by(user_name=body['user_name']).one()
        if single_user:
            exceptions.Conflict(description='User by this name already exists in the system')
    except exc.NoResultFound:
        LOG.info('User doesn\'t exist, system will add it')

    new_user = user.UserDB(**body)
    new_user.id = str(uuid.uuid4())
    database.db.session.add(new_user)
    try:
        database.db.session.commit()
        LOG.info('Added new user')
    except Exception:
        LOG.exception('Failed to add user')
        database.db.session.rollback()
        exceptions.InternalServerError(description='Failed to add new user to the system')
    return user.User(
        id=str(new_user.id),
        userName=new_user.user_name,
        firstName=new_user.first_name,
        lastName=new_user.last_name,
        email=new_user.email,
        address=new_user.address,
        postalCode=new_user.postal_code,
    ).dict(), 201
