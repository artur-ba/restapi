import logging
import typing
import uuid

import flask_restful
from sqlalchemy.orm import exc

from service.models import database
from service.models import user

LOG = logging.getLogger(__name__)


class Users(flask_restful.Resource):
    @flask_restful.marshal_with(user.USER_FIELDS)
    def get(self) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:
        arguments = user.USER_FILTER.parse_args()
        LOG.info('Received request to list users')
        if arguments['lastName']:
            users = user.User.query.filter(user.User.last_name.like(f'%{arguments["lastName"]}%'))
        else:
            users = user.User.query.all()
        return [u.to_dict() for u in users], 200

    @flask_restful.marshal_with(user.USER_FIELDS)
    def post(self) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
        LOG.info('Received request to create a new user')
        arguments = user.USER_CREATE_PARSER.parse_args()
        try:
            single_user = user.User.query.filter_by(user_name=arguments['user_name']).one()
            if single_user:
                flask_restful.abort(409, message='User by this name already exists in the system')
        except exc.NoResultFound:
            LOG.info('User doesn\'t exist, system will add it')

        new_user = user.User(**arguments)
        new_user.id = str(uuid.uuid4())
        database.db.session.add(new_user)
        try:
            database.db.session.commit()
            LOG.info('Added new user')
        except Exception:
            LOG.exception('Failed to add user')
            database.db.session.rollback()
            flask_restful.abort(500, message='Failed to add new user to the system')
        return new_user.to_dict(), 201
